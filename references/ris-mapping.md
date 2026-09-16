# RIS mapping reference for EndNote-oriented output

Use this file when the reference type or a less-common field is uncertain.

## Preferred reference types

| Semantic type | RIS `TY` | Notes |
|---|---|---|
| Journal article | `JOUR` | Includes online-first journal articles. |
| Meeting abstract/poster/oral presentation, conference-only | `CPAPER` | Preserve subtype such as `Meeting Abstract`, `Poster`, or `Oral Presentation` in `M3`/`N1`. |
| Meeting abstract formally published in journal supplement | `JOUR` | Keep journal volume/issue/supplement/pages; add `M3 - Meeting Abstract` when useful. |
| Published conference proceedings contribution | `CONF` | Use only when formal proceedings publication is supported. |
| Whole book | `BOOK` | |
| Book chapter/section | `CHAP` | `T2` = containing book title. |
| Thesis/dissertation | `THES` | |
| Report/guideline/white paper | `RPRT` | Use when report-like, not for journal articles. |
| Standalone web page | `ELEC` | Best-fit RIS electronic/web type; preserve semantic subtype in `M3`/`N1` if needed. |
| Dataset | `DATA` | |
| Newspaper article | `NEWS` | |
| Magazine article | `MGZN` | |
| Blog post | `BLOG` | |
| Patent | `PAT` | |
| Generic/unknown | `GEN` | Last resort only. |

## Preferred field tags

| Field | Tag | Guidance |
|---|---|---|
| Type | `TY` | Required first field. |
| Author | `AU` | One author per line. |
| Secondary author/editor | `A2` | One person per line. |
| Title | `TI` | Main work title. |
| Secondary/container title | `T2` | Journal, book, conference/proceedings container as appropriate. |
| Publication year | `PY` | Four-digit year when supported. |
| Date | `DA` | Use only if a more specific publication date is supplied. |
| Volume | `VL` | |
| Issue | `IS` | May preserve supplement notation when source gives it. |
| Start page | `SP` | May hold an article/e-location number if that is the citation locator. |
| End page | `EP` | Do not invent. |
| DOI | `DO` | Bare DOI, no `doi:` prefix or resolver URL. |
| URL | `UR` | Real resource URL. Avoid duplicating DOI resolver unless requested. |
| ISBN/ISSN | `SN` | Preserve supplied identifier. |
| Publisher | `PB` | |
| Place | `CY` | Publication place or conference location when appropriate. |
| Accession number | `AN` | Good place for `PMID: 12345678`. |
| Type/subtype | `M3` | Useful for Meeting Abstract, Poster, Guideline subtype, etc. |
| Notes | `N1` | Preserve otherwise-unmapped but useful bibliographic detail. |
| Abstract | `N2` | Only when actual abstract text is supplied. |
| Keyword | `KW` | Repeat per keyword if supplied. |
| Language | `LA` | Only when supplied or unambiguous and useful. |
| End record | `ER` | Required final field. |

## Meeting abstract decision tree

1. Does the citation identify a journal and provide journal-like bibliographic data such as volume/issue/supplement/pages/article number?
   - Yes → use `JOUR`; add `M3 - Meeting Abstract` if appropriate.
   - No → continue.
2. Is it clearly an abstract/poster/oral presentation/conference paper presented at a meeting?
   - Yes → use `CPAPER`.
   - No → continue.
3. Is it clearly published within formal conference proceedings?
   - Yes → use `CONF`.
   - No → use the best-supported other type or `GEN`.

## Web page decision tree

A URL does not determine type.

1. Is it a journal article with normal journal metadata? → `JOUR`.
2. Is it a report/guideline with issuing institution/report identity? → usually `RPRT`.
3. Is it a dataset/repository data record? → `DATA`.
4. Is its primary identity simply a webpage/online resource? → `ELEC`.

## Data-preservation rules

- Prefer omission over fabrication.
- If a supplied element is useful but cannot be safely mapped, retain it in `N1`.
- Preserve source order.
- Never silently deduplicate.
- Never expand journal abbreviations, author initials, or organization names from memory.
