# Release Readiness Report

## 结论

本地 release-candidate 已准备完成，可以作为后续初始化 Git repo / commit / push 的基础。最新版本已补上转换前 gate 状态机：`--probe`、`gates.json`、Conversion Mode Gate、OCR setup 确认、scope 确认。

位置：

```text
ppt-to-editable-3-0-release-candidate/
```

## 已按用户决策处理

- Repo 名称方向：`ppt-to-editable-3-0`
- 发布定位：`v3.0 preview`
- License：MIT
- 示例素材：不公开历史测试 deck 或任何真实业务素材
- README 语言：中文
- 多 Agent 说明：保留
- 正式替换方向：skill public name 使用 `ppt-to-editable`
- 当前动作边界：只准备本地文件夹，尚未初始化 git / commit / push
- 用户入口：保留“单页省 token 模式”，新增“全量省力模式”

## 文件结构

```text
ppt-to-editable-3-0-release-candidate/
  README.md
  LICENSE
  CHANGELOG.md
  RELEASE_CHECKLIST.md
  RELEASE_READINESS_REPORT.md
  requirements.txt
  .gitignore
  examples/
    README.md
  skills/
    ppt-to-editable/
      SKILL.md
      agents/openai.yaml
      references/
      scripts/
      tests/
```

## 已完成的清理

- `SKILL.md` frontmatter 已改为 `name: ppt-to-editable`。
- release-candidate 内部 engine id 已统一为 `ppt-to-editable-v3-preview`。
- 移除了内部开发语义中的用户可见表达。
- 未复制任何 Round 20/21/22/23/24 run 输出。
- 未复制历史测试 deck。
- 未复制私有素材。
- 已清理 `__pycache__`。
- OCR setup/check 里的中文提示已修复为正常 UTF-8。
- `deck_controller.py --probe` 已接入 CLI，初始化前强制校验 `gates.json`。
- `gates.json` 已升级为 `ppt-to-editable-gates-v3`，包含 `conversion_mode_gate`。
- `single-page-token-saving` 模式会拒绝 `--all-slides` 和多页 `--slides`。
- `setup_ocr_runtime.py --yes` 已强制要求 `--gates-file`，防止未确认就安装依赖或下载模型。

## 验证结果

已运行：

```text
敏感路径扫描：无命中
乱码扫描：count 0
AST 检查：ast-ok 29 files
Unit tests：Ran 27 tests OK
Compile check：compileall scripts/tests passed
Skill validator：Skill is valid!
OCR setup no-download check：status=requires-user-confirmation
Gate negative smoke：missing gates blocked before run initialization
```

## 仍需用户发布前确认

- MIT copyright holder 已确认使用 `Rachel Wang`。
- 是否需要补一个完全合成、可公开的 demo PPTX。当前 release candidate 不附带示例素材。
- 是否需要我下一步初始化 git repo、创建 initial commit，并准备 GitHub push。
- 是否在 push 前先做一次 fresh clone 风格的独立目录 smoke test。

## 不建议现在做的事

- 不建议直接上传整个内部升级项目文件夹。
- 不建议上传任何历史 run 输出、Activity Log、Tracker 或历史测试 deck。
- 不建议在没有 fresh smoke test 的情况下宣布 stable release。
