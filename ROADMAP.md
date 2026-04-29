# Devil's Silence Resurrected — Roadmap

Last updated: 2026-04-27

This is the master planning document. CHANGELOG.md tracks what shipped.
IDEAS.md tracks individual feature proposals. This file tracks the
*phases* — what order things happen in and why.

Each phase has a clear exit criterion. Don't move to the next phase
until the current one's exit criterion is met.

---

## Phase Status Summary

| Phase | Name | Status |
|---|---|---|
| 0 | Resurrection | ✅ Done |
| 1 | Combat Reconstruction — Basic | ✅ Done |
| 2 | Combat Reconstruction — DS Custom | 🔄 In Progress |
| 3 | Pre-built `.o` Reconstruction | ⏳ Queued |
| 4 | `update.c` DS Tick Layer | ⏳ Queued |
| 5 | Class Bug Fixing | ⏳ Queued |
| 6 | Stability & Diagnostics | ⏳ Queued |
| 7 | Stress Testing & Bots | ⏳ Queued |
| 8 | Balance Framework & Tuning | ⏳ Queued |
| 9 | Accessibility & Polish | ⏳ Queued |
| 10 | Expansion (Clans, Web Client, Oracle AI) | 🔭 Future |

---

## Phase 0 — Resurrection ✅ DONE

**What it was:** Get the 2003 source compiling and running on modern hardware
from a corrupted archive.

**What shipped:**
- Forensic extraction of 1,847 files (167.5 MB) from the damaged tar
- Modernisation patches (`rebuild_source.py`) to compile on GCC 11 / Ubuntu 22
- `act_combat.c` stub generated to replace the unrecoverable source
- Binary boots, world loads, telnet connections accepted on port 5000
- Public hosting via ngrok TCP (reserved address `7.tcp.ngrok.io:25597`)
- Watchdog auto-respawn (3-second cooldown, rate-limited)
- Copyover / hot-swap deploys tested and working
- Debug build (`-O0 -g`) and core dump capture configured

**Exit criterion met:** server boots, players can connect and create characters.

---

## Phase 1 — Combat Reconstruction: Basic & DS Custom First Pass ✅ DONE

**What it was:** Port every non-Psionic, non-Monk combat ability from the
original `act_combat.o` disassembly back into `act_combat.c`.

**Tiers completed:**
- BASIC ROM (11 commands): kill, flee, kick, bash, trip, disarm, rescue, backstab, berserk, circle, gouge, dirt
- BUFF-SELF cluster: concentration, ironwill, spellbane, resistance, warcry, battlehymn, bloodlust, warpaint
- DS-Custom small: mock, target
- STRIKE-PURE full batch: cleave, legsweep (anchors); dhammer, stomp, whirlwind (AOE); cross slash, garotte, strike, gore (single-target)

**30 commands live as of v0.4.10.**

**Exit criterion met:** all BASIC ROM and STRIKE-PURE tiers complete.

---

## Phase 2 — Combat Reconstruction: DS Custom Remainder 🔄 IN PROGRESS

**What it is:** Finish the remaining ~57 stubs in `act_combat.c`. This is
the main current sprint.

**Sub-phases in order:**

### 2a — STRIP-SELF cluster (next up)
`do_rub` (552b), `do_deepbreathing` (286b), `do_cleanse` (444b).
All share the `affect_strip()` / `affect_remove()` pattern. Code will
survey all three in one disasm pass and batch if the shape is consistent.

### 2b — `do_storm` (610b)
STRIKE-PURE AOE with a Dance precondition. Needs a disasm read on the
`paradox_is_on` / `ch->stance` / `ch->pcdata->dance` gate before writing.
Likely bundled with STRIP-SELF.

### 2c — CLASS ABILITY tier
ROT 1.4 source available as a starting template. DS tweaks caught via
disasm diff.

| Command | Size | Notes |
|---|---|---:|
| `do_charge` | 833b | Simplest |
| `do_jab` | 1080b | STANDING gate |
| `do_throw` | 1247b | |
| `do_dance` | 1282b | Dance state feeds storm's precondition |
| `do_hurl` | 2477b | Largest |

