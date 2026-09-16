[中文版](INSTALL.zh-CN.md) | English

# Installation Guide (for the agent performing the install)

Installing this skill means copying one folder into a directory the agent
reads. There is nothing to build and nothing to run at install time: the
folder is plain text plus one Python standard-library script that the agent
invokes later, only when it validates an output file.

This document is an operating spec: run the steps in order, check each step's
**expected output**, and finish with the acceptance checklist in section 3.
It can be followed by hand, but the intended flow is to paste the install
block from README.md into the agent and let it do the work.

## What "installed" looks like

- `<skills-dir>/citation-to-endnote-ris/SKILL.md` exists (the folder name must
  match the frontmatter `name` exactly — filesystem case matters).
- The agent can name the skill and shows its one-line description.
- `scripts/validate_ris.py` is executable (or at least runnable via Python).

## 0. Prerequisites

| # | Check | Command | Expected | Failure handling |
| ---- | ---- | ---- | ---- | ---- |
| 0.1 | git (or any way to get the repo) | `git --version` | a git version | download the release ZIP from the GitHub page instead |
| 0.2 | at least one of the three clients | `command -v claude; command -v codex; command -v opencode` | at least one present | install one of the clients first |
| 0.3 | Python 3, optional | `python3 --version` | 3.x | on Windows use `python` or `py -3`; validation is skipped when no Python exists |

## 0.5 Where each client reads personal skills

| Client | Personal (all projects) | Project (repo-scoped) | Documented |
| ---- | ---- | ---- | ---- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | Claude Code docs |
| Codex | `~/.agents/skills/` | `.agents/skills/` | Codex docs |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | OpenCode docs |
| OpenCode, compatibility paths | also reads `~/.claude/skills/` and `~/.agents/skills/` | same at project level | OpenCode skills docs |

On Windows, every `~` above is `%USERPROFILE%`. One install is enough for
OpenCode if you put the folder in a Claude Code or Codex directory instead of
the OpenCode-only one.

## 1. Install

**POSIX (macOS / Linux):**

```bash
mkdir -p ~/.claude/skills ~/.agents/skills
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris ~/.claude/skills/citation-to-endnote-ris
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris ~/.agents/skills/citation-to-endnote-ris
```

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.claude\skills, $env:USERPROFILE\.agents\skills
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris $env:USERPROFILE\.claude\skills\citation-to-endnote-ris
git clone --depth 1 https://github.com/JC-SYSU/citation-to-endnote-ris $env:USERPROFILE\.agents\skills\citation-to-endnote-ris
```

Cloning straight into the target keeps a `.git` inside each copy, which makes
later updates a simple `git pull` inside the skill folder.

Expected: two copies of the folder exist, one per skills directory.
Failure: no git → download the release ZIP from the GitHub page and unzip it
into the same target directories; an existing folder with the same name →
back it up first (clones and unzips do NOT merge).

Why both directories: Claude Code reads only `~/.claude/skills/`; Codex and
OpenCode read `~/.agents/skills/`. A single copy in one directory is enough
for the client it belongs to — both copies cover all three.

## 2. Verify

```bash
ls ~/.claude/skills/citation-to-endnote-ris/SKILL.md ~/.agents/skills/citation-to-endnote-ris/SKILL.md
python3 ~/.claude/skills/citation-to-endnote-ris/scripts/validate_ris.py ~/.claude/skills/citation-to-endnote-ris/examples/output.ris
```

Expected: both `ls` lines list `SKILL.md`; the validator prints
`RESULT: VALID`. Failure: folder mismatch with frontmatter `name` → the agent
will not load the skill; rename the folder.

To see the skill inside a client: in Claude Code, type `/` and the name should
appear in the menu. In Codex and OpenCode, ask the agent to list its skills.

## 3. Acceptance checklist

| # | Verify | Pass criteria |
| ---- | ---- | ---- |
| 1 | folder present | `SKILL.md` exists at both personal paths from section 1 |
| 2 | validation script | example output validates (`RESULT: VALID`) |
| 3 | agent sees the skill | the client lists `citation-to-endnote-ris` with its description |
| 4 | smoke run | give the agent a two-line fake citation and ask for a `.ris` file; it ends with a valid file and a type breakdown |

## 4. Optional: PubMed Surfing verification

The skill can verify references against PubMed when the environment has the
PubMed Surfing MCP server installed (`JC-SYSU/pubmed-surfing`). When the
server is missing, the skill offers to install it from that repository's
`INSTALL.md` with the user's consent; the offer is optional, and conversion
never blocks on it. No API key is involved in either case.

## 5. Uninstall

Delete the two folders:

```bash
rm -rf ~/.claude/skills/citation-to-endnote-ris ~/.agents/skills/citation-to-endnote-ris
```

No configuration files are touched; nothing else on the machine changes.

## 6. Troubleshooting

| Symptom | Cause & fix |
| ---- | ---- |
| the agent never uses the skill | folder name must equal the frontmatter `name` (`citation-to-endnote-ris`); the wrong skills directory is often the cause — see the 0.5 table |
| skill loads on one client but not another | you placed it in a directory that client does not read; use the per-client paths in section 1 |
| `python3` not found on Windows | run the validator as `python scripts/validate_ris.py ...` or `py -3 scripts/...` |
| skill works but the output file is not created | the skill needs filesystem write access; grant it or supply an explicit output path |