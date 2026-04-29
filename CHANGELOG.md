# Changelog

All notable changes to Devil's Silence Resurrected. Format inspired by
[Keep a Changelog](https://keepachangelog.com/) — semver-style versions
(MAJOR.MINOR.PATCH), most recent at the top, grouped by Added / Changed
/ Fixed / Removed / Deferred.

**Version scheme:**

- `MAJOR` — bumped at major project milestones (e.g., 1.0 = first
  publicly playable release with stable combat)
- `MINOR` — bumped per Phase boundary (0.2 = Phase B Step 1, 0.3 =
  Phase B Step 2, 0.4 = Phase B Step 3, etc.)
- `PATCH` — bumped per copyover-deploy

The `0.x` series signals we're pre-release / work-in-progress.

When something breaks, this file is the first place to look — find the
last known-good version, compare against the current build's notes,
narrow down the suspect change.

---

## [Unreleased / Staged]

### 0.4.15 — staged build md5 `a7d66b8998950835d3fcea6ec577dc02`

`do_charge` ported (Cowork Priority 3 — first of CLASS ABILITY tier).
Bundled on top of 0.4.14's do_storm. Staged at
`~/ds/recovered/devils/bin/ds.new`. Awaiting copyover.

#### Added
- **`do_charge`** (CLASS ABILITY single-target, 833b at `0x5966`).
  Body-slam opener — explicit-target via `one_argument` +
  `get_char_room`, can't initiate while in combat. Mostly garotte-
  shaped (HP-frac /3, AFF2 bit-15 halver, sleeping auto-HIT,
  multi_hit, gangbanger wait-doubler) plus two NEW DS-specific
  mechanics:
  1. **`gsn_wary` cooldown gate** — `is_affected(ch, gsn_wary)`
     blocks the cast (bypassed by IMM trust).
  2. **Victim wary-mark on HIT** — `effect_to_char(victim, &af)`
     with `gsn_wary`, hardcoded level=101, 10-tick duration. PCs
     only (no point marking mobs).
  3. **Alert flag at byte 0x17c bit 0x40** — yet another per-port
     victim-alert flag location. Adds to the schema delta.
  4. **MISS broadcast only on alert** — silent miss otherwise.
  Patcher: `port_charge.py`.

#### Schema deltas
One amendment to existing rows:
- "STRIKE-PURE victim-alert flags vary across cluster" — add
  do_charge's byte 0x17c bit 0x40. Full table now: cleave (none),
  cross_slash (0x17e/0x40), garotte (AFF2 bit15 halver), strike
  (0x17d/0x2), charge (0x17c/0x40). Confirms the "every port has
  a different alert byte/bit" heuristic.

---

### 0.4.14 — staged build md5 `16195e65ef94d8e4df139335e87c0287`

`do_storm` ported (Cowork Priority 2). Staged at
`~/ds/recovered/devils/bin/ds.new`. Awaiting copyover.

#### Added
- **`do_storm`** (STRIKE-PURE AOE, 610b at `0x11c2e`). Per-target
  variable-swing AOE iterator matching `do_whirlwind` (1 hit always
  + 1 more if percent > 50 + 2 more if percent > 90 — up to 3 swings
  per target). Patcher: `port_storm.py`.

#### Schema deltas
Three new `DS_SCHEMA.md` Discovered-deltas entries:

1. **Class + Dance precondition (do_storm)** — for class indices 16,
   34, 52 (the dance-using monk variants), `do_storm` requires
   `pcdata->dance == 2` (Storm Dance state) unless IMM. Other
   classes pass through. NEW pattern: stance/dance state as a class-
   conditional gate. Uses pcdata field at byte offset 0xf6c which
   maps to the `dance` field in `pc_data` per merc.h:1603.
2. **STRIKE-PURE AOE with mana cost** — most STRIKE-PURE AOE are
   free or move-cost (legsweep/dhammer/stomp/whirlwind). Storm is
   the first that costs **150 mana** (gate: `mana > 249`, cost
   subtracted after gate). Distinguishes "weapon-skill AOE" from
   "magical-style AOE" within the cluster.
3. **"Huh?" as the standard `get_skill <= 0` reply** — most ports
   use a verb-specific message ("You strike a pose.", "Grow some
   horns first.", etc.). do_storm and do_cleanse both use the
   generic "Huh?" — same string at `str1.1:0x5e`. Worth noting as
   the catch-all unknown-command idiom; either form is disasm-faithful
   per port.

---

### 0.4.13 — bot system overhaul + in-game `botspawn`

Bundled binary + Python tooling release for the PvP bot system. Live
binary at `~/ds/recovered/devils/bin/ds.new` (md5 covers do_botspawn /
do_botquit C wrappers; the bot logic itself is host-side Python that
hot-reloads on `stop_bots.sh && start_bots.sh`).

#### Added (in-game)
- **`do_botspawn`** (act_wiz.c, imm 107+) — forks a Python bot via
  `popen(python3 ds_bot.py --bot <name> --patrol &)` so imms don't
  need a shell. Validates names against the BOT_ROSTER list.
- **`do_botquit`** — `pkill -f ds_bot.py --bot <name>` (or `all`).
  Bots receive SIGTERM, run their clean-quit handler.
- Both registered in `interp.c` cmd_table; prototypes live in
  `interp.h` via `DECLARE_DO_FUN` (initial patcher landed them at
  the wrong location below the cmd_table — fixed inline, will fold
  back into add_botspawn_cmd.py next pass).

#### Bot lifecycle behaviors (ds_bot.py)
- **Incoming-attack detection** — new `INCOMING_DAMAGE_RE` and
  `INCOMING_ATTACK_RE` so the bot enters combat mode when hit, not
  only when it lands an attack. Previously stood still while taking
  damage if the other side opened.
- **Bow detection** rewritten — DS's TO_VICT bow social is `"$n bows
  before you."` (not `"...before $N."`). The old regex only matched
  the third-party form, so the bot literally never saw a bow at it.
- **Buff retry budget** — `state.buff_attempts` + `given_up_buffs`.
  After 3 failed attempts at a buff, the rotation marks it "given
  up" and advances. Reset on combat-end. Stops the bot looping
  forever on `berserk` when the MUD's combat-lag system blocks the
  cast ("You have far more lethal things to worry about!").
- **Idle vs combat rotation split** — buffs gate on `not s.in_combat
  and not s.has_buff(...)`, combat skills gate on `s.in_combat`.
  Pre-fight prep happens during patrol; combat is bash/kick/trip
  only, no wasted in-fight buff attempts.
- **PK flag detection** in prompt regex (optional `<PK>` prefix).
- **Cot recovery** — when PK timer clears with HP < 85%, bot recalls
  to temple, walks 1n into cots (8071), `sleep cot` until 95% HP,
  then `recall_to_solennir()` back to TC. Doesn't fall back to floor-
  rest if the cot navigation fails — Kyle's call: don't rest unless
  in the cot.
- **Death + corpse retrieval** — wait 120s for death lag, stand from
  cots, walk patrol corridor (s,s,e×6,w×12,e×6) scanning each room
  for `"corpse of <bot_name>"`. On match: `get all <BotName>` (uses
  bot's name as container keyword — only matches own corpse, never
  another player's drop) + `wear all`. Combat re-engagement breaks
  the search cleanly.
- **Proactive challenges** — when a non-bot player walks into the
  bot's room while patrolling and idle, 40% chance + 30s cooldown
  to bow at them. If they bow back, treated as acceptance — no
  second bow, just engage after a 1.5s ceremony.
- **Equip gear** — `wear all` fires every 60s while idle, also right
  after corpse pickup. Stops the "naked warden running around with
  gear in inventory" problem.
- **Personality-driven gear priority** — each PersonalityTemplate
  in `bot_personality.py` carries a `gear_priority` hint:
  Aggressive/GlassCannon → `hitdam`, Cautious → `ac`, Brawler →
  `balanced`, Technical → `saves`. Phase 2 (stat-comparison loadout
  optimizer) hooks are commented in ds_bot.py — needs `inventory`
  parser + per-item `look <item>` parser + per-slot swap logic.
- **Flame channel for death/flee** — passive-aggressive lines on the
  `flame` channel after a death or successful flee. Per-bot lists in
  `BOT_ROSTER`. Kyle's note: no caps in global channels — all yells/
  flames are sentence-cased.
- **Taunt cadence 60–90s random** (was every-10s, way too spammy).
- **Clean quit on SIGTERM/SIGINT** — `quit_clean()` sends `flee`
  (if in combat) + `quit` + 2s sleep before tearing down the socket.
  Stops `pkill` / `botquit` from leaving the char link-dead.
- **State reset on session restart** — broken-pipe reconnects had
  been carrying `combat_state = IN_COMBAT` into the new session,
  causing rotation to fire at the login prompt. Fresh BotState now
  re-allocated at session start.
- **`already playing` Y/N handler** — auto-sends `y` to force-
  reconnect after a stale TCP connection on the MUD side.
- **Line logging** in `_process_queue` — every parsed event tagged
  `[event_name]` in the log so we can grep `[buff_gained:berserk]`,
  `[incoming_attack]`, `[corpse_spotted]` etc. for behavior tracing.

#### Added (workspace)
- **`BOTS.md`** — full operator's helpfile (first-time setup,
  start/stop scripts, in-game `botspawn` command, bot roster, modes,
  customization, troubleshooting). Doc shipped earlier this session.

#### Notes
- `add_botspawn_cmd.py` patcher itself has the prototype-placement
  bug noted above (writes prototypes mid-`interp.c` instead of into
  `interp.h`). Manual fix is in the source tree; regenerating the
  patcher to match would be a clean follow-up.
- Phase-2 gear comparison is the obvious next bot improvement —
  needs the inventory + item-look parsers.

---

### 0.4.12 — staged build md5 `6a51b9cf2bd912030f780842f8e4df24`

STRIP-SELF cluster (Cowork Priority 1). Three small DS-custom self-cast
functions ported in one batch via `port_strip_self.py`. Staged at
`~/ds/recovered/devils/bin/ds.new`. Awaiting copyover.

#### Added
- **`do_rub`** (552b at `0x559e`) — counters `do_dirt`'s AFF_BLIND.
  Only removes blindness sourced from one of: fire breath, dirt
  kicking, blinding strike, eadbutt. Other forms of blindness bail
  with "Rubbing your eyes won't help that injury." Chance starts at
  skill/2, then ± dex deviation from 15 (penalty capped at -5),
  +10 if AFF_HASTE, -5 if AFF_SLOW. On HIT, calls `affect_strip` for
  all four candidates regardless of which one applied (idempotent).
  Confirmed `do_dirt` applies AFF_BLIND at line 1276; the schema
  delta about `affected_by` at offset 0x170 (AFF_BLIND bit 0) and
  AFF_HASTE/AFF_SLOW at bytes 0x172/0x173 bit 0x20 was already
  documented in the do_kick port comment.
- **`do_deepbreathing`** (286b at `0x1275e`) — toggle buff. If already
  affected, `affect_strip` + "You stop breathing so deeply." Otherwise
  rolls (chance halved if `ch->fighting != NULL`); on HIT, applies
  a permanent (`duration = -1`) marker affect with no stat modifier
  and no bitvector. The buff's effect is presumably checked elsewhere
  via `IS_AFFECTED(ch, gsn_deepbreathing)` for a passive bonus.
- **`do_cleanse`** (444b at `0x1ec6`) — multi-affect dispel chain.
  Costs 200 mana. Computes `level_eff = chance * ch->level / 100`,
  then runs `check_dispel` against poison (always), plague (if
  level_eff > 30), and curse (if level_eff > 50; looked up by name
  via `skill_lookup` since gsn_curse may not be a fixed extern).
  Each successful dispel fires a 2-line broadcast (TO_CHAR private +
  TO_ROOM act); the curse branch is silent (disasm-faithful, possibly
  an oversight in the original).

#### Per-port note (none new for DS_SCHEMA)
The `is_affected(ch, skill_lookup("name"))` pattern in `do_rub` and
the `check_dispel` chain in `do_cleanse` are both already in the
codebase from earlier ports, so no new schema rows. The "permanent
marker affect" pattern in `do_deepbreathing` (duration = -1, no stat
modifier) is also seen elsewhere — useful to note as a class of
buff-self mechanic but not a structural delta.

---

Rex's morpheous rating fix. Staged at `~/ds/recovered/devils/bin/ds.new`.
Awaiting copyover.

#### Added (Rex)
- **Six morph skills now buyable + practicable** —
  `apply_rex_morph_ratings.py` applies Rex's
  `rexdev/fix-morpheous-rating.patch`. Sets `rating[Chg=47] = 2` on
  the same six morph skills enabled in 0.4.10 (advanced dopple,
  chameleon, dopple, form memory, grow parts, mutate body). With
  rating = 0 the `rating[ch->pclass] < 1` filter rejected them from
  every add path; now each costs 2 CP and is buyable/practicable.
  Patch via Python (skill-name-anchored) because Rex's unified diff
  uses pre-edit line numbers and hunk #6 fails to locate even with
  fuzz; same name-anchor pattern as `apply_rex_morph_skills.py` from
  0.4.10. Companion to 0.4.10's level-enable.

---

## [0.4.10] — 2026-04-27

md5: 868d6ee31cf80602737550a69802eeae. Verified in-game by Kyle 2026-04-27.

### 0.4.10 — verified build

#### Changed
- **`exp_per_level()` clamped at 10000.** Per Kyle: the 10k value
  should be a TNL ceiling, not a gate. The function previously had no
  upper bound — each ~20 points doubled the inc accumulator. Now wraps
  the final return in `UMIN(..., 10000)` so the per-level XP plateaus
  at 10k regardless of how many skills/groups are bought. The cap-gate
  check at the single-target `add <skill>` callsites becomes
  permanently false (dead code; left in place for clarity, harmless).
  Patcher: `clamp_exp_per_level.py`.

(Prior staged md5s for this release: `8342a1d09…` was v3 with
sort-by-cost + cap-skipped reporting; `ec8457d2…` was v3.1 removing
the cap from `add all`. The clamp above supersedes both — `add all`
now adds everything AND the XP curve plateaus.)

`add all` real fix + cap relaxed for bulk-buy + Rex's morpheous skill
levels. Staged at `~/ds/recovered/devils/bin/ds.new`. Awaiting copyover.

#### Changed (IDEA-008 v3.1)
- **`add all` no longer gates on the 10000 TNL threshold.** Per Kyle:
  the 10k cap should be a soft TNL ceiling, not a restriction on which
  skills can be added. v3.1 (`relax_addall_cap.py`) removes the cap
  check from the bulk-buy loops. Every eligible group + skill gets
  purchased. The single-target `add <skill>` path keeps the cap (those
  are individual purchase decisions, not bulk). Sort-by-cost ordering
  is preserved for cosmetic correctness if the cap is ever re-added.

#### Fixed
- **`add all` no longer silently drops skills** (IDEA-008 v3, fixes the
  warrior-leftover-list reported 2026-04-26: rescue, sixth attack,
  smother, spirit, trip, warcry, 3rd/4th/5th dual). Root cause was the
  v2 implementation iterating `skill_table` by index `sn` ascending —
  once running `points_chosen` hit the 10000 TNL cap, all subsequent
  items got silently `continue`d past, regardless of cost. Whichever
  skills happened to sit at higher indices got skipped, including cheap
  ones that would have fit if purchased earlier. Affected every class.
- v3 collects every eligible group/skill, **sorts by CP cost ascending**
  (selection sort, in-place), then buys in that order until the cap
  rejects. Cheap skills always succeed first; expensive ones that don't
  fit are reported by name in a "Skipped N items (would push over CP
  cap): rescue, trip, …" message so the user knows what to drop and
  retry. Cap preserved per IDEA-008 spec. Patcher:
  `fix_add_all_sort_by_cost.py`.

