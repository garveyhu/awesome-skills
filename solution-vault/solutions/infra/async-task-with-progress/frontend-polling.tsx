/**
 * 前端典型用法：一个带进度条的导入 Modal。
 *
 * 关键逻辑：
 * 1. 点击上传 → 启动任务 → setInterval 轮询 getTaskStatus
 * 2. 每次轮询更新 progress 状态；单个请求失败不中断轮询
 * 3. 任务完成/失败时 clearInterval + 提示 + 关闭 Modal
 * 4. 进行中禁用 Modal 关闭，避免用户误操作
 */
import { Modal, Select, Upload, message } from 'antd';
import { RefreshCw, Upload as UploadIcon } from 'lucide-react';
import React, { useState } from 'react';

// ADAPT: 替换导入路径
import { asyncTaskApi } from './frontend-api';
// ADAPT: 换成你项目的进度条组件（Antd Progress / shadcn Progress / 自己的都行）
import CrystalProgress from '@/components/CrystalProgress';

// ADAPT: 任务结果类型（与后端 complete_task 里 result 对齐）
interface ImportResult {
  created?: number;
  skipped?: number;
  errors?: string[];
}

interface Props {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  primaryColor?: string; // ADAPT: 主题色，也可以写死
}

export const ImportModal: React.FC<Props> = ({
  open,
  onClose,
  onSuccess,
  primaryColor = '#2B6CB0',
}) => {
  const [importing, setImporting] = useState(false);
  const [datasourceId, setDatasourceId] = useState<number | undefined>();
  const [progress, setProgress] = useState({
    total: 0,
    processed: 0,
    currentItem: '',
    percentage: 0,
  });

  const handleImport = async (file: File) => {
    setImporting(true);
    setProgress({ total: 0, processed: 0, currentItem: '准备中...', percentage: 0 });

    try {
      const startRes = await asyncTaskApi.startImport(file, datasourceId);
      if (!startRes.success || !startRes.data) {
        message.error(startRes.message || '启动任务失败');
        setImporting(false);
        return;
      }
      const taskId = startRes.data.taskId;

      // 用 Promise + setInterval 轮询，任务结束 resolve
      await new Promise<void>(resolve => {
        const timer = setInterval(async () => {
          try {
            const statusRes = await asyncTaskApi.getTaskStatus<ImportResult>(taskId);
            if (!statusRes.success || !statusRes.data) return;
            const task = statusRes.data;

            setProgress({
              total: task.progress.total,
              processed: task.progress.processed,
              currentItem: task.progress.currentItem,
              percentage: task.progress.percentage,
            });

            if (task.status === 'completed') {
              clearInterval(timer);
              const d = task.result;
              message.success(
                `导入完成：新增 ${d?.created || 0} 条，跳过重复 ${d?.skipped || 0} 条`,
              );
              if (d?.errors?.length) {
                message.warning(`${d.errors.length} 条导入出错`);
              }
              onSuccess();
              onClose();
              resolve();
            } else if (task.status === 'failed') {
              clearInterval(timer);
              message.error(task.error || '任务执行失败');
              resolve();
            }
          } catch {
            // 网络抖动容忍，继续轮询。任务在后端还在跑。
          }
        }, 1000); // ADAPT: 轮询频率，1s 通常够用
      });
    } catch {
      message.error('导入失败');
    } finally {
      setImporting(false);
      setProgress({ total: 0, processed: 0, currentItem: '', percentage: 0 });
    }
  };

  return (
    <Modal
      title="导入"
      open={open}
      onCancel={() => !importing && onClose()}
      footer={null}
      width={480}
      // 关键：任务进行中禁用关闭，避免 Modal 销毁导致 setState 警告
      maskClosable={!importing}
      closable={!importing}
    >
      <div className="space-y-4 mt-4">
        <Select
          placeholder="选择关联项"
          allowClear
          style={{ width: '100%' }}
          value={datasourceId}
          onChange={setDatasourceId}
          disabled={importing}
          options={[]} // ADAPT: 你的 options
        />

        {importing && (
          <div
            className="p-4 rounded-lg border flex flex-col gap-2"
            style={{
              backgroundColor: `${primaryColor}08`,
              borderColor: `${primaryColor}20`,
            }}
          >
            <div className="flex items-center gap-2 text-sm font-medium" style={{ color: primaryColor }}>
              <RefreshCw size={14} className="animate-spin" />
              正在导入
            </div>
            <CrystalProgress percent={progress.percentage} color={primaryColor} />
            <div
              className="flex justify-between text-xs opacity-70"
              style={{ color: primaryColor }}
            >
              <span className="truncate mr-2">{progress.currentItem}</span>
              <span>{Math.floor(progress.percentage)}%</span>
            </div>
          </div>
        )}

        <Upload.Dragger
          accept=".xlsx,.xls"
          showUploadList={false}
          beforeUpload={file => {
            handleImport(file);
            return false; // 阻止默认上传
          }}
          disabled={importing}
        >
          <div className="py-4">
            <UploadIcon size={32} className="mx-auto text-neutral-400 mb-2" />
            <div className="text-sm text-neutral-600">
              {importing ? '导入中...' : '点击或拖拽文件到此处'}
            </div>
          </div>
        </Upload.Dragger>
      </div>
    </Modal>
  );
};