### 2d — DS Custom Other (small → big)
`roundhouse` · `powerinvuln` · `plantroots` · `powerstun` · `quickening` · `caltrops` · `healing touch` · `dislodge` · `powerblind` · `transfix` · `thousand wounds` · `gash` · `eadbutt` · `devils touch` · `earthbind` · `scream` · `shuriken` · `feed` · `bastion` · `strangle` · `chaos blow` · `toss daggers` · `hack` · `ambush` · `pinch` · `blackjack` · `blinding strike` · `assassinate` · `shield smash` · `forge` · `aura` · `stance` · `vital strike`

### 2e — Monk class
`do_deepbreathing` · `do_katana` · `do_buddha_palm` · `do_chi`
Plus the eight `monk_*` helpers behind `multi_kick`.

### 2f — Voodoo class
`do_voodoo` dispatcher · `do_jinx_palm`
Plus the three `voodoo_*` helpers.

### 2g — Psionics (last — Priority 4)
`do_biomanipulation` (2418b) · `do_electrokinesis` (3511b) · `do_telekinesis` (3536b) · `do_pyrokinesis` (3807b).
Largest functions in the catalog. Defer until all others are proven.

**Exit criterion:** every stub in `act_combat.c` is a real implementation.
Zero "ability not available right now" responses to player commands.

---

## Phase 3 — Pre-built `.o` Reconstruction

**What it is:** The three pre-built objects that shipped with the 2003 archive
without source. They work now, but can't be modified without reconstructing
the source from their disassembly.

**Targets:**

**`wizlist.o`** — the `wizlist` command. Reads `data/misc/wizlist.txt` at
runtime and formats the immortal roster. Low-risk, low-urgency. Reconstruct
only if we need to change the display format.

**`xsocial.o`** — the social command dispatch table (smile, nod, wave, etc.).
Source data comes from a text file; the `.o` is a thin dispatcher. Reconstruct
if we want to add or modify social commands.

**`util.o`** — the OS interface layer: signal handlers, `tell_all` broadcast
on fatal signals, process management helpers (pid file, fork/exec for
copyover). The most functionally important of the three. Reconstruct if we
need to change crash behavior, improve the watchdog handoff, or extend
copyover mechanics. The "relocation in read-only section" linker warning
points to a signal handler function pointer in `.rodata` — that's the
starting point for reconstruction.

**Exit criterion:** all three `.o` files have reconstructed `.c` source that
compiles to equivalent object code, passing a diff of `objdump -d` output.

---

## Phase 4 — `update.c` DS Tick Layer

**What it is:** The recovered `update.c` was truncated at line 1129. The
stock ROM 2.4 tail covers standard tick behavior but loses DS-specific
mechanics that will become visible once class abilities are live.

**What's missing from the DS tick layer:**
- Class resource regen — `wind` (Monk chi), `aura`, `dance`, `stance`,
  `pktimer`, `stimer` fields on `pc_data`. These pools don't regenerate.
- Status-effect side mechanics — plague spreading between players,
  pyrokinesis self-burn tick, ebola decay-rate variation. Affects expire
  correctly; the side mechanics attached to them don't fire.
- Giant spawner — area-tick logic for the Isles giant population.
- Clan upkeep / decay — moot until clans are rebuilt (Phase 10).

**Approach:** hand-decompile the DS-specific sections from the 2003 binary's
`update.o` disassembly, the same method used for `act_combat.c`. The
`update.o` file was recovered intact.

**Priority trigger:** Monk and Psionic abilities landing (Phase 2e/2g) will
make the missing regen obvious. Do this phase before those classes go to
wide playtesting.

**Exit criterion:** class resource pools regen correctly, plague/pyrokinesis
side mechanics fire on tick, giant spawner active in Isles.

---

## Phase 5 — Class Bug Fixing