#### Added (Rex)
- **Six morph-class skills enabled at mortal levels** — applied
  Rex's `rexdev/morpheous_skills.patch` via
  `apply_rex_morph_skills.py` (Rex's diff format had malformed hunk
  line counts, so GNU `patch` choked; the Python patcher does the same
  six edits via skill-name-anchored substitutions). For class index 47
  (Chg / morpheous / changeling): `advanced dopple` → 40, `chameleon`
  → 1, `dopple` → 1, `form memory` → 20, `grow parts` → 1, `mutate
  body` → 40. Was IMM-only; now learnable as a mortal morpheous.

---

---

## [0.4.9] — 2026-04-26

md5: e02e7209bd720bf9851edf9dde3c5df5. Verified in-game by Kyle.

`port_strike_extended.py` (do_strike + do_gore), Rex's `const.c`
class-table flag flip for Morpheous (tier 3) selection, and Rex's
`spell_renewal` duration-clamp fix (`rexdev/.0001-fix-renewal-duration.patch`).

#### Fixed (Rex)
- **`spell_renewal` no longer decreases buff durations.** Previously
  `paf->duration = level*1.5` unconditionally, which meant casting
  renewal at level 80 on a buff with 200 ticks left would DROP the
  buff to 120 ticks. Changed to `paf->duration = UMAX(paf->duration,
  level*1.5)` — matches the existing `paf->level` pattern on the next
  line. Renewal is now strictly beneficial. (`magic.c:4088`,
  `spell_renewal`.) Applied from Rex's mailbox-format patch in
  `rexdev/`.

