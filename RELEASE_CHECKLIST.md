# Release Checklist

## 发布前必须检查

- [ ] `skills/ppt-to-editable/SKILL.md` 的 frontmatter 为 `name: ppt-to-editable`。
- [ ] README 定位为 `v3.0 preview`，没有承诺 stable release。
- [ ] `UPGRADE.md` 已说明旧版用户如何更新、验证、处理 OCR Runtime Setup。
- [ ] README 和 `SKILL.md` 已说明转换前预检流程：`--probe`、Conversion Mode Gate、OCR Runtime Gate、Scope + Worker Gate、`gates.json`。
- [ ] Conversion Mode Gate 的用户提问使用普通语言说明“单页省 token 模式”和“全量省力模式”，并保留单张 PNG / 单页 sample 的低 token 入口。
- [ ] Scope + Worker Gate 的用户提问使用普通语言，不要求用户理解 `app-native`、`worker_mode` 或 `Codex worker runtime`。
- [ ] `deck_controller.py` 没有默认全页转换；初始化必须显式传 `--gates-file`，并传 `--all-slides` 或 `--slides`。
- [ ] `single-page-token-saving` 模式下，controller 会拒绝 `--all-slides` 和多页 `--slides`。
- [ ] `prepare_worker_dispatch.py` 已阻止未授权外部 Codex worker，并说明页数越多 token 越多。
- [ ] OCR 未达到 `passed-text-usable` 时，controller 默认拒绝创建质量转换任务。
- [ ] `setup_ocr_runtime.py --yes` 必须有 `--gates-file`，且 gates 文件记录用户已确认 OCR setup。
- [ ] 不包含私有 PPT、历史测试 deck、客户素材或过程 run 输出。
- [ ] 扫描本地绝对路径、线程 id、过程轮次名和私有项目名；公开包不应包含开发机路径、内部项目名或历史测试线程编号。
- [ ] `python -m unittest discover skills/ppt-to-editable/tests` 通过。
- [ ] `python -m py_compile` 或 AST 检查通过。
- [ ] `deck_controller.py --probe`、缺失 `--gates-file`、`--all-slides` / `--slides` scope gate 已通过测试。
- [ ] OCR setup/check 文档可读，首次 setup 的耗时和下载原因已经解释清楚。
- [ ] `requirements.txt` 包含运行脚本所需依赖。
- [ ] `examples/README.md` 明确说明本包不附带私有示例素材。
- [ ] LICENSE 已确认。

## 发布后建议

- [ ] 用一个全新目录 clone 后重新跑测试。
- [ ] 用一份可公开的 synthetic image-only PPTX 做 smoke test。
- [ ] 再决定是否替换本机正式 `ppt-to-editable` skill。
