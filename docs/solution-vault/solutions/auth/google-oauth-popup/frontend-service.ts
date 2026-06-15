/**
 * Google OAuth 前端服务
 *
 * 使用 Google Identity Services SDK 的 OAuth2 Token Client
 * 弹出独立授权窗口，获取 access_token 后发送给后端验证
 */

// ADAPT: 替换为你的 HTTP 客户端和类型
import { post } from '@/core/services';
import type { ResultVO } from '@/core/types/api';

// ADAPT: 替换为你的 Google Client ID
const GOOGLE_CLIENT_ID = '{{YOUR_GOOGLE_CLIENT_ID}}';

// ADAPT: 替换为你的登录响应类型
interface GoogleLoginPayload {
  accessToken: string;
  user: {
    id: number;
    email: string;
    nickname: string;
    avatarUrl: string | null;
  };
  isNewUser: boolean;
}

// --- Google SDK 类型声明 ---

interface TokenResponse {
  access_token: string;
  error?: string;
}

interface TokenClient {
  requestAccessToken: () => void;
}

declare global {
  interface Window {
    google?: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: (response: TokenResponse) => void;
          }) => TokenClient;
        };
      };
    };
  }
}

// --- Service ---

export const googleAuthService = {
  /**
   * 弹出 Google OAuth 独立授权窗口，返回 access_token。
   * 用户关闭弹窗时 Promise 不会 resolve 也不会 reject（SDK 限制）。
   */
  requestAccessToken: (): Promise<string> => {
    return new Promise((resolve, reject) => {
      if (!window.google?.accounts?.oauth2) {
        reject(new Error('Google SDK 未加载，请刷新页面重试'));
        return;
      }

      const client = window.google.accounts.oauth2.initTokenClient({
        client_id: GOOGLE_CLIENT_ID,
        scope: 'openid email profile',
        callback: (response: TokenResponse) => {
          if (response.error) {
            reject(new Error(`Google 登录失败: ${response.error}`));
            return;
          }
          resolve(response.access_token);
        },
      });

      client.requestAccessToken();
    });
  },

  /** 将 access_token 发送到后端进行登录 */
  login: (accessToken: string): Promise<ResultVO<GoogleLoginPayload>> => {
    // ADAPT: 替换为你的登录 API 路径
    return post('/auth/google', { accessToken });
  },

  /** 将 access_token 发送到后端绑定到当前用户 */
  bind: (accessToken: string): Promise<ResultVO<any>> => {
    // ADAPT: 替换为你的绑定 API 路径
    return post('/auth/google/bind', { accessToken });
  },
};

export default googleAuthService;
