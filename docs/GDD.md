# Elemental Affliction — Game Design Document

*Working title. Living document: update it whenever a decision is made.*

| | |
|---|---|
| **Designer** | Chris (solo, building with Claude) |
| **Last updated** | 2026-10-31 (session 5, in progress) |
| **Phase** | End of concept → starting pre-production (prototyping) |
| **Version** | 0.4 (0.5 pending: bumped at the end of session 5) |

**How to read this doc.** Every rule is tagged with its status:

- **[DECIDED]**: Chris has made the call. Change it only on purpose, and log the change in the changelog.
- **[TENTATIVE]**: leaning this way, to be confirmed by playtesting.
- **[PROPOSED]**: suggested by Claude, not yet accepted by Chris.
- **[OPEN]**: not decided. Each one has a stable ID (`Q-###`) listed in §10, and the ID is cited next to the tag.
- **[DEFERRED]**: deliberately postponed until later.

All numbers are placeholders until playtesting, unless marked otherwise.

**Terms.** The glossary (appendix) is the official word list. Use its exact terms in this doc, session summaries, commits and, later, code. A new term is added to the glossary before it is used.

**Checks.** `tools/check_gdd.py` checks this file's tags, version header, changelog and `Q-###` IDs. It runs on every commit (see `CLAUDE.md`).

---

## 1. Elevator pitch

A one-on-one fantasy card duel where **magic harms the caster**. There is no mana: every spell you cast afflicts your own body with its element. Afflictions make you stronger and can transform you, but they push you toward death. You win by mastering how much your body can take, and by reading how much your opponent's can.

It's a **push-your-luck** game: the player chooses how much risk to take, as in Blackjack.

## 2. Design pillars

Pillars are short statements that define the game. Every new feature is checked against them.

1. **[DECIDED]** *Affliction is the cost of casting spells. Mastering it is how you win.*
   Test: if you removed afflictions, there should be no game left.
2. **[PROPOSED]** *Read your opponent.* Deducing their hidden health and spellbook is a core skill.
3. **[PROPOSED]** *Every turn is a push-your-luck bet.*

> Target: 3–4 pillars before production. Session 1 proposed "Every spell costs your body; winning means mastering how much you can take." It was superseded by pillar 1.

### 2.1 Experience goals

An **experience goal** is the feeling a pillar should create in the player. It's the "Aesthetics" in MDA (see glossary): you pick the feeling first, then check that the rules produce it. Example: *Slay the Spire* aims for "tense, informed risk" on every card choice. Each playtest checks every goal (`docs/playtests/`).

**[OPEN]** (Q-013) Which goals to commit to. Candidates, all **[PROPOSED]**:

| Pillar | Experience goal (candidate) | Playtest question |
|---|---|---|
| 1. Affliction is the cost | **Tension:** every cast feels like it costs something. | Did the player ever hold back a spell because of affliction? |
| 2. Read your opponent | **Insight:** the satisfaction of guessing hidden health or spells correctly. | Did the player make a call based on a read, and say why? |
| 3. Push-your-luck bet | **Thrill of the gamble:** pushing into Charged or Overloaded feels risky and exciting, not forced. | Did the player choose to enter a high zone, and did it feel worth it? |

## 3. Designer constraints

- **Team:** solo with Claude's help. Strong coding experience, new to game design.
- **Time:** 3–4 h on workdays, 5+ h on weekends. Target is about 6 months, flexible.
- **Platform:** PC and/or web. **Engine:** [OPEN] (Q-014).
- **Inspirations:** card games (Magic: The Gathering, Hearthstone, Riftbound), RTS (StarCraft, Warcraft, Command & Conquer, Age of Wonders), RPGs.
- **What I enjoy most:** outmaneuvering an opponent 1v1, discovering card interactions and building decks, combining planning with combat.

## 4. Format and setting

