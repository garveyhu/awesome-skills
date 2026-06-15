# 把 ComfyUI 文生图接入 Web 应用（FastAPI 后端代理）

ComfyUI 的 HTTP API 默认在 `http://127.0.0.1:8188`，**只监听本地、无鉴权**。

## 架构：后端代理（推荐，别让前端直连）

```
React 前端  ──HTTP──►  你的 FastAPI 后端  ──HTTP──►  ComfyUI 127.0.0.1:8188
                       (鉴权/校验/限流)              (本机，不对外暴露)
```

为什么不让浏览器直连 ComfyUI：① 跨域(CORS) 报错；② 直连就得 `--listen 0.0.0.0` 把无鉴权生图后端暴露到网络，危险。后端代理可规避 CORS、隐藏 ComfyUI、加鉴权/限流/参数校验。

> 前提：FastAPI 后端与 ComfyUI 跑在**同一台机器**（或后端能访问到 8188）。ComfyUI 内部串行执行任务，并发提交会排队。

## ComfyUI 的"API"本质

没有"传 prompt 出图"的简单接口——它是**提交一整张工作流图(graph)**。文生图 = POST 一张 API 格式工作流（把提示词填进文本节点）→ 拿 `prompt_id` → 轮询 `/history/{id}` → 从 `/view` 取图。MPS 上单图较慢（Z-Image 8步约 15–30s，首次含加载更久），所以**接口要做成异步：提交立即返回 prompt_id，前端轮询状态**，不要阻塞 HTTP 连接等几十秒。

三个端点：`POST /prompt`、`GET /history/{prompt_id}`、`GET /view?filename=&subfolder=&type=`。

---

## FastAPI 实现（MVC 分层，按项目规范）

目录（落到你项目 `src/<app>/` 下）：

```
core/comfyui_client.py    # 纯 HTTP 客户端（与 ComfyUI 通信）
service/image_gen_service.py  # 业务：拼工作流、提交、查状态
schemas/image_gen.py      # Pydantic 出入参
api/image_gen_router.py   # 路由：POST 提交 / GET 查状态 / GET 取图
```

### core/comfyui_client.py — 通信层

```python
"""ComfyUI HTTP 客户端：只负责与本地 ComfyUI 通信。"""
from __future__ import annotations

import httpx
from loguru import logger

from ..core.config import settings  # settings.comfyui_host = "http://127.0.0.1:8188"


class ComfyUIClient:
    def __init__(self, host: str | None = None, timeout: float = 30.0) -> None:
        self.host = (host or settings.comfyui_host).rstrip("/")
        self.timeout = timeout

    async def submit(self, workflow: dict, client_id: str = "webapp") -> str:
        """提交工作流，返回 prompt_id。"""
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            resp = await c.post(f"{self.host}/prompt", json={"prompt": workflow, "client_id": client_id})
        if resp.status_code != 200:
            logger.error("comfyui submit rejected: {} {}", resp.status_code, resp.text)
            raise RuntimeError(f"ComfyUI 拒绝工作流: {resp.text}")
        data = resp.json()
        if data.get("node_errors"):
            raise RuntimeError(f"工作流校验失败: {data['node_errors']}")
        return data["prompt_id"]

    async def history(self, prompt_id: str) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            resp = await c.get(f"{self.host}/history/{prompt_id}")
        return resp.json().get(prompt_id, {})

    async def view_bytes(self, filename: str, subfolder: str, ftype: str) -> bytes:
        """取产物图片字节。"""
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            resp = await c.get(
                f"{self.host}/view",
                params={"filename": filename, "subfolder": subfolder, "type": ftype},
            )
        resp.raise_for_status()
        return resp.content
```

### schemas/image_gen.py — 出入参

```python
from pydantic import BaseModel, Field


class Text2ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    width: int = Field(1024, ge=256, le=2048)
    height: int = Field(1024, ge=256, le=2048)
    seed: int = 0
    steps: int = Field(8, ge=1, le=50)


class SubmitResponse(BaseModel):
    prompt_id: str


class ImageRef(BaseModel):
    filename: str
    subfolder: str
    type: str
    url: str  # 指向本后端的取图代理


class TaskStatus(BaseModel):
    prompt_id: str
    status: str  # running | success | error
    images: list[ImageRef] = []
```

### service/image_gen_service.py — 业务层

