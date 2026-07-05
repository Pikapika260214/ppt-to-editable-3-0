# Upgrade Guide

这份文档给已经安装过旧版 `ppt-to-editable` 的用户使用。

v3.0 preview 仍然使用公开 skill 名称 `ppt-to-editable`，但能力从“单张 PNG / 单页截图转 editable”扩展为两种入口：

- 单页省 token 模式：继续支持单张 PNG、截图、或 PPTX 的一页 sample。
- 全量省力模式：支持多页 image-only `.pptx` 转 editable deck。

## 升级前你需要知道

- 仓库名可以是 `ppt-to-editable-3-0`，但实际安装后的 skill 文件夹仍应叫 `ppt-to-editable`。
- 旧版主要面向单页 PNG；v3.0 preview 增加了 deck controller、OCR Runtime Gate、Conversion Mode Gate 和多页 worker 派发流程。
- 第一次 OCR setup 可能更慢，因为它可能需要安装依赖或下载 OCR 模型。
- 如果某一页转换失败，最终 deck 仍会生成；失败页会保留原 PNG，并在右上角加黄色贴纸“可编辑转换失败”。

## 推荐升级方式

如果你是通过 GitHub 安装的 skill，推荐重新从最新仓库安装：

```text
请从这个 GitHub 仓库安装 / 更新 ppt-to-editable skill。
仓库地址是：[把当前 GitHub 仓库 URL 粘贴在这里]
```

安装完成后，让 Codex 检查本地 skill 是否已更新到 v3.0 preview。

## 手动升级方式

如果你是手动安装的：

1. 找到旧版 skill 文件夹。

```text
Windows: %USERPROFILE%\.codex\skills\ppt-to-editable
macOS/Linux: ~/.codex/skills/ppt-to-editable
```

2. 备份旧版文件夹。

例如可以改名为：

```text
ppt-to-editable.backup
```

3. 把本仓库里的新 skill 文件夹复制过去：

```text
skills/ppt-to-editable
```

4. 确认最终路径仍然是：

```text
<Codex skills directory>/ppt-to-editable/SKILL.md
```

不要把安装后的 skill 文件夹命名为 `ppt-to-editable-3-0`，否则 Codex 可能不会按旧名称触发它。

## 验证升级是否成功

在仓库根目录运行：

```powershell
python -m unittest discover skills/ppt-to-editable/tests
```

也可以打开安装后的 `SKILL.md`，确认头部仍然是：

```yaml
name: ppt-to-editable
```

并且标题包含：

```text
PPT to Editable v3.0 Preview
```

## 升级后怎么使用

### 继续转单张 PNG

旧用户可以继续使用单页方式：

```text
请使用 ppt-to-editable，把这张 PNG 转成更可编辑的 PowerPoint。
我想使用单页省 token 模式。
```

这类任务不需要启动整份 deck controller，也不需要为每一页启动独立 worker。

### 转整份 image-only PPTX

如果要转完整 deck：

```text
请使用 ppt-to-editable，把这份 image-only PPTX 转成更可编辑的 PowerPoint deck。
我想使用全量省力模式。
```

v3.0 preview 会先问你：

- 选择单页省 token 模式，还是全量省力模式；
- OCR 是否已经可用，是否需要首次 setup；
- 转换全部页、指定页，还是先试一页；
- 是否接受页数越多 token 越多，以及每页由独立转换任务读取页面内容。

## OCR Runtime Setup

OCR 的作用不是只“识别文字”。它还会帮助确认：

- 原图里有哪些文字；
- 文字在图片里的位置；
- 哪些文字需要从 crop 里抹掉；
- editable text box 应该放在哪里；
- 中文识别结果是否可用。

如果 OCR 已经是 `passed-text-usable`，v3.0 preview 会记录自动通过，不会重复要求你确认安装。

如果 OCR 不可用，skill 会先解释为什么需要 setup，以及第一次 setup 可能更久。只有你确认后，才运行：

```powershell
python skills/ppt-to-editable/scripts/setup_ocr_runtime.py --runtime-dir .venv-ocr-3-0 --gates-file gates.json --yes
```

setup 完成后，用下面命令检查中文 OCR 是否可用：

```powershell
python skills/ppt-to-editable/scripts/check_ocr_runtime.py --json --output-dir .ocr-check
```

质量转换应以：

```text
ocr_runtime_status: "passed-text-usable"
```

为目标。

## 重要行为变化

### 1. 不会默认把整份 PPTX 全部转换

用户说“转换这个 PPTX”不等于自动同意转换全部页面。v3.0 preview 会先问你转全部页、指定页，还是先试一页。

### 2. 单页省 token 模式有硬约束

如果你选择单页省 token 模式，controller 会拒绝：

- `--all-slides`
- 多页 `--slides`

这样可以避免 Agent 擅自把一次低成本测试变成完整 deck 转换。

### 3. 多页转换会更耗 token

全量模式会把每页作为独立任务处理。页数越多，token 消耗越高，但上下文污染更少，质量也更容易逐页检查。

### 4. 失败页不会让整份 deck 中断

如果某页两轮仍失败，最终 deck 仍会生成。失败页会使用原图 fallback，并加上“可编辑转换失败”的黄色提示。

## 常见问题

### 我已经安装过旧版，还需要改 prompt 吗？

建议加一句模式选择。比如：

```text
我想使用单页省 token 模式。
```

或：

```text
我想使用全量省力模式。
```

这样可以减少误触发完整 deck 转换。

### 为什么还叫 `ppt-to-editable`，不是 `ppt-to-editable-3-0`？

为了让已安装旧版的用户可以继续用同一个 skill 名称。仓库可以叫 `ppt-to-editable-3-0`，但 skill 的 public name 保持 `ppt-to-editable`。

### 我可以回滚吗？

可以。如果你手动升级前备份了旧文件夹，把当前 `ppt-to-editable` 文件夹移走，再把备份文件夹改回 `ppt-to-editable` 即可。

### 旧版生成的输出还能用吗？

旧输出不会被自动迁移。v3.0 preview 建议从原始 PNG 或 image-only PPTX 重新开始转换，不要复用旧 run 里的中间产物作为新结果依据。