- **[DECIDED]** Fantasy setting.
- **[DECIDED]** Format: one-on-one card duel. Tactics (grid) was dropped in session 2.
- **[DEFERRED]** Side-scroller, as a possible later project. Out of scope for a solo dev at about 6 months.
- **[TENTATIVE]** Opponent: AI first, built so PvP could be added later (session 1 plan). Final choice is still [OPEN] (Q-010).

## 5. Core mechanics

### 5.1 Casting

- **[DECIDED]** No mana or other casting resource.
- **[DECIDED]** Every cast adds affliction of the spell's element to the caster, whatever else the spell does.
- **[DECIDED]** The affliction a spell adds **scales with its power** (session 4). Stronger spells cost more affliction **and** have longer cooldowns.
- **[DECIDED]** Spells deal health damage directly.
- **[DECIDED]** After a cast, the spell goes on **cooldown** (a wait of one or more turns before it can be used again, like abilities in *Overwatch*).
- **[DECIDED]** Cap on spells per turn: **2 or 3** (session 4). Exact value [TENTATIVE], to tune in playtesting.
- **[DECIDED]** The cap is "up to N" (session 4): casting fewer spells means less affliction, which makes how many to cast each turn part of the push-your-luck bet.
- **[DECIDED]** **Resting** (session 4): leaving a slot empty lowers the cooldown of another spell of the player's choice. Resting does **not** lower affliction, which stays element-only (§5.3); its affliction benefit is simply not casting. *Replaces the earlier idea that resting lowers affliction, which conflicted with §5.3.*
  - **[DECIDED]** Each empty slot takes **1 turn** off one spell's cooldown. Slots stack: resting 2 slots in one turn can take 2 turns off the same spell.
  - **[DECIDED]** Stronger spells have cooldowns longer than 1 turn. This stops a rest-and-recast loop on the strongest spell, and it makes resting over several turns, or resting several slots at once, a strategic choice at the cost of casting fewer spells.
  - Watch: there's some overlap with overcasting (below). Both get around cooldowns, so they should feel different.
- **[OPEN]** (Q-015) **Overcasting** (casting a spell before its cooldown ends) is not defined yet and can be changed (reopened in session 4). Idea so far: it belongs to one element only, for example lightning.
- Consequence: multiple casts let a player defend and attack in the same turn, which eases the rock-paper-scissors concern in §5.5. Affliction builds 2–3× faster per turn, so the per-spell affliction and the active-slot count must allow for it.

### 5.2 Health

- **[DECIDED]** Health and affliction are separate meters. Health at 0 loses the match.
- **[DECIDED]** Health is hidden from the opponent.
- **[DECIDED]** **Open information is deliberately scarce** (session 4). Public: each player's **affliction meters**, and **every spell that has been cast**, by either player, whoever it targets. Everything else, including health, the reserve and uncast spells, is hidden.
- **[DECIDED]** Health and spellbook size share one pool: more spells means less starting health, and vice versa.
- **[DECIDED]** Fixed rate (session 4): **starting health = total pool − number of spells in the spellbook**, counting active **and** reserve spells. Every spell costs the same health. Example: 8 spells (6 active, 2 reserve) gives pool − 8; 6 spells (all active) gives pool − 6.
  - Why a fixed rate works: strong spells are already priced by longer cooldowns and higher affliction (§5.1), so health doesn't also need to vary per spell. It also keeps deduction simple: each revealed spell lowers the cap on the opponent's possible health.
  - **[OPEN]** (Q-016) Pool size, and health cost per spell (the example uses 1).
- Affliction can be managed; health is harder to recover.

### 5.3 Affliction

- **[DECIDED]** One affliction meter per element. At most two elements per player.
- **[DECIDED]** High affliction empowers or transforms the caster and can unlock spells.
- **[DECIDED, may change]** Past a threshold, affliction grows on its own every turn **and** costs health every turn ("burn while high").
  - Backup if matches feel slow or predictable: **burnout**. Hitting max affliction costs a big chunk of health, then resets the meter and ends any transformation (like an overheated weapon in *Halo*).
