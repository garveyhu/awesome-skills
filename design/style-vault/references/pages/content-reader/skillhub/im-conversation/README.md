---
id: pages/content-reader/skillhub/im-conversation
type: page
name: 消息会话
description: 左会话列表 + 右消息流的经典 IM 布局，带搜索 / 未读 / 气泡区分自己对方
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/skillhub/glass-pill-navbar
  - components/avatars-icons/skillhub/letter-avatar
  - components/indicators/skillhub/pulse-dot
  - components/buttons/skillhub/dark-primary-cta
  - components/inputs/skillhub/soft-form-input
  - tokens/palettes/skillhub/skillhub-teal-mist
preview: /preview/pages/content-reader/skillhub/im-conversation
---

# IM Conversation

> 双列 IM：**左侧 320px 会话列表**（含搜索 + 未读 orange 点），**右侧主流**（消息气泡自己右对齐 teal 底 · 对方左对齐 slate-50 底）。底部固定 composer。

## 页面骨架

```
┌─ GlassPillNavbar ─────────────────────────────────────┐
│                                                       │
│  ┌─ IM 容器 h-[calc(100dvh-nav)] ──────────────────┐  │
│  │ Left 320px            │ Right                   │  │
│  │ ┌──────────────────┐  │ ┌─ 顶栏 ─────────────┐   │  │
│  │ │ 搜索 / 新对话     │  │ │ 对方头像+昵称 · 在线│   │  │
│  │ └──────────────────┘  │ └───────────────────┘   │  │
│  │ ┌─ 会话条 ─────────┐  │ ┌─ 消息流 (overflow-y)┐  │  │
│  │ │ 头像 · 昵称        │  │ │   对方气泡         │  │  │
│  │ │ 最新消息预览 + time │  │ │     自己气泡       │  │  │
│  │ │ [未读红点]         │  │ │   对方气泡         │  │  │
│  │ │─ 当前选中（bg 蓝）─│ │ │     自己气泡        │  │  │
│  │ │ ...                │  │ └───────────────────┘  │  │
│  │ └──────────────────┘  │ ┌─ Composer sticky ──┐   │  │
│  │                       │ │ textarea + 发送 btn │   │  │
│  │                       │ └───────────────────┘   │  │
│  └──────────────────────┴─────────────────────────┘   │
└───────────────────────────────────────────────────────┘
```

## 核心代码（骨架）

