# assets/ — 项目美术资产库

> 本目录由 comfyui skill 的 `init` 脚手架生成。它是**项目美术资产的单一真源**:
> 每类资产一个文件夹,`README.md` 给人看、`assets.json` 给批量脚本读。改成你项目的
> 风格只需改内容,不要动结构。

## 目录约定(每个文件夹 = 一类资产)

```
assets/
├── README.md      # 本文(总纲 + Style Bible + assets.json 规范)
├── scenes/        # 全屏背景/场景(整图,通常不抠)
├── props/         # 世界物件(道具/家具);量大可再分子目录,如 props/decor
├── ui/            # 界面(面板/按钮/图标;9-slice 框)
├── fx/            # 粒子/特效帧
├── characters/    # 角色(单帧/立绘走 char-edit;多姿势精灵表见规约)
└── branding/      # logo / 应用图标 / 启动图
```

- 加新类:建文件夹 + 放一个 `README.md` 和 `assets.json`,在本表加一行。
- 产物落到 `assets/<out_prefix>/<name>_NNNNN_.png`(`out_prefix` 在该文件夹 assets.json 里)。

## 状态图例(全库统一,写在各 README 状态表里)

| 标记 | 含义 |
|------|------|
| ⬜ | 待生成 |
| ✅ | 已生成且满意(预览列放 `![名](文件名.png)`) |
| 🔁 | 已生成但要重做(不满意/风格不符) |
| 🖐 | 手绘(非生成) |
| 📦 | 已切片接入运行时目录(代码在用) |

> 批量脚本**不自动改 status**:过夜出的是候选,早上挑好后手动改对应 item 的 `status`。

## Style Bible(风格基准 —— 一致性的生命线,改成你项目的)

所有 t2i 提示词都在这段之上写,只补该资源的具体内容:

```
<在这里写你项目的统一风格,例如:>
16-bit cozy pixel art, warm palette, crisp clean pixels, gentle dithering, calm mood
```

- 这段对应各文件夹 assets.json 的 `defaults.style_prefix`。
- 需抠透明的(道具/UI/fx)再加纯色底:`on a solid uniform magenta background, nothing else, no text`(对应 `defaults.suffix`)。
- Z-Image/FLUX 等:自然语言、低 cfg、**别堆质量词**(no "masterpiece/8k/ultra")。

---

## assets.json 规范(★ 批量脚本读的就是它)

每个资产文件夹放一个 `assets.json`。批量引擎(`scripts/comfyui/batch.sh`)递归读所有
`assets.json`,把每个 `item` 翻译成一句生成命令并执行。

```jsonc
{
  "category":   "props/decor",      // 类别名(信息用)
  "out_prefix": "props/decor",      // 产物前缀 → assets/<out_prefix>/<name>_NNNNN_.png

  "defaults": {                     // 本文件夹所有 item 的默认值;item 可逐项覆盖
    "workflow":     "t2i",          // 用哪条管线(见下)
    "style_prefix": "<Style Bible>",// t2i 提示词前缀(拼在最前)
    "suffix":       "on a solid uniform magenta background, nothing else, no text", // t2i 提示词后缀
    "size":         [768, 768],     // 宽,高
    "keyflat":      { "tol": 95 },  // 抠纯色底→透明;省略/null = 不抠
    "pixelize":     { "px": 120, "colors": 32 }, // 像素化+量化调色板;省略/null = 不像素化
    "variants":     3               // 每条默认出几张(命令 --variants 可覆盖)
  },

  "items": [
    // ① t2i 项:最终提示词 = style_prefix + prompt + suffix
    { "name": "table",  "status": "todo", "prompt": "a sturdy wooden table" },

    // ② item 覆盖 defaults(这条不抠、改尺寸、出 1 张)
    { "name": "logo",   "status": "todo", "prompt": "a minimal emblem",
      "keyflat": null, "pixelize": null, "size": [512, 512], "variants": 1 },

    // ③ 工作流项:workflow 指向 comfy-workflows 里的工作流,用 vars 填它的 <占位符>
    { "name": "hero-walk", "type": "character", "workflow": "char-edit",
      "vars": { "ref": "hero.png", "change": "walking, side profile view" } }
  ]
}
```
> JSON 不支持注释;上面 `//` 仅为讲解,真文件里删掉。

### 字段语义
- **workflow**:`"t2i"`(默认 builder,要 `prompt`)| `"char-edit"`/`"prop-gen"`/任意 `*.json` 路径(走 `raw`,用 `vars` 填工作流里的 `<占位符>`,相对路径相对 `comfy-workflows/`)。
- **status**:`todo`/`redo` 会跑;`done`/`skip` 跳过(命令加 `--redo` 可强制连 done 一起重跑)。
- **变体 & 续跑**:每条按 `variants` 出 N 张,seed 递增,ComfyUI 自动编号 `_00001_`、`_00002_`…。脚本**默认续跑**:数磁盘已有产物,只补到 N,中断后重跑自动接上(`--no-resume` 强制重出)。
- **后处理**:`keyflat`(纯色底洪水填充抠透明,扁平美术专用)、`pixelize`(降采样+量化调色板)在生成后自动串,`null`/省略即关闭。
- **type: "character"**:默认被批量跳过(角色多靠逐张参考图),要带上加 `--with-chars`。
- item 里任何键都覆盖 `defaults` 同名键。

> 完整命令选项见 skill 的 `scripts/batch/README.md`;用法见 `scripts/comfyui/batch.sh -h` 与项目 `docs/art-pipeline.md`。
