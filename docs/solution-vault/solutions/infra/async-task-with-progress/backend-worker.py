"""
Worker 模板：两阶段（快速准备 + 慢速执行）的典型长耗时操作。

这里以"Excel 批量导入 + 向量化"为例，但结构适用于任何两阶段任务：
- 阶段 1（快）：解析 / 去重 / 校验，毫秒级完成
- 阶段 2（慢）：批量调外部 API（embedding / LLM / 第三方服务），秒级以上

关键规则（见 README 陷阱 1）：
    processed 必须单调递增，只有阶段 2 才推进 processed。
    阶段 1 只更新 current_item 文字，不动 processed。
"""

from typing import List, Optional

from loguru import logger

# ADAPT: 替换为你项目的任务管理器、DB Session、业务模型、向量组件
from .backend_task_manager import async_task_manager
from app.db import SessionLocal
from app.models import BusinessRule
from app.vector import VectorIndexManager

VECTOR_BATCH_SIZE = 32  # ADAPT: 根据你的 embedding API 限制调整


class ImportService:
    @staticmethod
    def import_async(
        file_bytes: bytes,
        space_id: int,
        datasource_id: Optional[int],
    ) -> str:
        """启动异步导入任务，立即返回 task_id。"""
        task = async_task_manager.create_task("import_business_rules")
        async_task_manager.run_in_background(
            task.task_id,
            ImportService._worker,
            file_bytes=file_bytes,
            space_id=space_id,
            datasource_id=datasource_id,
        )
        return task.task_id

    @staticmethod
    def _worker(
        task_id: str,
        file_bytes: bytes,
        space_id: int,
        datasource_id: Optional[int],
    ):
        """后台 worker。异常会被 AsyncTaskManager.run_in_background 捕获并 fail_task。"""
        db = SessionLocal()
        created = 0
        skipped = 0
        errors: List[str] = []

        try:
            # ---------- 阶段 0：解析输入（可能失败就 fail_task 提前退出） ----------
            try:
                valid_rows = _parse_input(file_bytes)  # ADAPT: 你的解析逻辑
            except Exception as e:
                async_task_manager.fail_task(task_id, f"解析失败: {e}")
                return

            # total 设为"用户关心的总数"（这里是有效行数）
            async_task_manager.start_task(task_id, len(valid_rows))
            async_task_manager.update_progress(
                task_id, processed=0, current_item="正在检查重复..."
            )

            # ---------- 阶段 1：快速去重 / 校验（不动 processed） ----------
            # 一次性 SELECT 所有既有记录到 set，取代逐行 SELECT
            existing: set[str] = {
                r[0]
                for r in db.query(BusinessRule.rule)
                .filter(BusinessRule.space_id == space_id)
                .all()
            }

            pending: List[BusinessRule] = []
            for row in valid_rows:
                key = row["rule"]
                if key in existing:
                    skipped += 1
                    continue
                existing.add(key)
                try:
                    pending.append(BusinessRule(**row, space_id=space_id, datasource_id=datasource_id))
                except Exception as e:
                    errors.append(f"第 {row.get('row_idx')} 行: {e}")
                # 注意：这里**不**调 update_progress(processed=...)！

            if not pending:
                async_task_manager.complete_task(
                    task_id,
                    {"created": 0, "skipped": skipped, "errors": errors[:10]},
                )
                return

            # ---------- 阶段 2 入口：跳过的数量先计入 processed ----------
            async_task_manager.update_progress(
                task_id, processed=skipped, current_item="正在写入数据库..."
            )

            # 批量入库 + flush 拿自增 id（向量化要用）
            db.add_all(pending)
            db.flush()

            # ---------- 阶段 2：分批向量化（慢操作，推进 processed） ----------
            vector_manager = VectorIndexManager(space_id, datasource_id or 0)
            total_pending = len(pending)

            for batch_start in range(0, total_pending, VECTOR_BATCH_SIZE):
                batch = pending[batch_start : batch_start + VECTOR_BATCH_SIZE]
                try:
                    vector_manager.rules.add_rules_batch(
                        [_to_vector_dict(r) for r in batch]  # ADAPT: 转向量库需要的字段
                    )
                    created += len(batch)
                except Exception as e:
                    logger.error(f"批量向量化失败: {e}")
                    errors.append(f"向量化第 {batch_start + 1}-{batch_start + len(batch)} 条失败: {e}")

                batch_end = batch_start + len(batch)
                current_label = batch[-1].name or batch[-1].rule[:20]
                async_task_manager.update_progress(
                    task_id,
                    # processed = 已跳过 + 已处理完的 pending 数量，最终等于 total
                    processed=skipped + batch_end,
                    current_item=f"向量化 ({batch_end}/{total_pending}): {current_label}",
                )

            db.commit()

            async_task_manager.complete_task(
                task_id,
                {"created": created, "skipped": skipped, "errors": errors[:10]},
            )
            logger.info(
                f"Async import done: created={created} skipped={skipped} errors={len(errors)}"
            )

        except Exception as e:
            logger.error(f"Async import failed: {e}")
            db.rollback()
            async_task_manager.fail_task(task_id, str(e))
        finally:
            db.close()


def _parse_input(file_bytes: bytes) -> List[dict]:
    # ADAPT: 你的解析逻辑（openpyxl / csv / json / ...）
    raise NotImplementedError


def _to_vector_dict(record) -> dict:
    # ADAPT: 把你的 ORM record 转成向量库 add_batch 需要的字典
    raise NotImplementedError
