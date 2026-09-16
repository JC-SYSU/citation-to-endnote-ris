---
name: citation-to-endnote-ris
description: Convert messy, irregular text containing one or many bibliographic citations into a clean, semantically parsed, reference-type-aware, batch-importable EndNote RIS (.ris) file. Use when citations may have inconsistent punctuation, line breaks, field order, missing labels, mixed reference types, DOI/PMID/URL forms, journal articles, meeting abstracts, conference papers/proceedings, books, reports, theses, datasets, or web pages. Do not use merely to reformat an already-valid RIS file unless validation or repair is requested.
license: MIT
---

# Citation Text → EndNote RIS

Convert unstructured or semi-structured citation text into one validated RIS file containing all references in input order, suitable for batch import into EndNote.

Use with Claude Code, Codex, or OpenCode and filesystem write access. When PubMed Surfing is available, use network access for verification but never replace source data without user approval. When it is missing, offer to install it per section 4 before deciding the verification outcome; conversion must never be blocked by its absence.

The core task is semantic bibliographic reconstruction, not regex-only conversion.

## Primary outcome

When the user provides citation text or a text-containing file:

1. Identify how many distinct references are present.
2. Reconstruct wrapped or fragmented references.
3. Semantically extract bibliographic fields.
4. Determine the most appropriate reference type for each record.
5. Normalize only what can be supported by the source text or verified PubMed data approved by the user.
6. When PubMed Surfing is available, verify identified literature and collect discrepancies without changing source-derived fields.
7. Write all records to a single UTF-8 `.ris` file.
8. Validate the file, present verification discrepancies, and let the user choose whether to apply verified replacements.

If filesystem access is available, create the file rather than merely printing RIS in chat.

## Non-negotiable rules

- Never invent bibliographic facts.
- Never fabricate authors, titles, journal names, dates, volume/issue/pages, DOI, PMID, ISBN/ISSN, conference details, publishers, URLs, or access dates.
- Do not silently “correct” a field using model memory.
- By default, derive the RIS from only the supplied text/files. PubMed Surfing verification is the exception: use it automatically when available, but do not apply its values without user approval.
- Do not perform other online lookup, DOI resolution, or metadata enrichment unless the user explicitly asks to verify, complete, enrich, or look up the references.
- When a field is uncertain, preserve the best-supported interpretation and record the ambiguity in the completion report. Leave unsupported fields empty.
- Preserve the user's reference order unless they explicitly request sorting.
- Do not deduplicate automatically. Detect likely duplicates and report them; remove them only if the user asks.
- Do not confuse a DOI URL with a normal webpage URL. Normalize DOI URLs into the `DO` field.
- Do not treat every URL-bearing citation as a Web Page. A journal article with a URL remains a journal article.
- Do not treat every citation mentioning a conference as a conference-only record. Published journal supplements and published proceedings require different handling.

## Workflow

### 1. Read and segment the input

Treat citation-boundary detection as a semantic task.

Potential boundary signals include:

- numbered or bulleted entries;
- blank lines;
- author → year → title patterns;
- journal/container + volume/issue/pages patterns;
- DOI, PMID, ISBN, URL, accession number, or conference identifiers near the end of a record;
- repeated citation-style structures;
- explicit labels such as `Authors:`, `Title:`, `Journal:`, `DOI:`, `PMID:`, `Conference:`, or `URL:`.

Do not split a single citation merely because it wraps across lines. Merge continuation lines when they clearly belong to the same record.

Do not merge two references merely because punctuation is missing between them. Use semantic structure to infer the most likely boundary.

Strip list numbering/bullets only when they are structural and not part of bibliographic content.

### 2. Build an internal semantic record

For each reference, reason over these fields before rendering RIS:

