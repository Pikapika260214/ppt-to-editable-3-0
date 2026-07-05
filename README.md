# ppt-to-editable-3-0

`ppt-to-editable-3-0` 是 `ppt-to-editable` 的 v3.0 preview。它用于把图片型 PPT、单页 PNG、截图或栅格化幻灯片转换成更可编辑的 PowerPoint。

这个版本保留单页低成本转换，也新增多页 PPTX 转 editable deck 的工作流：

- 单页省 token 模式：适合单张 PNG、截图，或只想先测一页效果。
- 全量省力模式：适合整份 image-only `.pptx`，会按页拆开处理，再合成最终 PPTX。

如果你已经安装过旧版 `ppt-to-editable`，请先看 [UPGRADE.md](UPGRADE.md)。

## 当前状态

这是 `v3.0 preview`，不是 stable release。

适合：

- image-only `.pptx`，也就是每页主要是一整张图片；
- 单页 PNG / 截图转可编辑 PPT；
- 咨询风格、商业分析风格、结构化页面；
- 希望尽量保留原图观感，同时让主要文字可编辑的场景。

不适合：

- 需要 100% 全原生 shape / vector 的场景；
- 输入 PPT 已经有大量可编辑原生对象，但没有先做结构检查的场景；
- 需要零 token、零人工检查的一键稳定批处理场景。

## 安装

推荐安装到 Codex 的 skills 目录，并保持 skill 名称为 `ppt-to-editable`。仓库名可以叫 `ppt-to-editable-3-0`，但实际被 Codex 调用的 skill 文件夹应是：

```text
skills/ppt-to-editable
```

如果使用 Codex 的 skill installer，可以在 Codex 里说：

```text
请从这个 GitHub 仓库安装 / 更新 ppt-to-editable skill。
仓库地址是：[把当前 GitHub 仓库 URL 粘贴在这里]
```

如果手动安装，把本仓库里的：

```text
skills/ppt-to-editable
```

复制到你的 Codex skills 目录：

```text
Windows: %USERPROFILE%\.codex\skills\ppt-to-editable
macOS/Linux: ~/.codex/skills/ppt-to-editable
```

安装后可以检查 `SKILL.md` 头部仍然是：

```yaml
name: ppt-to-editable
```

## 依赖

建议使用 Python 3.10+。

```powershell
python -m pip install -r requirements.txt
```

OCR Runtime 不建议直接静默安装。第一次需要 OCR 时，skill 会先解释 OCR 的作用和可能耗时，再让用户确认是否 setup。

如果只是想看 OCR setup 会做什么，不下载依赖：

```powershell
python skills/ppt-to-editable/scripts/setup_ocr_runtime.py --runtime-dir .venv-ocr-3-0
```

确认后再运行：

```powershell
python skills/ppt-to-editable/scripts/setup_ocr_runtime.py --runtime-dir .venv-ocr-3-0 --gates-file gates.json --yes
```

检查 OCR 是否能识别中文：

```powershell
python skills/ppt-to-editable/scripts/check_ocr_runtime.py --json --output-dir .ocr-check
```

## 快速使用

### 单页省 token 模式

适合单张 PNG、截图，或只想从 PPTX 中先测试一页。

可以这样对 Codex 说：

```text
请使用 ppt-to-editable，把这张 PNG 转成更可编辑的 PowerPoint。
我想使用单页省 token 模式。
```

如果输入是 PPTX，也可以说：

```text
请使用 ppt-to-editable，把这份 image-only PPTX 的第 2 页先转成更可编辑的 PowerPoint。
我想先用单页省 token 模式测试效果。
```

### 全量省力模式

适合整份 image-only PPTX。

可以这样对 Codex 说：

```text
请使用 ppt-to-editable，把这份 image-only PPTX 转成更可编辑的 PowerPoint deck。
我想使用全量省力模式。
```

全量模式会按页拆开处理。页数越多，token 消耗越高。为了提高质量，每页会由独立转换任务读取对应页面图片和文字内容。

## 转换前确认

v3.0 preview 使用强制预检流程，避免 Agent 在用户没有确认前直接跑完整 deck：

1. Probe：只读取 PPTX 和 OCR 状态，输出 slide count、OCR 状态和 `gates_file_template`；不创建 run、不抽图、不下载依赖。
2. Conversion Mode Gate：先让用户选择“单页省 token 模式”或“全量省力模式”。
3. OCR Runtime Gate：如果 OCR 已经可用，只记录自动通过；如果不可用，先解释 OCR 的作用和可能耗时，只有用户确认后才安装依赖或下载模型。
4. Scope + Worker Gate：多页 `.pptx` 转换前，用普通语言确认转换全部页、指定页，还是先试一页；同时说明页数越多 token 越多，每页会交给独立转换任务处理，并会读取对应页面的图片和文字内容。

只读 probe 示例：

```powershell
python skills/ppt-to-editable/scripts/deck_controller.py input.pptx --probe --ocr-python .venv-ocr-3-0/Scripts/python.exe
```

初始化全部页转换：

```powershell
python skills/ppt-to-editable/scripts/deck_controller.py input.pptx --run-dir runs/my-deck --gates-file gates.json --all-slides --ocr-python .venv-ocr-3-0/Scripts/python.exe
```

初始化指定页转换：

```powershell
python skills/ppt-to-editable/scripts/deck_controller.py input.pptx --run-dir runs/my-deck --gates-file gates.json --slides "1,3,5" --ocr-python .venv-ocr-3-0/Scripts/python.exe
```

初始化后先生成 worker 派发报告，不要直接启动外部 worker：

```powershell
python skills/ppt-to-editable/scripts/prepare_worker_dispatch.py runs/my-deck --worker-mode app-native
```

## 输出策略

v3.0 preview 优先保证“可用编辑性 + 视觉保真”，不会强行把所有复杂视觉都重画成原生形状。

通常策略：

- 文字：尽量转成 PowerPoint 可编辑文本框；
- 简单形状：可重建为原生矩形、圆角矩形、线条、表格等；
- 复杂图标、照片、阴影、曲线路径、渐变箭头：优先用紧裁剪 crop 或 textless crop；
- 失败页：保留原 PNG，并在右上角加黄色贴纸“可编辑转换失败”。

## 多页工作流

全量模式会按页处理：

1. `deck_controller.py --probe` 检查输入和 OCR 状态。
2. 记录用户选择的转换模式、OCR 状态、页面范围和 worker/token/content 确认。
3. 初始化 deck run，生成 `deck_manifest.json`。
4. 为每页生成 `slide_job_manifest.json` 和 `AGENT_TASK.md`。
5. 每页由独立 per-slide Agent 处理。
6. controller 汇总每页结果，生成 `final-deck.pptx`。

输出位置通常是：

```text
runs/my-deck/output/final-deck.pptx
runs/my-deck/output/deck-level-qa-report.json
```

## 示例素材

本仓库不包含真实业务 deck、历史测试 deck 或私有素材。请使用自己的 image-only `.pptx` 或单页 PNG 测试。

更多说明见 [examples/README.md](examples/README.md)。

## 测试

```powershell
python -m unittest discover skills/ppt-to-editable/tests
```

如果本机没有 PowerPoint，render QA 相关测试或实际渲染可能受限。Windows + PowerPoint COM 是当前最完整的验证路径。

## License

MIT. See [LICENSE](LICENSE).
