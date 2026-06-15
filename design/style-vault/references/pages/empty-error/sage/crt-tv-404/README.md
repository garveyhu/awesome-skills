---
id: pages/empty-error/sage/crt-tv-404
type: page
name: 复古电视机 404
description: 复古橘色 CRT 电视机 + 天线 + 旋钮 + 喇叭 + 彩条信号干扰屏 + 4 0 4 大字阴影
platforms: [web]
theme: light
tags:
  aesthetic: [skeuomorph, retro]
  mood: [playful, nostalgic, dreamy]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/pages/empty-error/sage/crt-tv-404
---

# CRT TV 404

> sage 通配 404 路由 `*`。整页 styled-components 手绘的复古 CRT 电视机：弯曲天线 + 橘色机身 + 圆形旋钮 + 喇叭格栅 + 屏幕彩条信号 / 雪花干扰双模式（响应式：> 1024 显雪花 / ≤ 1024 显彩条）+ 屏上 "NOT FOUND" 黑底白字 + 背景巨型 "4 0 4" 透明阴影。**纯 CSS 艺术品，无 SVG 无图片**。

## 页面骨架（自上而下）

1. **整页**：`min-height: 100vh + flex center` 居中
2. **main_wrapper**：30em 方形舞台
3. **antenna**：5em 圆形橘色 (#f27405) 头 + 阴影 `inset 0px 16px #a85103` + ::before / ::after 两片天线翘起 + 两根斜向 V 字天线（a1 / a2 不规则 polygon clip-path）+ 末端两个银色小球（a1d / a2d）
4. **tv 机身**：
   - 17×9em 橘色 (#d36604) 圆角 + `inset 0.2em 0.2em #e69635` 高光 + ::after `repeating-radial-gradient + repeating-conic-gradient` 织物纹理
   - 左上 12px SVG 弧形装饰
5. **screen / screenM 屏幕**（媒体查询互斥）：
   - **screen** (>1024px)：`repeating-radial-gradient(black/white) + repeating-conic-gradient` 雪花信号干扰，`@keyframes b` 0.2s 背景位置切换
   - **screenM** (≤1024px)：垂直 3 段彩条 = 蓝/灰/紫红/灰/青/灰/白 七色高对比 RGB 测试图样
   - 屏上 "NOT FOUND" 黑底白字 `font-size: 0.75em; padding 0.3em letter-spacing 0; border-radius 5`
6. **lines 天线根**：line1/2/3 三根黑色 25px 顶部圆角竖线（伸入机身的"线缆"）
7. **buttons_div 右侧旋钮区**：4.25×8em 橘黄竖条 + 2 圆形旋钮（b1/b2 内阴影 #b49577 + ::before/::after 旋钮指针）+ 喇叭格栅（speakers · g1 三圆点 + 两条横线 g）
8. **bottom 支架**：base1/base2 两根 2×1em 灰色竖立支架 + base3 17.5em 黑底横杆
9. **text_404**：z-index -5 巨大 4 0 4，`transform: scaleY(24.5) scaleX(9)` 拉成阴影背景，`opacity: 0.5`

## 视觉要点

1. **整页只用一个 styled-components Card 组件 + 600 行 CSS**，无 props，无 state——纯静态艺术品
2. **配色固定 5 色**：`#f27405` 橘色头 / `#a85103` 深橘内阴影 / `#d36604` 主橘机身 / `#e69635` 浅橘高光 / `#171717` 黑色框线
3. **响应式互斥**：> 1024 走雪花信号；≤ 1024 走彩条；< 495 减少字 spacing；< 275 加 position relative
4. **screen 雪花动画**：`@keyframes b 100% { background-position: 50% 0, 60% 50% }` 0.2s 重复——做出"信号闪动"的电视感
5. **整组天线 / 旋钮 / 喇叭 / 支架** 全靠 box-shadow + ::before / ::after 伪元素拼装，不引入任何 SVG / 图片资源
6. **font-family Montserrat** —— 仅 404 大字用，跟 sage 主体 Inter 错开，给"复古"打标签

## 适配指南

- 视觉风格 100% 独立于 sage 整站——这是 sage 的"性格出口"，不要把它改成跟 chat 同样的 minimalism
- 不要替换为业务相关 404 illustration（团队人物 / 产品 logo 等）—— 这个 CRT 是"我们的开发者有趣"的暗号
- 文案可换："NOT FOUND" → "404" / 自定义口号 都 OK，但保持 6 字以内大写

## 反模式

- ❌ 替换为 antd Result 组件 —— 失去 sage 的彩蛋人格
- ❌ 加 "返回首页" 按钮 —— 这页的态度是 "你迷路了，逛逛吧"，按钮会破坏纯装饰感
- ❌ 简化到只剩屏幕 —— 整个 CRT 的天线 / 旋钮 / 喇叭 / 支架是一体的，少一样都失去性格