- `source_index`
- `raw_reference`
- `semantic_type`
- `ris_type`
- `authors[]`
- `editors[]`
- `title`
- `container_title`
- `year`
- `date`
- `volume`
- `issue`
- `start_page`
- `end_page`
- `article_number`
- `doi`
- `pmid`
- `isbn_or_issn`
- `publisher`
- `place_published`
- `conference_name`
- `conference_location`
- `conference_date`
- `url`
- `access_date`
- `language`
- `keywords[]`
- `notes[]`
- `confidence`

This internal model is for reasoning only. Do not create unsupported values just to fill every field.

### 3. Normalize conservatively

#### Authors

- Split multiple authors semantically, not only on commas.
- Emit one `AU` line per author.
- Prefer `Family, Given` when the source makes name order clear.
- Initials may be normalized cautiously, e.g. `Smith J` → `Smith, J.` when unambiguous.
- Preserve particles, hyphenated names, apostrophes, suffixes, and non-Latin names.
- For an organizational/corporate author, preserve the organization as one author. When useful for EndNote name handling, retain it as a corporate name rather than inventing personal-name structure.
- If the author string is too ambiguous to split safely, preserve it rather than hallucinating individual authors.

#### Titles

- Preserve substantive capitalization and punctuation unless the user requests a style transformation.
- Join accidental line breaks and repeated whitespace.
- Do not translate titles unless requested.

#### DOI

Normalize DOI to a bare identifier when possible:

- `https://doi.org/10.xxxx/abc` → `10.xxxx/abc`
- `http://dx.doi.org/10.xxxx/abc` → `10.xxxx/abc`
- `doi:10.xxxx/abc` → `10.xxxx/abc`

Remove trailing citation punctuation only when it is clearly not part of the DOI.

Write DOI to `DO  -`.

If the only URL is a DOI resolver URL, do not duplicate it into `UR` unless the user asks to preserve all URLs.

#### PMID

Preserve PMID as an accession identifier, e.g. `AN  - PMID: 12345678`.

Do not manufacture a PMID from other identifiers.

#### Pages and article numbers

- `123-130` → `SP  - 123` and `EP  - 130`.
- An electronic article number such as `e12345`, `102345`, or `P1234` may be stored in `SP` when it functions as the citation locator and there is no meaningful page range.
- Do not guess an end page.

#### Dates

- Put the publication year in `PY` when known.
- Preserve a more specific date in `DA` when the source provides it and it is useful.
- Preserve access date for web material only when explicitly supplied.

### 4. Verify identified literature with PubMed Surfing (install it first when missing)

After building and conservatively normalizing the semantic records, inspect the tools available in the current environment for the PubMed Surfing MCP tools (not merely a similarly named file or command).

If PubMed Surfing is available:

1. Verify every record that is plausibly indexed by PubMed. Use only the lookup tools below; journal profiling, related-article, citation-formatting, and article-type tools are not part of this check.
2. Accept a match only when identifiers agree or the title plus supporting author, journal, and year evidence establishes the same work. Treat ambiguous search results as unverified rather than choosing the closest result.
3. Compare source-derived values with PubMed values for bibliographic identity and RIS fields, including title, authors, journal, publication date/year, volume, issue, pages/article number, DOI, and PMID when available.
4. Record only material discrepancies. Keep the source-derived value in the RIS at this stage; never silently merge or replace it.
5. Distinguish `not indexed` or `no confident match` from an error. If PubMed Surfing is callable but lookup fails or times out, preserve the original data and report the verification failure.

#### PubMed Surfing lookup recipe

- Supplied PMID: call `pubmed_fetch_abstract` with `{"pmid":"<PMID>"}`.
- Supplied DOI but no PMID: call `pubmed_search` with `{"query":"<bare DOI>[doi]","retmax":3}`. Strip `doi:` and DOI-resolver prefixes first.
- No identifier: call `pubmed_search` with a narrow raw query such as `"<distinctive title>"[Title] AND <first-author surname>[Author]`, adding `<year>[dp]` only when needed. Start with `retmax:3`; broaden once by removing the least reliable term if there is no result.
- After a confident search match, call `pubmed_fetch_abstract` with its PMID. Use the fetch result—not the compact search summary—for field comparison because it returns `pmid`, `title`, `authors`, `journal`, `journal_abbrev`, `year`, `volume`, `issue`, `pages`, and `doi`.
- Treat a response with `error` as a lookup failure. Treat `partial:true`, blank identity fields, or multiple plausible hits as insufficient evidence until a successful fetch resolves the identity.

