# Rex (DionyzRex) — Contributor Notes

## Starting a Claude session

Paste this at the start of any Claude conversation to get full context:

```
I'm working on Devil's Silence Resurrected — a 2003 PvP MUD being
rebuilt from a corrupted archive. I'm a contributor (Rex / DionyzRex).

Please read these files in order:
1. CONTRIBUTOR_REX.md — my background, current work, and workflow
2. SESSION_STATE.md — current project state and live version
3. COMBAT_CATALOG.md — every combat ability and its port status
4. CONTRIBUTING.md — how code changes get submitted and reviewed

I'm currently working on the Morpheous class (tier 3, IS_CHANGELING).
Skill group "morpheous default" has: dopple, grow parts, mutate body,
advanced dopple, chameleon, form memory. None are implemented yet.

My changes go to GitHub. Kyle's Code agent pulls them, writes a
patcher script, and applies them to the live WSL2 server.
```

---

Active contributor as of 2026-04-26. Discord: DionyzRex.

Background: wrote a browser-based JavaScript RPG (combat ticks, leveling,
class switching, passive skills, equipment system). Comfortable reading and
writing code directly. Working in parallel with Code (the AI coding agent)
on the Morpheous class.

---

## Current work

**Morpheous class implementation** — tier 3, IS_CHANGELING family, INT-based,
dagger school. Skill group `morpheous default` includes:

- `dopple` — duplicate/mimic ability (exact mechanic TBD from disasm)
- `grow parts` — body modification combat modifier
- `mutate body` — shapeshifting
- `advanced dopple` — upgraded mimic
- `chameleon` — stealth/camo toggle
- `form memory` — save a shapeshifted form

None of these have implementations yet — they're skill names defined in
`const.c` but the functions behind them were in the lost `act_combat.c`.
Rex is either writing new implementations or pulling them from the original
binary via disasm.

**Reference:** there is a surviving 2003 player file for a character named
`Shade` who was classed as Morpheous — useful for checking what the class
looked like from the outside.

---

## Ideas Rex has contributed

These are logged in `IDEAS.md` with full context. Short version:

- **IDEA-013** — Modular PvE funnel leading into arena PvP. New players
  grind PvE to learn mechanics, then graduate into structured 1v1 arena.
  Separates the learning curve from the PvP risk.

- **IDEA-014** — Kensai class with builder/finisher/stance system. Named
  moves, slot symbols, finisher payloads that change based on stance.
  Co-designed with Kyle in a Discord session.

- **IDEA-015** — Combat feedback legibility + daze variance reduction.
  Players can't see the daze system working; messages should reflect it.
  Daze variance (2/3 skill reduction) could be tuned down or made visible.

---

## How Rex's workflow connects to the live server

Rex edits C files and pushes to GitHub. Kyle pulls the changes and tells
Code to pick them up. Code reviews the diff, writes a patcher, applies it
to WSL2, builds, and copyovers. Rex doesn't need WSL2 access or to know
the patcher pattern — Code handles the formalization step.

For anything that needs in-game testing, ask Kyle. He can `mload` mobs,
`advance` characters, and run commands as an Executive-level imm.

---

## Notes for Code when pulling Rex's changes

- Rex may edit `const.c`, `act_combat.c`, or class-specific files
- Always `git pull` before staging a new build that touches those files
- If there's a merge conflict between Rex's edit and a staged Code build,
  flag it in `CODE_HANDOFF.md` — Kyle will resolve manually
- Rex's C background is JavaScript-adjacent; review for ROM idiom
  correctness (especially CHAR_DATA field access, affect application,
  `send_to_char` vs `act()` broadcast patterns)
