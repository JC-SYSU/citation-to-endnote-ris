# citation-to-endnote-ris

Cross-platform Agent Skill for converting messy citation/reference text into one validated, batch-importable EndNote RIS file.

## Package contents

- `SKILL.md` — main skill instructions
- `references/ris-mapping.md` — type and field mapping rules
- `scripts/validate_ris.py` — lightweight RIS syntax/duplicate validator
- `examples/` — sample messy input and validated RIS output

## Install in Claude Code

Personal skill:

```bash
mkdir -p ~/.claude/skills
cp -R citation-to-endnote-ris ~/.claude/skills/
```

Project skill:

```bash
mkdir -p .claude/skills
cp -R citation-to-endnote-ris .claude/skills/
```

Invoke with:

```text
/citation-to-endnote-ris
```

or ask Claude naturally to convert a messy reference list into a batch EndNote RIS file.

## Install in Codex

Personal skill:

```bash
mkdir -p ~/.agents/skills
cp -R citation-to-endnote-ris ~/.agents/skills/
```

Project skill:

```bash
mkdir -p .agents/skills
cp -R citation-to-endnote-ris .agents/skills/
```

Invoke through the skills picker or mention the skill explicitly, for example:

```text
$citation-to-endnote-ris Convert these messy citations into one EndNote RIS file.
```

## Install in OpenCode

OpenCode reads skills from `~/.config/opencode/skills/`, and it also natively
reads the Claude Code and Codex locations from the two sections above — so in
most setups **installing once into `~/.claude/skills/` or `~/.agents/skills/`
already makes the skill available in OpenCode**. If you want the OpenCode-only
directory as well:

```bash
mkdir -p ~/.config/opencode/skills
cp -R citation-to-endnote-ris ~/.config/opencode/skills/
```

## Windows

All `~` paths above map to `%USERPROFILE%` on Windows:

| Client | Personal skills directory |
|---|---|
| Claude Code | `%USERPROFILE%\.claude\skills\` |
| Codex / OpenCode-compatible | `%USERPROFILE%\.agents\skills\` |
| OpenCode-only | `%USERPROFILE%\.config\opencode\skills\` |

No installation scripts are run at install time; skills are plain files, so a
`copy` command works on every platform.

## Client and platform compatibility

- Skill format: one `SKILL.md` per folder with YAML frontmatter (`name` plus
  `description`), following the [Agent Skills](https://agentskills.io) open
  standard. The folder name must match `name`; `citation-to-endnote-ris`
  complies with the naming rules of all three clients.
- The only executable is `scripts/validate_ris.py` — Python 3, standard library
  only, no `pip install`. On Windows run it as `python`/`py -3` instead of
  `python3`.
- The PubMed Surfing verification optional extra works on macOS and Windows via
  prebuilt release archives, and on Linux by building from source (Go >= 1.25);
  installation is driven by the surfacing repository's `INSTALL.md`, and its
  absence never blocks conversion.

## Default behavior

The skill is offline-first: it extracts only what the user supplied and does not query Crossref, PubMed, DOI resolvers, or the web unless the user explicitly asks for verification/enrichment. When the PubMed Surfing MCP server is missing, the skill offers — with the user's consent — to install it by following the repository's `INSTALL.md` (`https://github.com/JC-SYSU/pubmed-surfing`). Any install problem degrades back to skipping verification and never blocks conversion.

It preserves input order, does not silently deduplicate, reports ambiguous records, and validates the final `.ris` before completion.