#### Auto-install when missing

If the PubMed Surfing MCP tools are not available, do not silently skip: offer to install the server before deciding the verification outcome.

1. **Get consent, then install.** Explain briefly what installing involves: cloning `https://github.com/JC-SYSU/pubmed-surfing`, building the server (needs Go >= 1.25 unless using a prebuilt release archive), and registering it with the MCP client — which modifies the client's configuration. Proceed only with the user's agreement (an explicit "yes, install it" in this turn counts; a refusal or hesitation means degrade to skipping, below).
2. **Obtain the installation spec.** Clone the repository (a shallow clone is fine) and read its `INSTALL.md` first. The canonical online copy is `https://github.com/JC-SYSU/pubmed-surfing/blob/main/INSTALL.md`. If the user instead points you at a local checkout, reading its `INSTALL.md` is equally valid.
3. **Execute it in order.** INSTALL.md is an operating spec stating an expected output and failure handling per step: run prerequisites (0), build (1), per-user install (3), client registration (4), and the acceptance checklist (5). Respect its platform notes: prebuilt release archives exist only for darwin/arm64 and windows/amd64; every other platform builds from source.
   - For Claude Code registration, use `claude mcp add --scope user --transport stdio pubmed-surfing -- {{ENTRY}}`, substituting the entry path from section 3 of INSTALL.md. The `--scope user` part matters: the default scope is local, which registers the server only for the current project and would silently disappear in other working directories. On Windows, `{{ENTRY}}` is two argv entries (`<home>\pubmed-surfingctl.exe` plus `run-current`): pass them as separate arguments after the `--`. For Codex or OpenCode, follow INSTALL.md sections 4A/4C, splitting `{{ENTRY}}` into `command`/`args` the same way.
   - INSTALL.md uses POSIX utilities (e.g. `command -v` in the prerequisites). On Windows, translate them to platform equivalents (`command -v` → `Get-Command`, `rm -rf` → `Remove-Item -Recurse -Force`) rather than assuming they exist.
   - If INSTALL.md conflicts with the installed client's actual behavior, trust the client's own documentation.
4. **Verify the install** with the acceptance checklist in section 5 of INSTALL.md. Then note that MCP configuration is loaded at session start: newly registered tools typically become visible only after a session restart (in Claude Code, exit and restart the session). If the tools are not visible in the current session, report "installed — restart the session and re-run this skill to enable verification" instead of acting as if verification were possible.
5. **On any failure, degrade gracefully.** Missing Go, no network access, or a step that still fails after its documented failure handling: stop installing, do not block conversion, keep the source-derived RIS as the result, and report the install failure with the INSTALL.md link in the completion response. Do not retry installation within this conversion.

This step is complete when every plausibly PubMed-indexed record is matched, marked unverified, or has a reported lookup failure, and every matched record has been compared field by field.

### 5. Determine reference type

Use the most specific supported type justified by the citation.

Read `references/ris-mapping.md` when type selection or field mapping is uncertain.

#### Journal article → `TY  - JOUR`

Use when the work is an article in a scholarly journal, including online-first articles and articles that also have URLs.

Strong signals include journal title plus one or more of volume, issue, pages/article number, DOI, PMID, or an article publication date.

#### Meeting abstract / poster / oral presentation

Meeting abstracts require special handling.

**Conference-only abstract/presentation** → `TY  - CPAPER`

Use when the item is primarily an abstract, poster, oral presentation, or conference paper presented at a meeting and is not clearly published as a journal article or as a full proceedings contribution.

