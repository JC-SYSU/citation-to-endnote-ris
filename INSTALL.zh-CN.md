[English](INSTALL.md) | 中文版

# 安装指南（给执行安装的 agent 看）

装这个技能就是把一个文件夹复制到 agent 会读取的目录里。安装时没有任何要构建或运行的东西：这个文件夹是纯文本，外加一个 Python 标准库脚本——agent 只在校验输出文件时才会调用它。

本文档是操作规范：按顺序执行步骤，检查每一步的**预期输出**，最后跑第 3 节验收清单。也可以手动照做；但设计上的主要路径是：把 README.zh-CN.md 里的安装块粘给 agent，让它来干。

## "装好了"是什么样

- `<skills-dir>/citation-to-endnote-ris/SKILL.md` 存在（文件夹名必须与 frontmatter 里的 `name` 完全一致——区分大小写）。
- agent 能说出这个技能的名字，并显示它的一行描述。
- `scripts/validate_ris.py` 可执行（或至少能经 Python 调用）。

## 0. 前置条件

| # | 检查 | 命令 | 预期 | 失败处理 |
| ---- | ---- | ---- | ---- | ---- |
| 0.1 | git（或任何能取得仓库的方式） | `git --version` | 有版本号 | 改为从 GitHub 页面下载 release 的 ZIP |
| 0.2 | 三个客户端至少装了一个 | `command -v claude; command -v codex; command -v opencode` | 至少命中一个 | 先装其中一个客户端 |
| 0.3 | Python 3（可选） | `python3 --version` | 3.x | Windows 上改用 `python` 或 `py -3`；没有 Python 就跳过校验步骤 |

## 0.5 各客户端从哪里读个人技能

| 客户端 | 个人（所有项目） | 项目（仓库内） | 依据 |
| ---- | ---- | ---- | ---- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Claude Code 官方文档 |
| Codex | `~/.agents/skills/` | `.agents/skills/` | Codex 官方文档 |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | OpenCode 官方文档 |
| OpenCode（兼容路径） | 也读 `~/.claude/skills/` 和 `~/.agents/skills/` | 项目级同样兼容 | OpenCode skills 官方文档 |

Windows 上表中所有 `~` 都是 `%USERPROFILE%`。如果把文件夹放进 Claude Code 或 Codex 的目录（而不是 OpenCode 专用目录），OpenCode 一次也不用再装。

## 1. 安装

**POSIX（macOS / Linux）：**

```bash
mkdir -p ~/.claude/skills ~/.agents/skills
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris ~/.claude/skills/citation-to-endnote-ris
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris ~/.agents/skills/citation-to-endnote-ris
```

**Windows（PowerShell）：**

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.claude\skills, $env:USERPROFILE\.agents\skills
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris $env:USERPROFILE\.claude\skills\citation-to-endnote-ris
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris $env:USERPROFILE\.agents\skills\citation-to-endnote-ris
```

直接克隆进目标目录会在每份副本里保留 `.git`，之后更新就是进技能文件夹跑一次 `git pull`。

预期：两个技能目录里各有一份文件夹。
失败：没有 git → 从 GitHub 页面下载 release 的 ZIP，解压到同样的目标目录；目标目录已存在同名文件夹 → 先备份（克隆和解压都不会合并）。

为什么要装两个目录：Claude Code 只读 `~/.claude/skills/`；Codex 和 OpenCode 读 `~/.agents/skills/`。只装一份、装进它所属客户端的目录就够用——两份都装则覆盖全部三个客户端。

## 2. 验证

```bash
ls ~/.claude/skills/citation-to-endnote-ris/SKILL.md ~/.agents/skills/citation-to-endnote-ris/SKILL.md
python3 ~/.claude/skills/citation-to-endnote-ris/scripts/validate_ris.py ~/.claude/skills/citation-to-endnote-ris/examples/output.ris
```

预期：两条 `ls` 都列出 `SKILL.md`；校验器输出 `RESULT: VALID`。
失败：文件夹名与 frontmatter 的 `name` 不一致 → agent 不会加载该技能；把文件夹改名。

在客户端里确认：Claude Code 里输入 `/`，菜单里应出现该名字。Codex 和 OpenCode 里让 agent 列出它的技能。

## 3. 验收清单

| # | 验证 | 通过标准 |
| ---- | ---- | ---- |
| 1 | 文件夹就位 | 第 1 节两个个人路径下都有 `SKILL.md` |
| 2 | 校验脚本 | 示例输出通过（`RESULT: VALID`） |
| 3 | agent 看得到技能 | 客户端能列出 `citation-to-endnote-ris` 及其描述 |
| 4 | 冒烟测试 | 给 agent 一条两行的假引文，要求产出一个 `.ris` 文件；最终得到合法文件与类型分布报告 |

## 4. 可选：PubMed Surfing 校验

环境的 MCP 里装有 PubMed Surfing 服务（`JC-SYSU/pubmed-surfing`）时，技能可以用它对 PubMed 索引的文献做核对。服务缺失时，技能会在征得你同意后，按该仓库的 `INSTALL.md` 自动安装；这一步完全可选，转换流程不会被它卡住。两种情况都不涉及 API key。中文文献在环境里装有万方检索 MCP（`wanfang_search` / `wanfang_get`）时同样核对；它是否可用取决于你的 MCP 配置，缺失时技能直接跳过。

## 5. 卸载

删除两个文件夹：

```bash
rm -rf ~/.claude/skills/citation-to-endnote-ris ~/.agents/skills/citation-to-endnote-ris
```

不触碰任何配置文件，机器上的其他任何东西都不会被改动。

## 6. 故障排查

| 症状 | 原因与修复 |
| ---- | ---- |
| agent 从不使用该技能 | 文件夹名必须等于 frontmatter 的 `name`（`citation-to-endnote-ris`）；更常见的原因是目录放错——查第 0.5 节表格 |
| 一个客户端能加载、另一个不能 | 装进了那个客户端不读的目录；用第 1 节中的对应路径 |
| Windows 上找不到 `python3` | 改用 `python scripts/validate_ris.py ...` 或 `py -3 scripts/...` |
| 技能正常但输出文件没生成 | 技能需要文件系统写权限；授予权限，或明确给出输出路径 |