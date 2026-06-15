# characters/ — 角色

> 一类资产。**生成计划与提示词在本目录 `assets.json`**(批量脚本读它);本文给人看:状态表 + 集成说明。
> 风格基准与 assets.json 字段规范见 [`../README.md`](../README.md)。

单帧/立绘/换姿势/换装/出新角色 → 用 `char-edit` 工作流(给一张参考图,`vars.ref` + `vars.change`)。多姿势精灵表的一致性边界见 `docs/art-pipeline.md`。默认批量跳过 type=character,要带上加 `--with-chars`。

## 状态表(图例见总纲)

| 资源 | 文件 | 用途/规格 | 状态 | 预览 |
|------|------|-----------|------|------|
| _示例_ | `name.png` | … | ⬜ | — |

## 生成

1. 编辑 `assets.json` 填该类资源提示词(item 的 `prompt` 或工作流 `vars`)。
2. 项目根预览:`bash scripts/comfyui/batch.sh --only characters --dry-run`。
3. 出图:去掉 `--dry-run`(过夜在自己终端跑,`--variants N` 控制每条几张)。
4. 满意的把 item `status` 改 `done`,本表改 ✅ 补预览。

## 集成

切片/接入运行时目录(如 `frontend/public/characters/`)后,状态标 📦。

## 整套角色动作(图生图编辑锁角色)

用图像编辑模型(`i2i` / image_qwen_image_edit_2511)从**一张定妆参考图**锁住同一角色出全套动作,不用 ControlNet、不训 LoRA。

- 单张:`comfy.py i2i _base/hero-base.png "the same character running, full body, plain bg, keep identical design" --project <项目> --prefix characters/hero/run`
- 整套:见本目录 `assets.json`(参考图在 `defaults.vars.image`,每个动作一条 item)→ `batch.sh assets/characters --project <项目>`
- 提示词英文佳、强调 "the same character / keep identical design and outfit";动作别太复杂。