Preserve conference name, location/date, abstract/poster number, and presentation type when available. Use `M3` and/or `N1` for useful type details that lack a dedicated RIS field.

**Abstract published in a journal supplement** → normally `TY  - JOUR`

If the citation provides a real journal container with volume/issue/supplement/pages or article number, preserve it as a journal record so EndNote can retain the published citation. Add `M3  - Meeting Abstract` when appropriate and optionally a concise `N1` containing meeting information not otherwise represented.

Do not discard journal bibliographic data simply because the item originated at a meeting.

#### Published conference proceedings contribution → `TY  - CONF`

Use when the work is published as part of formal conference proceedings and the citation supports proceedings-level bibliographic data.

Do not use `CONF` merely because a meeting is mentioned.

#### Book → `TY  - BOOK`

Use for a whole authored book.

#### Book chapter / section → `TY  - CHAP`

Use for a chapter or contribution contained in a book.

#### Thesis/dissertation → `TY  - THES`

Use for dissertations, doctoral theses, master's theses, etc.

#### Report / guideline / institutional publication → `TY  - RPRT`

Use for technical reports, institutional reports, many guidelines, white papers, and similar report-like documents when they are not journal articles or books.

#### Web page → `TY  - ELEC`

Use for a standalone web resource whose bibliographic identity is primarily a webpage/online item rather than a journal article, report, book, or dataset.

Store the page URL in `UR`. Preserve site/publisher/organization information when supplied.

Because RIS and EndNote reference-type vocabularies are not perfectly one-to-one across versions/import filters, preserve the semantic nature of unusual web records in `M3` or `N1` when helpful.

#### Dataset → `TY  - DATA`

Use for datasets, repositories' dataset records, and data releases.

#### Newspaper article → `TY  - NEWS`

#### Magazine article → `TY  - MGZN`

#### Blog post → `TY  - BLOG`

#### Patent → `TY  - PAT`

#### Unknown / insufficiently specified → `TY  - GEN`

Use `GEN` only when a more specific type cannot be supported. Do not force an uncertain citation into `JOUR` merely because most inputs are journal references.

### 6. Render RIS

Each record MUST:

- start with exactly one `TY  - <TYPE>` line;
- contain one field per line;
- use repeated lines for repeated fields such as authors;
- end with exactly `ER  -`;
- be followed by a blank line before the next record.

Use the canonical spacing:

```text
TY  - JOUR
AU  - Smith, Jane
TI  - Example title
ER  -
```

Do not put Markdown fences, bullets, numbering, comments, or explanatory prose inside the `.ris` file.

Recommended field mapping:

| Meaning | RIS tag |
|---|---|
| Reference type | `TY` |
| Author | `AU` (repeat) |
| Editor/secondary author | `A2` (repeat) |
| Title | `TI` |
| Journal / secondary container / conference or book container | `T2` |
| Year | `PY` |
| Full/specific date | `DA` |
| Volume | `VL` |
| Issue | `IS` |
| Start page / article number | `SP` |
| End page | `EP` |
| DOI | `DO` |
| URL | `UR` |
| ISSN/ISBN | `SN` |
| Publisher | `PB` |
| Place published / conference location when appropriate | `CY` |
| Accession number such as PMID | `AN` |
| Type of work / subtype | `M3` |
| Notes | `N1` (repeat if useful) |
| Abstract | `N2` |
| Keyword | `KW` (repeat) |
| Language | `LA` |
| End record | `ER` |

Use `T2` according to the record type:

- journal article: journal title;
- book chapter: book title;
- conference record: conference/proceedings title when appropriate.

If a field does not map cleanly, prefer a concise `N1` note over inventing a misleading structured field.

### 7. File-writing requirements

Unless the user specifies a path/name:

- filename: `endnote_import_<timestamp>.ris` or another concise descriptive `.ris` name;
- do not overwrite an existing file; add a numeric suffix if needed;
- encoding: UTF-8, preferably without BOM;
- normalize Unicode to NFC when possible;
- line endings may be LF or CRLF, but keep them consistent within the file;
- ensure the file ends cleanly after the last record.

