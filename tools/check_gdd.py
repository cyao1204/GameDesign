"""Check docs/GDD.md and the session/playtest file names for mechanical mistakes.

Runs in the pre-commit hook. Written rules get forgotten; checks don't
(docs/design/process-research.md, §1.1). Standard library only.

Usage:
    python tools/check_gdd.py            # normal check
    python tools/check_gdd.py --ended    # also fail if a session is still marked in progress
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ALLOWED_TAGS = {"DECIDED", "TENTATIVE", "PROPOSED", "OPEN", "DEFERRED"}
TAG_RE = re.compile(r"\[([A-Z]{4,})(?:,[^\]]*)?\]")
QID_RE = re.compile(r"\bQ-(\d{3})\b")
QROW_RE = re.compile(r"^\|\s*Q-(\d{3})\s*\|")
CHANGELOG_ROW_RE = re.compile(
    r"^\|\s*(?P<ver>\d+\.\d+)(?P<pending>\s*\(pending\))?\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|\s*(?P<session>\d+)\s*\|"
)
HEADER_VERSION_RE = re.compile(r"^\|\s*\*\*Version\*\*\s*\|\s*(?P<ver>\d+\.\d+)(?P<rest>[^|]*)\|")
HEADER_UPDATED_RE = re.compile(r"^\|\s*\*\*Last updated\*\*\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})(?P<rest>[^|]*)\|")
SESSION_FILE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-s(?P<n>\d+)\.md$")
PLAYTEST_FILE_RE = re.compile(r"^P(?P<n>\d+)-\d{4}-\d{2}-\d{2}\.md$")
PLAYTEST_EXTRA_FILES = {"findings.md"}


@dataclass(frozen=True)
class ChangelogRow:
    """One row of the GDD changelog table."""

    version: tuple[int, int]
    pending: bool
    date: str
    session: int


def parse_version(text: str) -> tuple[int, int]:
    """Turn '0.4' into (0, 4) so versions compare as numbers, not strings."""
    major, minor = text.split(".")
    return int(major), int(minor)


def sections(text: str) -> dict[str, list[tuple[int, str]]]:
    """Split the GDD into top-level sections keyed by heading, keeping 1-based line numbers."""
    result: dict[str, list[tuple[int, str]]] = {"preamble": []}
    current = "preamble"
    for number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            current = line[3:].strip()
            result[current] = []
        result[current].append((number, line))
    return result


def find_section(parts: dict[str, list[tuple[int, str]]], prefix: str) -> list[tuple[int, str]]:
    """Return the lines of the first section whose heading starts with prefix (empty if missing)."""
    for heading, lines in parts.items():
        if heading.startswith(prefix):
            return lines
    return []


def check_tags(text: str) -> list[str]:
    """Every [ALLCAPS] tag must be one of the five status tags."""
    issues = []
    for number, line in enumerate(text.splitlines(), start=1):
        for match in TAG_RE.finditer(line):
            if match.group(1) not in ALLOWED_TAGS:
                issues.append(f"GDD line {number}: unknown status tag [{match.group(1)}]")
    return issues


def check_open_tags_cite_ids(text: str) -> list[str]:
    """An [OPEN] tag outside the legend and §10 must cite its Q-### on the same line."""
    issues = []
    for heading, lines in sections(text).items():
        if heading == "preamble" or heading.startswith("10."):
            continue
        for number, line in lines:
            if "[OPEN]" in line and not QID_RE.search(line):
                issues.append(f"GDD line {number}: [OPEN] tag without a Q-### ID")
    return issues


def defined_question_ids(text: str) -> list[int]:
    """Q-### IDs defined as rows of the §10 table, in order."""
    section = find_section(sections(text), "10.")
    return [int(m.group(1)) for _, line in section if (m := QROW_RE.match(line))]


def check_question_ids(text: str) -> list[str]:
    """IDs are unique, numbered 1..N with no gaps, and every cited ID is defined."""
    defined = defined_question_ids(text)
    if not defined:
        return ["GDD §10: no Q-### rows found"]
    issues = [f"GDD §10: Q-{i:03d} is defined twice" for i in sorted(set(defined)) if defined.count(i) > 1]
    missing = sorted(set(range(1, max(defined) + 1)) - set(defined))
    issues += [f"GDD §10: Q-{i:03d} is missing (IDs are never removed or skipped)" for i in missing]
    for number, line in enumerate(text.splitlines(), start=1):
        for match in QID_RE.finditer(line):
            if int(match.group(1)) not in defined:
                issues.append(f"GDD line {number}: Q-{match.group(1)} is cited but not defined in §10")
    return issues


def parse_changelog(text: str) -> list[ChangelogRow]:
    """Read the changelog table rows in order."""
    rows = []
    for _, line in find_section(sections(text), "12."):
        match = CHANGELOG_ROW_RE.match(line)
        if match:
            rows.append(
                ChangelogRow(
                    version=parse_version(match.group("ver")),
                    pending=bool(match.group("pending")),
                    date=match.group("date"),
                    session=int(match.group("session")),
                )
            )
    return rows


