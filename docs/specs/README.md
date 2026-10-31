# Build specs

Empty until the digital prototype starts.

The GDD (`docs/GDD.md`) is the creative vision: what the game is and why. Specs here say **how one system is built**: data, states, edge cases, and the tests that prove it. Game projects often fail at the handover from design document to production (`docs/design/process-research.md`, S4 and BP5), so the two are kept apart.

- One file per system, e.g. `turn-resolution.md`, `affliction.md`.
- Each spec cites the GDD sections and version it implements (`[GDD §5.5 @ v0.6]`).
- A spec never decides an [OPEN] question. If the GDD is silent, the spec lists it and a design session answers it.
