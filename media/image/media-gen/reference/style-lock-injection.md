# style-lock 注入规则

所有生图**默认**自动拼 style-lock，保跨内容品牌画风一致——单条内容不自由发挥，统一吃当前频道冻结的 token。**具体画风/配色一律以频道事实源为准，本文不复述色值以免漂移。**

## 事实源

当前频道的 style-lock，按优先级：

1. **`card.json` 的 `brand.style_lock`**（机器单一事实源，经 `_shared/channek.py` 读取）——`image_prompt` / `negative_prompt` / `version`。
2. 回落 `<频道根>/风格卡/风格锁/画风锁.md` 的 frontmatter（`locked_prompt` / `negative_prompt` / `version` / `seed` / `sref`）。

frontmatter 形态（**下为通用示意·非任何频道真值**）：

```yaml
locked_prompt: "<当前频道的锁定画风描述：美学/配色/构图/质感，读 card.json 或 画风锁.md>"
negative_prompt: "<要规避的 AI 味/杂质：如 purple-blue gradient, glassmorphism, watermark, text artifacts ...>"
backend: <主后端>        # 静态声明；本 skill 的 --prefer / 可用性 优先于它
seed:                    # 可选，锁可复现
sref:                    # 可选，风格参考图
```

路由器优先读 card.json，其次自动向上查找 画风锁.md（从 `--out` 目录逐级上溯，或 `--style-lock` 显式指定）。两者皆无 → 跳过注入，stderr 提示，**不报错**（非品牌场景也能用）。

## 注入规则（按后端能力分流）

| 后端能力 | locked_prompt 怎么进 | negative_prompt 怎么进 |
|----------|----------------------|------------------------|
| 支持负向（comfyui） | 拼到用户 prompt **前**：`<locked_prompt>, <用户 prompt>` | 走后端负向槽（当前脚本先拼进 prompt 尾「avoid: …」，TODO 接 comfyui 工作流 `--neg`） |
| 不支持负向（gemini-gen / codex-image-gen / browser-gen） | 拼到用户 prompt **前** | 以「`avoid: <negative_prompt>`」追加到 prompt 尾（自然语言后端能部分理解） |

**拼接形态**（最终 `prompt_final`）：

```
<locked_prompt>, <用户 prompt>. avoid: <negative_prompt>
```

例（`<locked_prompt>` 为当前频道实际锁定的画风，运行时从 card.json 读取）：
- 用户 prompt：`一条数据流穿过暗场`
- prompt_final：`<当前频道 locked_prompt 全文>, 一条数据流穿过暗场. avoid: <当前频道 negative_prompt>`

## seed / sref（待锁）

style-lock v1 的 `seed` / `sref` 当前为空（首批出图后回填）。注入逻辑：

- `seed` 非空 → 传给支持的后端（comfyui `--seed N`）锁可复现氛围；gemini/codex 当前 CLI 不暴露 seed，记进 meta 但不传。
- `sref` 非空 → 作为额外参考图风格锚点（若后端支持 ref 且未显式传 `--ref`，可把 sref 图当默认 ref）。
- 二者为空时跳过，不影响出图。

## 开关

- 默认**开**。
- `--no-style-lock`：完全关闭注入（非品牌图、纯功能性占位图才用）。
- `--style-lock <path>`：指定别的 style-lock.md（多品牌 / 实验风格）。

## 与 frontmatter `backend` 声明的关系

画风锁.md 写了 `backend: gemini-gen`（静态主后端声明）。本 skill 的路由：

- **不**直接照搬 frontmatter 的 backend 当唯一后端——而是用本 skill 的**默认降级链 + 可用性探测 + `--prefer`**。
- 二者本就同源（默认链首即 gemini-gen），所以一般行为一致；区别在本 skill 会**自动降级**，frontmatter 只是静态声明。
- 若未来 style-lock 改主后端，本 skill 默认链可对应调整（改 `reference/providers.md` + `scripts/providers.py`），保持同源。
