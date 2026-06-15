# comfy-workflows/(项目专用工作流)

只放**本项目专属**的 ComfyUI 工作流(固定构图、特殊产线等)。反向软链到
`<ComfyUI>/user/default/workflows/projects/<项目>/`,画布可编辑、随 git 共享。

**通用工作流不放这**:`t2i` / `i2i`(图生图编辑、角色动作)/ 抠图 / `i2v` 走 comfyui skill 的
canonical 工作流(`comfy.py t2i/i2i/i2v`;`assets.json` 里写 `workflow: "i2i"` 等,batch 自动
路由到 skill,不用在这放副本)。

需要项目专属工作流时,把 `<名>.json` 放进来,assets.json 里 `workflow: "<名>"` 引用即可。
