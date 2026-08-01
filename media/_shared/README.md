# media/_shared — 频道解析共享库（所有 media skill 的统一接入点）

> 分布式矩阵的地基。每个需要「频道值」（品牌 token / 音色 / 画风 / 路径 / 凭据）的 skill 脚本，
> 都通过本目录 `channek.py` 取值，**绝不硬编码本机路径或任何频道品牌**。
> `_shared/` 不是 skill（无 SKILL.md）；vendor 时随 media 树带进 `skills/media/_shared/`。

## 频道单一事实源 = 风格卡 `card.json`

- 机器读：每频道一张 **`card.json`**（Channek 风格卡 v2；位置 `_channel/<slug>/风格卡/card.json`，
  一台机器可多频道并存）。**卡是唯一真相源**——旧 `card.json` 已彻底退役，不兼容、不双读。
- 人读「为什么」：频道侧 `风格卡/品牌套件/品牌文档/IP定位书.md` · `风格锁/画风锁.md` · `音色/voice.md`（参照·机器值以 card.json 为准）。
- schema 以 Channek 的 `shared/style-card`（`card.schema.ts` 的 v2 面）为准。

## 点号路径速查（旧 `card.json` → 新 `card.json`）

`ch.get(...)` 的路径**就是 card.json 的真实结构**，库内不做任何旧路径翻译。

| 旧路径（已废） | 新路径（card.json） |
|---|---|
| `channel.slug` / `channel.name` | **顶层** `slug` / `name` |
| `channel.niche` / `audience` / `persona` / `slogan` / `pillars` / `bio` / `strategy` | `identity.niche` / `identity.audience` / …（同名平移） |
| `channel.format` | `identity.format`（**对象**：`orientation` / `persona` / `captions`） |
| `channel.mind_word` | `identity.mindWord` |
| `brand.style_lock.image_prompt` | `locks.visualStyle.imagePrompt` |
| `brand.style_lock.negative_prompt` | `locks.visualStyle.negativePrompt` |
| `brand.style_lock.version` / `seed` / `sref` / `backend` | `locks.visualStyle.<同名>` |
| `brand.ip.*` | `brand.mascot.*` |
| `brand.ip.i2v_subject` / `i2v_style` / `asset_ref` / `clip_map` | `brand.mascot.i2vSubject` / `i2vStyle` / `assetRef` / `clipMap`（同段另有 `kind` / `eyeColor` / `earColor` / `signature` / `visualPrompt`） |
| `brand.ip.clips_dir` / `badge_asset` | **卡 v2 无此二键**；IP 动作库目录 = `layout.cardAssets.brandAssets.root` + `brand.mascot.name` + `layout.cardAssets.libraries.ipActions` |
| `brand.sound` | `locks.motionSound.sound` |
| `brand.code_theme` | `brand.codeTheme` |
| `secrets_needed` | `requires.secrets` |
| `brand.tokens.*`（colors/accent/fonts/stroke/radius/grid） | **同名不变** |
| `voice.default` / `voice.profiles` / `captions` / `cover` / `audio` / `platforms` / `publish` | **同名不变** |

便捷属性（是 API 不是路径，名字不随卡改）：`ch.slug` · `ch.name` · `ch.identity` · `ch.brand` ·
`ch.mascot`（旧名 `ch.ip` 保留为同值别名） · `ch.style_lock`（读 `locks.visualStyle`） ·
`ch.sound`（读 `locks.motionSound.sound`） · `ch.colors` · `ch.voice_profile()` ·
`ch.path()` / `ch.style_path()`。

## 怎么 import（粘到 skill 脚本顶部）

```python
# ── channek 导入引导（走 _shared，dev 真身 / vendored 两处都成立）──
import sys, pathlib
for _anc in pathlib.Path(__file__).resolve().parents:
    if (_anc / "_shared" / "channek.py").exists():
        sys.path.insert(0, str(_anc / "_shared")); break
```

然后：

```python
import channek
ch = channek.load(required=False)          # 解析当前频道的卡；找不到返回 None（不抛）
mint = (ch.get("brand.tokens.colors.mint") if ch else None) or "#888888"  # 兜底=中性占位·绝不写频道值
ref  = ch.path("风格卡/品牌套件/音色/...") if ch else None                # 频道相对路径（相对频道根）
keys = channek.find_secrets()              # 凭据文件定位（找不到返 None）
```

## ★ 纯净度 + 零回归铁律（最高约束）

**内核与 skill 不许有任何频道实例（`_channel/<slug>/`）的品牌 / IP / 色 / 音色 / 赛道痕迹；
各频道的产出靠「card.json 在就读它」保持一字不差——不靠 skill 藏频道值。**

1. **频道值只活在 card.json**：skill 读 `ch.get(...)`，兜底一律**中性占位**（灰阶色 / "a mascot" / 空 prompt / None），**绝不**回落到任何频道实例的真值。
   `值 = (ch.get(...) if ch else None) or <中性占位>`。
2. **零回归靠 card.json 在场**：实际工作流永远解析得到当前频道（env / cwd / `.active` / 单频道自动），
   skill 读 card.json = 该频道真值 → 产出不变。中性兜底只在「无频道」时生效（非工作流路径）。
3. **示例 / 默认 / 注释里也不许有频道身份**：任何频道的颜色 / 签名色名 / IP 名 / slogan / 赛道 / 脸风格名等一律不写进 skill；要举例用通用占位或「读 card.json」。
4. **文件路径**：频道资产在 `_channel/<slug>/风格卡/...`；用 `ch.path("风格卡/...")` 解析（相对频道根）。
5. **改完自测**：`CHANNEK_CHANNEL=…/_channel/<slug>` 下跑 skill，确认卡在场时输出与改前一致；再跑无频道场景确认中性兜底不报错、不泄露任何频道实例。

## 环境变量约定（机器级·与频道无关）

| 变量 | 用途 | 缺省回退 |
|------|------|---------|
| `CHANNEK_CHANNEL` | 当前频道根（`_channel/<slug>`） | cwd 上溯 / `_channel/.active` / 唯一频道 |
| `AGENTS_RESOURCES` | 凭据文件（也可传其所在目录） | 上溯 `_secrets/resources.json` → `$AGENTS_HOME/resources.json` |
| `AGENTS_HOME` | 机器级凭据库根目录（其下 `resources.json`） | 无——**不设就没有兜底**（返 None） |
| `COMFYUI_HOME` / `VOXCPM_HOME` | 运行时依赖 | 见各 skill 自身说明 |

> 凭据定位**不再有家目录硬编码兜底**（旧版会落到某个私人 vault 路径）。随卡分发的文件里绝不留
> 指向他人密钥文件的路径——要用机器级共享凭据库，显式设 `$AGENTS_RESOURCES` 或 `$AGENTS_HOME`。

**不要编辑 `channek.py`**（共享库）；需要的值用 `ch.get()` 取。`channek.py --root` 打印当前频道根。
