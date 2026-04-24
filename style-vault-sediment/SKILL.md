---
name: style-vault-sediment
description: >
  写入类 skill：把风格沉淀到 style-vault（新增 / 修改 / 删除）。默认进入新增沉淀流程，
  支持 4 种起点（本地项目 / 在线资源 / 从零创作 / 兜底），按作者版本化记录沉淀历史。
  硬依赖 style-vault skill 作为分类字典源。
  Triggers: "/style-vault-sediment"、"沉淀"、"存一下样式"、"加到 vault"、"记录这个风格"、
  "修改 <id>"、"删除 <id>"、"下掉 <id>"、"调整已有的 xxx"、在完成风格创作后希望把它写入 vault 的场景。
---

# Style Vault Sediment

style-vault 的**写入端 skill**。全部新增 / 修改 / 删除操作都从这里进。

## 依赖声明

**硬依赖** `style-vault` skill：
- 读 `style-vault/assets/taxonomy.json`（分类字典真相源）
- 调 `style-vault/scripts/taxonomy.py`（查询 id / 反向引用 / tag 枚举）
- 引 `style-vault/references/README.md`（frontmatter 规范）

两 skill 必须成对安装。

## 入口路由

根据触发语判定操作模式，默认进 **create**。

| 触发情况 | 走的路径 |
|---|---|
| `/style-vault-sediment` 裸词 / "沉淀" / "加到 vault" | **默认 create**，见下面"默认 create"节 |
| 描述里有项目路径 / cwd 提示 | create + [sediment-from-project](references/sediment-from-project.md) |
| 描述里有 URL / "截图" / "参考这个网站" | create + [sediment-from-web](references/sediment-from-web.md) |
| "想做一个 xxx 风格" / "从零" | create + [sediment-from-scratch](references/sediment-from-scratch.md) |
| 起点不明 | [sediment-from-other](references/sediment-from-other.md) |
| **"修改 <id>"** / **"改 <id> 的 tag"** / **"调整已有的 xxx"** | [modify-workflow](references/modify-workflow.md) |
| **"删除 <id>"** / **"下掉 <id>"** / **"移除 <id>"** | [delete-workflow](references/delete-workflow.md) |

## 默认 create

如果触发语没给起点，先问用户：

> 本次沉淀的起点是？
> 1) 本地项目路径（扫项目提取风格）
> 2) 在线资源（URL / 截图 / 设计稿）
> 3) 从零创作（有想法，要落成资产）
> 4) 其他 / 不确定

用户回复后路由到对应 `sediment-from-*.md`。

### 进入对应分支前，先问深度档位

所有 create 分支进入自己的 discovery 前，**第一步一律是问档位**（见 [depth-tiers.md](references/depth-tiers.md)）：

- **Tier 1 · 精髓**（5–8 条 · 20–30 min）：最独特视觉点
- **Tier 2 · 基础**（12–18 条 · 1–1.5 h）：可启动同风格新产品的最小系统 · **默认档**
- **Tier 3 · 全量**（30–50+ 条 · 3–4 h）：每条路由独立 page + 模式 / 表单 / 状态 / 动效全扫

档位决定各分支 discovery 的强度与硬下限（例如 Tier 3 必须产出路由清单 / 全局模式清单 / 表单清单 / 状态清单，且 ≥ 80% 覆盖率才能继续）。

## 共享原则（所有路径都遵守）

- **档位先行**：进入任何 create discovery 前必须先选 Tier 1/2/3（[depth-tiers.md](references/depth-tiers.md)）
- **写入前必须让用户 review 整批方案**（[shared-workflow 步骤 4](references/shared-workflow.md)）
- **Tier 3 写入前必须覆盖率核对 ≥ 80%**，未达标打断询问补齐或降档
- **元信息 AI 自动填需一次性授权**（步骤 2），可选 Y / N / 逐条决定
- **双仓独立 commit，同一次沉淀各仓聚合为一个 commit**，不 push
- **沉淀报告是每次写入的收尾**，同时落盘到 `assets/sediment-history/`
- **分类字典以 style-vault/assets/taxonomy.json 为准**，新 category / tag 值必须先改字典再写条目
- **Skill 可自迭代**：沉淀结果出错时，区分"一次小错"与"模式错"——模式错必须回写到对应 workflow 文件并登记到 [lessons-loopback.md](references/lessons-loopback.md) 清单；小错改条目即可

## 入口索引

- [共享主流程 shared-workflow.md](references/shared-workflow.md)
- [深度档位 depth-tiers.md](references/depth-tiers.md)
- [教训回写 lessons-loopback.md](references/lessons-loopback.md) · skill 自迭代机制
- [Create 分支一览](references/README.md)
- 沉淀历史归档：`assets/sediment-history/<author>/<date-topic>/`
- 查询工具（读侧）：`style-vault/scripts/taxonomy.py`