The output must be one file containing all records for batch import.

If the environment supports file associations, a `.ris` file may be opened directly by EndNote when the operating system associates RIS with EndNote. Do not claim the association exists if it has not been configured on that machine.

### 8. Validate before completion

If `scripts/validate_ris.py` exists and Python 3 is available, run:

```bash
python3 scripts/validate_ris.py /path/to/output.ris
```

On Windows, `python3` is often not on PATH; use `python` or `py -3` instead. The script uses the Python standard library only — no `pip install` step.

Resolve syntax errors before reporting success.

Validation must check at least:

- UTF-8 readability;
- at least one record exists;
- every record starts with `TY`;
- every record ends with `ER`;
- RIS tag syntax is valid;
- no Markdown fences or obvious commentary leaked into the file;
- record count matches the parsed reference count;
- duplicate DOI/title warnings are surfaced but do not cause automatic deletion.

After machine validation, perform a semantic sanity pass:

- title is not accidentally an author list;
- journal/container is not accidentally a DOI/URL;
- year is plausible as a year and came from the source;
- page/volume/issue fields were not shifted;
- meeting abstracts use the nuanced rules above;
- web URLs are not misclassified journal articles;
- no inferred data was presented as certain.

## Confidence handling

Assign an internal confidence for each parsed record:

- **high**: citation boundaries and major fields are clear;
- **medium**: record is recoverable but one or more fields/type choices are ambiguous;
- **low**: boundaries or identity are substantially uncertain.

Do not put confidence labels into RIS unless the user asks. Report low-confidence records in the completion summary using their input index and a short explanation.

If most records are low confidence, still produce the best valid RIS possible unless doing so would create misleading bibliographic records. In that case, preserve uncertain data conservatively in `N1` and clearly report the limitation.

## Apply verified corrections only after confirmation

After writing and validating the source-derived RIS, if PubMed Surfing found discrepancies, show a compact Markdown table with one row per record and field discrepancy:

| Record | Field | Original | PubMed Surfing | Match evidence |
|---|---|---|---|---|

Then ask whether the user wants to replace the original values with the verified values. Do not claim completion while this choice is pending.

- If the user approves all corrections, update only the listed fields in the RIS and validate it again.
- If the user approves selected corrections, ask for or follow their selection, update only those fields, and validate again.
- If the user declines, leave the original RIS unchanged.
- Never overwrite ambiguous values, unmatched records, or fields absent from the verified result.
- Do not add unrelated PubMed metadata merely because it is available.

If no discrepancies are found, state that verification found no material conflicts and do not ask an unnecessary overwrite question.

## Completion response

After creating the file, keep the response concise and include:

- output file path/name;
- number of references written;
- type breakdown, e.g. `JOUR 18 / CPAPER 3 / ELEC 2`;
- count/list of ambiguous or low-confidence records, if any;
- duplicate warnings, if any;
- validation result.
- PubMed Surfing verification result: discrepancy table and overwrite question, no material conflicts, lookup failure, install declined or failed (verification skipped), or installed but awaiting a session restart, as applicable.

Do not paste the entire RIS into chat unless the user asks to inspect it.

## Example behavior

Input may look like:

```text
1. Smith J, Lee A. Example article. Journal of Examples. 2024;12(3):101-109. doi:10.1234/example.1

2 Brown T Example poster title. Poster 442. Annual Example Congress, Boston, 2023.

World Health Organization. Example web guidance. Updated 5 May 2025. https://example.org/guidance Accessed 2 June 2025
```

Interpretation:

- record 1 → journal article → `JOUR`;
- record 2 → conference-only poster/meeting abstract → `CPAPER`, subtype retained in `M3`/`N1`;
- record 3 → standalone web page → `ELEC`.

Write all three records to one `.ris` file and validate it.