```python
"""文生图业务：拼 Z-Image 工作流、提交、查状态。"""
from __future__ import annotations

from loguru import logger

from ..core.comfyui_client import ComfyUIClient
from ..schemas.image_gen import ImageRef, TaskStatus, Text2ImageRequest

_client = ComfyUIClient()


def _build_zimage_workflow(req: Text2ImageRequest) -> dict:
    """把请求拼成 ComfyUI API 格式工作流（Z-Image Turbo 文生图）。

    模型名按当前 ComfyUI 库存写死；换模型时改这里，或先查 /object_info 动态取。
    """
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.0}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": req.prompt}},
        "6": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["5", 0]}},
        "7": {"class_type": "EmptySD3LatentImage", "inputs": {"width": req.width, "height": req.height, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {
            "model": ["4", 0], "seed": req.seed, "steps": req.steps, "cfg": 1.0,
            "sampler_name": "res_multistep", "scheduler": "simple",
            "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0], "denoise": 1.0}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "webapp"}},
    }


async def submit_text2image(req: Text2ImageRequest) -> str:
    workflow = _build_zimage_workflow(req)
    prompt_id = await _client.submit(workflow)
    logger.info("submitted t2i task: prompt_id={} prompt={!r}", prompt_id, req.prompt[:50])
    return prompt_id


async def query_task(prompt_id: str) -> TaskStatus:
    entry = await _client.history(prompt_id)
    if not entry:
        return TaskStatus(prompt_id=prompt_id, status="running")
    if entry.get("status", {}).get("status_str") == "error":
        return TaskStatus(prompt_id=prompt_id, status="error")
    images: list[ImageRef] = []
    for _node, out in entry.get("outputs", {}).items():
        for img in out.get("images", []) or []:
            images.append(ImageRef(
                filename=img["filename"], subfolder=img.get("subfolder", ""), type=img.get("type", "output"),
                url=f"/comfyui/image?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img.get('type','output')}",
            ))
    return TaskStatus(prompt_id=prompt_id, status="success" if images else "running", images=images)


async def fetch_image(filename: str, subfolder: str, ftype: str) -> bytes:
    return await _client.view_bytes(filename, subfolder, ftype)
```

### api/image_gen_router.py — 路由层（GET+POST，Result 包装）

```python
from fastapi import APIRouter
from fastapi.responses import Response

from ..core.result import Result  # 你项目的统一响应包装
from ..schemas.image_gen import SubmitResponse, TaskStatus, Text2ImageRequest
from ..service import image_gen_service as svc

router = APIRouter(prefix="/comfyui", tags=["comfyui"])


@router.post("/text2image", response_model=Result[SubmitResponse])
async def text2image(req: Text2ImageRequest):
    prompt_id = await svc.submit_text2image(req)
    return Result.ok(SubmitResponse(prompt_id=prompt_id))


@router.get("/text2image/{prompt_id}", response_model=Result[TaskStatus])
async def text2image_status(prompt_id: str):
    return Result.ok(await svc.query_task(prompt_id))


@router.get("/image")
async def proxy_image(filename: str, subfolder: str = "", type: str = "output"):
    """代理取图：把 ComfyUI 的图片字节透传给前端（不暴露 8188）。"""
    data = await svc.fetch_image(filename, subfolder, type)
    return Response(content=data, media_type="image/png")
```

> 异常一律 raise（如客户端层的 `RuntimeError`/你的 `BusinessError`），交给项目的全局异常 handler 兜成失败响应——不要在路由里 try/except 吞掉。`settings.comfyui_host` 走 pydantic-settings + `.env`。

---

## React 前端调用（service 层，TanStack Query 轮询）

```ts
// services/comfyuiApi.ts  —— 所有 HTTP 只在 service（项目 axios 实例已解包 Result.data）
import { http } from '@/services/http';

export interface Text2ImageReq { prompt: string; width?: number; height?: number; seed?: number; steps?: number }
export interface ImageRef { filename: string; url: string }
export interface TaskStatus { promptId: string; status: 'running' | 'success' | 'error'; images: ImageRef[] }

export const submitText2Image = (body: Text2ImageReq) =>
  http.post<{ promptId: string }>('/comfyui/text2image', body);

export const getTaskStatus = (promptId: string) =>
  http.get<TaskStatus>(`/comfyui/text2image/${promptId}`);
```

```ts
// hooks/useText2Image.ts —— 提交后用 TanStack Query 轮询，success 即停
import { useMutation, useQuery } from '@tanstack/react-query';
import { getTaskStatus, submitText2Image } from '@/services/comfyuiApi';

export function useText2Image() {
  const submit = useMutation({ mutationFn: submitText2Image });
  const promptId = submit.data?.promptId;
  const status = useQuery({
    queryKey: ['t2i', promptId],
    queryFn: () => getTaskStatus(promptId!),
    enabled: !!promptId,
    refetchInterval: q => (q.state.data?.status === 'success' || q.state.data?.status === 'error' ? false : 2000),
  });
  return { submit, status: status.data };
}
```

```tsx
// 组件里：<img src> 直接用后端代理返回的 url（拼上你的 API baseURL）
{status?.images.map(img => <img key={img.filename} src={`${API_BASE}${img.url}`} alt="" />)}
```

后端字段 snake_case、前端 camelCase 的转换走你的 axios 拦截器统一处理。

---

## 安全 / 部署清单

- ComfyUI **保持只监听 127.0.0.1**，永远不要为了前端直连而 `--listen 0.0.0.0` 暴露公网。
- 鉴权/限流加在**你的后端**，不是 ComfyUI。
- 校验 prompt 长度、尺寸/步数范围（schema 已做），防止超大请求拖垮 MPS。
- 生产建议：把 ComfyUI 用 `run.sh` 常驻；后端与它同机；前端只认你后端域名。
- 想换模型/架构：改 `_build_zimage_workflow`，或参考 `architectures.md` 换工作流；要动态适配库存就在 service 里先查 `/object_info`（见 `scripts/core/inventory.py` 思路）。
