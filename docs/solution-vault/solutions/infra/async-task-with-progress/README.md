# 长耗时操作异步任务 + 实时进度条

> 把 5 秒以上的操作改为后台任务，前端轮询进度，不再阻塞 HTTP 连接也不再白屏。

## 适用场景

- Excel 批量导入（100+ 条）、批量向量化 / embedding
- 数据库迁移、批量数据清洗
- 重新训练索引、重建缓存
- 任何单次调用会超过 5-10 秒的同步接口
- 前端希望看到"当前处理到第 N 条 / N%"的实时进度

**不适合**：秒级完成的操作（进度条会闪一下很突兀，直接同步返回更好）。

## 技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 状态存储 | 进程内单例 + `dict` | 单进程部署够用，不需要 Redis。多进程时再换 |
| 后台执行 | `threading.Thread(daemon=True)` | 导入/向量化是 I/O bound，GIL 不是瓶颈。不用 asyncio 避免侵入同步代码 |
| 进度同步 | 轮询（GET /task/{id}/status 每 1s） | 比 SSE / WebSocket 简单得多，不需要处理连接生命周期，经代理穿透好 |
| 任务 ID | `uuid.uuid4()[:8]` | 8 位够用（并发任务远小于 2^32），全局唯一，可安全打日志 |
| 状态枚举 | pending / running / completed / failed | 覆盖所有 UI 态：排队中、执行中、成功、失败 |
| 进度模型 | `total / processed / current_item / percentage` | percentage 由 total/processed 计算，避免前后端算不一致 |
| 清理策略 | 超过 100 个任务时删最旧的一半 | 内存不会无限增长；已完成任务保留一段时间方便复查 |

## 技术栈要求

- **后端**: Python（FastAPI / Flask / Django 均可）+ SQLAlchemy（或任意 ORM）
- **前端**: React + TypeScript（普通 JS 也能用，但类型清晰度会降）
- **浏览器**: 支持 `setInterval` 即可，无特殊要求

## 文件清单

| 文件 | 说明 |
|------|------|
| `backend-task-manager.py` | 核心 `AsyncTaskManager` 单例：任务创建 / 进度更新 / 后台线程启动 |
| `backend-worker.py` | 典型 worker 模板：**如何正确更新进度**（踩坑点都标注了） |
| `backend-route.py` | 两个端点：`POST /xxx-async` 启动任务、`GET /task/{id}/status` 查进度 |
| `frontend-api.ts` | API 客户端：`startXxxAsync` + `getTaskStatus` |
| `frontend-polling.tsx` | React 组件模板：启动任务 + 1s 轮询 + 进度条 UI + Modal 禁用交互 |
| `frontend-types.ts` | AsyncTask / TaskProgress / AsyncTaskStartResponse 类型 |

## 适配指南

复刻到新项目时需要调整：

1. **任务类型字符串** — 替换 `task_type` 常量（如 `"import_business_rules"` → 你的业务名）
2. **worker 业务逻辑** — `backend-worker.py` 里的"阶段 1 / 阶段 2"换成你的实际操作
3. **DB Session** — 替换 `SessionLocal` 为你项目的 Session 工厂
4. **响应封装** — 替换 `Result.ok()` 为你项目的响应标准
5. **API 路径** — 替换 `/xxx-async` 和 `/task/{id}/status` 前缀
6. **进度 UI 组件** — `CrystalProgress` 或任何进度条都行（Ant Design Progress、shadcn Progress、自己做的都可以）
7. **权限装饰器** — 替换 `PermissionChecker(...)` 为你项目的鉴权

所有需要适配的地方在模板代码中用 `# ADAPT:` 或 `// ADAPT:` 标注。

## 核心陷阱（踩过的坑）

### 1. 进度条跳回去 bug ⚠️ 最容易踩

**现象**：点击开始后进度先冲到 100%，然后重置到 0% 再慢慢爬。

**原因**：worker 有"准备阶段"和"执行阶段"两段逻辑，两段都在更新 `processed`。准备阶段快速跑完会让 `processed == total` → 瞬间 100%；执行阶段又从小数字累加。

**正解**：**只有真正耗时的那一段才更新 `processed`**。准备/去重/校验阶段只更新 `current_item` 文字，不动 `processed`。

```python
# ❌ 错误：两段都 update processed
for row in rows:
    # fast dedup
    processed += 1
    update_progress(processed=processed)  # 会到 100%

for batch in batches:
    # slow work
    processed = skipped + batch_end  # 从小数字重来
    update_progress(processed=processed)

# ✅ 正确：准备阶段只更新文字
for row in rows:
    # fast dedup
    pass  # 不 update processed
update_progress(processed=skipped, current_item="开始执行...")

for batch in batches:
    # slow work
    update_progress(processed=skipped + batch_end, ...)
```

### 2. 网络抖动导致轮询中断

前端 `getTaskStatus` 失败时**不要停止轮询**，catch 住继续。任务在后端还在跑，轮询恢复后能拿到最新状态。

### 3. Modal 关闭不意外中止任务

后台线程独立于 HTTP 连接，即使用户关了浏览器任务照样跑完。但 Modal 组件销毁后 setState 会报 warning，所以轮询时要检查组件是否 mounted（React 18 严格模式下尤其明显）。

**简化方案**：任务进行中禁用 Modal 的 `maskClosable` 和 `closable`，避免用户在运行期关闭。

### 4. 任务 ID 生命周期

任务完成后不要立刻删除 — 前端最后一次轮询可能还需要拿 `result`。`AsyncTaskManager` 保留最近 100 个任务就是这个目的。

### 5. 多进程部署时会失效

`_tasks` 是进程内 dict。如果用 gunicorn 多 worker，每个进程有自己的 dict，`start` 请求落在 A 进程、`status` 请求落在 B 进程就查不到。

**解决**：
- 方案 A：固定单进程（加 `--workers 1`）
- 方案 B：把 `_tasks` 换成 Redis（见 `AsyncTaskManager._tasks` 那里的注释）
- 方案 C：用 sticky session 让同 task_id 落到同 worker

### 6. 不要把整张 Excel bytes 塞进 task result

任务参数通过 `run_in_background(*args, **kwargs)` 传进线程，但**不要**把大 payload（如 Excel 原文件）塞到 `task.result` 里，那是给前端 JSON 序列化用的。result 只放统计汇总。

## 示例统计值（参考）

实际项目里 400 条业务规则导入：
- 优化前：同步接口 13 秒（卡住前端），偶发超时
- 优化后：接口 50ms 返回 task_id，后台 3.5 秒完成（embedding 从 400 次降到 13 次批量调用），进度条平滑 0 → 100%
