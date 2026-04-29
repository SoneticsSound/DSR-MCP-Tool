# Cowork → Code Prompt

**Cowork writes the next task here. Code reads it at the start of each
session. Kyle just says "go" — no repasting needed.**

WSL2 path to this folder:
`/mnt/c/Users/danbl/Documents/Claude\ DS/Devil\'s\ Silence\ Resurrected/`

After completing a task, write findings + staged build info to
`CODE_HANDOFF.md` in this same folder. Cowork reads it directly.

---

## Session sync — 2026-04-29 (updated — post 0.4.33)

**State of play:**
- Staged: **v0.4.33** — do_voodoo dispatcher + voodoo_pin/trip/throw. Awaiting Kyle copyover.
- **Priority right now:** do_jinx_palm (0.4.34), then fight.c WEAR_THIRD/FOURTH uncomment (grow arms re-enable), then BUG-020 monk valid flag flip. See `CODE_HANDOFF.md` for full queue.

**New file structure (2026-04-29):**
- `CODE_HANDOFF.md` — current build only, kept under 200 lines. Move old builds to BUILD_LOG.md.
- `BUILD_LOG.md` — all superseded build entries (append, newest first).
- `DECISIONS.md` — permanent design decisions with rationale. Read before re-asking settled questions.
- `DS_SCHEMA.md` — static constants. Still the source of truth.

**Completed since last sync:**
- ✅ Priorities 1–6 complete (STRIP-SELF, storm, charge, dance, jab, throw, hurl, stance, assassinate, shield_smash, kick, roundhouse, buddha_palm, chi, multi_kick helpers, voodoo dispatcher+helpers)
- ✅ push/drag/chameleon/grow re-enabled in disabled.txt (fight.c uncomment still needed)
- ✅ Class indices corrected: monk {8,26,44}, gladiator {3,21,39}
- ✅ AQ veteran gear (17 slots, 100 AQP each)
- ✅ Solennir shop wired for adamantite bars (do_forge unblocked)

