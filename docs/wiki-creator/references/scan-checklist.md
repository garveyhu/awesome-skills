# 项目深度扫描清单

执行全面扫描时，按此清单逐项检查。目标：不遗漏任何关键信息源。

## 1. 项目元信息

- [ ] `package.json` / `pyproject.toml` / `pom.xml` / `Cargo.toml` / `go.mod` — 依赖、脚本、版本
- [ ] `README.md` — 项目概述、功能描述
- [ ] `LICENSE` — 许可证类型
- [ ] `.gitignore` — 推断技术栈和工具链

## 2. 入口文件

- [ ] 主入口（`main.ts`, `index.ts`, `app.py`, `main.go`, `Main.java`, `src/main.rs` 等）
- [ ] 应用初始化/启动流程
- [ ] 中间件/插件注册顺序

## 3. 配置系统

- [ ] 配置文件（`.env*`, `config/`, `settings/`, YAML/TOML/JSON）
- [ ] 环境变量定义和使用
- [ ] 多环境配置（dev/staging/prod）

## 4. 路由与 API

- [ ] 路由定义文件（`routes/`, `router/`, controller 装饰器）
- [ ] API 端点完整列表
- [ ] 中间件链
- [ ] OpenAPI/Swagger 定义（如有）

## 5. 数据模型

- [ ] ORM 模型/Schema 定义（`models/`, `entities/`, `schema/`）
- [ ] 数据库迁移文件（`migrations/`, `alembic/`）
- [ ] 数据验证（Zod/Joi/Pydantic schema）
- [ ] 类型定义文件（`types/`, `interfaces/`）

## 6. 业务逻辑

- [ ] 服务层（`services/`, `usecases/`, `domain/`）
- [ ] 核心算法和业务规则
- [ ] 状态机/工作流定义
- [ ] 事件处理/消息消费者

## 7. 前端（如适用）

- [ ] 组件目录结构（`components/`, `views/`, `pages/`）
- [ ] 状态管理（store 定义、actions、reducers）
- [ ] 路由配置
- [ ] 样式方案（CSS Modules/Tailwind/styled-components）
- [ ] 构建配置（`vite.config`, `webpack.config`, `next.config`）

## 8. 基础设施

- [ ] `Dockerfile` / `docker-compose.yml`
- [ ] CI/CD 配置（`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`）
- [ ] Kubernetes 配置（`k8s/`, `helm/`）
- [ ] IaC（Terraform/Pulumi 文件）

## 9. 测试

- [ ] 测试目录（`tests/`, `__tests__/`, `spec/`）
- [ ] 测试配置（jest.config, pytest.ini, vitest.config）
- [ ] 测试工具和 fixtures

## 10. 文档与注释

- [ ] 已有文档（`docs/`, `wiki/`）
- [ ] 代码内注释和 JSDoc/docstring
- [ ] CHANGELOG / HISTORY
- [ ] 架构决策记录（ADR）

## 扫描策略

**广度优先**：先扫描所有顶层目录和文件，建立全局视图。

**深度跟踪**：对关键模块（入口、路由、模型、服务）深入读取源码。

**依赖追踪**：从入口文件出发，沿 import/require 链追踪核心模块依赖关系。

**模式识别**：识别项目使用的设计模式（MVC/MVVM/DDD/微服务等），据此调整文档结构。