def check_changelog_order(rows: list[ChangelogRow]) -> list[str]:
    """Versions go up by 0.1, sessions by 1, dates never go back, and only the last row may be pending."""
    if not rows:
        return ["GDD §12: no changelog rows found"]
    issues = []
    for previous, row in zip(rows, rows[1:]):
        label = f"GDD §12: row for session {row.session}"
        if row.version != (previous.version[0], previous.version[1] + 1):
            issues.append(f"{label}: version should follow {previous.version[0]}.{previous.version[1]} by 0.1")
        if row.session != previous.session + 1:
            issues.append(f"{label}: session number should be {previous.session + 1}")
        if row.date < previous.date:
            issues.append(f"{label}: date {row.date} is earlier than the row above")
    issues += ["GDD §12: only the last changelog row may be pending" for row in rows[:-1] if row.pending]
    return issues


def header_fields(text: str) -> tuple[re.Match[str] | None, re.Match[str] | None]:
    """Find the Version and Last updated rows of the header table."""
    version = updated = None
    for line in text.splitlines():
        version = version or HEADER_VERSION_RE.match(line)
        updated = updated or HEADER_UPDATED_RE.match(line)
    return version, updated


def check_header(text: str, rows: list[ChangelogRow], ended: bool) -> list[str]:
    """The header version and 'in progress' markers must agree with the changelog."""
    version, updated = header_fields(text)
    if not (version and updated and rows):
        return ["GDD header: Version or Last updated row not found"]
    last = rows[-1]
    finished = [row for row in rows if not row.pending]
    issues = []
    if finished and parse_version(version.group("ver")) != finished[-1].version:
        issues.append("GDD header: Version doesn't match the last finished changelog row")
    if updated.group("date") != last.date:
        issues.append(f"GDD header: Last updated date should be {last.date}, the last changelog date")
    in_progress = "in progress" in updated.group("rest") or "pending" in version.group("rest")
    if last.pending != in_progress:
        issues.append("GDD header: 'in progress' / 'pending' markers don't match the changelog's pending row")
    if last.pending and f"session {last.session}" not in updated.group("rest"):
        issues.append(f"GDD header: Last updated should name session {last.session}")
    if ended and last.pending:
        issues.append("GDD: session still marked in progress (run the end-of-session steps)")
    return issues


def check_session_files(folder: Path) -> list[str]:
    """Session summaries are named yyyy-mm-dd-s#.md, numbered 1..N within each day."""
    by_day: dict[str, list[int]] = {}
    issues = []
    for path in sorted(folder.glob("*.md")):
        match = SESSION_FILE_RE.match(path.name)
        if not match:
            issues.append(f"{path.as_posix()}: name should be yyyy-mm-dd-s#.md")
            continue
        by_day.setdefault(match.group("date"), []).append(int(match.group("n")))
    for day, numbers in by_day.items():
        if sorted(numbers) != list(range(1, len(numbers) + 1)):
            issues.append(f"{folder.as_posix()}: sessions on {day} should be numbered s1..s{len(numbers)}")
    return issues


def check_playtest_files(folder: Path) -> list[str]:
    """Playtest reports are named P#-yyyy-mm-dd.md with unique numbers."""
    issues = []
    numbers: list[int] = []
    for path in sorted(folder.glob("*.md")):
        if path.name in PLAYTEST_EXTRA_FILES:
            continue
        match = PLAYTEST_FILE_RE.match(path.name)
        if not match:
            issues.append(f"{path.as_posix()}: name should be P#-yyyy-mm-dd.md")
            continue
        numbers.append(int(match.group("n")))
    issues += [f"{folder.as_posix()}: P{n} is used twice" for n in sorted(set(numbers)) if numbers.count(n) > 1]
    return issues


def check_gdd_text(text: str, ended: bool = False) -> list[str]:
    """Run every check that only needs the GDD text."""
    rows = parse_changelog(text)
    return (
        check_tags(text)
        + check_open_tags_cite_ids(text)
        + check_question_ids(text)
        + check_changelog_order(rows)
        + check_header(text, rows, ended)
    )


def run(root: Path, ended: bool) -> list[str]:
    """Check the GDD and the docs folders under root."""
    gdd = root / "docs" / "GDD.md"
    if not gdd.is_file():
        return [f"{gdd.as_posix()}: not found"]
    issues = check_gdd_text(gdd.read_text(encoding="utf-8"), ended)
    issues += check_session_files(root / "docs" / "sessions")
    issues += check_playtest_files(root / "docs" / "playtests")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ended", action="store_true", help="fail if a design session is still in progress")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    issues = run(args.root, args.ended)
    for issue in issues:
        print(f"check_gdd: {issue}")
    if issues:
        print(f"check_gdd: FAILED ({len(issues)} issue{'s' if len(issues) != 1 else ''})")
        return 1
    print("check_gdd: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