**Schema notes from 0.4.15 (Code's findings):**
- `do_storm` — class+dance gate (indices 16/34/52 + `pcdata->dance == 2`). Mana cost 150.
  AOE iterator: 1 hit always, +1 if number_percent > 50, +2 if > 90 (up to 3 per target).
- `do_charge` — `gsn_wary` cooldown via `effect_to_char` — NEW mechanic. Victim wary-mark
  (level=101, duration=10) on HIT against PCs. Caster-side gate also checks gsn_wary.
  Alert flag at byte 0x17c bit 0x40 (unique per port — never reuse another port's offset).
- Alert flag table now confirmed: every STRIKE-PURE has a different byte+bit combo.
  Pull fresh from disasm for every new port.

**New from Cowork planning session (2026-04-28):**
- FTUE helpfiles expanded to 17 drafted (added LEVEL, AREAS, GEAR, TOWN_CENTER, GUILDS, TICK, AREA_RESET). All cross-referenced. NEWBIE updated with full "good first steps" chain.
- Helpfile keyword convention confirmed: underscores for multi-word (TOWN_CENTER, AREA_RESET).
- dummies.are vnum range shifted to **89000–89099** (9000 range was taken). Files updated. Bundle B ready to deploy.
- Hint system investigation added to Bundle A+ — find do_hint, locate hint data file, report format to Cowork.
- New IDEAS logged: IDEA-023 (PvE mode — Sanctuary formula, half damage both ways, yield bonus), IDEA-024 (player count in status bot), IDEA-025 (area reorganization — tiered by distance/difficulty, gear meta at levels 30/85/hero).
- Patch notes workflow confirmed: Code writes player-facing entry in PATCH_NOTES.md before telling Kyle to copyover. Kyle runs post_patch_notes.py after.
- Autonomous mode: Kyle has given permission to chain functions without pausing between ports. Only stop for: unresolvable blocker, copyover-ready staged build.

**All previous tasks resolved:**
- ✅ STRIP-SELF cluster (do_rub, do_deepbreathing, do_cleanse) — live 0.4.12
- ✅ add all (IDEA-008) — live 0.4.10
- ✅ Morpheous skills + ratings (Rex) — live 0.4.12
- ✅ Bot system (ds_bot.py + bot_personality.py) — live 0.4.13
- ✅ botspawn / botquit imm commands — live 0.4.13
- ✅ do_storm — staged 0.4.15
- ✅ do_charge — staged 0.4.15

**Next:** `do_dance` is priority within CLASS ABILITY tier — it sets `pcdata->dance`
which gates do_storm. Port it first so storm is testable end-to-end by Wardancer-class players.

**⚠️ Rex parallel contributor:** Git pull before touching `const.c` or `act_combat.c`.

---

## Current tasks (priority order)

---

### ~~Priority 1 — STRIP-SELF cluster~~ ✅ Done in 0.4.12
### ~~Priority 1 — `do_storm`~~ ✅ Done in 0.4.15
### ~~Priority 3 — `do_charge`~~ ✅ Done in 0.4.15

---

### Priority 1 — `do_dance` (1282b) — PORT THIS FIRST

Sets `pcdata->dance` — this is what gates `do_storm` for Wardancer-class players.
Has a `dance_table` lookup (multiple dance names), `gsn_dance_of_the_devil`,
and `affect_strip` to cancel previous dance. 1282b — moderate complexity,
lots of `str_prefix` calls to parse the dance name argument.

```bash
objdump -d ~/ds/recovered/devils/bin/ds | grep -A 700 "<do_dance>:"
```

**Key unknowns:**
- How many dances are in the table and what are their names?
- Does it set `pcdata->dance` as an int index or by affect?
- What value does Storm Dance set? (Expected: 2, per do_storm disasm)
- Does cancelling a dance strip the affect and zero the field?

Port `do_dance` before `do_jab` / `do_throw` / `do_hurl`.

---

### ⚠️ Before CLASS ABILITY tier — verify `pcdata->dance` offset

do_storm assumes `pcdata->dance` lives at offset `0xf6c`. If layout has
drifted, the storm dance gate misfires silently. Quick check before
porting any further dance-class abilities:

```c
printf("dance offset: %zu\n", offsetof(PC_DATA, dance));
```

Or compute manually from merc.h field order. Report confirmed offset in
`CODE_HANDOFF.md` before proceeding to `do_dance`.

---

### Priority 3 — CLASS ABILITY tier (ROT 1.4 source + disasm diff)

Port in this order. Each has a public ROT 1.4 source equivalent — use it
as the starting template, then disasm the DS symbol to catch tweaks.

```bash
objdump -d ~/ds/recovered/devils/bin/ds | grep -A 600 "<do_charge>:"
# repeat for each symbol
```

| Function | Size | Key unknowns vs ROT 1.4 |
|---|---:|---|
| `do_charge` | 833b | Damage formula, position requirement |
| `do_jab` | 1080b | STANDING gate (not FIGHTING), mana/move cost |
| `do_throw` | 1247b | Item-type gate (what can be thrown?), trajectory |
| `do_dance` | 1282b | DS dance state — sets `ch->pcdata->dance`? Feeds into do_storm |
| `do_hurl` | 2477b | Largest — defer until others confirmed |

**Important:** `do_dance`'s implementation determines what `do_storm`'s
precondition is checking. Port `do_dance` before finalising `do_storm`
if the disasm isn't clear about the gate field.

Patcher: `port_class_ability.py` (one function per section).

---

### Priority 4 — DS Custom Other (small → big)

After CLASS ABILITY tier, work through the remaining DS CUSTOM functions
in size order. All are hand-decompile from disasm — no public source template.

Run `objdump` on each before writing:
```bash
objdump -d ~/ds/recovered/devils/bin/ds | grep -A <N> "<do_FUNCNAME>:"
```

**Order:**

| Function | Cmd | Size |
|---|---|---:|
| `do_roundhouse` | roundhouse | 339b |
| `do_powerinvuln` | powerinvuln | 428b |
| `do_plantroots` | plantroots | 500b |
| `do_powerstun` | powerstun | 529b |
| `do_quickening` | quickening | 568b |
| `do_caltrops` | caltrops | 585b |
| `do_healing_touch` | htouch | 598b |
| `do_dislodge` | dislodge | 631b |
| `do_powerblind` | powerblind | 641b |
| `do_transfix` | transfix | 701b |
| `do_thousand_wounds` | thousand wounds | 704b |
| `do_gash` | gash | 748b |
| `do_eadbutt` | eadbutt | 771b |
| `do_devils_touch` | devils touch | 776b |
| `do_earthbind` | earthbind | 797b |
| `do_scream` | scream | 801b |
| `do_shuriken` | shuriken | 812b |
| `do_feed` | feed | 813b |
| `do_bastion` | bastion | 815b |
| `do_strangle` | strangle | 825b |
| `do_chaos_blow` | chaos blow | 870b |
| `do_toss` | toss daggers | 892b |
| `do_hack` | hack | 959b |
| `do_ambush` | ambush | 967b |
| `do_pinch` | pinch | 1018b |
| `do_blackjack` | blackjack | 1018b |
| `do_blinding_strike` | blinding strike | 1022b |
| `do_assassinate` | assassinate | 1148b |
| `do_shield_smash` | smash | 1169b |
| `do_forge` | forge | 1200b |
| `do_aura` | aura | 1452b |
| `do_stance` | stance | 1479b |
| `do_vital_strike` | vital strike | 1690b |

Batch into patcher scripts by size cluster — group the ≤600b functions
together, then the 600–900b cluster, etc. One patcher per cluster.

---

### Priority 5 — Monk class

`do_deepbreathing` is in the STRIP-SELF batch (Priority 1). The remaining
Monk functions and helpers:

| Function | Size |
|---|---:|
| `do_katana` | 748b |
| `do_buddha_palm` | 842b |
| `do_chi` | 1042b |
| `monk_backfist` (helper) | 113b |
| `monk_elbow` (helper) | 113b |
| `monk_knee` (helper) | 113b |
| `monk_palmstrike` (helper) | 113b |
| `monk_shinkick` (helper) | 113b |
| `monk_thrustkick` (helper) | 113b |
| `monk_reverse` (helper) | 192b |
| `monk_spinkick` (helper) | 203b |
| `multi_kick` (helper) | 383b |

Port `multi_kick` last — it calls all the `monk_*` helpers and won't
link correctly until they're all real implementations. Port the helpers
first, smallest to largest, then `multi_kick` as the capstone.

---

### Priority 6 — Voodoo class

| Function | Size |
|---|---:|
| `do_voodoo` (dispatcher) | 274b |
| `do_jinx_palm` | 1096b |
| `voodoo_pin` (helper) | 519b |
| `voodoo_trip` (helper) | 533b |
| `voodoo_throw` (helper) | 814b |

Port the helpers first (`voodoo_pin`, `voodoo_trip`, `voodoo_throw`),
then the `do_voodoo` dispatcher which calls them, then `do_jinx_palm`.

---

### Priority 7 — Psionics (last)

These are the four largest functions in `act_combat.o`. Defer until all
other priorities are complete.

| Function | Cmd | Size |
|---|---|---:|
| `do_biomanipulation` | biomanipulation | 2418b |
| `do_electrokinesis` | electrokinesis | 3511b |
| `do_telekinesis` | telekinesis | 3536b |
| `do_pyrokinesis` | pyrokinesis | 3807b |

---

## Priority 8 — Room Pathfinding System

BFS-based pathfinding across the DS world graph. Three deliverables:

### A. Python utility — `build_world_graph.py`

Parse all `.are` files from `~/ds/recovered/devils/data/area/` and build
a vnum→exits dict. Export as `world_graph.json` (or equivalent).

```python
# Target interface
from world_graph import pathfind
steps = pathfind(8084, 3001)   # → "1n2e4d" or ["n","e","e","d","d","d","d"]
```

- Direction keys: n/s/e/w/u/d
- Skip impassable exits (door flags: EX_CLOSED|EX_LOCKED — flag these
  as optionally traversable, not hard-blocked, since imms/mobs ignore locks)
- Handle one-way exits correctly (exit only stored on source room)
- Integrate into `ds_bot.py`: replace hardcoded PATROL_ROUTE with
  `pathfind(current_vnum, target_vnum)` when dynamic routing is needed

### B. Imm command — `do_pathfind` (act_wiz.c)

```
pathfind <vnum>              — print walk from your location to vnum
pathfind <mob_name> <vnum>   — start named mob walking toward vnum
```

- Self form: BFS on the in-memory room graph (follow `exit[d]->to_room`
  pointers), print result as `"Route: 2n 1e 3d"` to imm only.
- Mob form: validate mob is in the same connected graph, then set
  `mob->path_dest` and populate `mob->path_buf[]` with direction chars.
  `mobile_update()` checks path_buf each pulse — if set and mob not
  fighting, pop next direction char and call `do_move`.

Level gate: 107 (same as botspawn). LOG_ALWAYS.
Patcher: `add_pathfind_cmd.py`. Sentinel-checked, atomic backup.

### C. Mprog command — `mpwalk`

New mprog opcode `mpwalk <vnum>`:
- Same logic as mob-form of `do_pathfind` — set path_dest + path_buf.
- Fires from any mprog trigger (greet, fight, death, timer, etc.)
- Lets area builders script patrol routes, chase sequences, ambush walks
  without imm involvement.
- Example mprog use:
  ```
  >greet_prog 100~
  mpwalk 3001
  ~
  ```

### Schema delta required

Add to `CHAR_DATA` (merc.h):
```c
sh_int   path_dest;          /* vnum mob is walking toward; 0 = idle */
char     path_buf[64];       /* remaining direction chars, null-terminated */
int      path_pos;           /* current index into path_buf */
```

Only mobs use these fields — mortal/imm chars always have path_dest = 0.
`mobile_update()` guard: `if (IS_NPC(ch) && ch->path_dest != 0 && !ch->fighting)`.

### Design constraints (Kyle's call)

- **Mobs do NOT self-initiate pathfinding** — no autonomous AI. A mob
  only paths if an imm command or mprog sets it in motion.
- Guardian-style patrol is scripted via mprog, not an ACT_ flag.
- No per-mob re-path on target move — path is computed once at trigger
  time. If mob gets blocked (closed door, etc.), it stops and path_dest
  clears. Re-trigger via mprog or imm if needed.

### Build order

1. ✅ `build_world_graph.py` + pathfind() — written by Cowork, in workspace folder.
   **Code: copy to `~/ds/` and run:**
   ```bash
   python3 ~/ds/build_world_graph.py
   python3 ~/ds/build_world_graph.py --pathfind 8084 8097   # test TC route
   python3 ~/ds/build_world_graph.py --pathfind 8084 3001   # test cross-zone
   ```
   Verify room count looks sane (DS world should be several thousand rooms).
   Report any parse failures in CODE_HANDOFF.md.

2. `add_pathfind_cmd.py` — C patcher (merc.h delta + act_wiz.c + interp.c
   + mobile_update hook)
3. mpwalk opcode — C patcher (interp_mob.c or equivalent mprog dispatch)

---

## Queued non-combat tasks (do when there's a natural break between batches)

### Bundle C — FTUE Helpfile rewrite (content task, no C changes)

Helpfile drafts are in `FTUE_HELPFILES.md` in the workspace. Ten files,
priority ordered. These replace the terse 2003 stubs currently in the
DS help system.

**⚠️ Before replacing any helpfile, rename the original:**
Append `_OLD` to the keyword of the existing entry so it's preserved
for legacy reference. Example: `NEWBIE` → `NEWBIE_OLD`. This lets us
roll back or compare without losing the originals.

**Implementation steps:**
1. Find the helpfile location:
   ```bash
   grep -rn "NEWBIE\|newbie" ~/ds/recovered/devils/data/ | head -10
   ```
2. For each of the 10 helpfiles in `FTUE_HELPFILES.md`:
   a. Find the existing entry by keyword.
   b. Rename it to `<KEYWORD>_OLD` in the file.
   c. Insert the new entry from `FTUE_HELPFILES.md` above it.
3. No compile needed — help files are data. Reload or copyover to test.
4. In-game: type `help newbie`, `help classes`, `help combat` etc.
   and verify each renders correctly.

No patcher needed for this — direct file edit is fine since help files
are plain text. Back up the help file before editing.

**Helpfiles to implement (in order):**
NEWBIE, CLASSES, COMBAT, RECALL, SKILLS, DEATH, PVP, EQUIPMENT,
NAVIGATION, SCORE, LEVEL, AREAS, GEAR, TOWN CENTER, GUILDS

(FTUE_HELPFILES.md now has all 15 drafted — priorities 1–15.)

---

### Bundle A+ — Hint system investigation (trivial, no C changes likely)

DS:R veterans remember a hint message appearing on each tick — a broadcast
tip to all players. This was useful both as a tick clock and as FTUE info.

**Code tasks:**
1. Check if `do_hint` exists in the command table:
   ```bash
   grep -rn "do_hint\|\"hint\"" ~/ds/recovered/devils/src/ ~/ds/src_patched/
   ```
2. Find the hint data file:
   ```bash
   find ~/ds/recovered/devils/ -name "*.txt" -o -name "*.hlp" | xargs grep -l -i "hint" 2>/dev/null
   ```
3. Check `update.c` or `handler.c` for the tick broadcast:
   ```bash
   grep -n "hint" ~/ds/src_patched/update.c ~/ds/src_patched/handler.c
   ```
4. Report to Cowork: is it present/disabled/missing? What's the hint file
   format? Cowork will write the tip content once the mechanism is confirmed.

If the hint system is intact but the file is empty or missing, just report
the file path and format — Cowork will populate it with FTUE-friendly tips.

---

### Bundle A — trivial, no design questions (slip into any build)

- **`version` command** — patch `act_info.c` to print the current project
  version string. Define `DS_VERSION_STRING` in `merc.h`, bump per build.
  IDEA-006, complexity trivial.
- **Wizlist `.gitignore`** — add `devils/data/misc/wizlist.txt` to `.gitignore`
  so the runtime-touched file stops appearing in `git status` every session.
  One line, no compile needed.
- **`botspawn` helpfile** — find the help file location with:
  `grep -r "wizhelp\|do_wiz" ~/ds/recovered/devils/data/ | head -5`
  Entry should cover: syntax, what it does, known bot names, how to stop
  bots (`botquit all` / `pkill`), log location (`/tmp/ds_bot_*.log`).
  Content-only, no C changes.

These three can ship in a single non-binary commit or alongside any build.

---

### Bundle B — `dummies.are` training hall (medium, content task)

**Location:** South from vnum 33100 (Guildmaster Hall — north side leads
to individual guildmaster rooms). Mirrors that layout: a south corridor
with each dummy in their own named chamber off it.

**Vnum range confirmed free: 89000–89099.**
Kyle ran the grep — top of world is 88065, 89000 range is clear.

**Room layout (straight south corridor, one dummy per chamber):**

```
         [33100 Guildmaster Hall]
                  |  (new south exit)
         [9000 The South Hall]  ← entry/hub
                  |
         [9001 The Resilience Chamber]  — Hit Pillow mob
                  |
         [9002 The Bulwark Chamber]     — Iron Maiden mob
                  |
         [9003 The Warded Chamber]      — Warded One mob
                  |
         [9004 The Arena Chamber]       — The Slammer mob
```

**Dummy stat profiles (one stat focus each, no mixed stats):**

| Dummy | HP | AC | Hitroll | Damroll | Saves | Offense |
|---|---:|---:|---:|---:|---:|---|
| Hit Pillow (9001) | 100,000 | 0 | 0 | 0 | 0 | none |
| Iron Maiden (9002) | 10,000 | −1000 | 5 | 5 | 0 | minimal |
| Warded One (9003) | 10,000 | 0 | 5 | 5 | −200 all | minimal |
| Slammer (9004) | 10,000 | 0 | +100 | +100 | 0 | hits hard |

All dummies: `ACT_NOEXP ACT_NOLOOT ACT_SENTINEL`. Reset on area tick.
No wander, no flee.

**`dummies.are` is drafted by Cowork and sitting in the workspace.**
Patcher `patch_add_dummies_area.py` adds the south exit to room 33100
and registers `dummies.are` in `area.lst`. Sentinel-checked, atomic backup.

**Code tasks:**
1. Confirm 9000–9099 is clear (grep above)
2. Copy `dummies.are` from workspace to `~/ds/recovered/devils/data/area/`
3. Run `patch_add_dummies_area.py`
4. `make` + copyover
5. In-game: walk south from guildmaster hall, verify all four chambers load

---

## Patch notes workflow

`PATCH_NOTES.md` (workspace folder) is the player-facing patch notes archive.
Newest entry at top. Format:

```
---

## v0.X.Y — YYYY-MM-DD

🩸 **Devil's Silence Resurrected — vX.Y**

<player-facing description of what changed>

Server: `7.tcp.ngrok.io:25597`

---
```

**Tone rules for patch note entries:**
- Open with `🩸 **Devil's Silence Resurrected — vX.Y**`
- Write for players who have never read source code. No function names, no offsets.
- Describe what the player *feels* — "now you can", "you'll notice", "this used to crash, it doesn't"
- Use bold for new command names. Use code backticks for commands they type.
- Keep it punchy. Two sentences per feature is plenty. No walls of text.
- Emojis are fine for bullet headers (✅ ⚔️ 🛡️ 🐛) — match the energy of the existing entries.
- Close with: `Server: \`7.tcp.ngrok.io:25597\``

**After every build that goes live:**
1. Prepend a new entry to `PATCH_NOTES.md` following the format above.
2. **Commit and push `PATCH_NOTES.md` to GitHub** as part of the build commit — this is what gets it to Kyle's server. If it's only written locally in the workspace, the server won't see it.
3. Drop a summary in `CODE_HANDOFF.md` so Cowork can review tone before posting.
4. Kyle runs `git pull` on the server, then `python3 ~/ds/post_patch_notes.py` to post the newest entry to Discord. Script auto-skips already-posted versions.

**Catching up on multiple unposted versions:**
- `python3 ~/ds/post_patch_notes.py --all` — posts everything from v0.4.4 onward, oldest-first, skipping already-posted.
- `python3 ~/ds/post_patch_notes.py --from v0.4.x` — starts from a specific version.
- State lives in `/tmp/ds_patchnotes_state.json` — safe to re-run.

**If PATCH_NOTES.md was written in Cowork but not yet on the server:** Code should pull from the workspace path at `/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/PATCH_NOTES.md`, commit it, and push.

---

## Deploy reminder (every build)

```bash
cp --remove-destination ~/ds/src_patched/ds.new ~/ds/recovered/devils/bin/ds.new
md5sum ~/ds/recovered/devils/bin/ds.new   # verify matches staged md5
# then copyover in-game: type 'copyover' as an Executive-level char
```

---

## One-time housekeeping task

**Move CLAUDE.md to repo root** — it currently lives in `claude_code_setup/`
which Claude Code does not auto-read. Move it so all sessions pick it up:

```bash
cp "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/claude_code_setup/CLAUDE.md" \
   ~/ds/CLAUDE.md
# or wherever the repo root is
git add CLAUDE.md
git commit -m "Move CLAUDE.md to repo root so Claude Code auto-reads it"
```

Also: `VISION.md` is now in the workspace folder. Copy it into the repo
so Rex gets it on next pull:
```bash
cp "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/VISION.md" \
   ~/ds/VISION.md
git add VISION.md
git commit -m "Add VISION.md — PvP/PvE symbiosis design philosophy"
```

---

## Standing instructions

- Read `DS_SCHEMA.md` before writing any new act_combat function.
- All patchers: sentinel check, atomic backup, surgical edit.
- Disasm the target symbol *before* writing the C. Never assume it matches
  a ROM/ROT template — DS always has tweaks.
- Mark functions STAGED in `CODE_HANDOFF.md` after building. Do NOT mark
  IMPLEMENTED — that's Kyle's call after in-game verification.
- After every build: overwrite `CODE_HANDOFF.md` with md5, what changed,
  variability findings, test plan, and suggested next step.
- Log schema deltas to `DS_SCHEMA.md` directly, or note them in
  `CODE_HANDOFF.md` so Cowork can update it.
- Do a `git pull` before touching `const.c` or `act_combat.c` — Rex
  may have pushed morpheous changes.
- **After every build, sync changed source files to the workspace** so
  Cowork can read them directly without relying on disasm notes:
  ```bash
  cp ~/ds/src_patched/act_combat.c "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/recovered/devils/src/act_combat.c"
  cp ~/ds/src_patched/fight.c      "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/recovered/devils/src/fight.c"
  cp ~/ds/src_patched/act_move.c   "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/recovered/devils/src/act_move.c"
  ```
  Add any other frequently-edited files as the project grows.

## How Cowork ↔ Code ↔ server sync works

- **Cowork writes files to the local workspace folder** (this folder).
  Code shares the same local filesystem and can read them directly —
  no git or copy step needed between Cowork and Code.
- **GitHub is for Rex/external collaboration only.** Cowork cannot push
  to git. Code pushes to GitHub when Rex needs the changes.
- **Server is separate.** Scripts Cowork writes reference server paths
  (`~/ds/src_patched/`) — Code either SCPs them to the server or applies
  the equivalent changes directly. Kyle then runs `git pull` + the script.
- **Cowork's job:** write the script/file + a brief note in `CODE_HANDOFF.md`
  pointing to it. Code reads the script itself — don't over-document in
  the handoff. One line on what it does is enough.
