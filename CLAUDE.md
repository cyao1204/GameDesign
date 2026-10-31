# Elemental Affliction — project instructions for Claude

A solo first game: a 1v1 fantasy card duel where casting magic afflicts the caster. Currently in **design / pre-production**, with no code yet.

## Files
- `GDD.md`: the living Game Design Document and the single source of truth for the design. Read it before any design discussion.
- `GameDesignSessions/`: one summary per design session, named `yyyy-mm-dd-s#.md`, where `#` is the session's number **within that day** (first session of the day is `s1`, the second `s2`, and so on). Count from the dates in the GDD changelog.
- `.claude/skills/game-design-session/`: the procedure for starting and ending a design session.

## About me
- New to game design, no formal background. Explain any jargon the first time it comes up, with a short example from a well-known game.
- Solo. 3–4 h on workdays, 5+ h on weekends. Lots of coding experience.
- Target platform: PC and/or web. Engine: undecided.

## How to work with me
- This is mainly for brainstorming. When I bring an idea, give 2–3 distinct directions with their trade-offs, not one answer.
- Be honest. Push back if an idea is vague, derivative, or too big for my resources. Don't just validate.
- Ask at most one or two clarifying questions at a time.
- Keep scope realistic for a first game. Flag anything that would take a large team or years.
- Don't jump to code or engine specifics unless I ask. Design first.

## Design sessions
- A session starts when I say something like **"Starting game design session"** and ends only when I say **"End game design session"**. Follow the `game-design-session` skill for both.
- **Version bumps happen once per session, at the end.** Never bump the GDD version mid-session, however many decisions we make.
- At the end of a session: bump the version, finalize the changelog row, write the summary to `GameDesignSessions/yyyy-mm-dd-s#.md`, and tell me what changed in the GDD.

## Keeping the GDD
- When I make a decision, update `GDD.md` straight away: change the item's status tag and add it to the session's pending changelog row. Don't bump the version (see above).
- Status tags: [DECIDED] (my call), [TENTATIVE] (leaning, needs playtest), [PROPOSED] (your suggestion, not yet accepted), [OPEN], [DEFERRED]. Never mark your own suggestion as [DECIDED].
- Don't silently resolve contradictions. Flag them with ⚠ in the GDD and ask.
- Commit GDD changes locally as we go. Push only when I ask.
