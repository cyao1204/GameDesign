# Session 2 — 2026-10-29

Full summary doc: https://claude.ai/artifact/83cXKwV5K7jC4sZDK1pgkJ
Chat: https://claude.ai/chat/98ce249e-5135-47e8-9c60-4d8c96ae25b1

## Covered
- Turned the concept into a card-duel framework from Chris's six rules: hidden health from deckbuilding, no casting resource, spell cap per turn, no draw, cooldowns, element and preparation limits.
- Risks: solved openings, death spiral, simultaneous resolution, flat spell cost.
- Research on comparable games: Mage Wars, Wizards of the Grimoire, Witcher 3 toxicity, MechWarrior heat, Astrea.

## Decided
- Card duel (tactics dropped). Pillar: affliction is the cost of casting; mastering it is how you win.
- Every spell adds its element's affliction to the caster. Spells deal damage directly.
- No draw. Prepared spells plus a hidden reserve. Cooldowns. Spell cap.
- Separate health and affliction meters, one meter per element, at most two elements.
- Threshold → passive growth plus health loss (may change). Empowerment, transformation, unlocks.
- Raise, lower and transfer belong to certain elements. Transfer is not central. Overcasting belongs to one element.
- Spell count and health share one pool. Opponents see only cast spells.

## Tentative
- Simultaneous turns, alternating as the fallback.

## Left open
- Outer loop, element roster, swap cost, all numbers, transfer target meter, double-KO.