#### Added
- **`do_strike`** (STRIKE-PURE extended single-target, 660b at `0x07d62`).
  Single-weapon gate (WEAR_WIELD only), HP-frac /10, multi_hit HIT
  helper, gangbanger wait-doubler. MISS path has two variants — alert
  (victim->byte_at_0x17d & 0x2 set) vs not-alert — with separate 3-line
  broadcasts. Caster rift gate (`is_affected(ch, gsn_rift)`). Hand-
  decompiled from disasm; verified against the original `act_combat.o`.
- **`do_gore`** (STRIKE-PURE outlier, 680b at `0x10a5c`). Explicit-target
  via `one_argument` with `ch->fighting` fallback. No HP-frac, no weapon
  check. Chance × 9/10 scaling. Level-scaled direct damage formula
  `number_range(level*2, level*4) + 100` with `DAM_PIERCE` — uses
  `damage()` directly, not `multi_hit`. Two new secondary-roll patterns:
  HIT bonus (chance/4 odds → victim->stunned for 1–2 ticks, 3-line
  broadcast) and MISS penalty (chance/2 odds on the worse half of the
  miss → ch->stunned for 1–2 ticks, 2-line broadcast). First STRIKE-PURE
  with a caster self-effect.
- **Morpheous class enabled** — Rex (`f21095b1`) flipped
  `class_table[47].available_for_creation = TRUE` so testers can pick
  the tier-3 class after remort. Bundled into this binary.

