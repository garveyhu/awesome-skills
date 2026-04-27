---
id: blocks/form/sage/chat-composer
type: block
name: 消息输入器
description: 整体 ChatInput 模块——glow border textarea + skill bar + voice + send/stop，sage 主聊天页输入腰带
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, confident, dreamy]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/sage/twelve-theme-spectrum
  - components/inputs/sage/glow-border-textarea
  - components/buttons/sage/theme-bg-cta
  - components/buttons/sage/stop-pulse-button
preview: /preview/blocks/form/sage/chat-composer
---

# Chat Composer

> ChatPage 底部消息输入腰带——一个圆角 24 的大白盒，包含 textarea + 左下技能栏 + 右下工具组（voice / send 或 stop）。focus 时整个盒子打主题色霓虹光晕；技能激活时（数据查询 / 代码 / 搜索）显示技能配置条；textarea 自动 resize 到 200px max。底部一行 disclaimer。

## 视觉特征 / 关键结构

- 父容器：`fixed | sticky bottom 区域 + 内含 max-w-4xl mx-auto`
- 推荐问题 tip 行（顶部）：`flex items-center gap-2 mb-2 + text-xs text-slate-400 + 横滚 chip 列表`
- form 主体：`flex flex-col gap-0 bg-white border rounded-[24px] shadow-sm transition-all p-2.5`
- form border + glow（见 `components/inputs/sage/glow-border-textarea`）
- textarea 行：`relative w-full + textarea auto-resize + min-h-[35px] max-h-[200px]`
- AI 联想气泡（textarea 上方）：`absolute bottom-full bg-white border border-gray-200 rounded-xl shadow-lg mb-2 overflow-hidden z-10`，header `bg-gray-50 + text-xs font-medium text-gray-500`，每条 `hover:bg-gray-50` 边间 `border-b border-gray-100 last:border-0`
- Controls Row：`flex justify-between items-center pt-1 select-none`
- 左侧（技能 / 配置）：技能未激活时 `<SkillBar>`（chip 列表）；激活时 `<SkillConfigBar>`（如选数据源 / 选代码语言）+ 关闭按钮
- 右侧：`flex items-center gap-2 + <VoiceRecorder> + 1px 5px 高 bg-gray-200 分隔 + send 或 stop`
- send：`w-8 h-8 ${themeClasses.bg} ${themeClasses.bgHover} text-white rounded-full + Send size={16} -ml-0.5 mt-0.5 + disabled:opacity-40`
- stop（loading 时）：见 `components/buttons/sage/stop-pulse-button`
- disclaimer：`text-center text-xs text-gray-400 mt-2 mb-2`

## 核心代码

```tsx
<form
  onSubmit={handleSubmit}
  onFocus={() => setIsFocused(true)}
  onBlur={() => setIsFocused(false)}
  className="relative flex flex-col gap-0 bg-white border rounded-[24px] shadow-sm transition-all p-2.5"
  style={{
    borderColor: isInSkillMode || isFocused ? `${hex}50` : '#e2e8f0',
    boxShadow: isInSkillMode || isFocused
      ? `0 0 4px ${hex}40, 0 0 15px ${hex}30`
      : `0 0 4px rgba(148, 163, 184, 0.15), 0 0 15px rgba(148, 163, 184, 0.08)`,
  }}
>
  {/* AI 联想 */}
  {showSuggestions && (
    <div className="absolute bottom-full left-0 w-full bg-white border border-gray-200 rounded-xl shadow-lg mb-2 overflow-hidden z-10">
      <div className="flex justify-between px-4 py-2 bg-gray-50 border-b border-gray-100">
        <span className="text-xs font-medium text-gray-500">AI 联想</span>
        <button onClick={() => setShowSuggestions(false)}><X size={14} /></button>
      </div>
      {suggestions.map(s => (
        <button onClick={() => apply(s)} className="w-full text-left px-4 py-3 hover:bg-gray-50 text-sm text-gray-700 border-b border-gray-100 last:border-0 flex items-center gap-2">
          <Sparkles size={14} className={tc.text} /> {s}
        </button>
      ))}
    </div>
  )}

  <textarea
    ref={textareaRef}
    rows={1}
    placeholder={...}
    className={`w-full bg-transparent border-none pl-2.5 focus:ring-0 outline-none px-1 py-1 text-base text-gray-800 placeholder:text-gray-400 resize-none overflow-hidden min-h-[35px] max-h-[200px] ${isLoading ? 'opacity-60' : ''}`}
  />

  <div className="flex justify-between items-center pt-1 select-none">
    <div className="flex items-center gap-1.5 flex-1 min-w-0">
      {activeSkill ? <SkillConfigBar ... /> : <SkillBar ... />}
    </div>
    <div className="flex items-center gap-2 select-none">
      <VoiceRecorder onTranscript={handleVoice} themeColor={themeColor} />
      <div className="w-px h-5 bg-gray-200 ml-0.5 mr-1" />
      {isLoading ? <StopPulseButton onStop={onStop} themeColor={themeColor} /> : (
        <button type="submit" disabled={!canSend()} className={`w-8 h-8 flex items-center justify-center ${tc.bg} ${tc.bgHover} text-white rounded-full disabled:opacity-40 disabled:cursor-not-allowed transition-colors`}>
          <Send size={16} className="-ml-0.5 mt-0.5" />
        </button>
      )}
    </div>
  </div>
</form>

<p className="text-center text-xs text-gray-400 mt-2 mb-2">AI 也会出错 — 关键决策请二次确认</p>
```

## 视觉要点

1. **rounded-[24px]** 不是常规 rounded-3xl(24) 的 alias，而是显式的 24px——配合 textarea 25px min-height 形成"几乎一个圆"的视觉
2. 技能激活后 `isInSkillMode || isFocused` 共用同一组光晕——意味着选了技能即"已沉浸"
3. textarea `pl-2.5`（10px）给文字留呼吸感，比 px-1 大
4. 中间分隔条 `w-px h-5 bg-gray-200 ml-0.5 mr-1` 极细短—— sage 用最小化的视觉切分
5. send 按钮 `<Send>` 内部 `-ml-0.5 mt-0.5` 微偏移让箭头看起来居中（默认 SVG 视觉重心偏右下）

## 适配指南

- skill 激活时屏蔽掉 SessionConfig 中的 ephemeral key（防火墙逻辑）—— 保证下次切换技能时清干净
- AI 联想用 debounce 300ms 触发 `chatApi.getSuggestions(input)`
- VoiceRecorder 是独立组件，传 `onTranscript` 回调把语音文字塞回 input
- isLoading 期间 `disabled` textarea + 切 stop 按钮

## 反模式

- ❌ 把 chat composer 写成 fixed bottom，而非父级 flex —— 移动端键盘弹起会盖住
- ❌ 移除 disclaimer —— sage 显式声明 "AI 也会出错"，是合规要求