```tsx
export const IMConversation = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [thread, setThread] = useState<MessageItem[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const threadEndRef = useRef<HTMLDivElement>(null);

  return (
    <>
      <GlassPillNavbar sticky={false} /* ... */ />

      <div className="h-[calc(100dvh-80px)] bg-white flex overflow-hidden">
        {/* 左：会话列表 */}
        <aside className="w-80 border-r border-slate-200/60 flex flex-col">
          <div className="p-4 border-b border-slate-200/60">
            <SoftFormInput placeholder="搜索会话 / 新对话" />
          </div>
          <div className="flex-1 overflow-y-auto">
            {conversations.map((c) => (
              <button
                key={c.userId}
                onClick={() => setSelectedUserId(c.userId)}
                className={`w-full px-4 py-3 flex items-start gap-3 text-left
                            hover:bg-slate-50 transition-colors
                            ${selectedUserId === c.userId ? 'bg-teal-50/40' : ''}`}
              >
                <LetterAvatar name={c.nickname} index={c.userId} size={40} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="text-sm font-bold text-slate-900 truncate">{c.nickname}</span>
                    <span className="text-xs text-slate-400 whitespace-nowrap">{formatSmartTime(c.updatedAt)}</span>
                  </div>
                  <div className="flex items-center justify-between gap-2 mt-0.5">
                    <p className="text-xs text-slate-500 truncate">{c.lastMessage}</p>
                    {c.unreadCount > 0 && (
                      <span className="shrink-0 text-[10px] font-bold text-white
                                       bg-orange-500 rounded-full px-1.5 min-w-[18px] text-center">
                        {c.unreadCount}
                      </span>
                    )}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </aside>

        {/* 右：消息主流 */}
        <main className="flex-1 flex flex-col">
          {selectedUserId ? (
            <>
              {/* 顶栏 */}
              <div className="h-14 border-b border-slate-200/60 px-6 flex items-center gap-3">
                <LetterAvatar name={'selected'} index={selectedUserId} size={32} />
                <div>
                  <div className="text-sm font-bold text-slate-900">{selectedNickname}</div>
                  <div className="text-xs text-slate-400 flex items-center gap-1.5">
                    <PulseDot color="emerald" size={6} animated={false} /> 在线
                  </div>
                </div>
              </div>

              {/* 消息流 */}
              <div ref={threadContainerRef} className="flex-1 overflow-y-auto px-6 py-4 space-y-3">
                {thread.map((m) => (
                  <MessageBubble key={m.id} own={m.fromUserId === currentUserId} {...m} />
                ))}
                <div ref={threadEndRef} />
              </div>

              {/* Composer */}
              <div className="border-t border-slate-200/60 p-4 bg-white">
                <div className="flex items-end gap-2">
                  <textarea
                    rows={2}
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
                    }}
                    placeholder="输入消息，Enter 发送 / Shift+Enter 换行"
                    className="flex-1 bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm
                               focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20
                               outline-none transition-all resize-none"
                  />
                  <DarkPrimaryCta size="md" onClick={handleSend} disabled={!newMessage.trim()}
                    icon={<Send size={14} />}>
                    发送
                  </DarkPrimaryCta>
                </div>
              </div>
            </>
          ) : (
            <EmptyState icon={MessageSquare} title="选择一个会话" hint="或在左侧搜索用户新开对话" />
          )}
        </main>
      </div>
    </>
  );
};
```

## 消息气泡

```tsx
const MessageBubble = ({ own, content, createdAt }: MessageBubbleProps) => (
  <div className={`flex ${own ? 'justify-end' : 'justify-start'}`}>
    <div className={`max-w-[70%] px-4 py-2.5 rounded-2xl text-sm
                     ${own
                       ? 'bg-teal-500 text-white rounded-br-sm'
                       : 'bg-slate-100 text-slate-900 rounded-bl-sm'}`}>
      <div className="leading-relaxed whitespace-pre-wrap">{content}</div>
      <div className={`text-[10px] mt-1 ${own ? 'text-teal-100' : 'text-slate-400'}`}>
        {formatSmartTime(createdAt)}
      </div>
    </div>
  </div>
);
```

## 视觉要点

- 外层 `h-[calc(100dvh-80px)] overflow-hidden`——不让 navbar 外的部分滚，而是消息流自己滚
- 会话列表宽 320px 固定；主流 `flex-1`
- 当前选中会话 `bg-teal-50/40` 轻染（不要全填 teal-100 太抢眼）
- 未读红点 orange，不是 rose——orange 是通知/未读的语义色；rose 留给错误态
- 气泡自己方 `bg-teal-500 text-white rounded-br-sm`（右下小圆角），对方 `bg-slate-100 rounded-bl-sm`（左下小圆角）
- Composer 用 `onKeyDown` 捕获 Enter 发送 / Shift+Enter 换行

## 适配指南

- IM 页 navbar 建议关 sticky（`sticky={false}`）——不然 h-[calc(100dvh-nav)] 计算时 sticky nav 还占位
- Composer 不要做成浮在消息流上——占底空间对齐，键盘弹起时 textarea 可见
- 消息滚动到底：`useEffect` 监听 thread.length 后 `threadEndRef.current?.scrollIntoView()`
- 新消息到达不在可视区时显示"↓ 查看新消息"小 pill（可选优化）

## 反模式

- 不要用 Antd List 做会话列表——自己 map 更好控制间距 + hover
- 不要把气泡做成尖角小三角（chat classic）——rounded-br/bl-sm 更现代
- 不要把自己方气泡做成 dark CTA 色（#1a1a1a）——会把"主动作"和"消息"语义色混
- 不要让气泡最大宽度 100%——70% 最保险，长内容自动换行