#### Schema deltas
Seven new rows in `DS_SCHEMA.md` Discovered deltas:

1. STRIKE-PURE chance scaling — third value (gore `× 9/10`).
2. Per-port victim-alert flag at byte 0x17d, bit 0x2 (do_strike).
3. Direct-damage HIT helper option (first STRIKE-PURE without
   `multi_hit`/`one_hit`).
4. Secondary-roll bonus on HIT — victim-stun pattern.
5. Secondary-roll penalty on MISS — caster self-stun pattern.
6. do_gore gate-order without HP-frac/weapon check; race-lock implicit
   through `skill_table[gsn_gore]`.
7. do_strike vs do_cross_slash variability — single-weapon gate,
   two-variant MISS broadcast, caster-rift gate.

---

## [0.4.8] — 2026-04-26 (QoL patches)

### Added / Changed
- **`spellup` open to all players** — trust level lowered from L7 (Angel
  IMM) to 0 (all players); position changed from `POS_DEAD` (any) to
  `POS_STANDING` (blocks mid-combat). Patcher: `patch_spellup_all.py`.
  Confirmed live by Kyle.

### Fixed
- **Lights no longer crumble** — `obj_update` guard in `update.c`
  changed from `if (obj->item_type != ITEM_LIGHT || obj->value[2] == 0)`
  to `if (obj->item_type != ITEM_LIGHT)`. DSA-format lights have
  `value[2]=0` which bypassed the stock ROM protection; all ITEM_LIGHT
  objects now fully exempt from timer decay. Lights with fuel still burn
  down via `char_update`. Patcher: `patch_lights_permanent.py`.

