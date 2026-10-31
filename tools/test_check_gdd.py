"""Tests for check_gdd.py. Standard library only: python -m unittest discover -s tools"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import check_gdd  # noqa: E402

HEADER_DONE = "| **Last updated** | 2026-10-30 (session 2) |\n| **Version** | 0.2 |\n"
HEADER_OPEN = (
    "| **Last updated** | 2026-10-31 (session 3, in progress) |\n"
    "| **Version** | 0.2 (0.3 pending: bumped at the end of session 3) |\n"
)
ROWS_DONE = "| 0.1 | 2026-10-25 | 1 | a |\n| 0.2 | 2026-10-30 | 2 | b |\n"
ROW_PENDING = "| 0.3 (pending) | 2026-10-31 | 3 | In progress. |\n"


def make_gdd(
    header: str = HEADER_DONE,
    rows: str = ROWS_DONE,
    body: str = "- **[DECIDED]** A rule.\n- **[OPEN]** (Q-001) A question.\n",
    questions: str = "| Q-001 | A question | Prototype | Open. |\n",
) -> str:
    """Build a small GDD that passes every check unless a part is overridden."""
    return (
        "# GDD\n\n| | |\n|---|---|\n" + header
        + "\n- **[OPEN]**: legend line, exempt.\n\n## 1. Rules\n\n" + body
        + "\n## 10. Open questions\n\n| ID | Question | Needed by | Status |\n|---|---|---|---|\n" + questions
        + "\n## 12. Changelog\n\n| Version | Date | Session | Changes |\n|---|---|---|---|\n" + rows
    )


class CheckGddTextTests(unittest.TestCase):
    def test_CheckGddText_ValidFinishedSession_ReturnsNoIssues(self) -> None:
        self.assertEqual(check_gdd.check_gdd_text(make_gdd()), [])

    def test_CheckGddText_ValidSessionInProgress_ReturnsNoIssues(self) -> None:
        text = make_gdd(header=HEADER_OPEN, rows=ROWS_DONE + ROW_PENDING)
        self.assertEqual(check_gdd.check_gdd_text(text), [])

    def test_CheckGddText_InProgressWithEndedFlag_ReportsSessionStillOpen(self) -> None:
        text = make_gdd(header=HEADER_OPEN, rows=ROWS_DONE + ROW_PENDING)
        issues = check_gdd.check_gdd_text(text, ended=True)
        self.assertTrue(any("still marked in progress" in issue for issue in issues))

    def test_CheckTags_UnknownTag_ReportsIt(self) -> None:
        issues = check_gdd.check_gdd_text(make_gdd(body="- **[DECIDDED]** Typo.\n"))
        self.assertTrue(any("[DECIDDED]" in issue for issue in issues))

    def test_CheckTags_TagWithQualifier_IsAllowed(self) -> None:
        self.assertEqual(check_gdd.check_tags("- **[DECIDED, may change]** Rule."), [])

    def test_CheckOpenTags_OpenWithoutId_ReportsIt(self) -> None:
        issues = check_gdd.check_gdd_text(make_gdd(body="- **[OPEN]** No ID here.\n"))
        self.assertTrue(any("without a Q-### ID" in issue for issue in issues))

    def test_CheckQuestionIds_CitedButUndefined_ReportsIt(self) -> None:
        issues = check_gdd.check_gdd_text(make_gdd(body="- **[OPEN]** (Q-007) Unknown.\n"))
        self.assertTrue(any("Q-007 is cited but not defined" in issue for issue in issues))

    def test_CheckQuestionIds_GapInNumbering_ReportsMissingId(self) -> None:
        questions = "| Q-001 | A | Prototype | Open. |\n| Q-003 | C | Prototype | Open. |\n"
        issues = check_gdd.check_gdd_text(make_gdd(questions=questions))
        self.assertTrue(any("Q-002 is missing" in issue for issue in issues))

    def test_CheckQuestionIds_DuplicateId_ReportsIt(self) -> None:
        questions = "| Q-001 | A | Prototype | Open. |\n| Q-001 | B | Prototype | Open. |\n"
        issues = check_gdd.check_gdd_text(make_gdd(questions=questions))
        self.assertTrue(any("defined twice" in issue for issue in issues))

    def test_CheckChangelog_VersionSkipped_ReportsIt(self) -> None:
        rows = "| 0.1 | 2026-10-25 | 1 | a |\n| 0.3 | 2026-10-30 | 2 | b |\n"
        header = "| **Last updated** | 2026-10-30 (session 2) |\n| **Version** | 0.3 |\n"
        issues = check_gdd.check_gdd_text(make_gdd(header=header, rows=rows))
        self.assertTrue(any("should follow 0.1" in issue for issue in issues))

    def test_CheckChangelog_VersionTen_ComparesAsNumber(self) -> None:
        rows = "| 0.9 | 2026-10-25 | 1 | a |\n| 0.10 | 2026-10-30 | 2 | b |\n"
        header = "| **Last updated** | 2026-10-30 (session 2) |\n| **Version** | 0.10 |\n"
        self.assertEqual(check_gdd.check_gdd_text(make_gdd(header=header, rows=rows)), [])

    def test_CheckChangelog_DateGoesBack_ReportsIt(self) -> None:
        rows = "| 0.1 | 2026-10-30 | 1 | a |\n| 0.2 | 2026-10-25 | 2 | b |\n"
        header = "| **Last updated** | 2026-10-25 (session 2) |\n| **Version** | 0.2 |\n"
        issues = check_gdd.check_gdd_text(make_gdd(header=header, rows=rows))
        self.assertTrue(any("earlier than the row above" in issue for issue in issues))

    def test_CheckHeader_VersionBumpedEarly_ReportsMismatch(self) -> None:
        header = "| **Last updated** | 2026-10-31 (session 3, in progress) |\n| **Version** | 0.3 (pending) |\n"
        issues = check_gdd.check_gdd_text(make_gdd(header=header, rows=ROWS_DONE + ROW_PENDING))
        self.assertTrue(any("Version doesn't match" in issue for issue in issues))

    def test_CheckHeader_PendingRowButNoMarker_ReportsMismatch(self) -> None:
        header = "| **Last updated** | 2026-10-31 (session 3) |\n| **Version** | 0.2 |\n"
        issues = check_gdd.check_gdd_text(make_gdd(header=header, rows=ROWS_DONE + ROW_PENDING))
        self.assertTrue(any("markers don't match" in issue for issue in issues))


class FileNameTests(unittest.TestCase):
    def _folder(self, names: list[str]) -> Path:
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        folder = Path(holder.name)
        for name in names:
            (folder / name).write_text("x", encoding="utf-8")
        return folder

    def test_CheckSessionFiles_ValidNames_ReturnsNoIssues(self) -> None:
        folder = self._folder(["2026-10-30-s1.md", "2026-10-30-s2.md", "2026-10-31-s1.md"])
        self.assertEqual(check_gdd.check_session_files(folder), [])

    def test_CheckSessionFiles_SkippedNumber_ReportsIt(self) -> None:
        folder = self._folder(["2026-10-30-s1.md", "2026-10-30-s3.md"])
        self.assertEqual(len(check_gdd.check_session_files(folder)), 1)

    def test_CheckSessionFiles_BadName_ReportsIt(self) -> None:
        folder = self._folder(["session5.md"])
        self.assertTrue(check_gdd.check_session_files(folder)[0].endswith("yyyy-mm-dd-s#.md"))

    def test_CheckPlaytestFiles_TrackerAndReport_ReturnsNoIssues(self) -> None:
        folder = self._folder(["findings.md", "P1-2026-11-02.md"])
        self.assertEqual(check_gdd.check_playtest_files(folder), [])

    def test_CheckPlaytestFiles_DuplicateNumber_ReportsIt(self) -> None:
        folder = self._folder(["P1-2026-11-02.md", "P1-2026-11-03.md"])
        self.assertTrue(any("used twice" in issue for issue in check_gdd.check_playtest_files(folder)))


if __name__ == "__main__":
    unittest.main()
