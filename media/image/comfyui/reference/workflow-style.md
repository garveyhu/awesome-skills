# 画布工作流出厂标准(强制)

> **铁律:用本 skill 创建/产出的任何「画布工作流」(给人在 ComfyUI 网页里用的 .json),
> 都必须达到本标准——分组 + 说明 + 命名 + 布局。不达标不算完成。**
> 参考官方 `image_z_image_turbo` / `video_wan2_2_5B_ti2v` 的质感。
> 现成范例(照抄结构):`workflows/image/image_cutout_rmbg2_sam2.json`、`image_qwen_image_edit_2511.json`。

## 1. 命名:`<媒介>_<主模型>[_版本/变体]`
- 前缀媒介:`image_` / `video_`;全小写、下划线分词。
- **必须带上主模型名**:
  - `image_qwen_image_edit_2511`(Qwen-Image-Edit 编辑)
  - `image_cutout_rmbg2_sam2`(RMBG-2.0 自动 + SAM2 文字抠图)
  - `image_z_image_turbo`、`video_wan2_2_5B_ti2v`(官方)
- ❌ 不要 `edit` / `cutout` / `my_workflow` 这种没模型名的裸名。

## 2. 分组(必须):彩色 Group 框 + 步骤标题
按数据流分 3–5 个步骤组,标题带序号:
```
① 输入/上传  →  ② 加载模型(设一次)  →  ③ 提示词/参数  →  ④ 输出
```
- 颜色:动作/可调组用 `#3f789e`(蓝);"设一次"的模型加载组用 `#444`(灰)淡化。
- 用 **`scripts/build/groupify.py`** 机械加组(按节点位置自动算 bounding):
  ```bash
  python scripts/build/groupify.py <wf>.json --spec spec.json --inplace
  ```
  spec.json 见该脚本头部;`groups[].nodes` 填该组的节点 id,`note` 填用法说明。

## 3. 说明 Note(必须)
左上方放一个 `Note` 节点(groupify 的 `note` 字段自动加),写清:**①②③④ 每步干什么 + 关键参数/注意**(如 cfg 取值、提示词语言、Mac 注意)。让人不看文档也会用。

## 4. 布局(必须)
- **输入/上传节点放左上角**(最小 x、最小 y),数据流**从左到右**。
- 尽量**一屏装下**(节点别一条线拖太长;多了换行成 2 行或竖排末列)。
- 节点不重叠(同列 x 间距 ≥ 节点宽 + 40)。
- 参数(seed/steps/cfg/size…)归到对应步骤组,别散落。

## 5. 干净
- 一个用途一个工作流(别把无关功能塞一起)。
- 用得上的参数留,没用的别外露;复杂内部链尽量收进核心组。
- 正/负提示词节点加 `title`(✅正面 / 🚫负面)区分。

## 6. 出厂流程(建任何工作流照此)
1. 写/改 **API 格式** `*.api.json`(节点链,见 `api-format.md`);
2. `api2ui.py` 转 UI `.json`;
3. **排版**(输入左上、左→右、一屏内);
4. **`groupify.py --spec`** 加分组框 + Note;
5. 放进 skill `workflows/<媒体>/` + 在 `workflows/catalog.json` 加一条(category/task/file/vars/models/nodes/note);`init` 会自动拷到 `<ComfyUI>/user/default/workflows/`;
6. 自检:命名带模型名?✓ 有分组?✓ 有 Note?✓ 输入左上?✓ 一屏?✓

> 自定义节点同样沉淀进 `comfyui-nodes/`(`init` 安装);模型/依赖写进 `manifests/models.json`,复刻脚本 `scripts/setup/`。