- **[DECIDED]** Raising, lowering and transferring affliction are abilities of certain elements, not universal.
- **[DECIDED]** Transfer is limited to a few elements and is not a central theme. *(Supersedes session 1's "transfer is part of the core.")*
- **[DECIDED]** Transferred affliction raises one of the target's existing element meters.
- **[DEFERRED]** Which meter it raises when the target has two elements (session 4). Deferred along with Chaos, which likely owns transfer.
- **[DECIDED]** **Zone boundaries are fixed and the same for everyone** (session 4, for the prototype). Both players know exactly what a meter value means.
  - Rejected: boundaries as a share of each player's hidden health. With public meters, this would reveal hidden health the moment someone crossed a boundary.
  - **[DEFERRED]** Elements shifting their own boundaries (for example, a wider Calm zone for the Defensive element, or odd zones for Chaos). A later tool for element personality.
- **[DECIDED]** **Affliction meters are public** (session 4). They are among the few pieces of open information in the game (see §5.2). A Charged opponent visibly threatens a finisher, and burn damage from Overloaded is visible, so it helps deduce hidden health.

**Meter and zones** (session 4)
- **[DECIDED]** Each meter runs **0–20**. Spells add roughly **1–4**, scaled by power (§5.1). Exact numbers [TENTATIVE].
- **[DECIDED]** The meter has three **zones** instead of a single threshold:

  | Zone | Rough range | Effect |
  |---|---|---|
  | **Calm** | 0 to about 7 | No effect. |
  | **Charged** | about 8 to 13 | Empowerment: stronger spells or new options. The reward for taking the risk. |
  | **Overloaded** | about 14 to 20 | Empowerment continues, plus affliction grows by itself each turn and burns health (the "burn while high" rule above). |

  Zone boundaries are [TENTATIVE].
- **[DECIDED]** (session 5) Check pacing with a quick script before paper playtesting: casts per turn × affliction per spell against the 8–12 turn target, plus the Overloaded "death clock". Built once the starter spells have first-pass numbers (process item P-10 in `docs/design/process-research.md`).

**Element afflictions (examples from session 1, not final; Fire and Frost are no longer the starter pair, see §6):**
- Fire: builds heat that burns you every turn.
- Frost: numbs you and makes spells harder to cast.
- Lightning: makes your hands shake.
- Transformation example: a frost-saturated mage can't move but freezes everything nearby.

### 5.4 Spellbook

**Terms** (session 4): the **spellbook** is every spell a player brings. **Active** spells are in the active slots and usable from turn one. **Reserve** spells are the rest, hidden until swapped in. *Earlier versions said "prepared spells" for the active loadout; that word is dropped because it was being used for both meanings.*

- **[DECIDED]** No card draw.
- **[DECIDED]** **Active spells** are the starting loadout, all available from turn one.
- **[DECIDED]** A **hidden reserve** holds more spells that can be swapped in during the match.
- **[DECIDED]** **Deckbuilding room** (session 4): fewer slots now, more spells later.
  - **Prototype:** 8 spells per element, **4–5 active slots** (exact count [TENTATIVE], to tune).
  - **Full game:** grow to **12 or more spells per element** for real deckbuilding depth.
  - Why: with 6 active slots and 8 spells, a mono-element book leaves only 2 spells out. The prototype tests the core duel, not deckbuilding depth, and mixing two elements already gives 16 spells to choose from.
  - Tuning lever: the ratio of **active slots to casts per turn** sets how often a player must rest. Start testing at 2 casts per turn with 4–5 active slots.
- **[DECIDED]** Deckbuilding is restricted by element (at most two) and by how many active slots there are.
- **[DECIDED]** Opponents see only spells that have been cast, but they see **all** of them, self-targeted spells included (confirmed in session 4).
- **[DEFERRED]** Swap cost. Candidate: the player chooses each time. Either swap free and the spell arrives on cooldown, or give up this turn's cast and it arrives ready.
- **[DEFERRED]** Minimum and maximum spellbook size.
- **[OPEN]** (Q-017) Swap triggers (after N turns, conditions, or spells).

### 5.5 Turn structure

- **[TENTATIVE]** **Secret choice, resolved by speed category** (session 4). Both players pick in secret, then reveal. Spells resolve in category order, not by a per-spell speed number:
  1. **Defensive** (fastest): cast on yourself, so they don't need to travel. Both players' defensive spells resolve together and don't interact with each other.
  2. **Offensive** (slowest): always resolve last. If both players cast offensive spells, they resolve at the same time and don't interact with each other.
- **[DECIDED]** Speed is set by **target** (session 4): a spell targeting yourself is fast (defensive step), a spell targeting the opponent is slow (offensive step). No separate utility category is needed. A self-cleanse is fast; transfer and debuffs are slow. *Watch:* a fast cleanse can escape a burn before the enemy's attack lands. That could be good drama or too safe.
- **[DECIDED]** Test only the simultaneous (speed-category) structure. **Alternating** turns are dropped, since spells for them would be designed completely differently.
- Resolved ⚠ from session 2 (sequential vs. simultaneous): the speed-category hybrid replaces both pure options.
- Consequence: defence beats offence on timing, so classic reactive spells (reflect, counter) can work as fast defensive spells. Guessing wrong still costs you the turn plus the affliction.
- Watch: each turn could shrink to "attack or defend?" (close to rock-paper-scissors). Casting 2–3 spells per turn (§5.1) and varied defensive options should prevent this.
- **[DECIDED]** **Both players reach 0 health on the same turn** (session 4): the player with **lower total affliction** wins, since the mage who controlled their magic survives. A draw happens only if total affliction is also tied. Because meters are public, players can see a near-tie coming.
  - Watch: this slightly favours the Defensive element, which can lower its affliction. Fallback if playtests show that bias: the player with more health left (least far below 0) wins.

## 6. Elements

- **[DEFERRED]** Roster and themes. Each element has a **personality** (for example, fire is aggressive and reckless) and can touch more than one affliction role while staying in character.
- Trade-off built into deckbuilding: **one element** fills one meter fast (quick empowerment, quick burnout). **Two elements** spread affliction (safer, slower to empower).
- Prototype needs: 2 elements with 6–8 spells each.
- **[DECIDED]** The two starter elements are **one offensive-oriented and one defensive-oriented element** (session 4). Fire + Frost was rejected as too cliché.
- **[DEFERRED]** Element names. Placeholders for now: **Offensive element** and **Defensive element**.
- **[DECIDED]** **Chaos** is the third element, after the starter pair (session 4). It replaces the Shadow/information idea. Name may change.
  - **[DECIDED]** Direction: **rule-breaking**. Chaos bends the game's normal rules.
  - **[DEFERRED]** Candidate ideas, to explore after the starter pair works: Chaos is the element that owns affliction **transfer**; spells that push affliction to the maximum and then spend it as fuel; a **death-defying** mechanic.
  - Watch: rule-breaking elements are the hardest to balance and to teach. Each exception adds to the complexity budget (§9).
- **[DECIDED]** Elements differ by their **mix of spell roles**, not by which roles they're allowed (session 4). A defensive element still has damage spells; it just has fewer of them.
- **Spell roles:** *attack* (damages the opponent), *defensive* (protects the caster), *utility* (anything else, such as cleansing, cooldown tricks or transfer). These are **roles, not speed categories**: speed still comes only from the target (§5.5). For example, a self-cleanse is a fast utility spell and a transfer is a slow one.
- **[TENTATIVE]** Example mixes for 8-spell elements:

  | Element | Attack | Defensive | Utility |
  |---|---|---|---|
  | Offensive | 6 | 0 | 2 |
  | Defensive | 3 | 3 | 2 |

- Consequences:
  - A mono-Offensive player has no protection except utility and resting. That makes it a pure race, and it gives players a reason to pair it with a second element. This supports the one-vs-two element trade-off above.
  - With only 3 attack spells, the Defensive element's attacks may need to hit harder, cost less affliction or have shorter cooldowns to threaten a kill. To be tuned.
- **[DECIDED]** The **Offensive element can never lower its own affliction** (session 4). In return, it gets **significant rewards for high affliction**: spells that are empowered, or only castable, in the Charged or Overloaded zones (§5.3).
  - **[DECIDED]** The reward is a **mix, led by unlocks**:
    1. **Main: unlocked spells.** Finishers that can only be cast while Charged or higher.
    2. **Empowered spells.** Some spells deal more damage at high affliction.
    3. **Overloaded transformation.** Reaching Overloaded unlocks extra effects, or changes the player's play style dramatically.
  - Watch: the transformation is the most expensive part to build and the most likely to be cut (§9). For the prototype, consider at most one simple transformation, or leave it out until finishers and empowerment have been tested.
  - Consequence: a mono-Offensive player is on a **death clock**. Once Overloaded, affliction keeps rising and burning even while resting, so they must win before it runs out. Their hidden health means the opponent can't be sure exactly when that is.
  - Watch: the Defensive player's best plan may become "outlast the clock." Check that this doesn't become dull turtling. Defensive casts also add affliction, which should help.
- Watch: an offensive/defensive split has the same structure as fire/frost. Freshness has to come from each element's **affliction effect** and transformation, not from its name.

| Element | Personality | Affliction effect | Special role | Status |
|---|---|---|---|---|
| Offensive (placeholder) | Aggressive (about 6 attack / 0 defensive / 2 utility) | [OPEN] (Q-018) | Can't lower its own affliction; big rewards at high affliction | starter, decided |
| Defensive (placeholder) | Defensive (about 3 attack / 3 defensive / 2 utility) | [OPEN] (Q-018) | Likely the element that can lower affliction | starter, decided |
| Chaos | Rule-breaking | [DEFERRED] | Transfer? Max-affliction fuel? Death-defying? | third element, decided |
| Lightning | — | Shaking hands | Overcasting? | session 1 example |

## 7. Core loop (draft)

A **core loop** is the cycle of actions players repeat (in *Slay the Spire*: fight → pick a reward → choose the next room).

**Each turn**
1. Choose a spell (in secret, if simultaneous).
2. Cast: apply its effect and gain affliction of its element.
3. Reveal and resolve: defensive spells first, then offensive spells (each category resolves together).
4. Affliction check: passive growth and health loss above the threshold, plus empowerment or unlocks.
5. Cooldowns tick down, and swap options open.

**Match length**
- **[TENTATIVE]** Target: 8–12 turns, about 15 minutes (session 4). With 2–3 casts per turn, that means 16–36 casts per player, so affliction per spell must be small enough to last.
- **[DEFERRED]** Shape pacing by **phases** instead of a fixed count: probing, then escalation, then a decisive peak, driven by when players cross the threshold. Revisit once the affliction numbers exist.

**Between matches**
Build a spellbook (choose elements, weigh spell count against health) → duel → adjust the book → repeat.

**Outer loop:** [OPEN] (Q-011). Matches only, or a campaign or run around them. This is the biggest scope decision left.

## 8. Comparable games

| Game | What it shares | How we differ |
|---|---|---|
| *Mage Wars* | Full-access spellbook, school restrictions, point-budget building | It uses mana; ours has affliction instead |
| *Wizards of the Grimoire* | Cooldowns, swapping spells | No body cost or hidden health |
| *The Witcher 3* | Toxicity from potions hurts you | A side system there; the core here |
| *MechWarrior / BattleTech* | Heat builds up and punishes overuse | Not a card duel; heat isn't also power |
| *Hearthstone* (Overload), *MTG* (Phyrexian mana), *Darkest Dungeon* (afflictions) | A cost or affliction that echoes ours | Side mechanics, not the core |

**Most original rule:** hidden health set by spellbook size, deduced as spells are revealed. No precedent found.
**Risk:** players summing it up in five minutes as "Wizards of the Grimoire with Witcher toxicity." The distinctive parts must show up from the first turn.

## 9. Risks and watch-list

A **risk register**: each risk has the current answer (mitigation) and a **trigger**, the sign that it is actually happening and needs action. Review it at the start of each phase. Triggers are **[PROPOSED]** (session 5).

| Risk | What could go wrong | Mitigation (current answer) | Trigger (act when…) |
|---|---|---|---|
| **Solved game** | With no draw, players find one best opening (a **rotation**) and repeat it. | Hidden health, the hidden reserve, simultaneous play. | Playtests or the simulation show one opening winning most matches. |
| **Death spiral** | Falling behind keeps making you fall further behind. Passive growth plus health loss could decide matches early. | Ways to reduce affliction must be able to pull a player back, and high-affliction rewards must be worth the risk. | The player who is behind early almost never wins. |
| **Pillar drift** | Spells deal damage directly, so the game could become a plain damage race with an affliction tax. | Playtest check: *does a player ever cast a weaker spell because of affliction?* (experience goal "Tension", §2.1). | The answer is "no" in two playtests in a row. |
| **Hidden health feedback** | Hitting someone without seeing the result can feel hollow. | Test signals such as visible wounds or rough health bands. | Playtesters say hits feel empty, or can't tell who is winning. |
| **Flat spell cost** | Every spell costs the same health, so players always take the strongest spells. | *Session 4:* strong spells pay with longer cooldowns and more affliction. Still to check: an all-strong book may have everything on cooldown, and resting must not erase cooldowns too cheaply. | One kind of spellbook (all strong, or all weak) wins most matches. |
| **Complexity budget** | Meters, thresholds, passive growth, empowerment, unlocks, transformations, cooldowns, swaps, overcasting and hidden health is a lot for a first game. | Expect to cut about a third after prototyping. A scope freeze before prototype code (process item P-25). | A new player can't play a match after a 5-minute explanation. |
| **Scope of the opponent** | A good AI for a hidden-information game is hard to build. PvP needs networking and a player base. | AI first, built so PvP can be added later (§4). Decided in Q-010. | Before development starts. |
| **Brainstorm drift** | Too many decisions made on paper before anything has been played. | Paper prototype next (§11). After it, design sessions start from playtest findings. | Two more design sessions pass with no playtest. |
| **Solo obstacles** | Small teams hit obstacles about twice as often as large ones (postmortem study S2 in `docs/design/process-research.md`). | This register, reviewed at each phase start; checks instead of memory (`tools/check_gdd.py`). | Any trigger above fires. |

## 10. Open questions

Every open question has a stable ID. IDs are never reused or renumbered. Cite them in the doc (next to the [OPEN] tag), in session summaries and in commits. **Never resolve a `Q-###` silently:** ask Chris, then record the answer here.

| ID | Question | Needed by | Status |
|---|---|---|---|
| Q-001 | Turn structure | Prototype | Resolved (session 4): secret choice resolved by speed category, speed set by target. Alternating dropped. |
| Q-002 | Two starter elements and their 6–8 spells each | Prototype | Open. Archetypes decided (one Offensive, one Defensive); roles and spells still open. |
| Q-003 | Affliction numbers: threshold, growth rate, health cost per turn, at least one way to reduce affliction | Prototype | Open. Decided so far: affliction per cast scales with spell power; 0–20 meter with Calm / Charged / Overloaded zones; the Offensive element can't lower its own affliction. Still open: exact numbers and the Defensive element's reduction spells. |
| Q-004 | Threshold placement | Prototype | Resolved (session 4): fixed boundaries, the same for everyone. Element-shifted boundaries deferred. |
| Q-005 | Spells per turn | Prototype | Resolved (session 4): up to 2–3, exact value to tune; empty slots rest. |
| Q-006 | Health vs. spellbook-size formula | Prototype | Resolved (session 4): health = pool − all spells (active + reserve), fixed rate. Pool size is Q-016; min/max book size deferred (§5.4). |
| Q-007 | Deckbuilding room | Prototype | Resolved (session 4): 8 spells per element and 4–5 active slots in the prototype; 12+ per element for the full game. |
| Q-008 | Target match length | Prototype | Resolved (session 4): 8–12 turns, TENTATIVE. Phase-based shaping deferred. |
| Q-009 | Simultaneous 0-health outcome | Prototype | Resolved (session 4): lower total affliction wins, then a draw. |
| Q-010 | Opponent: AI, local hot-seat, or online PvP | Development | Open. |
| Q-011 | Outer loop: matches only, or campaign/run | Development | Open. The biggest scope decision left. |
| Q-012 | Pillars 2–3: confirm or replace the proposed ones | Development | Open. |
| Q-013 | Experience goals per pillar (§2.1) | First paper playtest | Open (session 5). Candidates proposed. |
| Q-014 | Engine | Development | Open. 💡 **[PROPOSED]** (session 5): move to "before the digital prototype", since changing tools during production is costly (BP8 in `docs/design/process-research.md`). |
| Q-015 | Overcasting: what it is and which element owns it (§5.1) | Not blocking | Open (reopened in session 4). |
| Q-016 | Health pool size and health cost per spell (§5.2) | Prototype | Open. |
| Q-017 | Swap triggers (§5.4) | Not blocking | Open. Reserve and swaps are out of the first prototype. |
| Q-018 | Each starter element's affliction effect (§6) | Prototype | Open. Needed together with Q-002. |

**Deferred** (not questions yet)
- Defensive spells, full element roster, swap cost and triggers, transformations beyond one example, progression, art, audio.
- Chaos element design, and which meter transferred affliction enters (session 4).

## 11. Next steps

- [ ] Design the starter spells (Q-002, Q-018): 8 per element (Offensive about 6/0/2, Defensive about 3/3/2), each with affliction cost, cooldown and effect. Include 1–2 Offensive finishers.
- [ ] Set first-pass numbers (Q-003, Q-016): health pool, zone boundaries, Overloaded growth and burn.
- [ ] Pacing script against the 8–12 turn target, once the numbers above exist (P-10).
- [ ] Decide the experience goals (Q-013) before the first playtest.
- [ ] Paper prototype (or throwaway digital one) of the core duel: cast, cooldown, affliction, hidden health. No reserve or swaps yet.
- [ ] Play it with speed-category resolution, at 2 and at 3 spells per turn. Run each playtest with the `playtest-session` skill and log it in `docs/playtests/`.
- [ ] Watch or play *Mage Wars* and *Wizards of the Grimoire* (on Board Game Arena).
- [ ] Decide opponent type (Q-010) and outer loop (Q-011).
- [ ] At each new phase, do the process items whose trigger has been reached (§5 of `docs/design/process-research.md`).

## 12. Changelog

| Version | Date | Session | Changes |
|---|---|---|---|
| 0.1 | 2026-10-25 | 1 | Concept: magic harms the caster, no mana, empowerment and transformation, transfer. Fantasy setting. "Body is the board" dropped. Side-scroller deferred. |
| 0.2 | 2026-10-29 | 2 | Format: card duel (tactics dropped). Pillar 1 decided. Cooldowns, spell cap, no draw, prepared spells plus hidden reserve. Separate health and affliction meters, one meter per element, max two elements. Threshold growth and burn. Direct damage. Transfer demoted from core. Hidden health tied to spellbook size. Simultaneous play tentative. Draft core loop. |
| 0.3 | 2026-10-30 | 3 | Consolidated into this living GDD. Added proposed pillars 2–3, the turn-structure inconsistency flag, hidden-health feedback and opponent-scope risks, and the pre-prototype vs. pre-development question split. No new decisions. |
| 0.4 | 2026-10-30 | 4 | Answered the pre-prototype questions. Turn structure: secret choice, self-targeted spells resolve first and opponent-targeted last (tentative); alternating dropped; resolves the session-2 ⚠. Up to 2–3 spells per turn; an empty slot takes 1 turn off a chosen spell's cooldown; stronger spells have longer cooldowns and cost more affliction. Match length 8–12 turns (tentative). Starter elements: one Offensive (6/0/2 mix, can't lower its own affliction, rewarded with finishers, empowerment and an Overloaded transformation) and one Defensive (3/3/2); placeholder names; Fire + Frost rejected. Chaos is the rule-breaking third element (deferred). Health = pool − all spells in the book; terms changed to spellbook / active / reserve; prototype at 8 spells per element and 4–5 active slots. Affliction meter 0–20 with fixed Calm / Charged / Overloaded zones; meters and all cast spells are public. Double knockout: lower total affliction wins. Overcasting reopened; transfer-meter question deferred. Version is now bumped once per session. |
| 0.5 (pending) | 2026-10-31 | 5 | In progress. Process setup, no rule changes: moved files to `docs/`; open questions get stable IDs (Q-001 to Q-018), with Q-013 experience goals, Q-015 overcasting, Q-016 health pool, Q-017 swap triggers and Q-018 element affliction effects newly listed; glossary is now the official term registry, with game terms added; experience goals per pillar added (§2.1, proposed); §9 is a risk register with mitigation and trigger (triggers proposed); pacing check decided, built after the starter spells (P-10); Q-014 proposed to move earlier; research record in `docs/design/process-research.md`. |

