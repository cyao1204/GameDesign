---
name: playtest-session
description: Record an Elemental Affliction playtest. Use when Chris says "Starting playtest session", "log this playtest", or brings notes from a paper or digital playtest. Checks each experience goal and risk trigger, sorts every finding (design / balance / clarity / bug), writes docs/playtests/P#-yyyy-mm-dd.md and updates docs/playtests/findings.md. Does NOT change GDD rules; findings feed the next design session.
---

# Playtest session

A playtest session turns what happened at the table into a durable record. It doesn't fix or redesign
anything: rule changes happen in a design session, which reads the findings marked **New**.

Why this exists: game teams find fun and balance mainly by playing, and the most common fix for "lack of fun" is
more playtesting (`docs/design/process-research.md`, BP2).

## Steps (in order)

1. **Collect** from Chris, one or two questions at a time:
   - GDD version played (from the `docs/GDD.md` header) and any house rules used.
   - Format: paper or digital, number of matches, who played, element pairing, spells per turn, active slots.
   - What happened: match lengths in turns, who won and how, moments that stood out. Raw notes are fine.
2. **Experience goals.** For each goal in GDD §2.1, answer its playtest question with evidence from the matches.
   If a goal is still [OPEN] or [PROPOSED], check the candidate anyway and say so.
3. **Risk triggers.** Go through the GDD §9 risk register. For each risk, say whether its trigger fired, with evidence.
4. **Sort each finding** into one category:
   - **Design:** a rule doesn't create the intended experience, or a dominant strategy appeared.
   - **Balance:** the rule is fine but a number is off (damage, affliction, cooldown, health).
   - **Clarity:** players misread or forgot a rule, or it was hard to teach.
   - **Bug:** the prototype didn't follow the GDD (digital prototypes only).
5. **Check each finding:**
   - Is it already addressed by a later GDD change? If so, mark it **Stale**.
   - Was it seen once or repeated? One observation is a lead, not a verdict. Say which.
   - Link it to the GDD section, `Q-###` or risk it touches.
6. **Write the report** to `docs/playtests/P#-yyyy-mm-dd.md` (template below). `#` is the next playtest number
   overall: the highest `P#` in `docs/playtests/`, plus 1.
7. **Update the tracker** `docs/playtests/findings.md`: add one row per finding with the next free `F-###` ID and
   status **New**.
8. **Commit:** `docs: playtest P# - <one-line summary> [GDD @ vA.B]`. Don't push unless asked.
9. **Tell Chris** the top three findings, which goals held up, which triggers fired, and what the next design
   session should start with.

## Rules

- Never edit GDD rules in a playtest session. A finding that needs a new open question is listed as such; the
  design session adds the `Q-###`.
- Use the exact words in the GDD glossary.
- Record what happened, then what it might mean. Keep the two apart.

## Tracker statuses (`findings.md`)

| Status | Meaning |
|---|---|
| New | Recorded, not yet discussed in a design session. |
| Accepted | A design session decided to act; note the GDD change or `Q-###`. |
| Rejected | Discussed and not acted on; note why. |
| Stale | Already covered by a later GDD change. |
| Fixed | Prototype bug fixed (bugs only). |

A design session that acts on a finding updates its row in the same commit as the GDD change.

## Report template

```markdown
# Playtest P# — yyyy-mm-dd

GDD: vA.B · Format: paper / digital · Matches: N · Players: …
Setup: elements …, spells per turn …, active slots …, house rules …

## What happened
- Match 1: … turns, winner …, how …
- Notable moments.

## Experience goals (GDD §2.1)
| Goal | Held up? | Evidence |
|---|---|---|

## Risk triggers (GDD §9)
| Risk | Fired? | Evidence |
|---|---|---|

## Findings
| ID | Category | Finding | Seen | Links |
|---|---|---|---|---|
| F-### | Design / Balance / Clarity / Bug | … | once / repeated | §x.y, Q-###, risk |

## For the next design session
- Top questions to start with.
```
