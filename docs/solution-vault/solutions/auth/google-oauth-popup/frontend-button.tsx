/**
 * Google 登录按钮组件
 *
 * 特性：
 * - 两阶段 loading：SDK 弹窗阶段 + 后端验证阶段
 * - Google 官方彩色 logo SVG
 * - 分隔线 "或" + 按钮布局
 */

import { useState } from 'react';

// ADAPT: 替换为你的 Google auth service 导入路径
import googleAuthService from '../services/google-auth.service';

interface GoogleLoginButtonProps {
  /** 外部 loading 状态（后端验证阶段由父组件控制） */
  loading?: boolean;
  /** 成功获取 access_token 的回调 */
  onSuccess: (accessToken: string) => void;
  /** 错误回调 */
  onError: (error: string) => void;
}

const GoogleLoginButton = ({ loading: externalLoading, onSuccess, onError }: GoogleLoginButtonProps) => {
  const [requesting, setRequesting] = useState(false);
  const isLoading = requesting || externalLoading;

  const handleClick = async () => {
    setRequesting(true);
    try {
      const accessToken = await googleAuthService.requestAccessToken();
      setRequesting(false);
      onSuccess(accessToken);
    } catch (error: any) {
      setRequesting(false);
      onError(error.message || 'Google 登录失败');
    }
  };

  const loadingText = requesting ? '等待 Google 授权...' : '正在登录，请稍候...';

  return (
    <>
      {/* 分隔线 */}
      <div className="flex items-center gap-3 my-5">
        <div className="flex-1 h-px bg-slate-200" />
        <span className="text-xs text-slate-400 font-medium">或</span>
        <div className="flex-1 h-px bg-slate-200" />
      </div>
      {/* 按钮 */}
      {/* ADAPT: 按钮样式可根据项目设计系统调整 */}
      <button
        type="button"
        onClick={() => void handleClick()}
        disabled={isLoading}
        className="w-full py-3 bg-white border border-slate-300 rounded-xl text-sm font-semibold text-slate-700 hover:bg-slate-50 hover:border-slate-400 transition-all flex items-center justify-center gap-2.5 disabled:opacity-60 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-4 w-4 text-slate-400" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {loadingText}
          </>
        ) : (
          <>
            {/* Google 官方彩色 logo */}
            <svg width="18" height="18" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
            </svg>
            使用 Google 账号登录
          </>
        )}
      </button>
    </>
  );
};

export default GoogleLoginButton;
