# 从 ppt-to-editable 升级

新版 Skill 名称和目录为 `astralow-for-editable-ppt`。仓库 URL 保持不变。

1. 将旧 `ppt-to-editable` 文件夹备份到 skills 搜索目录之外，避免两个转换 Skill 同时被发现。
2. 按 README 安装 `skills/astralow-for-editable-ppt`，安装其 requirements.txt 中的依赖。
3. 将提示词中的 `$ppt-to-editable` 改为 `$astralow-for-editable-ppt`，选择 Astra low 后先转换一页。

这是新的轻量重建流程，不兼容旧版 `deck_controller.py`、gates.json 或 OCR setup 命令。已有 PPT、源图和输出不用删除；旧 OCR 环境不必卸载。新版在需要时可使用已有 OCR，但不默认要求部署旧 OCR 流程。

单页工具不提供旧版多页 controller。多页需逐页处理，再单独合并和检查。

需要旧版时，可从 [旧版提交](https://github.com/Pikapika260214/ppt-to-editable-3-0/tree/6acf48e) 获取原文件。