**What it is:** Once every class has its full ability set active for the
first time since 2003, class-specific interaction bugs surface. This is
a dedicated QA and fixing sprint, one class at a time.

**Process per class:**
1. Full ability audit against test dummies (IDEA-005).
2. 1v1 playtest against a live opponent.
3. Bugs logged to BUGS.md, fixed in batches per class.
4. Apply IDEA-020 (contextual error messages) to all gate/reject paths
   encountered during the audit.

**Highest-risk classes (do these first):**
- **Monk** — `multi_kick` calls eight helpers; one bad secondary breaks the suite.
- **Voodoo** — curse timing depends on the DS tick layer (Phase 4).
- **Psionic** — elemental type interactions with resist/vuln tables are complex.
- **Morpheous** — Rex owns this; his reports are the model.

**Exit criterion:** no known class-breaking bugs. Every ability has a
"when do I use this?" answer that isn't "never."

---

## Phase 6 — Stability & Diagnostics

**What it is:** Formal diagnosis and resolution of BUG-001 (spontaneous
SIGABRT) and a general stability sweep using watchdog + boot log data.

**Tasks:**
- Grep `~/ds_watchdog.log` and `/tmp/ds_boot.log` for every signal-6
  and signal-11 event; correlate with player activity timestamps.
- Attach gdb to a running server under the debug build and wait for a
  crash to get a real backtrace.
- Fix `core_pattern` permanently: `sysctl kernel.core_pattern=/tmp/core.%e.%p.%t`
  (this should already be set; verify it survives WSL reboots).
- Mass password migration: one Python script over all 1,250 player files,
  rewrites DES hashes to SHA-512. Unlocks the entire 2003 roster.
- Add `wizlist` to `.gitignore` to stop the runtime-touched file
  appearing in `git status` every session.

**Exit criterion:** no undiagnosed SIGABRT crashes over a 48-hour
sustained-play window. All 1,250 legacy characters accessible.

---

## Phase 7 — Stress Testing & Bots

**What it is:** Automated testing to validate the server under real load
and produce the empirical data the balance framework needs.

**Two tracks:**

**Track A — Connection stress test:**
Python script opens N simultaneous telnet connections, creates or logs in
with pre-seeded bot accounts, runs a scripted combat loop for a set duration.
Captures: connection stability, memory footprint growth (leak check), and
whether any SIGABRT triggers appear under sustained multi-player combat.
This is the BUG-001 investigation's most powerful tool.

**Track B — Bot players for balance measurement:**
Two or more bot characters of specified classes fight each other in a
controlled environment using their full ability rotation. Script captures:
damage per round, TTK (time-to-kill), which abilities fired how often, and
whether any ability is never chosen by the rotation (dead-ability signal).
This data feeds directly into the IDEA-019 balance spreadsheet.

**Prerequisites:** IDEA-005 (test dummies) live, bot accounts pre-created
and imm-set to max level with skills at 100%.

**Exit criterion:** server handles 20 concurrent connections without
degradation; balance dataset exists for all ported abilities.

---

## Phase 8 — Balance Framework & Tuning

**What it is:** Use the stress test data (Phase 7) to establish balance
targets and then tune ability constants to hit them. See IDEA-019 and IDEA-021.

**Deliverables:**
- `BALANCE.md` — design targets: expected DPS, TTK, per-ability contribution vs. auto-attack, acceptable proc rate ranges.
- Balance spreadsheet: each ability's damage formula output at level 10/50/101, wait state, secondary effect and proc rate, role tag.
- Tuning patcher scripts: one per ability that needs adjustment. Constants only — no logic changes. Port accuracy stays intact; numbers are a design call.

**First tuning candidates (from current observation):**
- `do_cleave` — moderate damage, no secondary, notable wait state. Needs either a defensive debuff on hit (reduce target parry/dodge for 1–2 rounds) or a significantly more aggressive damage formula to justify the lag. A two-handed weapon requirement with real damage upside would give it a clear identity.
- Any damage-only ability at sub-auto-attack DPS with no situational advantage.

