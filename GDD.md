# Elemental Affliction — Game Design Document

*Working title. Living document: update it whenever a decision is made.*

| | |
|---|---|
| **Designer** | Chris (solo, building with Claude) |
| **Last updated** | 2026-10-30 (session 4, in progress) |
| **Phase** | End of concept → starting pre-production (prototyping) |
| **Version** | 0.3 (0.4 pending: bumped at the end of session 4) |

**How to read this doc.** Every rule is tagged with its status:

- **[DECIDED]**: Chris has made the call. Change it only on purpose, and log the change in the changelog.
- **[TENTATIVE]**: leaning this way, to be confirmed by playtesting.
- **[PROPOSED]**: suggested by Claude, not yet accepted by Chris.
- **[OPEN]**: not decided. Listed in §10.
- **[DEFERRED]**: deliberately postponed until later.

All numbers are placeholders until playtesting, unless marked otherwise.

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

## 3. Designer constraints

- **Team:** solo with Claude's help. Strong coding experience, new to game design.
- **Time:** 3–4 h on workdays, 5+ h on weekends. Target is about 6 months, flexible.
- **Platform:** PC and/or web. **Engine:** [OPEN].
- **Inspirations:** card games (Magic: The Gathering, Hearthstone, Riftbound), RTS (StarCraft, Warcraft, Command & Conquer, Age of Wonders), RPGs.
- **What I enjoy most:** outmaneuvering an opponent 1v1, discovering card interactions and building decks, combining planning with combat.

## 4. Format and setting

- **[DECIDED]** Fantasy setting.
- **[DECIDED]** Format: one-on-one card duel. Tactics (grid) was dropped in session 2.
- **[DEFERRED]** Side-scroller, as a possible later project. Out of scope for a solo dev at about 6 months.
- **[TENTATIVE]** Opponent: AI first, built so PvP could be added later (session 1 plan). Final choice is still [OPEN] (§10).

## 5. Core mechanics

### 5.1 Casting

- **[DECIDED]** No mana or other casting resource.
- **[DECIDED]** Every cast adds affliction of the spell's element to the caster, whatever else the spell does.
- **[DECIDED]** Spells deal health damage directly.
- **[DECIDED]** After a cast, the spell goes on **cooldown** (a wait of one or more turns before it can be used again, like abilities in *Overwatch*).
- **[DECIDED]** Cap on spells per turn: **2 or 3** (session 4). Exact value [TENTATIVE], to tune in playtesting.
- **[DECIDED]** The cap is "up to N" (session 4): casting fewer spells means less affliction, which makes how many to cast each turn part of the push-your-luck bet.
- **[DECIDED]** **Resting** (session 4): leaving a slot empty lowers the cooldown of another spell of the player's choice. Resting does **not** lower affliction, which stays element-only (§5.3); its affliction benefit is simply not casting. *Replaces the earlier idea that resting lowers affliction, which conflicted with §5.3.*
  - **[DECIDED]** Each empty slot takes **1 turn** off one spell's cooldown. Slots stack: resting 2 slots in one turn can take 2 turns off the same spell.
  - **[DECIDED]** Stronger spells have cooldowns longer than 1 turn. This stops a rest-and-recast loop on the strongest spell, and it makes resting over several turns, or resting several slots at once, a strategic choice at the cost of casting fewer spells.
  - Watch: there's some overlap with overcasting (below). Both get around cooldowns, so they should feel different.
- **[OPEN]** **Overcasting** (casting a spell before its cooldown ends) is not defined yet and can be changed (reopened in session 4). Idea so far: it belongs to one element only, for example lightning.
- Consequence: multiple casts let a player defend and attack in the same turn, which eases the rock-paper-scissors concern in §5.5. Affliction builds 2–3× faster per turn, so the per-spell affliction and the prepared-spell count must allow for it.

### 5.2 Health

- **[DECIDED]** Health and affliction are separate meters. Health at 0 loses the match.
- **[DECIDED]** Health is hidden from the opponent.
- **[DECIDED]** Health and spellbook size share one pool: more spells means less starting health, and vice versa.
- Affliction can be managed; health is harder to recover.

### 5.3 Affliction

- **[DECIDED]** One affliction meter per element. At most two elements per player.
- **[DECIDED]** High affliction empowers or transforms the caster and can unlock spells.
- **[DECIDED, may change]** Past a threshold, affliction grows on its own every turn **and** costs health every turn ("burn while high").
  - Backup if matches feel slow or predictable: **burnout**. Hitting max affliction costs a big chunk of health, then resets the meter and ends any transformation (like an overheated weapon in *Halo*).