## Appendix: glossary (term registry)

The official word list (see "Terms" at the top). Use these exact words; no synonyms. Game terms first, then design jargon.

**Game terms**
- **Active spells:** the spells in a player's active slots, usable from turn one (§5.4).
- **Affliction:** the cost of casting. Each cast adds affliction of the spell's element to the caster (§5.3).
- **Affliction meter:** one per element, 0–20, public (§5.3).
- **Burn:** health lost each turn while Overloaded (§5.3).
- **Calm / Charged / Overloaded:** the three zones of an affliction meter (§5.3).
- **Death clock:** a mono-Offensive player's limited time once Overloaded, since affliction keeps rising and burning (§6).
- **Finisher:** an Offensive spell that can only be cast while Charged or higher (§6).
- **Overcasting:** casting a spell before its cooldown ends. Not defined yet (Q-015).
- **Reserve:** spells in the spellbook but not in the active slots, hidden until swapped in (§5.4).
- **Resting:** leaving a cast slot empty to take 1 turn off a chosen spell's cooldown (§5.1).
- **Speed category:** when a spell resolves. Self-targeted spells are *defensive* (fast); opponent-targeted spells are *offensive* (slow) (§5.5).
- **Spell roles:** attack, defensive, utility. Roles are not speed categories (§6).
- **Spellbook:** every spell a player brings, active and reserve (§5.4).
- **Swap:** moving a reserve spell into an active slot (§5.4).

**Design jargon**
- **Cooldown:** turns a spell must wait before reuse (*Overwatch* abilities).
- **Core loop:** the repeated cycle of play (*Tetris*: rotate, place, clear lines).
- **Death spiral:** falling behind makes you fall further behind (*Monopoly*).
- **Design pillar:** a short statement that defines the game and filters features.
- **Experience goal:** the feeling a pillar should create in the player; the "Aesthetics" of MDA (§2.1).
- **MDA:** Mechanics (rules) → Dynamics (behavior) → Aesthetics (feelings).
- **Pre-production:** the phase of cheap prototypes to "find the fun" before building the real game.
- **Push-your-luck:** you choose how much risk to take (Blackjack).
- **Risk register:** a list of risks, each with a mitigation and a trigger for action (§9).
- **Rotation:** a fixed, always-optimal ability order (MMOs).
- **Tell:** an unintended signal that gives away hidden information (poker).
- **Yomi:** "reading the mind"; predicting what the opponent will choose (*Street Fighter* mind games).
