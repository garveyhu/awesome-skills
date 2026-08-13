# 素材溯源 · style-vault 自指沉淀

## 项目路径
- $PROJECT = ~/Coding/Archer/style-vault（即 vault 网站自身仓）
- 技术栈指纹：react@19 + antd@6 + tailwind@3 + react-router-dom@7 + vite@8
- VAULT_OK = true（项目即 vault，preview tsx 直接写在 frontend/src/preview/）

## 关键源文件

### Tokens 来源
- `frontend/tailwind.config.js`（fontFamily 仅 Inter / display 同一字族）
- `frontend/src/index.css`（285 行，全部 sv-* 全局类 + keyframes）
  - L37-50：sv-fade-up / sv-fade-in keyframes
  - L52-66：sv-blob-drift / sv-blob-drift-slow keyframes（双 blob 异步漂移）
  - L83-103：8 个 fade-up 延迟槽 sv-delay-{0,75,150,225,300,400,500,600}
  - L132-167：sv-underline-tab + scaleX gradient cyan→slate-900
  - L173-205：sv-text-link "查看更多" 下划线 hover 铺满 + 箭头位移
  - L208-238：.sv-card hover 浮起 + 三层柔投影 + 内容缩放
  - L241-247：sv-anim-breathe 空态 blob 呼吸

### Pages 来源
- `frontend/src/App.tsx`（路由清单 + lazy preview glob）
- `frontend/src/pages/HomePage.tsx`（458 行，落地页 5 段堆叠）
- `frontend/src/pages/BrowsePage.tsx`（97 行，五类目每类一行）
- `frontend/src/pages/BrowseCategoryPage.tsx`（156 行）
- `frontend/src/pages/DetailPage.tsx`（465 行，左 sidebar + 右 chrome）
- `frontend/src/pages/ProductListPage.tsx`（260 行，浮起作品照行卡）
- `frontend/src/pages/ProductDetailPage.tsx`（558 行，cover hero + sticky TOC + masonry）
- `frontend/src/pages/ProfilePage.tsx`（323 行）

### Components 来源
- `frontend/src/components/StyleCard.tsx`（246 行，1440 虚拟视口缩放卡）
- `frontend/src/components/TopBar.tsx`（159 行，sticky 玻璃感顶栏）
- `frontend/src/components/CategoryTabs.tsx`（45 行，sticky 大档下划线 tab）
- HomePage 各部件 inline（dark-pill-cta / cyan-dot-meta-pill / value block）
- DetailPage CTA（ghost-bordered-cta / browser-chrome-frame）

## taxonomy 字典改动

`~/.agents/skills/style-vault/assets/taxonomy.json`：
- 新增 `category.design = { zh: "设计", dot: "#6366f1", order: 6 }`

## 识别的技术栈

react-antd-tailwind（package.json 含 react@19 + antd@6 + tailwindcss@3）

## 自指沉淀注释

这是一次"自己沉淀自己"的沉淀。skill 仓 ref markdown 写在 `~/.agents/skills/style-vault/references/` 下，preview tsx 直接写在被沉淀的项目自身 `frontend/src/preview/` 下——两者本就是同一套同步关系（skill = 真相源 / 网站 = 渲染层）。

唯一需要注意：项目里有 1 个预先修改 `frontend/src/pages/ProductDetailPage.tsx`（用户进行中工作），与本次沉淀无关，commit 时显式跳过。
