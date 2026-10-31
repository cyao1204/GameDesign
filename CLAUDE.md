# Elemental Affliction — project instructions for Claude

A solo first game: a 1v1 fantasy card duel where casting magic afflicts the caster. Currently in **design / pre-production**, with no code yet.

## Files
- `docs/GDD.md`: the living Game Design Document and the single source of truth for the design. Read it before any design discussion.
- `docs/sessions/`: one summary per design session, named `yyyy-mm-dd-s#.md`, where `#` is the session's number **within that day** (first session of the day is `s1`, the second `s2`, and so on). Count from the dates in the GDD changelog.
- `docs/playtests/`: one report per playtest (`P#-yyyy-mm-dd.md`) plus `findings.md`, the tracker of every finding and its status.
- `docs/design/process-research.md`: why the process is set up this way, and the **process items still owed** at each phase (§5). Read §5 at the start of each new phase.
- `docs/specs/`: build specs, one per system, once prototyping starts. The GDD stays the creative vision.
- `tools/check_gdd.py`: checks the GDD and session files. Runs on every commit.
- `.claude/skills/`: `game-design-session` (start and end a design session), `playtest-session` (record a playtest).

## Setup (once per clone)
```bash
git config core.hooksPath .githooks
```
This turns on the pre-commit check. Run the check by hand with `python tools/check_gdd.py`, and its tests with `python -m unittest discover -s tools`.

## About me
- New to game design, no formal background. Explain any jargon the first time it comes up, with a short example from a well-known game.
- Solo. 3–4 h on workdays, 5+ h on weekends. Lots of coding experience.
- Target platform: PC and/or web. Engine: undecided (Q-014).

## How to work with me
- This is mainly for brainstorming. When I bring an idea, give 2–3 distinct directions with their trade-offs, not one answer.
- Be honest. Push back if an idea is vague, derivative, or too big for my resources. Don't just validate.
- Ask at most one or two clarifying questions at a time.
- Keep scope realistic for a first game. Flag anything that would take a large team or years.
- Don't jump to code or engine specifics unless I ask. Design first.

## Session roles
- **Design session:** changes the GDD. Follows the `game-design-session` skill.
- **Playtest session:** records what happened in a playtest. Follows the `playtest-session` skill. It doesn't change rules; findings feed the next design session.
- **Build session** (from the prototype on): builds against the GDD and `docs/specs/`. It doesn't redesign. If the GDD is silent or [OPEN], stop and ask.
- **Review:** a check of finished work runs in a fresh session, never in the one that did the work.

## Design sessions
- A session starts when I say something like **"Starting game design session"** and ends only when I say **"End game design session"**. Follow the `game-design-session` skill for both.
- **Version bumps happen once per session, at the end.** Never bump the GDD version mid-session, however many decisions we make.
- At the end of a session: bump the version, finalize the changelog row, write the summary to `docs/sessions/yyyy-mm-dd-s#.md`, and tell me what changed in the GDD.

## Keeping the GDD
- When I make a decision, update `docs/GDD.md` straight away: change the item's status tag and add it to the session's pending changelog row. Don't bump the version (see above).
- Status tags: [DECIDED] (my call), [TENTATIVE] (leaning, needs playtest), [PROPOSED] (your suggestion, not yet accepted), [OPEN], [DEFERRED]. Never mark your own suggestion as [DECIDED].
- **Open questions** have stable IDs (`Q-###`) in GDD §10. Every [OPEN] tag cites its ID. Never resolve a `Q-###` silently, never reuse or renumber an ID. A new open question gets the next free number.
- **Terms:** game terms are working names and can change. Until one is renamed, use the exact word in the GDD glossary (term registry). Add a new term there before using it.
- Don't silently resolve contradictions. Flag them with ⚠ in the GDD and ask.
- Commit GDD changes locally as we go. Push only when I ask.

## Commits
- Format: `docs: session N - <topic> [GDD §x.y @ vA.B]`, citing the sections changed and the GDD version in the header. During a session that is the current version, e.g. `[GDD §5.3 @ v0.4]`. Also cite any `Q-###` answered.
- Never bypass the pre-commit check (`--no-verify`). If it fails, fix the cause.