---

## [0.4.7] — 2026-04-26 (remort restored + multi_hit fix)

md5: 7209d8837d3f5fb8a64443c429e91067

### Fixed
- **BUG-005** — `do_cross_slash` + `do_garotte` were passing literal
  `0` to `multi_hit()` on the HIT path instead of their gsn, producing
  ~75 `Dam message odd for dt 0` bug entries per minute of combat.
  Patcher `fix_multi_hit_gsn.py` corrects both call sites
  (act_combat.c:2910 → `gsn_garotte`, :3431 → `gsn_cross_slash`).

### Changed
- **BUG-002 / BUG-006 RESOLVED** — `do_remort` and `do_reroll`
  un-stubbed via `restore_remort_reroll.py`. Original 2003 bodies
  restored from `act_comm.c.pre_remort_stub.bak`. Tested live
  2026-04-26 by Kyle and Rex — no crash. Original SIGSEGV was caused
  by class re-init touching then-stubbed `act_combat.c`; with ~22
  combat verbs now ported, that path is no longer hollow.
- **Morpheous class (tier 3) now reachable** — gated only behind
  tier 3 remort, which is now functional. Queued for in-game testing.

---

## [0.4.6] — 2026-04-26 (STRIKE-PURE single-target batch)

md5: 5e99e72347f08f4b51a7362845cb5db1

