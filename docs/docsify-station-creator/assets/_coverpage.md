<!--
  _coverpage.md · 封面页（粒子背景 + 渐变标题）
  封面与首页是【独立路由】：封面在 #/（onlyCover，不可下滑进正文），
  首页（landing）在 #/docsify/README。点目录树标题(app-name)→封面；点「文档首页」→首页。
  原则：不要 emoji。pill 标签与按钮文案按项目实际填写（3~5 个 pill 即可）。
-->

<canvas id="cover-canvas"></canvas>

# {{PROJECT_NAME}}

> {{PROJECT_DESCRIPTION}}
>
> **{{COVER_TAGLINE}}**

<span class="pill hot">{{TAG_1}}</span> <span class="pill">{{TAG_2}}</span> <span class="pill">{{TAG_3}}</span> <span class="pill">{{TAG_4}}</span>

<p class="cover-actions">
  <a class="cover-btn cover-btn-primary" href="#/docsify/README">开始阅读 →</a>
  <a class="cover-btn" href="#/{{FIRST_CONTENT_ROUTE}}">{{FIRST_CONTENT_TITLE}}</a>
</p>
