---
name: game-design-session
description: Start, run and end an Elemental Affliction design session. Use when Chris says "Starting game design session" (or similar) to open one, and "End game design session" to close it. Covers when to update docs/GDD.md, open-question IDs, the once-per-session version bump, the pending changelog row, and writing the summary to docs/sessions/yyyy-mm-dd-s#.md.
---

# Game design session

A design session is bounded by two phrases from Chris:
- **Start:** "Starting game design session" (or a close variant).
- **End:** "End game design session". Only this phrase ends a session. Finishing a topic or a long pause does not.

## Starting a session

1. Read `CLAUDE.md` and `docs/GDD.md`. If `docs/playtests/findings.md` has findings marked **New**, read them too: they are inputs for this session.
2. Read the most recent summary in `docs/sessions/` (latest date, then highest `s#`).
3. Work out the overall session number (used in the GDD and changelog): the highest session number in the GDD changelog, plus 1. This is separate from the within-day number used in the summary filename.
4. In the GDD header, set **Last updated** to today with "(session N, in progress)". Set **Version** to the current version with "(X.Y pending: bumped at the end of session N)". Don't change the version number itself.
5. Add one changelog row: `| X.Y (pending) | <date> | N | In progress. |`, where X.Y is the current version + 0.1.
6. Tell Chris in 2–3 lines where the last session left off and what's next (usually the open questions in GDD §10). Then ask which topic to start with.

## During the session

- Follow the "How to work with me" rules in `CLAUDE.md`: 2–3 directions with trade-offs, honest push-back, at most 1–2 questions at a time.
- When Chris decides something, update `docs/GDD.md` right away: set the status tag, fix any section it affects (core loop, §10 open questions, §11 next steps, §9 risks, glossary), and add a short note to the pending changelog row.
- **Never bump the version mid-session.**
- Flag contradictions with ⚠ and ask. Never resolve them silently.
- New open question: add it to §10 with the next free `Q-###` and cite the ID next to its [OPEN] tag. When one is answered, update its §10 status. Never renumber or reuse an ID.
- New term: add it to the glossary (term registry) before using it.
- Commit GDD changes locally as you go: `docs: session N - <topic> [GDD §x.y @ vA.B]`, using the current, un-bumped version. The pre-commit hook runs `tools/check_gdd.py`; fix any failure, never `--no-verify`. Don't push unless asked.

## Ending a session (on "End game design session")

1. **Bump the version** by 0.1. Update the header: remove "pending" and "in progress".
2. **Finalize the changelog row:** replace "(pending)" with the version number, and rewrite the notes into one tidy summary of the session's changes.
3. **Write the summary** to `docs/sessions/yyyy-mm-dd-s#.md`. Use the date the session ended. `#` is the session's number **within that day**, not the overall session number: count the GDD changelog rows with the same date, and this session's place among them is `#`. Example: session 3 and session 4 were both on 2026-10-30, so session 4's file is `2026-10-30-s2.md`. Use the template below.
4. **Check and commit:** run `python tools/check_gdd.py --ended` (it fails if a "pending" or "in progress" marker is left), then commit with `docs: end session N - GDD vX.Y`.
5. **Tell Chris** what changed in the GDD (decided / tentative / proposed / reopened), what's still open, and ask whether to push.

## Summary template

```markdown
# Session N — yyyy-mm-dd

GDD: vOLD → vNEW

## Covered
- Topics discussed, briefly.

## Decided
- Chris's calls this session, with GDD section refs and any `Q-###` answered.

## Tentative
- Leanings that need playtesting.

## Proposed (awaiting Chris)
- Claude's suggestions not yet accepted.

## Reopened / changed
- Earlier decisions that were changed or reopened, and why.

## Flagged
- ⚠ contradictions still unresolved (or "None").

## Carried forward
- Open questions to start the next session with, by `Q-###` ID.
```

Leave out any section that would be empty, except **Decided** and **Carried forward**.
