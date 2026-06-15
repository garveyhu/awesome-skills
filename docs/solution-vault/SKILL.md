---
name: solution-vault
description: >
  Personal solution library for replicating proven technical solutions across projects.
  Use when: the user needs to implement a feature that matches an existing solution
  (e.g., Google OAuth login, region picker, file upload, payment integration),
  or when the user asks to save/record a solution they just completed.
  Triggers: "solution-vault", "用我之前的方案", "复刻", "之前是怎么做的",
  "save this solution", "record this approach", or when a requirement matches
  a known solution category (auth, integration, UI patterns, etc.).
---

# Solution Vault

## 定位

沉淀经过验证的完整技术方案，下次遇到同类需求时快速适配复刻。与 style-vault 互补：style-vault 管样式资产，solution-vault 管功能方案。

## 使用方式

### 场景一：复刻已有方案

用户提出需求时，检查 `solutions/` 下是否有匹配的方案：

1. 读取 `solutions/README.md` 查看分类索引
2. 找到匹配方案后，读取方案目录下的 `README.md`
3. 根据 `适配指南` 和 `# ADAPT:` 注释，结合当前项目的技术栈和结构适配生成代码
4. 不要照搬代码 — 理解方案的核心逻辑后，按当前项目的约定生成

### 场景二：沉淀新方案

用户明确要求保存某个方案时：

1. 确定方案归入哪个分类（auth/ui/data/integration/infra 等）
2. 在对应分类目录下创建方案文件夹
3. 编写 README.md（按下方格式）
4. 提取核心模板代码为独立文件，用真实语言扩展名
5. 在模板代码中用 `# ADAPT:` 注释标记需要根据项目调整的部分
6. 更新 `solutions/README.md` 索引

## 方案 README.md 格式

```markdown
# 方案名称

> 一句话描述

## 适用场景

什么时候用这个方案

## 技术决策

为什么选这个方案（关键决策和理由）

## 技术栈要求

依赖的技术栈

## 文件清单

| 文件 | 说明 |
|------|------|

## 适配指南

复刻时需要调整什么（占位符、配置项等）

## 注意事项

踩过的坑、易错点
```

## 模板代码规范

- 文件用真实扩展名（`.py`、`.tsx`、`.ts`），便于语法高亮
- 用 `# ADAPT:` (Python) 或 `// ADAPT:` (JS/TS) 注释标记需适配的部分
- 代码应该是可直接参考的完整实现，不是片段
- 不包含项目特定的导入路径，用通用占位符

## 方案索引

见 [solutions/README.md](solutions/README.md)