### Added
- `do_cross_slash` (STRIKE-PURE single-target, 536b — dual-wield gate,
  HP-frac /10, multi_hit) — verified in-game.
- `do_garotte` (560b — whip-only stealth opener, sleeping-victim
  auto-HIT, AFF2 bit 15 halver, gangbanger wait-doubler) — verified
  in-game.

### Schema deltas
9 new rows added to `DS_SCHEMA.md` Discovered deltas, including:
HP-fraction divisor varies across STRIKE-PURE single-target
(cleave skips, cross_slash /10, garotte/backstab /3); AFF2 bit 15
halver at offset `0x174`; `is_gangbanger` as wait-clamp doubler;
sleeping-victim auto-HIT idiom; pre-helper caster broadcast NOT
cluster-universal; `one_argument`+`get_char_room` canonical
explicit-target idiom; gate order is per-port; dual-wield gate idiom;
`WEAPON_WHIP=7` weapon-type checks read `value[0]` directly.

### Known issues
- BUG-005 (Dam message odd for dt 0) discovered in QA — fix staged for 0.4.7.

---

## [0.4.5] — 2026-04-26 (isles.are saving_throw fix)

## [0.4.5] — 2026-04-26 (isles.are saving_throw fix)

Data-file copyover only. Binary unchanged from 0.4.4
(md5 `9c2e60f0f73ac0e63a4ea05222503796`).

### Fixed
- **BUG-004:** `isles.are` mob-extension parser-key typo. 14 mob
  definitions had `Saivs` (mis-spelling) instead of `Saves` on the
  saving_throw line. The mob-extension parser at `db_mobile.c:373`
  dispatches on `UPPER(word[0])` and the `S` arm only knows `Saves`
  and `Speed`, so `Saivs` was silently dropped via `fread_to_eol`
  while emitting `LOAD_MOBILE: no match` to the boot log. Result:
  14 Isles mobs were spawning with `saving_throw = 0` instead of
  the area's authored values (range −50 to −1000).
- Affected vnums: 30003–30005 and 31802–31884. Casters who fight
  Isles mobs will notice spells landing far less often — by design,
  not a regression. `#30004` at −1000 is essentially spell-immune.

### Changed
- Boot log clean for `isles.are` — was emitting 14 LOAD_MOBILE
  warnings per boot (~602 cumulative across ~43 prior boots).

### Notes
- Original BUG-004 hypothesis (bad-vnum reset entries → null deref
  under `area_update()` → idle SIGABRT) was incorrect. Errors fired
  at *parse* time, not reset time, and the parser recovers cleanly.
  Idle SIGABRT investigation continues independently under BUG-001.
- COWORK_PROMPT.md Track 2 (reset null-check guard) retired — its
  premise was based on the wrong hypothesis.

---

## [0.4.4] — 2026-04-26 (STRIKE-PURE AOE batch + BUG-003 + QoL)

md5: 9c2e60f0f73ac0e63a4ea05222503796

### Added
- `do_legsweep` (STRIKE-PURE AOE sub-anchor, 555b) — verified in-game.
  Revealed that STRIKE-PURE splits into single-target and AOE-iterator
  sub-clusters. do_legsweep is the AOE template going forward.
- `do_dhammer` (473b), `do_stomp` (522b), `do_whirlwind` (537b) — full
  AOE-iterator batch, verified in-game 2026-04-26. (`apply_strike_pure_aoe.py`)
- `add all` v1 + v2 — purchases all skill groups AND individual skills at
  creation. (`add_all_groups.py` + `add_all_groups_v2.py`)
- Debug binary deployed — `-O0 -g`, symbols confirmed. Next crash produces
  a real gdb backtrace.
- `CODE_HANDOFF.md` + `COWORK_PROMPT.md` — shared handoff files so Code
  and Cowork bounce tasks without Kyle repasting.

### Fixed
- Colour parser: 9 self-aliasing sprintf sites in `colorize()` rewritten
  to bare function calls. Colour bleed eliminated across all output.
- **BUG-003:** Level-1 chars lost on copyover — `copyover_in_progress`
  global bypasses save gate for new chars during copyover only.
  (`fix_copyover_level1_save.py`)
