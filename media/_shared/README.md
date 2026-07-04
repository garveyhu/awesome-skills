# media/_shared — 频道解析共享库（所有 media skill 的统一接入点）

> 分布式矩阵的地基。每个需要「频道值」（品牌 token / 音色 / 画风 / 路径 / 凭据）的 skill 脚本，
> 都通过本目录 `ms_channel.py` 取值，**绝不硬编码本机路径或任何频道品牌**。
> `_shared/` 不是 skill（无 SKILL.md）；vendor 时随 media 树带进 `skills/media/_shared/`。

## 频道单一事实源

- 机器读：每频道一个 **`channel.json`**（容器 `_channel/<slug>/channel.json`，一台机器可多频道并存）。
- 人读「为什么」：频道侧 `风格卡/品牌套件/品牌文档/IP定位书.md` · `风格锁/画风锁.md` · `音色/voice.md`（参照·机器值以 channel.json 为准）。
- schema 见 `_meta/CONTRACT.md` 与 `_meta/channel.json.example`。

## 怎么 import（粘到 skill 脚本顶部）

```python
# ── ms_channel 导入引导（走 _shared，dev 真身 / vendored 两处都成立）──
import sys, pathlib
for _anc in pathlib.Path(__file__).resolve().parents:
    if (_anc / "_shared" / "ms_channel.py").exists():
        sys.path.insert(0, str(_anc / "_shared")); break
```

然后：

```python
import ms_channel
ch = ms_channel.load(required=False)          # 解析当前频道；找不到返回 None（不抛）
mint = (ch.get("brand.tokens.colors.mint") if ch else None) or "#888888"  # 兜底=中性占位·绝不写频道值
ref  = ch.path("风格卡/品牌套件/音色/...") if ch else None                # 频道相对路径（相对频道根）
keys = ms_channel.find_secrets()              # 凭据文件定位
```

## ★ 纯净度 + 零回归铁律（最高约束）

**内核与 skill 不许有任何频道实例（`_channel/<slug>/`）的品牌 / IP / 色 / 音色 / 赛道痕迹；
各频道的产出靠「channel.json 在就读它」保持一字不差——不靠 skill 藏频道值。**

1. **频道值只活在 channel.json**：skill 读 `ch.get(...)`，兜底一律**中性占位**（灰阶色 / "a mascot" / 空 prompt / None），**绝不**回落到任何频道实例的真值。
   `值 = (ch.get(...) if ch else None) or <中性占位>`。
2. **零回归靠 channel.json 在场**：实际工作流永远解析得到当前频道（env / cwd / `.active` / 单频道自动），
   skill 读 channel.json = 该频道真值 → 产出不变。中性兜底只在「无频道」时生效（非工作流路径）。
3. **示例 / 默认 / 注释里也不许有频道身份**：任何频道的颜色 / 签名色名 / IP 名 / slogan / 赛道 / 脸风格名等一律不写进 skill；要举例用通用占位或「读 channel.json」。
4. **文件路径**：频道资产在 `_channel/<slug>/风格卡/...`；用 `ch.path("风格卡/...")` 解析（相对频道根）。
5. **改完自测**：`MEDIA_STUDIO_CHANNEL=…/_channel/<slug>` 下跑 skill，确认 channel.json 在场时输出与改前一致；再跑无频道场景确认中性兜底不报错、不泄露任何频道实例。

## 环境变量约定（机器级·与频道无关）

| 变量 | 用途 | 缺省回退 |
|------|------|---------|
| `MEDIA_STUDIO_CHANNEL` | 当前频道根（`_channel/<slug>`） | cwd 上溯 / `_channel/.active` / 唯一频道 |
| `AGENTS_RESOURCES` | 凭据文件 | 上溯 `_secrets/resources.json` → `~/.agents/resources.json` |
| `COMFYUI_HOME` / `VOXCPM_HOME` | 运行时依赖 | 见 `_meta/.env.example` |

**不要编辑 `ms_channel.py`**（共享库）；需要的值用 `ch.get()` 取。`ms_channel.py --root` 打印当前频道根。
