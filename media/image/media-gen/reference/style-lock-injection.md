# style-lock 注入规则

所有生图**默认**自动拼 style-lock v1，保跨内容品牌画风一致（暗场数据流·克制科技脸·近黑 #0A0C12 + 唯一薄荷青 #34E0B0 + 几何线框）。这一层是「品牌一致性」的关键——单条内容不自由发挥，统一吃冻结 token。

## 事实源

`Media-Studio/1-资产库/风格锁/style-lock.md` 的 frontmatter：

```yaml
locked_prompt: "dark technical aesthetic, near-black #0A0C12 background, single mint-green #34E0B0 accent glow, thin wireframe geometry, data-flow lines, subtle film grain, matte non-reflective, volumetric light from one direction, generous negative space, asymmetric composition, low saturation, precise and restrained"
negative_prompt: "purple-blue gradient, glassmorphism, neon overload, busy, cluttered, glossy plastic, lens flare spam, multiple light sources, cute, childish, watermark, text artifacts"
backend: gemini-gen      # 静态声明的主后端；本 skill 的 --prefer / 可用性 优先于它
seed:                    # 待锁（首批出图后回填）
sref:                    # 待锁
```

路由器自动向上查找该文件（从 `--out` 目录逐级上溯，或 `--style-lock` 显式指定）。找不到 → 跳过注入，stderr 提示，**不报错**（非品牌场景也能用）。

## 注入规则（按后端能力分流）

| 后端能力 | locked_prompt 怎么进 | negative_prompt 怎么进 |
|----------|----------------------|------------------------|
| 支持负向（comfyui） | 拼到用户 prompt **前**：`<locked_prompt>, <用户 prompt>` | 走后端负向槽（当前脚本先拼进 prompt 尾「avoid: …」，TODO 接 comfyui 工作流 `--neg`） |
| 不支持负向（gemini-gen / codex-image-gen / browser-gen） | 拼到用户 prompt **前** | 以「`avoid: <negative_prompt>`」追加到 prompt 尾（自然语言后端能部分理解） |

**拼接形态**（最终 `prompt_final`）：

```
<locked_prompt>, <用户 prompt>. avoid: <negative_prompt>
```

例：
- 用户 prompt：`一条数据流穿过暗场`
- prompt_final：`dark technical aesthetic, near-black #0A0C12 ... precise and restrained, 一条数据流穿过暗场. avoid: purple-blue gradient, glassmorphism, ...`

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

style-lock.md 写了 `backend: gemini-gen`（静态主后端声明）。本 skill 的路由：

- **不**直接照搬 frontmatter 的 backend 当唯一后端——而是用本 skill 的**默认降级链 + 可用性探测 + `--prefer`**。
- 二者本就同源（默认链首即 gemini-gen），所以一般行为一致；区别在本 skill 会**自动降级**，frontmatter 只是静态声明。
- 若未来 style-lock 改主后端，本 skill 默认链可对应调整（改 `reference/providers.md` + `scripts/providers.py`），保持同源。