- TNL cap: 500k threshold in `skills.c` lowered to 10k — prevents
  ungodly TNL for full skill loadouts at creation.
  (`cap_creation_exp_per_level.py`)
- Selective `make clean` — no longer nukes unrecoverable pre-built
  objects (util.o, wizlist.o, xsocial.o).

---

## [0.4.3] — 2026-04-26 (UTILITY-TARGET + STRIKE-PURE anchor + QoL)

### Added
- `do_target` (UTILITY-TARGET anchor, 344 bytes) — verified in-game
- `do_cleave` (STRIKE-PURE anchor, 559 bytes) — hand-decompiled 0x65b0..0x67df,
  disasm-verified, tested in-game. Template established for 6 remaining
  STRIKE-PURE ports (garotte, stomp, cross_slash, whirlwind, legsweep, dhammer).
- New character defaults: auto all, brief, scroll 0, and default prompt
  `<<%h/%Hhp %m/%Mmp %v/%Vmv $%pp/%gg>>` set at creation. Gated on
  `!HAS_PLR(ch, PLR_REROLL)` — rerolling chars keep their existing prefs.

### Changed
- `do_warpaint` skull requirement removed (IDEA-004 — deliberate divergence)

### Fixed
- `is_safe` call in `do_target` corrected to 3-arg DS form `is_safe(ch, victim, TRUE)`.
  Schema delta already captured from do_kill port; Cowork patcher used 2-arg stock ROM
  form in error — fixed by Code before staging.

---

## [0.4.2] — 2026-04-25 (reroll lockdown)

### Fixed
- **BUG-002:** `do_reroll` neutralized — was crashing the server with
  SIGABRT every time anyone tried it (same family as `do_remort`,
  caught by `tell_all` signal handler in `comm.c:3178`). Body
  replaced with polite-message stub via `neutralize_reroll.py`.
  Original backed up to `act_comm.c.pre_reroll_stub.bak`.
- Long-term fix tracked as IDEA-003 (auto-promote new chars to tier 3
  at creation, after skills/spells stabilise).

### Added (infrastructure)
- Crash-diagnostic pipeline: core dumps enabled, gdb confirmed
  reading symbols cleanly. Future SIGABRT/SIGSEGV crashes capture to
  `/tmp/ds_core.<pid>.<time>` for post-mortem.
- BUGS.md and IDEAS.md tracking files added (with format spec).
- Identified that DS's `tell_all` signal handler in comm.c:3178
  catches SIGSEGV and converts to abort() — most "SIGABRT" crashes
  in the watchdog log are actually SIGSEGVs caught by tell_all.

---

## [0.4.1] — 2026-04-25 (BUFF-SELF cluster)

### Added
- `do_spellbane` (BUFF-SELF anchor port — established the 5-bullet
  variability template the batch followed)
- BUFF-SELF batch (7 functions, single patcher):
  `do_resistance`, `do_warcry`, `do_concentration`, `do_ironwill`,
  `do_battlehymn`, `do_bloodlust`, `do_warpaint`
- All 7 verified via in-game `affects` panel matching disasm specs
  (bloodlust's HP +500, concentration's hitroll +250, etc.)
- 8 schema deltas captured during the batch (get_skill bypass via raw
  pcdata->learned[], variable check_improve polarity, cost-before-roll
  patterns, AFFECT_DATA bitvector-per-where idiom, etc.)

---

## [0.4.0] — 2026-04-25 (Phase B Step 3 anchor)

### Added
- `do_mock` (RESTING position, 183 bytes — smallest DS-custom function,
  workflow proof-of-concept for the hand-decompile-from-disasm pattern
  that drives Step 3)

### Added (infrastructure)
- `extract_skill_table.py` produces `SKILL_TABLE.md` from `const.c`'s
  `skill_table[]` definition
- `dump_helpfile.py` produces `HELPFILES.md` (currently broken — only
  emits header, see deferred section)
- `DS_CUSTOM_SURVEY.md` from Code: 24 small-DS-custom functions
  surveyed and clustered into 7 groups

### Deferred
- HELPFILES.md output is broken (5 lines, header only). Investigation
  deferred — not blocking porting since disasm is authoritative.
- Schema extractor v2 (enum parser for POS_*, AFF_*, AFF2_*, WEAR_*,
  WEAPON_*, etc.) deferred to after Step 3.

---

## [0.3.1] — 2026-04-25 (Phase B Step 2 Bundle B)

