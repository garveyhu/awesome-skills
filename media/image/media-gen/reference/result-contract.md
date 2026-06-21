# 统一结果契约（借 Pixelle MediaService 的 MediaResult）

无论底下走哪个后端，`media_gen.py gen` 的 **stdout 只吐一行 JSON**（进度 / 决策走 stderr）。上游编排（asset-bridge / produce-pipeline）只认这一份契约，不需要知道走了哪个后端——这正是 Pixelle `MediaService` 用一个 `MediaResult{type,url/path,duration}` 把 ComfyUI / RunningHub / 直连 API 三态统一起来的思路。

## schema

```jsonc
{
  "ok": true,                      // bool：最终是否出图成功
  "type": "image",                 // 媒体类型（本 skill 恒为 image；预留 video 扩展）
  "path": "/abs/out/hero.png",     // 绝对路径；失败为 null
  "backend": "gemini-gen",         // 最终成功出图的后端 id；失败为 null
  "meta": {
    "prompt_final": "<style-lock locked_prompt> + <用户 prompt>",  // 真正喂给后端的提示词
    "prompt_user": "<用户原始 prompt>",                            // 未拼 style-lock 的原始输入
    "negative_prompt": "<style-lock negative_prompt>",            // 透传给支持负向的后端，否则仅记录
    "aspect": "16:9",
    "refs": ["refs/hero.png"],
    "style_lock": "v1",            // 注入的 style-lock 版本；未注入为 null
    "cost": "free-quota",          // 成功后端的成本档（透出给上游算账）
    "fallback_chain": ["gemini-gen", "codex-image-gen", "comfyui", "browser-gen"],
    "attempts": [                  // 按顺序记录每个试过的后端
      {"backend": "gemini-gen", "status": "ok"}
    ]
  }
}
```

## attempts 的 status 取值

| status | 含义 | 是否继续降级 |
|--------|------|--------------|
| `ok` | 该后端出图成功（链路在此终止） | 终止 |
| `failed` | 真跑了但失败（撞额度 / 报错 / 退出码非零；带 `error` 摘要） | 继续下一个 |
| `unavailable` | 依赖缺失（脚本不在 / 服务没起 / key 没配）——未真跑 | 继续下一个 |
| `slot` | 半自动 / 付费需用户显式启用（带 `hint` 提示如何启用）——未真跑 | 继续下一个 |

`attempts` 让上游一眼看清**到底走了哪个、为什么降级**。例：

```jsonc
"attempts": [
  {"backend": "gemini-gen",      "status": "failed", "error": "limit resets / 撞额度"},
  {"backend": "codex-image-gen", "status": "ok"}
]
```

## 失败结果

链路耗尽仍没出图：

```jsonc
{
  "ok": false,
  "type": "image",
  "path": null,
  "backend": null,
  "meta": {
    "fallback_chain": ["gemini-gen", "codex-image-gen", "comfyui"],
    "attempts": [
      {"backend": "gemini-gen",      "status": "unavailable"},
      {"backend": "codex-image-gen", "status": "failed", "error": "..."},
      {"backend": "comfyui",         "status": "unavailable", "error": "127.0.0.1:8188 连不上"}
    ],
    "error": "所有后端均未出图（unavailable/failed/slot）"
  }
}
```

**铁律**：`ok:false` 时 `path` 必为 `null`——**绝不**在没真出图时返一个假路径或假装成功。

## dry-run 结果

`--dry-run` 不真生成，吐**决策预演**（同样一行 JSON）：

```jsonc
{
  "ok": true,
  "dry_run": true,
  "type": "image",
  "path": null,
  "meta": {
    "prompt_final": "...",
    "fallback_chain": ["gemini-gen", "codex-image-gen", "comfyui", "browser-gen"],
    "routing": [
      {"backend": "gemini-gen",      "available": true,  "decision": "would-try (1st)"},
      {"backend": "codex-image-gen", "available": true,  "decision": "fallback"},
      {"backend": "comfyui",         "available": false, "decision": "skip (service down)"},
      {"backend": "browser-gen",     "available": "slot","decision": "slot (half-auto, hint)"}
    ]
  }
}
```

## 给上游编排的消费建议

- 只读 `ok` + `path` 就能拿到成品；要算账 / 排障再读 `meta.attempts` 与 `meta.cost`。
- 批量出图：每张独立调一次，各自拿一行 JSON；并发由上游控制（与 codex-image-gen 的 gen-batch 并发理念一致，但跨后端的并发要注意各后端自己的限流）。
- 预留 `type:"video"`：未来若把视频后端（jimeng / browser-gen Veo）纳入同一抽象，契约不变、`type` 切 `video` 并加 `duration` 字段即可。
