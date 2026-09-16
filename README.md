[中文版](README.zh-CN.md) | English

# Citation to EndNote RIS

While writing a paper, references arrive from everywhere. Your adviser
leaves "cite the recent work on this" in a chat message or a Word comment — no
journal, no volume, sometimes not even a full title. You paste passages from
webpages and PDFs into your notes as you search. Different sources, different
formats, different languages, all mixed into one pile. Getting them into
EndNote normally means normalizing every record by hand, one at a time. This
skill takes the whole pile of mixed citation text — chat messages, comments,
web clippings, whatever you have — and turns it into one validated,
batch-importable EndNote RIS file, keeping your reference order, keeping your
wording, inventing nothing.

## What it does

Give it a block of text containing one or many citations, pasted or from a
file. It:

1. **Segments.** Finds how many references are actually there, including
   line-wrapped or fragmentary ones.
2. **Extracts.** Reads every field off the supplied text: authors, titles,
   journal, volume/issue/pages, DOI, PMID, year, and the rest.
3. **Classifies.** Picks the most specific RIS type each citation supports —
   journal article, meeting abstract, conference paper, book, chapter,
   thesis, report, web page, dataset, and more.
4. **Verifies — only when you have it.** If the PubMed Surfing MCP server is
   connected (or you agree to install it), it checks PubMed for discrepancies
   and shows you a table. Nothing from PubMed touches your file until you
   approve it.
5. **Writes.** Produces a single UTF-8 `.ris` with one record per reference,
   then runs its own syntax validator over it.

That is the whole flow: messy text in, one valid file out.

## What it won't do

- It never invents bibliographic facts. No author, title, year, volume, or
  page range is filled in from memory or guessing. Unsupported fields are left
  empty or marked ambiguous, never fabricated.
- It does not silently "fix" your text, deduplicate records, or reorder
  references — duplicates and uncertainty are reported to you, and changes
  happen only if you ask.
- It does not query Crossref, DOI resolvers, or the web on its own. Offline is
  the default; PubMed Surfing is the only voluntary exception, and it needs
  your consent to install and your approval to apply anything.

## What kind of thing this is

A _skill_, not a program: one folder with a `SKILL.md` and a few small support
files, following the [Agent Skills](https://agentskills.io) open standard.

- It runs inside an agent: Claude Code, Codex, or OpenCode, whichever you have.
- The only executable is a Python 3 validator using the standard library —
  no `pip install`, no build step on any OS.
- The client/OS matrix follows each client's documented skills locations
  (macOS, Linux, and Windows; path table in INSTALL.md section 0.5). We develop
  and test on macOS; the Windows notes in INSTALL.md follow the clients'
  documentation.
- OpenCode additionally reads the Claude Code and Codex skills directories,
  which its own docs confirm — so one install can cover more than one client.

## How to use

**Install** — paste into your agent (Claude Code, Codex, or OpenCode); the
agent reads INSTALL.md and does the work:

```
Install the citation-to-endnote-ris skill. The repository is
https://github.com/JC-SYSU/citation-to-endnote-ris.

1. Read INSTALL.md in full and execute it step by step. If you cannot clone
   the repo, read it directly:
   https://raw.githubusercontent.com/JC-SYSU/citation-to-endnote-ris/main/INSTALL.md
2. Probe the machine, pick the right skills directories, and copy the skill
   folder in (sections 0.5 and 1).
3. Run the acceptance checklist (section 3) and report each item to me.
   Anything that fails gets fixed before you report back.
```

Or install by hand: follow `INSTALL.md` directly. Nothing runs at install
time; it is a folder copy.

**Day-to-day** — paste a reference list into the agent and ask for an
EndNote RIS file, or point it at a text file:

> Convert these citations into one RIS file I can import into EndNote.

The agent writes the file, validates it, and reports the type breakdown.

## Quick verification

```bash
python3 scripts/validate_ris.py examples/output.ris
```

Expected: `RESULT: VALID` with 3 records (JOUR, CPAPER, ELEC).

## License

MIT. Details of the mapping rules live in `references/ris-mapping.md`, field
semantics in `SKILL.md`.