### Added
- `do_berserk`, `do_circle`, `do_backstab`, `do_gouge`, `do_dirt`
- Class-flavoured ROM combat verbs — sneak/hide visibility,
  weapon-type bits, class restrictions, affect application

### Verified
- Bundle B ✅ working in-game (Kyle confirmed)

---

## [0.3.0] — 2026-04-25 (Phase B Step 2 Bundle A)

### Added
- `do_rescue`, `do_trip`, `do_disarm` (with `disarm()` helper for
  actual weapon-drop), `do_bash`
- Standard ROM combat repertoire — completes BASIC ROM tier alongside
  `do_kill`/`do_flee` from 0.2.x

### Added (infrastructure)
- `PHASE_B_STEP_2_PREP.md` (prep-doc pattern established in 0.2.x,
  reused here)
- Anchor-then-batch workflow proven (do_kick + do_rescue as anchors,
  then trip/disarm/bash batched on the same template)

---

## [0.2.1] — 2026-04-25 (do_kick port + side-mechanic verified)

### Added
- `do_kick` with knee-breaker / limp side-mechanic for elder class

### Fixed
- Limp side-mechanic verified to be working as intended (affect
  persistence, not a bug — addressed Code's earlier diagnostic)

---

## [0.2.0] — 2026-04-25 (Phase B Step 1)

### Added
- `do_kill` and `do_flee` — first real combat verbs from
  disasm-and-port pattern
- `do_kill` includes `check_killtimer` integration
- `do_flee` includes the 6-attempt random-door logic, exp penalty,
  auto-look on arrival
- `DS_SCHEMA.md` infrastructure with `extract_ds_schema.py`
- `COMBAT_CATALOG.md` cataloguing all 102 functions in `act_combat.o`
- `PHASE_B_STEP_1_PREP.md` (prep-doc pattern established)
- Copyover verified end-to-end — hot-swap deploys with no
  disconnect (per `COPYOVER_PLAN.md`)
- Schema-first writing workflow established

### Fixed
- Initial `do_kill` port had inverted POS_STUNNED check (caught and
  fixed by step 1c patcher)

### Added (tooling)
- `fix_combat_step1*.py` patcher series (a/b/c/d) — surgical edits
  with sentinel checks and atomic backup/rollback
- `grant_skills.py` (broken initially due to skill-name mismatch
  with `skill_table[]`; deferred until validated against const.c)

---

## [0.1.2] — 2026-04-25 (initial stability patch)

### Fixed
- `do_remort` neutralized to polite-message stub after SIGSEGV
  crash (`neutralize_remort.py`). Original body backed up to
  `act_comm.c.pre_remort_stub.bak`.

---

## [0.1.1] — 2026-04-25 (public + supervised)

### Added
- Public ngrok TCP hosting at `7.tcp.ngrok.io:25597` (paid plan,
  reserved address)
- `run_mud_watchdog.sh` auto-respawns ds.new on crash with rate
  limiting (10 restarts per 60s)
- `start_mud_public.sh` / `stop_mud_public.sh` runtime ops scripts

---

## [0.1.0] — Initial boot (pre-conversation)

### Added
- Recovered 2003 source from corrupted 205 MB tar archive
  (`recovery_carver.py` extracted 1,847 files)
- `rebuild_source.py` modernization patcher for gcc 11
- 32-bit Linux binary built and running locally (port 5000)
- Full world loads; telnet connections accepted
- `act_combat.c` written as stub generator (`generate_act_combat_stub.py`
  — every combat ability replies with placeholder message)
- `update.c` truncated at line 1129 (corrupted tail) and appended
  with stock ROM 2.4 implementations
- Julian promoted to level 110 (Executive — top imm tier)
- `reset_character.py` for password reset + level/trust setting

---

## Versioning conventions going forward

- **Bump the patch number** every time a copyover lands (each new
  set of staged combat verbs, each stability fix, each delibrate
  divergence from 2003 source).
- **Bump the minor number** at Phase boundaries (Phase B Step 3 →
  Step 4, Phase B → Phase C, etc.).
- **Bump the major** when DS hits a stable, publicly-playable
  baseline — currently un-scheduled, probably after combat porting
  reaches the psionics suite or similar coverage threshold.

When a copyover is live, update `[Unreleased / Staged]` to `[X.Y.Z]`
with the date and move it down. The ` [Unreleased / Staged]` block
above the current version is always for in-flight, pre-deploy work.
