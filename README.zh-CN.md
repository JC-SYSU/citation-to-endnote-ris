[English](README.md) | 中文版

# Citation to EndNote RIS（文献转 EndNote RIS）

写论文时，参考文献的来路五花八门。导师在聊天软件或 Word 批注里丢一句"记得引那篇最近的相关研究"——没有期刊、没有卷期，有时连标题都不完整。查资料时从网页、PDF 里顺手粘一段进笔记。不同来源、不同格式、不同语言，最后全堆在一起。要把它们弄进 EndNote，平时只能一条一条手动规范化。这个技能把这一堆杂七杂八的引文文本——聊天消息、批注、网页摘录，什么样的都有——一次性整理成一份经过校验、可直接批量导入 EndNote 的 RIS 文件，保留你的引用顺序，保留你的原文，不替你编造任何东西。

## 它做什么

把一段包含一条或多条引文的文本（粘贴，或放进文件里指明）交给它。它：

1. **切分**。识别出里面到底有几条文献，包括被换行截断或残缺的记录。
2. **抽取**。从给定的文本里读出各字段：作者、标题、期刊、卷/期/页、DOI、PMID、年份等。
3. **判型**。为每条文献选最贴切的 RIS 类型——期刊论文、会议摘要、会议论文、图书、章节、学位论文、报告、网页、数据集等。
4. **校验——仅当你具备条件时**。如果环境里已接上 PubMed Surfing MCP 服务（或你同意安装它），它会去 PubMed 核对差异，并给你一张对比表。未经你批准，PubMed 的结果不会落到你的文件里。
5. **落盘**。产出一个 UTF-8 编码的 `.ris`，每条文献一条记录，再用自带的语法校验器过一遍。

整条流程就这样：乱文本进，合格文件出。

## 它不会做什么

- 从不编造文献事实。不会凭记忆或猜测补作者、标题、年份、卷号、页码。没有来源支撑的字段留空或标记为存疑，绝不捏造。
- 不会静默"修正"你的文本、自动去重，或重排引用顺序——重复和不确定之处会报告给你，改动只在你明确要求后进行。
- 不会自行查 Crossref、DOI 解析器或上网。离线是默认；PubMed Surfing 是唯一自愿的例外，且安装要经过你同意，校验结果要经过你确认才可应用。

## 这是什么类型的东西

一个 _skill_（技能），不是程序：一个文件夹，内含 `SKILL.md` 和几个小支持文件，遵循 [Agent Skills](https://agentskills.io) 开放标准。

- 它运行在 agent 里：Claude Code、Codex 或 OpenCode，有哪个用哪个。
- 唯一的可执行文件是一个只用 Python 标准库的校验脚本——不需要 `pip install`，任何系统上都没有构建步骤。
- 客户端/系统组合遵循各客户端文档规定的技能目录（macOS、Linux、Windows 的路径表见 INSTALL.zh-CN.md 第 0.5 节）。我们在 macOS 上开发与测试；INSTALL 里的 Windows 说明以各客户端官方文档为准。
- OpenCode 还会额外读取 Claude Code 和 Codex 的技能目录（OpenCode 官方文档确认），所以一次安装有时能覆盖不止一个客户端。

## 怎么用

**安装** —— 把这个块粘贴给你的 agent（Claude Code、Codex 或 OpenCode），agent 会读 INSTALL.zh-CN.md 自己干活：

```
请安装 citation-to-endnote-ris 技能。仓库地址是
https://github.com/JC-SYSU/citation-to-endnote-ris。

1. 完整阅读 INSTALL.zh-CN.md（读不到就改为直接读
   https://raw.githubusercontent.com/JC-SYSU/citation-to-endnote-ris/main/INSTALL.md）
   并按步骤执行。
2. 探测本机环境，选好技能目录，把技能文件夹复制进去（第 0.5 节和第 1 节）。
3. 跑第 3 节验收清单，把每一项结果报给我。有失败的先修好再汇报。
```

或者手动装：直接按 INSTALL.zh-CN.md 操作。安装时不需要运行任何东西，只是复制文件夹。

**日常使用** —— 把文献列表粘贴给 agent，让它输出一个 EndNote 可导入的 RIS 文件，或指向一个文本文件：

> 把这些引文转成一个我能导入 EndNote 的 RIS 文件。

agent 会写文件、跑校验，并报告类型分布。

## 快速验证

```bash
python3 scripts/validate_ris.py examples/output.ris
```

预期输出：`RESULT: VALID`，3 条记录（JOUR、CPAPER、ELEC）。

## License

MIT。映射规则细节见 `references/ris-mapping.md`，字段语义见 `SKILL.md`。