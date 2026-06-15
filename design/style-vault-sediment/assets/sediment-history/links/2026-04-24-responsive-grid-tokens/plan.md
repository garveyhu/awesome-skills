# 沉淀计划 · 响应式 Grid 双策略 Token

日期：2026-04-24
作者：links
模式：create
起点：from-project（源于 style-vault 网站自身 BrowsePage / BrowseCategoryPage 的实战演化）
档位：**Tier 1 · 精髓级（2 条 token）**

## 目标

沉淀两种响应式 grid 策略为独立 token，供未来任意项目 refs 引用：

- **策略 1**（useCols + slice）：卡宽稳定、一行填满、数据量 = 列数
- **策略 2**（auto-fit + 1fr）：永远填行、卡宽随数据量和容器宽度浮动

两者语义差异大、使用场景互斥，故独立沉淀两条 token 而非合并单条。

## 涉及条目（2 新增 · 无更新）

1. `tokens/layout/fixed-cols-row`
2. `tokens/layout/auto-fit-fluid`

（新子桶 `tokens/layout/` · taxonomy 不限制 sub-bucket，直接建目录即可）

## 依赖关系

无外部依赖。两者互不 uses。

## 元信息填写方式

- AI 自动填（Y 模式授权）：全部 2 条

## 用户定制

- B 方案：独立两条 token（非合并单条）
- a 选项：`useCols` hook 代码嵌入 `fixed-cols-row` token 正文，不独立沉淀

## 执行状态

☑ 用户已确认 · VAULT_OK=true（双仓同步）· 已上锁 · 待写入
