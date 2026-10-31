# Process research: design and development practices

*Session 5, 2026-10-31. Why this project's process looks the way it does, and what is still owed.*

This file is the record of the process review done before prototyping. It keeps three things:
the sources and what each says, the practices they agree on, and every process item with its status
and **when** it must be done. Items for later phases are listed here so they are not lost.

**How to use it.** At the start of each new phase (paper prototype, digital prototype, development),
read §5 and do the items whose trigger has been reached. When an item is done, change its status here
in the same commit.

---

## 1. Inputs

1. **RBOnline** (`C:\cy_proj_RB`): Chris's mature game project (TypeScript rules engine for a TCG,
   about 660 sessions). Its own process retrospective (`docs/audits/a4_process_retrospective.md`,
   about 5,400 process failures) is the main lesson source.
2. **15 published sources** (§2), found and read on 2026-10-31. All links answered HTTP 200 on that date.

### 1.1 Lessons from RBOnline

- **Prose rules did not stop failures.** In 31 of 35 failure types, failures kept happening after a
  rule was written. 14 of those rules lived only in prose (CLAUDE.md, skills, memory).
- **Mechanical checks did.** Its pre-commit lint hook was one of the few rules that kept catching real defects.
- **Process prose grew to about 2,265 lines**, and about 80 lines of the global CLAUDE.md (C#/.NET)
  never applied to that repo.
- **Worth copying:** one source-of-truth design doc, IDs for open questions, a term registry,
  commits that cite the doc version, a fresh-session review, a deterministic rules engine, spells/cards as data.
- **Not worth copying:** waves and packets, the 542-line dispatch skill, two-commit closes, rolling
  archives, hundreds of memory files, the project-knowledge manifest.

**Rule for this repo:** prefer a check over a written rule, and keep process prose short.

---

## 2. Sources

Peer-reviewed unless marked ⚠.

| # | Source | Why it is used |
|---|---|---|
| S1 | Murphy-Hill, Zimmermann, Nagappan. *Cowboys, Ankle Sprains, and Keepers of Quality: How Is Video Game Development Different from Software Development?* ICSE 2014. [PDF](https://thomas-zimmermann.com/publications/files/murphyhill-icse-2014.pdf) | Interviews (14) and a survey (364) of developers. Games lack requirement specs; automated tests break fast as the design changes; teams work iteratively; build/configuration management matters more. |
| S2 | Washburn, Sathiyanarayanan, Nagappan, Zimmermann, Bird. *"What Went Right and What Went Wrong": An Analysis of 155 Postmortems from Game Development.* ICSE 2016. [PDF](https://thomas-zimmermann.com/publications/files/washburn-icse-2016.pdf) | Best practices: clear vision, planning, prototypes that become the base, iteration. Pitfalls: over-ambitious design, optimistic schedules, untested core concepts. Small teams (≤20) report obstacles twice as often (50% vs 26%). |
| S3 | Politowski, Petrillo, Ullmann, Guéhéneuc. *Game Industry Problems: An Extensive Analysis of the Gray Literature.* Information and Software Technology 134, 2021. [DOI](https://doi.org/10.1016/j.infsof.2021.106538) · [arXiv](https://arxiv.org/abs/2009.02440) | 927 problems from 200 postmortems. Top types: technical and game design (11% each). Top root causes include underestimation, unclear design vision, lack of fun and design complexity. Fixes: more pre-production and prototyping, more playtests, feature lockdown dates, choosing tools in pre-production. |
| S4 | Callele, Neufeld, Schneider. *Requirements Engineering and the Creative Process in the Video Game Industry.* IEEE RE 2005. [PDF](https://www.cs.usask.ca/~kas/Publications_files/Callele_Neufeld_Schneider_RE_VideoGames.pdf) | Many failures trace to the move from pre-production to production. The GDD is a creative-vision document; production specs should be separate. Shared terminology and early feedback from production catch hidden ("implied") requirements. |
| S5 | Ampatzoglou, Stamelos. *Software Engineering Research for Computer Games: A Systematic Review.* IST 52, 2010. [DOI](https://doi.org/10.1016/j.infsof.2010.05.004) | Baseline review of the field. Requirements work dominates the research; testing and maintenance are neglected. |
| S6 | Pascarella, Palomba, Di Penta, Bacchelli. *How Is Video Game Development Different from Software Development in Open Source?* MSR 2018. [Page](https://2018.msrconf.org/details/msr-2018-papers/39/How-Is-Video-Game-Development-Different-from-Software-Development-in-Open-Source-) | 60 open-source projects plus a survey. Confirms S1: game developers find automated testing, code reuse and requirements harder. |
| S7 | Kasurinen, Smolander. *What Do Game Developers Test in Their Products?* ESEM 2014. [dblp](https://dblp.org/rec/conf/esem/KasurinenS14.html) | Seven game teams. Testing with real users matters more than in other software; usability, exploratory and unit-test variants are the common methods. |
| S8 | ⚠ Politowski, Petrillo, Guéhéneuc. *A Survey of Video Game Testing.* 2021. [arXiv](https://arxiv.org/abs/2103.06431) | Game testing is almost all manual; fun and balance are found by playtesters; automation is the next step; test early. ⚠ Only the preprint was found, so the peer-reviewed venue is unconfirmed. Used as support only. |
| S9 | Pieva, Bernardino. *Trends and Research in Digital Game Project Management: A Systematic Literature Review.* Journal on Interactive Systems, 2023. [Page](https://journals-sol.sbc.org.br/index.php/jis/article/view/3196) | 65 studies (2010–2021). Most adapt Scrum for games; no single process fits all projects. |
| S10 | Hunicke, LeBlanc, Zubek. *MDA: A Formal Approach to Game Design and Game Research.* AAAI 2004 Workshop on Challenges in Game AI. [PDF](https://users.cs.northwestern.edu/~hunicke/MDA.pdf) | Mechanics → Dynamics → Aesthetics. Design from the player experience you want, then check the rules produce it. |
| S11 | Jaffe, Miller, Andersen, Liu, Karlin, Popović. *Evaluating Competitive Game Balance with Restricted Play.* AIIDE 2012. [Page](https://ojs.aaai.org/index.php/AIIDE/article/view/12513) | Automated balance measures from AI agents, shown on a card game. Fast feedback lets the designer try many variants and playtest only the best. |
| S12 | Nelson. *Game Metrics Without Players: Strategies for Understanding Game Artifacts.* AIIDE 2011 Workshop on AI in the Game Design Process. [Page](https://ojs.aaai.org/index.php/AIIDE/article/view/12479) | Seven ways to learn about a game from its rules and code alone. Do this early so playtests can focus on subjective questions. |
| S13 | Tyree, Akerman. *Architecture Decisions: Demystifying Architecture.* IEEE Software 22(2), 2005. [IEEE](https://ieeexplore.ieee.org/document/1407822) | Record major decisions explicitly, with their rationale, so the design stays transparent. The origin of decision-record templates. |
| S14 | Hilton, Tunnell, Huang, Marinov, Dig. *Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects.* ASE 2016. [PDF](https://cs.uwaterloo.ca/~m2nagapp/courses/CS846/1171/papers/hilton_ase16.pdf) | 34,544 projects, 1.5M builds, a survey of 442 developers. Projects with continuous integration (automatic build and checks on every change) release more often. |
| S15 | Chatlatanagulchai et al. *On the Use of Agentic Coding Manifests: An Empirical Study of Claude Code.* PROFES 2025 (short paper). [Page](https://conf.researchr.org/details/profes-2025/profes-2025-short-papers-and-posters/17/On-the-Use-of-Agentic-Coding-Manifests-An-Empirical-Study-of-Claude-Code) · [arXiv](https://arxiv.org/abs/2509.14744) | 253 CLAUDE.md files. Most hold build/run commands (77%), implementation rules (72%), architecture (65%) and testing (61%); structure is shallow (one H1, a few H2s). Their effect on results is not yet measured. |

---

## 3. Best practices (where sources agree)

| ID | Practice | Sources |
|---|---|---|
| BP1 | Invest in pre-production: a clear vision, a prototype early, then iterate on it. | S2, S3, S4, S9 |
| BP2 | Test the core concept with real players early. Fun and balance are found by playing. | S2, S3, S7, S8 |
| BP3 | Automate tests only for what is stable. Tests on a changing design break fast: test the rules logic, play-test the rest. | S1, S6, S8 |
| BP4 | Use simulation for fast balance feedback before playtests, so playtests focus on feel. | S11, S12, S8 |
| BP5 | Keep the GDD as the creative vision; write build specs separately; surface hidden requirements early with prototypes. | S4, S1, S5 |
| BP6 | Record decisions with their reasons. | S13, S4 |
| BP7 | Control scope: watch design complexity, set a feature lockdown date, estimate tasks one by one. | S2, S3 |
| BP8 | Choose tools in pre-production. Changing them during production is costly. | S3, S2 |
| BP9 | Automate building and checking on every change. | S14, S1 |
| BP10 | State design goals as player experiences and check mechanics against them. | S10, S4 |
| BP11 | Keep agent instruction files short and structured, with build and test commands. | S15 |
| BP12 | Small teams hit more obstacles, so track risks on purpose. | S2 |

---

## 4. How the original proposal changed

The first proposal (session 5, before the research) came from RBOnline alone. Cross-checked against §3:

| Original item | Result | Reason |
|---|---|---|
| Q-IDs for open questions | Kept | BP6 |
| Glossary as the official word list | Kept, stronger | BP5 (S4 names shared terminology as a requirements problem) |
| Commits cite GDD section and version | Kept | BP6 |
| Session roles, fresh-session review | Kept, light | BP9 indirectly; S1 notes games often skip review |
| Stop hook + GDD lint | Kept | BP9 |
| Folder tidy | Changed | Added `docs/specs/` for build specs, apart from the GDD (BP5) |
| Pacing / balance simulation | **Moved earlier** (prototype → now) | BP4 is the strongest finding |
| Playtest-session skill | **Moved earlier** | BP2 |
| Deterministic rules engine + rule tests | Kept | BP3 |
| Snapshot ("golden") match tests | **Weakened** | BP3: they break on every tweak. Only after rules settle. |
| Spells as data | Kept | Supports fast tuning (S11) |
| Subagents | **Trimmed** | No evidence yet (S15); start with two |
| Build version, bug tracker, review ledger | Kept deferred | Nothing to version yet |
| New: experience goals per pillar | Added | BP10 |
| New: risk register with mitigation and trigger | Added | BP12 |
| New: prototype scope freeze | Added | BP7 |
| New: CI on GitHub | Added | BP9 |
| New: move the engine decision earlier | Added (suggestion, Chris's call) | BP8 |

---

## 5. Process items and status

Status: **Done** (in the repo), **Pending** (do when the trigger is reached), **Deferred** (no trigger yet).

### 5.1 Now: design phase

| ID | Item | Practice | Status |
|---|---|---|---|
| P-01 | Open questions get stable IDs (`Q-###`) in GDD §10; never resolved silently. | BP6 | Done (session 5) |
| P-02 | GDD glossary is the official term registry; use its exact words everywhere. | BP5 | Done (session 5) |
| P-03 | Commits cite the GDD: `docs: session N - <topic> [GDD §x.y @ vA.B]`. | BP6 | Done (session 5) |
| P-04 | Session roles in CLAUDE.md: design, build, review (review in a fresh session). | BP9 | Done (session 5) |
| P-05 | Stop hook warns on uncommitted changes; pre-commit hook runs the GDD lint (`tools/check_gdd.py`). | BP9 | Done (session 5) |
| P-06 | Folders: `docs/GDD.md`, `docs/sessions/`, `docs/design/`, `docs/specs/`, `docs/playtests/`. | BP5 | Done (session 5) |
| P-07 | Experience goals per pillar (MDA aesthetics) in GDD §2, checked in every playtest. | BP10 | Done as structure; goals [PROPOSED], Chris to decide (`Q-013`) |
| P-08 | Risk register: GDD §9 gets mitigation and trigger per risk. | BP12 | Done (session 5) |
| P-09 | `playtest-session` skill and `docs/playtests/` findings tracker. | BP2 | Done (session 5) |
| P-10 | Pacing script: casts per turn × affliction per spell against the 8–12 turn target, plus the Overloaded "death clock". | BP4 | **Pending.** Trigger: starter spells have first-pass numbers (GDD §11). Needs damage and affliction values that don't exist yet. |
| P-11 | Engine decision moved from "before development" to "before the digital prototype". | BP8 | **Pending: Chris's call** (`Q-014`) |

### 5.2 Prototype: when the digital prototype starts

| ID | Item | Practice | Status |
|---|---|---|---|
| P-20 | **Deterministic rules engine.** No I/O, no clock, all randomness from one seeded generator. Rules are separate from UI. | BP3 | Pending. Trigger: digital prototype starts. |
| P-21 | **Rule tests** named after GDD sections (`Rest_EmptySlot_ReducesCooldownByOne`). Numbers come from data, never hard-coded, so balance tweaks don't break tests. | BP3 | Pending. Same trigger. |
| P-22 | **Spells as data.** One spell table file is the source of truth. A check enforces GDD limits (affliction 1–4 per spell, role mix per element). | BP4, BP9 | Pending. Same trigger. |
| P-23 | **Simulation harness.** Bots play many matches; report turn count, win rate per element pair, affliction curves, and how often a weaker spell is chosen because of affliction (GDD §9 pillar-drift check). Grows out of P-10. | BP4 | Pending. Same trigger. |
| P-24 | **Subagents** in `.claude/agents/`: `balance-analyst` (runs the simulation and reports, read-only) and `design-critic` (reads only the GDD, looks for dominant strategies and exploits). | BP4 | Pending. Same trigger. |
| P-25 | **Prototype scope freeze.** A fixed feature list and a cut list before building; new ideas go to the cut list. | BP7 | Pending. Trigger: before the first line of prototype code. |
| P-26 | **CI on GitHub.** Run the GDD lint and tests on every push. | BP9 | Pending. Trigger: first code in the repo. |
| P-27 | **Build specs** in `docs/specs/`, one per system, each citing its GDD sections. | BP5 | Pending. Trigger: first system is built. |
| P-28 | **CLAUDE.md build and test commands**, and a project override of the global C# defaults (no Clean Architecture layers for a game; coverage goal on the rules engine only). | BP11, BP8 | Pending. Trigger: engine chosen. |

### 5.3 Development: when the game itself is built

| ID | Item | Practice | Status |
|---|---|---|---|
| P-40 | Snapshot ("golden") match tests: recorded matches replayed to show what a change moved. | BP3 | Deferred. Trigger: core rules stop changing between playtests. |
| P-41 | `rules-dev` and `spell-dev` subagents (build against cited GDD sections; stop on any [OPEN] item). | BP3 | Deferred. Trigger: rules engine exists. |
| P-42 | Playtest build version, bug tracker, review ledger. | BP9 | Deferred. Trigger: first build shared with another player. |
| P-43 | Per-task estimates before each milestone. | BP7 | Deferred. Trigger: development milestone planning. |