**Process:** stress test → measure → compare to targets → adjust constants → re-test. Always tune after data, never before.

**Exit criterion:** every ability has a clear "when do I use this?" answer, validated by bot rotation data showing it gets chosen in the appropriate situations.

---

## Phase 9 — Accessibility & Polish

**What it is:** Two interconnected polish passes that make the game legible
to new players and give experienced players better mechanical information.

**9a — Contextual error messages (IDEA-020):**
Every ability's rejection path gets a message that names the missing
requirement and points to help: "You need a whip wielded to garotte.
Type `help garotte` to learn more." Applied progressively during Phase 5
class audits and Phase 8 tuning pass, then swept for any misses.

**9b — Affect visibility (IDEA-015):**
Daze, stun, spellbane, bash-interrupt, and saving-throw results each get
distinct combat strings so players can perceive what the system is doing.
Reduce mechanic variance first (tighter proc windows, more consistent
durations), *then* expose it clearly through text. A predictable mechanic
that's visible is one players can build strategy around.

**9c — Helpfile rewrite:**
2003 helpfile stubs rewritten to teach, not just document. Pairs with
IDEA-012 (Oracle AI) for dynamic explanations. Kyle and Rex can draft
these in `HELPFILES.md`; they get patched in as a content PR.

**9d — New player experience:**
Auto-spellup on first spawn (IDEA-010), starter gear auto-equipped (IDEA-009),
default prompt / auto all / brief on creation (IDEA-007, partially done).

**Exit criterion:** a new player with no MUD experience can log in, understand
what their character does, and meaningfully participate in combat without
needing to ask in Discord.

---

## Phase 10 — Expansion

These items are future work — not gated on Phase 9 completion, but
not worth starting until the server is stable and the combat system is solid.

**Clan reconstruction from logs** — 306 session logs may contain enough
clan event records (creation, promotions, war declarations) to reconstruct
named clan shells with approximate membership. Worth a grep-pass session.
Not urgent; zero empty clans is fine for now.

**Browser web client (IDEA-011)** — WebSocket bridge + xterm.js frontend.
One afternoon of Python + HTML once stability is solid. Unlocks mobile
and no-install play. PWA wrap for home-screen install.

**Arena PvP structure (IDEA-013)** — PvE funnel (1–101 levelling) into a
controlled 1v1 arena layer. Requires all abilities working and the balance
framework in place. The `battle.are` area already exists in the recovered
world.

**Kensai class (IDEA-014)** — Rex's original combo/finisher design. Huge
scope. Requires the stance machinery (`do_stance`, Phase 2d) understood
first. The right home is the arena context.

**Oracle AI in-game help (IDEA-012)** — `ask <question>` delivers an
LLM answer as a tell from an NPC, contextualised to the player's class
and level. Defer until helpfiles (Phase 9c) are good enough to build a
system prompt from.

**Wwise audio layer (IDEA-016)** — Stage 1 is a web client that parses
combat text for keywords and fires Wwise events. Kyle's domain entirely.
Can start as soon as the web client (Phase 10) exists. Stage 2 adds a
structured sidecar event channel. Stage 3 is the full Unreal client.

**Public web status page** — single-page status showing server up/down,
player count, last patch version. Half a session once the server is stable.

---

## Open Questions & Deferred Decisions

- **VPS migration** — ngrok hosting works for the friend group. Persistent
  uptime independent of Kyle's laptop requires a VPS (~$5–10/mo). Decision
  whenever uptime SLA becomes important.
- **Clan data from logs** — feasibility pass needed before committing effort.
  Check whether the 306 log files actually contain parseable clan records.
- **Psionic balance** — the four Psionic abilities are the most complex in
  the catalog and almost certainly need their own balance pass after Phase 2g.
  Treat as a sub-phase of Phase 8.
- **`util.o` reconstruction priority** — only urgent if we need to change
  crash behavior or copyover mechanics. Current behavior is acceptable;
  defer Phase 3 until something specific requires it.
