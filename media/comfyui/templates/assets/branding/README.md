# branding/ — logo / 应用图标 / 启动图

> 一类资产。**生成计划与提示词在本目录 `assets.json`**(批量脚本读它);本文给人看:状态表 + 集成说明。
> 风格基准与 assets.json 字段规范见 [`../README.md`](../README.md)。

通常单张、按需是否抠;尺寸按用途单独设(item 覆盖 size)。

## 状态表(图例见总纲)

| 资源 | 文件 | 用途/规格 | 状态 | 预览 |
|------|------|-----------|------|------|
| _示例_ | `name.png` | … | ⬜ | — |

## 生成

1. 编辑 `assets.json` 填该类资源提示词(item 的 `prompt` 或工作流 `vars`)。
2. 项目根预览:`bash scripts/comfyui/batch.sh --only branding --dry-run`。
3. 出图:去掉 `--dry-run`(过夜在自己终端跑,`--variants N` 控制每条几张)。
4. 满意的把 item `status` 改 `done`,本表改 ✅ 补预览。

## 集成

切片/接入运行时目录(如 `frontend/public/branding/`)后,状态标 📦。
