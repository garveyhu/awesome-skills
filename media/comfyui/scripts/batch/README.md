# 批量生图引擎(batch.sh / batch/run.py)

读各资产文件夹下的 `assets.json`,照计划无人值守批量出图。**数据(JSON)与逻辑(脚本)分离**,任何项目放好 `assets.json` 即可用。
> **纯机械、零 LLM**:本引擎不调用 Claude/任何大模型——Claude 的活在前期(把 assets.json/提示词/工作流配好);批量执行是纯脚本、零 API 成本,适合过夜跑。


## 用法
```bash
# 先看计划(不生成,强烈建议先跑这个核对)
bash scripts/batch.sh <资产根目录> --project <名> --workflows-dir <仓>/comfy-workflows --dry-run
# 真跑(睡前在自己终端执行,实时面板可观测、可中断)
bash scripts/batch.sh <资产根目录> --project <名> --workflows-dir <仓>/comfy-workflows --variants 3
```
选项:`--only props,ui`(只跑某些类)`--variants N`(每条出几张)`--redo`(连 done 也重跑)
`--no-resume`(不续跑,强制重出;默认续跑=按磁盘已有只补缺的,中断可接)`--with-chars`(含 type=character,需逐个参考图)`--timeout 1800`(单条超时秒)`--seed-base N`。

> **约定**:批量/过夜任务**由用户在自己终端跑**(观测性/控制权更好);Claude 只负责写好 `assets.json`、`--dry-run` 验证、给出完整命令。

## assets.json 结构(放在每个资产文件夹里,与 README.md 并列)
```json
{
  "category": "props/decor",
  "out_prefix": "props/decor",
  "defaults": {
    "workflow": "t2i",                     // t2i(builder) | char-edit | prop-gen | 相对/绝对 .json 路径
    "style_prefix": "16-bit cozy pixel art, ... a single isolated",
    "suffix": "on a solid uniform magenta background, nothing else, no text",
    "size": [768, 768],
    "keyflat": { "tol": 95 },              // 抠透明;null/省略=不抠
    "pixelize": { "px": 120, "colors": 32 }, // 像素化+调色板;null/省略=不像素化
    "variants": 3
  },
  "items": [
    { "name": "anvil", "status": "done" },
    { "name": "bookshelf", "status": "todo", "prompt": "tall wooden bookshelf ..." },
    { "name": "hero-walk", "type": "character", "workflow": "char-edit",
      "vars": { "ref": "char0.png", "change": "walking, side view" } }
  ]
}
```
- **t2i 项**:最终提示词 = `style_prefix, prompt, suffix` 拼接。
- **工作流项**(char-edit/prop-gen/路径):用 `vars` 填工作流里的 `<占位符>`(经 `--var`)。
- `status`:`todo`/`redo` 会跑,`done`/`skip` 跳过(`--redo` 可强制)。变体靠 `--seed` 换种子,ComfyUI 自动编号 `_00001_` `_00002_`。
- 每条 item 可覆盖 defaults 里任意键。
- **不自动改 status**:过夜出的是候选,早上挑好再手动把 status 改 done。
