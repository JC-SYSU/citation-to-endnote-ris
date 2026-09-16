#!/usr/bin/env python3
"""Lightweight syntax and consistency validator for EndNote-oriented RIS files.

Exit codes:
  0 = no syntax errors (warnings may exist)
  1 = syntax/structure errors found
  2 = usage or file-read error
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

TAG_RE = re.compile(r"^([A-Z0-9][A-Z0-9])  -(?: (.*))?$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)

KNOWN_TYPES = {
    "ABST", "ADVS", "AGGR", "ANCIENT", "ART", "BILL", "BLOG", "BOOK",
    "CASE", "CHAP", "CHART", "CLSWK", "COMP", "CONF", "CPAPER", "CTLG",
    "DATA", "DBASE", "DICT", "EBOOK", "ECHAP", "EDBOOK", "EJOUR", "ELEC",
    "ENCYC", "EQUA", "FIGURE", "GEN", "GOVDOC", "GRANT", "HEAR", "ICOMM",
    "INPR", "JFULL", "JOUR", "LEGAL", "MANSCPT", "MAP", "MGZN", "MPCT",
    "MULTI", "MUSIC", "NEWS", "PAMP", "PAT", "PCOMM", "RPRT", "SER",
    "SLIDE", "SOUND", "STAND", "STAT", "THES", "UNPB", "VIDEO",
}


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def parse_records(lines: list[str]):
    records: list[list[tuple[int, str, str]]] = []
    current: list[tuple[int, str, str]] = []
    errors: list[str] = []

    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        if line.startswith("```"):
            errors.append(f"line {lineno}: Markdown fence found")
            continue
        m = TAG_RE.match(line)
        if not m:
            errors.append(f"line {lineno}: invalid RIS syntax: {line!r}")
            continue
        tag, value = m.group(1), (m.group(2) or "")

        if tag == "TY" and current:
            errors.append(
                f"line {lineno}: new TY encountered before previous record ended with ER"
            )
            records.append(current)
            current = []

        current.append((lineno, tag, value))

        if tag == "ER":
            records.append(current)
            current = []

    if current:
        first_line = current[0][0]
        errors.append(f"record starting at line {first_line}: missing ER terminator")
        records.append(current)

    return records, errors


def validate(path: Path) -> int:
    try:
        data = path.read_bytes()
    except OSError as exc:
        print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    if data.startswith(b"\xef\xbb\xbf"):
        print("WARNING: UTF-8 BOM detected; UTF-8 without BOM is preferred")

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        print(f"ERROR: file is not valid UTF-8: {exc}", file=sys.stderr)
        return 2

    lines = text.splitlines(keepends=True)
    records, errors = parse_records(lines)
    warnings: list[str] = []

    if not records:
        errors.append("no RIS records found")

    type_counts = Counter()
    dois: defaultdict[str, list[int]] = defaultdict(list)
    titles: defaultdict[str, list[int]] = defaultdict(list)

    for idx, record in enumerate(records, start=1):
        tags = [tag for _, tag, _ in record]
        if not tags:
            errors.append(f"record {idx}: empty record")
            continue
        if tags[0] != "TY":
            errors.append(f"record {idx}: first tag must be TY, found {tags[0]}")
        if tags[-1] != "ER":
            errors.append(f"record {idx}: last tag must be ER, found {tags[-1]}")
        if tags.count("TY") != 1:
            errors.append(f"record {idx}: expected exactly one TY, found {tags.count('TY')}")
        if tags.count("ER") != 1:
            errors.append(f"record {idx}: expected exactly one ER, found {tags.count('ER')}")

        fields = defaultdict(list)
        for lineno, tag, value in record:
            fields[tag].append(value.strip())
            if tag == "ER" and value.strip():
                warnings.append(f"record {idx}, line {lineno}: ER should normally have no value")

        ty = fields.get("TY", [""])[0]
        if not ty:
            errors.append(f"record {idx}: TY has no value")
        else:
            type_counts[ty] += 1
            if ty not in KNOWN_TYPES:
                warnings.append(f"record {idx}: uncommon/unknown RIS type {ty!r}")

        for doi in fields.get("DO", []):
            d = doi.strip().rstrip(".,; ")
            if d:
                if not DOI_RE.match(d):
                    warnings.append(f"record {idx}: DOI does not look canonical: {doi!r}")
                dois[d.casefold()].append(idx)

        for title in fields.get("TI", []) + fields.get("T1", []):
            norm = normalize_title(title)
            if norm:
                titles[norm].append(idx)

        if not fields.get("TI") and not fields.get("T1"):
            warnings.append(f"record {idx}: no title field (TI/T1)")

    for doi, idxs in sorted(dois.items()):
        if len(idxs) > 1:
            warnings.append(f"possible duplicate DOI {doi!r} in records {idxs}")

    for title, idxs in sorted(titles.items()):
        if len(idxs) > 1 and len(title) >= 12:
            warnings.append(f"possible duplicate normalized title in records {idxs}: {title!r}")

    for msg in errors:
        print(f"ERROR: {msg}")
    for msg in warnings:
        print(f"WARNING: {msg}")

    print(f"Records: {len(records)}")
    if type_counts:
        print("Types: " + ", ".join(f"{k}={v}" for k, v in sorted(type_counts.items())))
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("RESULT: INVALID")
        return 1
    print("RESULT: VALID")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an EndNote-oriented RIS file")
    parser.add_argument("ris_file", type=Path)
    args = parser.parse_args()
    return validate(args.ris_file)


if __name__ == "__main__":
    raise SystemExit(main())
