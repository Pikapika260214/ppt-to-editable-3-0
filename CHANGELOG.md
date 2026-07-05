# Changelog

## v3.0 Preview

- 新增 image-only `.pptx` 多页 deck controller。
- 集成成熟单页 reconstruction / mixed reconstruction 脚本链路。
- 支持 per-slide Agent 工作流，每页独立转换后合并 final deck。
- 新增 OCR runtime setup/check 流程。
- 新增 `UPGRADE.md`，给已安装旧版 skill 的用户说明如何更新和验证。
- 新增转换前确认状态机：`deck_controller.py --probe` 先只读检查 deck/OCR 状态，输出 `gates_file_template`。
- 新增 Conversion Mode Gate：用户先选择“单页省 token 模式”或“全量省力模式”，避免默认跑完整 deck 造成不必要 token 消耗。
- `deck_controller.py` 新增 `--gates-file` 和 `--slides`，支持记录用户 conversion mode、OCR、范围、worker、token 确认，只为指定页生成任务并合成指定页 deck。
- `gates.json` 升级为 `ppt-to-editable-gates-v3`：新增 `conversion_mode_gate`；OCR 已可用时自动记录通过；页码范围、worker 授权、token 成本确认、内容共享确认合并为 `scope_and_worker_gate`。
- 新增 `prepare_worker_dispatch.py`：初始化后先生成 worker 派发报告，未明确授权时阻止外部 Codex worker。
- 优化 Scope + Worker Gate 用户提问：用户看到的是“转几页、页数越多 token 越多、每页会由独立转换任务读取页面内容”，不再要求用户理解 `app-native worker` 或 `Codex worker runtime`。
- `deck_controller.py` 新增硬约束：初始化时必须显式传 `--gates-file`，并传 `--all-slides` 或 `--slides`；OCR 未达到 `passed-text-usable` 时默认拒绝创建质量转换任务。
- `setup_ocr_runtime.py --yes` 新增硬约束：必须传入已记录用户确认的 `--gates-file`，避免未授权安装依赖或下载 OCR 模型。
- 新增 deck-level QA、失败页 fallback sticker、PowerPoint render QA。
- 强化复杂视觉策略：复杂图标、路径、阴影、照片、渐变模块优先 crop/textless crop，不强行 native 重建。
- 强化非文字结构保护：textless crop 不应抹掉箭头、路线、步骤编号、卡片边缘、图标等结构元素。
