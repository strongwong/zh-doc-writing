# zh-doc-writing

中文技术文档写作与去 AI 味规范。给 Qoder、Claude Code 等 agent（智能体）用，写、改、审中文文档时按这套规则来。

规范整合自三份文档：阮一峰《中文技术文档的写作规范》、sparanoid《中文文案排版指北》、安居客《中文文档格式规范》。冲突处已选定一种写法，细节见[SKILL.md](SKILL.md)。

## 能做什么

- 写新文档。句子、语气、段落结构、排版的完整规则。
- 改已有文档。按“原句 → 改后 → 原因”给意见，或直接修改。
- 去 AI 味。`ai_scan.py` 扫描常见 AI 腔词语，配合[references/de-ai.md](references/de-ai.md)逐类自查。
- 查排版细则。数字、标点、引号、英文处理，见[references/typography.md](references/typography.md)。
- 定手册结构。成套文档的目录和文件名规范，见[references/structure.md](references/structure.md)。

## 安装

把仓库克隆到对应软件的 skills 目录即可。

Qoder：

```bash
mkdir -p ~/.qoder/skills
git clone https://github.com/strongwong/zh-doc-writing.git ~/.qoder/skills/zh-doc-writing
```

重启会话或运行 `/skills reload` 后生效。

Claude Code：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/strongwong/zh-doc-writing.git ~/.claude/skills/zh-doc-writing
```

其他支持 Skill 的 agent（Codex、OpenCode 等）结构相同，把目录放到各自软件的 skills 目录即可，路径见对应软件的文档。

## 使用

写、改中文技术文档时告诉 agent：“按 zh-doc-writing 规范写（或润色）”。Qoder 里也可以直接调 `/zh-doc-writing`。

适用场景：README、设计文档、接口说明、教程、评审报告、变更说明、Wiki、周报，以及“去掉 AI 味”“检查中英文空格和标点”这类要求。

## 依赖

- `scripts/ai_scan.py` 需要 Python 3。
- `autocorrect` 可选。没装也可以，按 SKILL.md 的“排版”一节手动检查。