- **[DECIDED]** Raising, lowering and transferring affliction are abilities of certain elements, not universal.- **[DECIDED]** Transfer is limited to a few elements and is not a central theme. *(Supersedes session 1's "transfer is part of the core.")*
- **[DECIDED]** Transferred affliction raises one of the target's existing element meters.
- **[OPEN]** Threshold placement: a fixed public number, or a share of each player's own limit (which would act as a "tell" about hidden health).

**Element afflictions (examples from session 1, not final):**
- Fire: builds heat that burns you every turn.
- Frost: numbs you and makes spells harder to cast.
- Lightning: makes your hands shake.
- Transformation example: a frost-saturated mage can't move but freezes everything nearby.

### 5.4 Spellbook

- **[DECIDED]** No card draw.
- **[DECIDED]** **Prepared spells** are the starting loadout, all available from turn one.
- **[DECIDED]** A **hidden reserve** holds more spells that can be swapped in during the match.
- **[DECIDED]** Deckbuilding is restricted by element (at most two) and by how many spells can be prepared.
- **[DECIDED]** Opponents see only spells that have been cast.
- **[DEFERRED]** Swap cost. Candidate: the player chooses each time. Either swap free and the spell arrives on cooldown, or give up this turn's cast and it arrives ready.
- **[DEFERRED]** Minimum and maximum spellbook size.
- **[OPEN]** Swap triggers (after N turns, conditions, or spells).

### 5.5 Turn structure

- **[TENTATIVE]** **Secret choice, resolved by speed category** (session 4). Both players pick in secret, then reveal. Spells resolve in category order, not by a per-spell speed number:
  1. **Defensive** (fastest): cast on yourself, so they don't need to travel. Both players' defensive spells resolve together and don't interact with each other.
  2. **Offensive** (slowest): always resolve last. If both players cast offensive spells, they resolve at the same time and don't interact with each other.
- **[DECIDED]** Speed is set by **target** (session 4): a spell targeting yourself is fast (defensive step), a spell targeting the opponent is slow (offensive step). No separate utility category is needed. A self-cleanse is fast; transfer and debuffs are slow. *Watch:* a fast cleanse can escape a burn before the enemy's attack lands. That could be good drama or too safe.
- **[DECIDED]** Test only the simultaneous (speed-category) structure. **Alternating** turns are dropped, since spells for them would be designed completely differently.
- Resolved ⚠ from session 2 (sequential vs. simultaneous): the speed-category hybrid replaces both pure options.
- Consequence: defence beats offence on timing, so classic reactive spells (reflect, counter) can work as fast defensive spells. Guessing wrong still costs you the turn plus the affliction.
- Watch: each turn could shrink to "attack or defend?" (close to rock-paper-scissors). Casting 2–3 spells per turn (§5.1) and varied defensive options should prevent this.
- **[OPEN]** What happens when both players reach 0 health on the same turn (still possible, since offensive spells resolve together).

## 6. Elements

- **[DEFERRED]** Roster and themes. Each element has a **personality** (for example, fire is aggressive and reckless) and can touch more than one affliction role while staying in character.
- Trade-off built into deckbuilding: **one element** fills one meter fast (quick empowerment, quick burnout). **Two elements** spread affliction (safer, slower to empower).
- Prototype needs: 2 elements with 6–8 spells each.

| Element | Personality | Affliction effect | Special role | Status |
|---|---|---|---|---|
| Fire | Aggressive, reckless | Heat burns you each turn | — | example |
| Frost | — | Numbs, makes spells harder | — | example |
| Lightning | — | Shaking hands | Overcasting? | example |

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

**Outer loop:** [OPEN]. Matches only, or a campaign or run around them. This is the biggest scope decision left.

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

- **Solved game.** With no draw, players may find one best opening (a **rotation**) and repeat it. Current answers: hidden health, the hidden reserve, simultaneous play.
- **Death spiral.** Falling behind keeps making you fall further behind. Passive growth plus health loss could decide matches early. Ways to reduce affliction must be able to pull a player back, and high-affliction rewards must be worth the risk.
- **Pillar drift.** Because spells deal damage directly, the game could become a plain damage race with an affliction tax. Playtest check: *does a player ever cast a weaker spell because of affliction?*
- **Hidden health feedback.** Hitting someone without seeing the result can feel hollow. Test whether there's enough signal, such as visible wounds or rough health bands.
- **Flat spell cost.** Every spell costs the same health, so spells must be close in power or players will always take the strongest.
- **Complexity budget.** Meters, thresholds, passive growth, empowerment, unlocks, transformations, cooldowns, swaps, overcasting and hidden health is a lot for a first game. Expect to cut about a third after prototyping.
- **Scope of the opponent.** A good AI for a hidden-information game is hard to build. PvP needs networking and a player base.
- **Brainstorm drift.** Too many decisions made on paper before anything has been played.

## 10. Open questions

**Must answer before prototyping**
- [x] Turn structure: secret choice resolved by speed category, speed set by target (session 4). Alternating dropped.
- [ ] Two starter elements and their 6–8 spells each.
- [ ] Affliction numbers: threshold, growth rate, health cost per turn, at least one way to reduce affliction.
- [ ] Threshold placement: fixed public number or share of own limit.
- [x] Spells per turn: 2 or 3, exact value to tune (session 4).
- [ ] Health vs. spellbook-size formula, with min and max.
- [x] Target match length: 8–12 turns, TENTATIVE (session 4). Phase-based shaping deferred.
- [ ] Which meter transferred affliction enters when the target has two elements (caster's choice, target's choice, or fixed).
- [ ] Simultaneous 0-health outcome.

**Must answer before development**
- [ ] Opponent: AI, local hot-seat, or online PvP.
- [ ] Outer loop: matches only, or campaign/run.
- [ ] Pillars 2–3 (confirm or replace the proposed ones).
- [ ] Engine.

**Deferred**
- Defensive spells, full element roster, swap cost and triggers, transformations beyond one example, progression, art, audio.

## 11. Next steps

- [ ] Answer the "before prototyping" questions in §10.
- [ ] Paper prototype (or throwaway digital one) of the core duel: cast, cooldown, affliction, hidden health. No reserve or swaps yet.
- [ ] Play it with speed-category resolution, at 2 and at 3 spells per turn.
- [ ] Watch or play *Mage Wars* and *Wizards of the Grimoire* (on Board Game Arena).
- [ ] Decide opponent type and outer loop.

## 12. Changelog

| Version | Date | Session | Changes |
|---|---|---|---|
| 0.1 | 2026-10-25 | 1 | Concept: magic harms the caster, no mana, empowerment and transformation, transfer. Fantasy setting. "Body is the board" dropped. Side-scroller deferred. |
| 0.2 | 2026-10-29 | 2 | Format: card duel (tactics dropped). Pillar 1 decided. Cooldowns, spell cap, no draw, prepared spells plus hidden reserve. Separate health and affliction meters, one meter per element, max two elements. Threshold growth and burn. Direct damage. Transfer demoted from core. Hidden health tied to spellbook size. Simultaneous play tentative. Draft core loop. |
| 0.3 | 2026-10-30 | 3 | Consolidated into this living GDD. Added proposed pillars 2–3, the turn-structure inconsistency flag, hidden-health feedback and opponent-scope risks, and the pre-prototype vs. pre-development question split. No new decisions. |
| 0.4 (pending) | 2026-10-30 | 4 | In progress. Turn structure (TENTATIVE): secret choice resolved by speed category, defensive first and offensive last, no interaction within a category; resolves the session-2 ⚠. Decided: speed set by target (self = fast, opponent = slow), no utility category. Decided: test simultaneous only, alternating dropped. Decided: up to 2–3 spells per turn ("up to N"), exact value to tune. Tentative: match length 8–12 turns; phase-based pacing deferred. Decided: resting, where each empty slot takes 1 turn off a chosen spell's cooldown, stacking; it does not lower affliction. Decided: stronger spells have cooldowns longer than 1 turn. Reopened: overcasting is now OPEN. |

## Appendix: glossary

- **Cooldown:** turns a spell must wait before reuse (*Overwatch* abilities).
- **Core loop:** the repeated cycle of play (*Tetris*: rotate, place, clear lines).
- **Death spiral:** falling behind makes you fall further behind (*Monopoly*).
- **Design pillar:** a short statement that defines the game and filters features.
- **MDA:** Mechanics (rules) → Dynamics (behavior) → Aesthetics (feelings).
- **Push-your-luck:** you choose how much risk to take (Blackjack).
- **Rotation:** a fixed, always-optimal ability order (MMOs).
- **Yomi:** "reading the mind"; predicting what the opponent will choose (*Street Fighter* mind games).
- **Tell:** an unintended signal that gives away hidden information (poker).
- **Pre-production:** the phase of cheap prototypes to "find the fun" before building the real game.
