# astralow-for-editable-ppt

将整页 PNG、幻灯片截图或图片型 PPT 的页面转换成可编辑 PowerPoint。模型负责理解原图与重建布局，Skill 提供轻量绘图、PowerPoint 实际渲染和按需检查工具。

本仓库现以 `astralow-for-editable-ppt` 替代旧 `ppt-to-editable`，仓库地址保持不变。旧用户请看 [升级说明](UPGRADE.md)。

## 安装与下载

[下载仓库 ZIP](https://github.com/Pikapika260214/ppt-to-editable-3-0/archive/refs/heads/main.zip)，将 `skills/astralow-for-editable-ppt` 文件夹复制到你的 Codex skills 目录：

- Windows：`%USERPROFILE%\.codex\skills\astralow-for-editable-ppt`
- macOS/Linux：`~/.codex/skills/astralow-for-editable-ppt`

也可以向 Codex 提出：

```text
请从 https://github.com/Pikapika260214/ppt-to-editable-3-0 安装 Skill，路径为 skills/astralow-for-editable-ppt。
```

Python 3.10+，在下载的仓库根目录安装依赖：

```sh
python -m pip install -r requirements.txt
```

实际 Office 渲染与编辑验证需要 Windows 桌面版 PowerPoint。其他环境可以构建 PPTX，但不能据此宣称通过 Office 验证。

## 使用流程

1. 在调用环境选择 Astra low；Skill 本身不会切换模型。
2. 提供一张完整页面 PNG 或截图，提出以下请求。
3. 查看交付的 PPTX 和实际渲染预览，确认还原效果与需要编辑的元素。

```text
使用 $astralow-for-editable-ppt 将这张图转成可编辑 PPT。
保留原文、布局和视觉关系，主要文字、数字与结构使用原生可编辑对象。
输出 PPTX 和实际渲染预览，说明哪些局部仍是图片。
```

基础工具一次处理一张源图、一页 PPT。多页需逐页处理后另行合并并检查；本包没有通用多页合并器，也不沿用旧版 controller 命令。

## 能力与限制

- 文字、数字和适合原生表达的结构重建为可编辑对象；复杂照片或视觉可保留局部裁图。
- 提供绘图、保存、实际渲染、简短报告和副本改字后保存重开的验证工具。
- 模型仍需判断内容、坐标、字体、颜色和裁图范围；不能保证像素级还原或全部元素可编辑。
- 本轮价格阶梯单页对比中，Astra low 加 Skill 用时 3.12 分钟，裸跑 3.40 分钟；含缓存总 Token 分别为 416,099 与 327,138。单次结果不代表稳定提速或 Token 节省，也不代表费用对比。

详细接口见 [工具说明](skills/astralow-for-editable-ppt/references/tools.md)，检查方法见 [质量检查](skills/astralow-for-editable-ppt/references/quality.md)。

## License

MIT，见 [LICENSE](LICENSE)。
