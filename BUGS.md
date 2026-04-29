# DS Bugs Log

Active and historical bugs in the Devil's Silence resurrection. Add new
entries at the **top** of the Open list (newest first). Move resolved
entries down into the Resolved section, keeping the history.

## Format

Each entry uses this shape:

```
### BUG-NNN: Short title

- **Status:** open / investigating / fix-staged / resolved / wontfix
- **Severity:** crash / data-loss / functional / cosmetic
- **Reporter:** name (or "Kyle" / "Code" / "playtest")
- **Date opened:** YYYY-MM-DD
- **Affects:** which functions / commands / subsystems

Description of the bug — what was expected, what happened.

**Repro:** numbered steps if known.
**Notes:** anything learned along the way; updated freely.
**Resolved:** YYYY-MM-DD + reference to fix (commit, patcher script, PR)
```

ID numbers monotonic — when you add a new bug, take the next BUG-NNN.

Severities, in order of urgency:
- **crash** — server dies (signal 6, signal 11, etc.)
- **data-loss** — character files corrupted, items vanish, levels lost
- **functional** — command does the wrong thing or fails when it shouldn't
- **cosmetic** — wrong message, color glitch, double-print, etc.

---

## Open

### BUG-022: `do_spellup` — spam on cast + no auto-spellup on first login or remort

- **Status:** fix-staged (0.4.43) — awaiting Kyle copyover
- **Severity:** functional
- **Reporter:** Kyle (2026-04-29)
- **Date opened:** 2026-04-29
- **Date staged:** 2026-04-29
- **Affects:** do_spellup, login handler, remort handler

Two issues in one command:

1. **Spam on cast** — `spellup` floods the player with messages when casting buffs.
   Likely missing a message-rate gate or sending individual spell messages instead
   of a single consolidated "you cast your spells" line.

2. **No auto-spellup on first creation login or remort** — new characters and
   remorted characters should receive an automatic spellup on their first login
   to avoid landing in the world unbuffed. Hook not firing in either the
   creation login path or the remort completion path.

**Repro:** Create a new character and log in — no spellup fires. Type `spellup`
manually — observe message flood. Remort a character and log back in — no
auto-spellup.

**Fix (0.4.43):**
- `act_wiz.c:8482` — `do_spellup` now NULLs caster + recipient `desc` for the
  duration of the 19-spell loop, suppressing per-spell `send_to_char` output.
  After the loop, descriptors are restored and one consolidated line is sent
  ("A shimmering aura of magical protections envelops you."). Same treatment
  applied to the `spellup room` form per-iteration. Effects apply identically;
  only the messaging is suppressed.
- `comm.c:2418` — entry-game block now calls `do_spellup` on the player when
  `!IS_NPC && !IS_IMMORTAL && level == 1`. Catches both fresh creation
  (always level 1) and remort (resets to level 1). Auto-fire stops at
  level 2. Forward declaration added at top of comm.c.

**Caveat:** room-mate `act(... TO_ROOM)` broadcasts from each spell still fire
because they iterate other people's descs, not ch's. Few buff spells use
TO_ROOM in practice, so spectator spam is minimal — if it's still bad, the
followup is to trim the buff list (Cowork design call).

---

### BUG-021: Paradox events not ticking — event never fires or expires

- **Status:** fix-staged (0.4.42) — needs Kyle QA
- **Severity:** functional
- **Reporter:** Kyle (2026-04-29)
- **Date opened:** 2026-04-29
- **Affects:** `paradox.c` — tick/update handler, event scheduling

Paradox events are not ticking. Either the Paradox trigger is never firing, the tick rate handler isn't calling paradox update, or the event duration/expiry logic is broken. Paradox should be a periodic world event — currently it appears to do nothing in-game.

**Design note (confirmed 2026-04-29):** When Paradox IS active, Grace defensive bonuses (Alecca's Grace / Essence damage reduction) must be suspended. Everyone should be killable at normal TTK during Paradox regardless of Essence stack. This is an intentional escalation mechanic — Paradox makes the world dangerous for everyone. Wire this suppression into the Grace damage modifier check: `if (IS_PARADOX_ACTIVE) skip grace modifier`.

**Repro:** Trigger or wait for a Paradox event in-game. Observe whether anything changes (messaging, flags, mob behavior). Confirm whether the event ever ends on its own.

**Notes:** Fix the tick first, then add the Grace suppression once the economy system ships. Two separate issues; log them together since they share the same Paradox flag.

---

### BUG-020: Monk/Shaolin/Sensei not selectable — valid flag off

- **Status:** fixed (0.4.41) ✅
- **Severity:** functional
- **Reporter:** DionyzRex (Discord, 2026-04-29)
- **Date opened:** 2026-04-29
- **Date fixed:** 2026-04-29
- **QA:** Kyle confirmed — race gate working correctly, Sensei selectable on valid races
- **Affects:** character creation, reroll, remort — const.c class_table

All three monk-family classes have `valid=FALSE` in class_table. The
`valid` field gates both `show_class_choice` (display) and
`get_class_by_num` (selection), so the entire family is invisible and
unselectable at every tier. Not a race restriction — race class_mult
values are fine.

The 73 skills across monk/shaolin/sensei are **fully populated**.
No skill work needed.

**Fix:** Set `valid=TRUE` in const.c at:
- Line 2644: monk (class //8)
- Line 2800: shaolin (class //26)
- Line 2963: sensei (class //44)

**Notes:** This also corrects a prior wrong assumption that the class
indices were 18/36/54. Actual global indices confirmed from `//N`
comment system: monk=8, shaolin=26, sensei=44.

---

### BUG-019: Cursed player following someone can still recall

- **Status:** fixed (0.4.41) ✅
- **Severity:** functional
- **Reporter:** Alecca (original dev todo, 2003)
- **Date opened:** 2026-04-29
- **Date fixed:** 2026-04-29
- **Affects:** do_recall, curse affect check

When a player is cursed (normally blocks recall) but is **following**
another character, the curse check is bypassed and recall succeeds.
Original note: *"when following someone, if you are cursed you can
still recall."* Logged by Alecca in 2003, never fixed.

**Repro:** Curse a player. Have them follow another PC. Have them recall.
**Notes:** Likely the follow check short-circuits before the curse gate
in do_recall or act_move.c. Needs code trace.

---

### BUG-018: Chill touch on weapon causes invincible AC after combat

- **Status:** open
- **Severity:** functional
- **Reporter:** Alecca (original dev todo, 2003)
- **Date opened:** 2026-04-29
- **Affects:** fight.c, magic.c (chill touch weapon apply), AC calculation

When chill touch is applied to a weapon, the AC modifier is not correctly
cleaned up after combat ends, leaving the victim with an extremely large
negative AC value. Original note: *"BUG: with chill touch on weaps you
get INVINCIBLE ac after a fight."* Logged by Alecca May 2003, never fixed.

**Repro:** Apply chill touch to a weapon. Fight a target. After combat
ends, check target's AC — likely shows an extreme negative value.
**Notes:** Probably an affect not being stripped or a delta being applied
twice. Check chill touch's weapon-proc path in fight.c and the AC
recalculation on affect_remove.

---

### BUG-017: `do_kick` is stubbed — "combat module rebuilding" message in-game

- **Status:** open
- **Severity:** functional
- **Reporter:** Kyle (2026-04-28, in-game)
- **Date opened:** 2026-04-28
- **Affects:** `do_kick` in `act_combat.c`

Typing `kick` in-game returns "That ability isn't available right now (combat module rebuilding)." — the standard stub message. `do_kick` is declared in `fight.c` (line 64) and called internally during combat rounds (line 1301), but the player-facing command is hitting the unported stub in `act_combat.c`.

This is a foundational combat move used by many classes. High priority — should be ported before or alongside the Priority 4 queue.

**Notes:** fight.c's internal call at line 1301 means auto-kick during combat rounds is also broken (the stub will fire silently or no-op there). Confirm behavior once ported.

---

### BUG-016: Ticks not firing — affect durations and travel cooldown never expire

- **Status:** fix-staged (0.4.30) — TRAVEL_COOLDOWN lowered from 1440s to 90s
- **Severity:** functional
- **Reporter:** Kyle (2026-04-28, observed in-game)
- **Date opened:** 2026-04-28
- **Affects:** `do_travel` cooldown, possibly `char_update` tick rate

**Updated findings (2026-04-28):** The travel input lock DID eventually release — Kyle was able to recall after a long wait. Ticks are probably firing, just slowly or the walk completed on its own. The cooldown however has NOT reset — Kyle still gets "You are still too weary from your last journey to travel again" after the travel completed. These are now two separate issues:

1. **Cooldown not resetting** — `TRAVEL_COOLDOWN` may be set to an absurdly long value, or it's `time_t` wall-clock based and the comparison logic is wrong. Check what value `TRAVEL_COOLDOWN` is defined as and how the expiry check works (`time(NULL) - ch->pcdata->travel_cooldown > TRAVEL_COOLDOWN`?).

2. **Travel input UX** — Even if ticks are fine, the full input lock during travel is too aggressive. Moving mid-travel should echo a message and cancel travel, not freeze all input. (See handoff for UX spec — this is a separate design fix.)

**Repro:**
1. `travel <area>` — wait for walk to complete.
2. Try `travel` again — "still too weary" persists indefinitely.

**Notes:** Apply any timed affect (haste, bless) and check if it eventually drops. If it does, ticks are fine and BUG-016 is purely a TRAVEL_COOLDOWN value/logic bug. If affects never drop, tick rate is also broken.

---

### BUG-015: Silver, wood, and iron damage types not classified as weapon damage

- **Status:** fix-staged (0.4.30)
- **Severity:** functional
- **Reporter:** Leto changelog (Jul 18 2003), found by Kyle 2026-04-28
- **Date opened:** 2026-04-28
- **Affects:** damage calculation in `fight.c`, resist/vuln math

Per Leto's Jul 18 2003 changelog: "Silver, wood and iron will now count as weapon instead of magic damage. So, Bash, Pierce, Slash, Iron, Wood and Silver are weapon. Everything else is magic." `DAM_SILVER`, `DAM_WOOD`, `DAM_IRON` are defined in `bit.h` (bits 21/22/23) but the resist/vuln classification in `fight.c` needs to treat them as weapon damage, not magic. Verify the damage math applies the correct armor vs magic resistance path for these types.

---

### BUG-014: `do_quaff` missing combat fumble

- **Status:** resolved (already implemented at act_obj.c:3599-3611, predates BUG report)
- **Severity:** functional
- **Reporter:** Leto changelog (Jun 21 2003), found by Kyle 2026-04-28
- **Date opened:** 2026-04-28
- **Affects:** `do_quaff` in `act_obj.c`

Per Leto's Jun 21 2003 changelog: "You can now fumble and fail to quaff a pot whilst fighting. The pot is lost and you get the normal 1 round lag." Current `do_quaff` has no combat fumble check. When `ch->fighting != NULL`, there should be a skill/chance roll — on fail, extract the potion and apply wait state without the benefit firing.

---

### BUG-013: Flee success not gated to 5/6 attempts per round

- **Status:** fix-staged (0.4.30)
- **Severity:** functional
- **Reporter:** Leto changelog (Apr 29 2003), found by Kyle 2026-04-28
- **Date opened:** 2026-04-28
- **Affects:** `do_flee` in `fight.c`

Per Leto's Apr 29 2003 changelog: "Its now harder to flee, you can only attempt to flee 5/6 times a round." Current `do_flee` has no such gate — every attempt is processed. Needs a `number_range(1,6) == 1` (or equivalent) failure path that eats the flee attempt with a "You couldn't escape!" message and applies wait state.

---

### BUG-012: `do_ambush` missing spear weapon bonus

- **Status:** fix-staged (0.4.30)
- **Severity:** functional
- **Reporter:** Leto changelog (Apr 22 2003), found by Kyle 2026-04-28
- **Date opened:** 2026-04-28
- **Affects:** `do_ambush` in `act_combat.c`

Per Leto's April 22 2003 changelog: "Ambush now does bonus damage wielding spears." The current 0.4.22 port of `do_ambush` uses `multi_hit` on HIT with no weapon-type bonus. Needs a spear check on the wielded weapon and a damage modifier applied when `wtype == WEAPON_SPEAR` (or equivalent in DS source).

**Notes:** Pair with BUG-011 (charge/sword bonus) — same pattern, fix together.

---

### BUG-011: `do_charge` missing sword weapon bonus

- **Status:** fix-staged (0.4.30)
- **Severity:** functional
- **Reporter:** Leto changelog (Apr 22 2003), found by Kyle 2026-04-28
- **Date opened:** 2026-04-28
- **Affects:** `do_charge` in `act_combat.c`

Per Leto's April 22 2003 changelog: "Charge does bonus damage if you wield swords." The current charge port applies no weapon-type modifier. Needs a sword check on the wielded weapon and a damage bonus when `wtype == WEAPON_SWORD`.

**Notes:** Pair with BUG-012 (ambush/spear bonus) — fix together in one patch.

---

### BUG-010: `travel <area name>` crashes the server

- **Status:** resolved
- **Severity:** crash
- **Reporter:** Kyle (2026-04-28, in-game)
- **Date opened:** 2026-04-28
- **Resolved:** 2026-04-28 — fix landed in 0.4.25, rolled into 0.4.26, confirmed by Kyle in-game: no crash, visited list persists across login.
- **Affects:** `do_travel` in `act_move.c`, BFS pathfinding, area name lookup, `fread_char` save loader

Typing `travel the sprite village` (or any area name) caused an immediate hard
crash — "Oh Shit! We're going down! Devil's Silence is Crashing!" with SIGSEGV
logged.

`travel` with no argument works correctly — lists discovered areas. The crash
was specifically in the name-lookup or BFS pathing triggered by the argument.

**Root cause analysis (2026-04-28):**

Code-reading turned up several real defects on the argument path that together
explain the crash and likely contributed to follow-up corruption:

1. **Area matcher used `arg` (first word only), not the full argument.**
   `one_argument("the sprite village", arg)` extracts `arg = "the"`. Then
   `str_prefix("the", a->name)` matches WHICHEVER `"The X"` area appears first
   in `area_first` — non-deterministic, often not what the player meant. If
   the picked area is one Julian had visited, BFS proceeded against an
   unintended target, increasing the chance of edge-case path states. Fixed
   in 0.4.25 by matching against the full stripped argument first, with
   first-word-only as a fallback.
2. **`Visited` save round-trip was broken.** The `TrvlVst` load handler in
   `fread_char` was placed in `case 'R'` (right after `RecallV`) but the
   keyword starts with `T`. Case dispatch is by first letter, so the load
   was never reached — every login wiped the visited list. The boot log's
   `[*****] BUG: Fread_char: no match. Error matching word: TrvlVst` was
   the giveaway. Moved to `case 'T'` in 0.4.25.
3. **`new_room_index` did not initialise the new BFS scratch fields**
   (`bfs_tag`, `bfs_pvnum`, `bfs_pdir`). Garbage values are very unlikely
   to crash on their own (the algorithm bails on `bfs_pvnum != -1`), but
   they could silently cause incorrect "already visited" skips or weird
   path-recon walks. Initialised to 0 in 0.4.25 as defense in depth.

**Diagnostic logging added in 0.4.25:** `travel_bfs` now emits `log_string()`
breadcrumbs at entry, on entrance discovery, on path-out, on bail, and on
any out-of-range `bfs_pdir` (with an early return). If the crash recurs
post-0.4.25, the boot log will pinpoint the failing branch.

**Repro:**
1. Walk into The Sprite Village (or any area) to mark it visited.
2. Walk back to a different area.
3. Type `travel the sprite village` (or the area name).

**Verification (Kyle to do post-copyover):**
- Repeat the original repro and confirm no crash.
- Walk into a few areas, log out, log back in, `travel list` — visited
  areas should still be present (formerly wiped by the load bug).

---

### BUG-009: `~/ngrok.log` always empty — start script's redirect doesn't capture ngrok 3.x output

- **Status:** open
- **Severity:** cosmetic (ops only — does not affect tunnel)
- **Reporter:** Code (2026-04-28, during session resync)
- **Date opened:** 2026-04-28
- **Affects:** `start_mud_public.sh`, ops diagnostics for tunnel zombies

`~/ngrok.log` is 0 bytes despite the ngrok process running and serving traffic
(495 lifetime conns confirmed via `:4040` API on 2026-04-28). The file got
last-touched 2026-04-27 21:40 — when `start_mud_public.sh` truncated it on
launch — and has had nothing written to it since.

This breaks one of the diagnostic signals we use to spot the recurring
"ngrok process up but tunnel zombie" failure mode (CODE_HANDOFF "Ngrok ops
issue" section): a stale `ngrok.log` mtime currently reads as "ngrok is
silent" but really means "we're not capturing its output at all."

**Likely cause:** `start_mud_public.sh` uses `nohup ngrok ... > ~/ngrok.log
2>&1 &` but ngrok 3.x writes its agent log to its own configured path
(`~/.config/ngrok/ngrok.yml` `log` key) and only emits a brief banner to
stdout before backgrounding internally. The redirect catches the banner
and nothing else.

**Repro:** start MUD via `start_mud_public.sh`; check `~/ngrok.log` after
any tunnel activity — it stays empty/static.

**Fix candidates:**
1. Configure ngrok's own logging in `ngrok.yml`:
   `log: /home/kwebb/ngrok.log` + `log_level: info` + `log_format: logfmt`.
   That's the supported path and writes continuously.
2. Add `--log=stdout --log-level=info` flags to the ngrok invocation in
   `start_mud_public.sh`, so the existing `> ~/ngrok.log` redirect works.

Either approach restores the file as a useful liveness signal. Watchdog
work proposed in CODE_HANDOFF should poll `:4040` API regardless.

**Notes:** the `:4040` local API + a `cat </dev/tcp/7.tcp.ngrok.io/25597`
probe are the authoritative health checks until this is fixed. Don't trust
`ngrok.log` mtime as a freshness signal in the meantime.

---

### BUG-008: do_throw missing "victim alert" check — chance-zero and messaging omitted

- **Status:** investigating
- **Severity:** functional
- **Reporter:** Kyle (2026-04-28)
- **Date opened:** 2026-04-28
- **Affects:** `do_throw` (act_combat.c), `do_charge`, and all future ports of skills that set/read the wary flag

In the 2003 binary, `do_throw` reads bit `0x04` from `CHAR_DATA` offset `0x16c` on the victim.
When set, throw chance is zeroed (auto-miss) and a distinct alert miss message fires.
The 0.4.17 port omits this entirely — the field has no name in current `merc.h`.

**Wary flag identified (2026-04-28) via `chang.not`:**
Leto's April 16 2003 changelog entry documents it explicitly:
> "Wary flag. Whenever someone is hit by backstab, ambush, charge, bastion or chromatic salvo
> they will get a flag which prevents anyone else using a similar attack until a number of
> rounds have passed. The flag will also vanish if fighting stops."

The `0x16c bit 0x04` field IS the wary flag. A victim recently hit by a rush/surprise opener
becomes wary — alert enough to resist being thrown. do_throw and do_charge both READ it.
do_backstab, do_ambush, do_charge, do_bastion SET it on HIT. HP is not a factor (Kyle confirms).
See `RECOVERED_INTEL.md` for full source documentation.

**What still needs to be done:**
1. Add a `wary` flag field to `CHAR_DATA` in `merc.h` (timer or bit field).
2. Set it in `do_backstab`, `do_ambush`, `do_charge`, `do_bastion` on HIT path.
3. Clear it in `char_update` after N rounds and on combat end (exact duration needs disasm check).
4. `do_throw` and `do_charge` checks will work once the field exists.
5. Add distinct "alert victim" miss messaging to `do_throw`.
6. `do_bastion` and `do_ambush` will also need the set-call when they are ported.

**Duration design intent (Kyle confirmed 2026-04-28):** 10 ticks, matching chromatic_salvo. Clears when fighting stops (flee/stop_fighting) per Leto's changelog.

**PC targets only (Kyle confirmed 2026-04-28):** Wary flag is a PvP anti-spam mechanic. Check `!IS_NPC(victim)` before setting and before gating — mobs should never receive the wary flag and openers should always land freely on NPCs.

**Repro (once implemented):** Backstab a player → immediately throw them → should auto-miss
with alert messaging. Currently always uses normal miss path.

**Notes:** `do_charge` has the same flag family at `0x17c/0x40`. Implement both together.
fight.c has zero wary/alert logic — entirely in lost act_combat.c, hence the full port needed.

**Notes:** `do_charge` has the same family bug at `0x17c/0x40` — investigate both together.
The 0x2f0 chance modifier (BUG-009 candidate if confirmed needed) is a separate unrecoverable
field affecting both do_jab and do_throw.

---

### BUG-007: OLC `oedit` — insufficient security despite correct level/trust

- **Status:** resolved
- **Severity:** functional
- **Reporter:** Rex (Llanos, 2026-04-27)
- **Date opened:** 2026-04-27
- **Affects:** `do_oedit`, OLC access for contributor accounts

Rex at level 107 with trust set could not use `oedit` — received "insufficient security" regardless of `advance` or `set char trust`. Root cause: two separate gate systems. The interp.c level gate (`L3`) was one check; `ch->pcdata->security` inside `do_oedit` is a completely independent OLC security check. Level and trust don't affect it.

DS saves the field as `Sec` (confirmed `save.c:506`: `fprintf(fp, "Sec %d\n", UMIN(ch->pcdata->security,9))`; loaded via `KEY("Sec",...)` at line 1796). No in-game `do_set` support for the field — had to write it directly to the player file.

**Resolved:** 2026-04-27 — `grant_olc_llanos.py` writes `Sec  9` directly to Llanos's player file. Llanos logged back in and `oedit` confirmed working. `fix_oedit_level.py` also applied (lowers interp.c gate from `L3` to `107`) — redundant for this bug but correct long-term.

**Note for future contributors needing OLC access:** run `grant_olc_llanos.py` as a template, hardcode the new character name, confirm `Sec` is the field name, ensure target is fully offline before running.

---

### BUG-006: do_remort + do_reroll un-stubbed — re-test required

- **Status:** resolved
- **Severity:** crash (potential — original SIGSEGV did NOT reproduce)
- **Reporter:** Code (2026-04-26)
- **Date opened:** 2026-04-26
- **Affects:** `do_remort`, `do_reroll`, ultimately `prepare_reroll` (creation.c)

The neutralization stubs from BUG-002 were removed in the 0.4.7 staged
build. Original 2026-04-25 hypothesis was that the SIGSEGV came from
class re-init touching stubbed `act_combat.c` paths and the stock-ROM
`update.c` tail. Since then ~22 combat verbs have been ported back from
disasm (BASIC ROM tier complete, BUFF-SELF cluster complete, STRIKE-PURE
cluster mostly complete) so the original crash path may no longer
exist. We need to verify by re-attempting remort/reroll with a
sacrificial test character.

**Repro plan:**
1. As Julian (level 110), make a sacrificial alt or use a throwaway
   mortal character.
2. Advance it: `advance <char> 101` (HERO) and set tier:
   `set char <char> tier 2` (or whatever the imm syntax is — `wizhelp`
   if unsure).
3. As that char, type `reroll`. Expect the confirmation prompt.
4. Type `reroll` again to confirm.
5. Watch outcomes:
   - **Success:** char drops to creation prompt for tier-2 reroll. No
     SIGSEGV in `~/ds_watchdog.log`. Mark BUG-002 + BUG-006 fully
     resolved; remove the IDEA-003 deferral note from `IDEAS.md`.
   - **Crash:** server respawns via watchdog. Pull the debug-build
     core dump (`/tmp/ds_core.*`) and run gdb backtrace to identify
     the actual fault. Open follow-up bug with the stack trace.
6. Same procedure for `remort` (requires HERO + tier 2 → tier 3).

**Notes:**
- `creation.c::prepare_reroll` does the actual class re-init; the
  do_* wrappers are gates + confirmation prompts.
- Riskiest helpers (per source review at lines 240-252):
  `extract_char(ch, TRUE)`, `free_char(ch)`, `save_char_obj(rch)`,
  `start_reroll(d)`. Any of those could be the SIGSEGV origin.
- Debug build (`-O0 -g`) has been live since 0.4.4, so any new core
  dump will have full symbols — gdb gets a real backtrace.
- BUG-002 stays in the Resolved section as historical record; this
  is a fresh investigation tracking the un-stubbing decision.

**Resolved:** 2026-04-26 — remort tested live by Kyle (and Rex). Server
did not crash. Original SIGSEGV was almost certainly caused by class
re-init touching the then-stubbed `act_combat.c` paths. With ~22 combat
verbs now ported, that path is no longer hollow. Morpheous class (tier 3)
is now reachable and queued for in-game testing. BUG-002 cross-reference:
both resolved together.

---

### BUG-005: cross_slash + garotte spam "Dam message odd for dt 0"

- **Status:** resolved (live in 0.4.7)
- **Severity:** functional (log spam — does NOT affect gameplay damage,
  only breaks the per-hit damage *message* lookup, which falls back to
  a default attack noun)
- **Reporter:** Cowork (2026-04-26 — discovered while resyncing post-0.4.6 deploy)
- **Date opened:** 2026-04-26
- **Affects:** `do_cross_slash`, `do_garotte` HIT paths

`do_cross_slash` (act_combat.c:3431) and `do_garotte` (act_combat.c:2910)
both call `multi_hit(ch, victim, 0)` on the HIT path — passing literal
`0` instead of the skill's gsn. multi_hit propagates `dt` down to
`one_hit` → `damage` → `dam_message`, where `dam_message` looks up
`skill_table[0].noun_damage`, finds the empty placeholder, and emits
`bug("Dam message odd for dt 0.")`.

Result: ~75 bug entries per minute of combat from a player using
either skill. 157 bugs accumulated in `/tmp/ds_boot.log` in the first
two minutes of the 0.4.6 playtest (18:47–18:50).

**Repro:** any successful `cross slash` or `garotte` swing.

**Notes:**
- Both functions correctly pass `gsn_cross_slash` / `gsn_garotte` to
  `check_improve()` and to `damage()` on the MISS path. Only the
  multi_hit calls were wrong — internal inconsistency within the same
  function body, classic typo signature.
- Backstab (`act_combat.c:1894`) and circle (`act_combat.c:2032`) both
  pass their gsn to multi_hit. Pattern is unambiguous across the rest
  of the cluster; cross_slash + garotte were anomalous.
- No gameplay damage impact — `dam_message` falls back to a default
  attack noun when its lookup fails, so hits still land for the right
  amount. Just noisy in the log and slightly off in the per-hit
  message text.

**Resolved:** 2026-04-26 — `fix_multi_hit_gsn.py` patcher (sentinel-checked,
atomic backup of `act_combat.c` to `*.pre_multi_hit_gsn.bak`). Bundled
with the BUG-002/BUG-006 un-stubbing into a single 0.4.7 staged build
at md5 `7209d8837d3f5fb8a64443c429e91067` in `~/ds/src_patched/ds.new`.

---

---

## Resolved

### BUG-004: `isles.are` LOAD_MOBILE noise (parser-key typo)

- **Status:** resolved
- **Severity:** functional (silent saving_throw drop on 14 mobs) + cosmetic (boot-log noise)
- **Reporter:** Kyle (2026-04-26)
- **Date opened:** 2026-04-26
- **Affects:** boot-log cleanliness; spell-resistance balance on 14 Isles mobs

Boot log emitted 14 `LOAD_MOBILE: no match` warnings every boot, all from
`../data/area/isles.are` at fixed line numbers (87, 105, 126, 200, 255,
292, 411, 435, 457, 481, 511, 534, 583, 613).

**Root cause:** the area-file authors mis-typed `Saivs` instead of
`Saves` on the saving_throw line of 14 mob definitions. `db_mobile.c:340-389`
dispatches mob-extension keywords on `UPPER(word[0])` and the `S` arm
only knows `Saves` and `Speed`; `Saivs` falls through to the default arm
at line 386, emits `bug("LOAD_MOBILE: no match.",0)`, and `fread_to_eol`
skips the line. The `saving_throw` field silently defaults to 0 for
those 14 mobs.

**Notes on misdiagnosis:** the original BUG-004 entry hypothesised that
the LOAD_MOBILE warnings came from bad-vnum reset entries dereferencing
null `MOB_INDEX_DATA*` and crashing under `area_update()`, and treated
this as a SIGABRT crash candidate. Wrong on two counts:

1. The error fires at parse time (boot/copyover), not reset time —
   `LOAD_MOBILE: no match` here is the mob-extension *parser*'s default
   switch arm, not a null-deref from `get_mob_index()`.
2. The parser cleanly recovers via `fread_to_eol` and continues. No
   crash potential. Idle SIGABRTs are unrelated and remain tracked
   under BUG-001.

**Behaviour change after fix:** affected mobs gain their intended
saving_throw modifiers (range −50 to −1000). Lower values = harder to
land spells. `#30004` at −1000 is essentially spell-immune by design.
Casters fighting Isles mobs will notice spells suddenly missing — that
is the area's authored intent restored, not a regression.

| vnum | Saves || vnum | Saves |
|---|---|---|---|---|
| #30003 | −100 || #31878 | −100 |
| #30004 | −1000 || #31879 | −65 |
| #30005 | −80 || #31880 | −110 |
| #31802 | −100 || #31881 | −100 |
| #31805 | −150 || #31883 | −50 |
| #31807 | −50 || #31884 | −100 |
| #31876 | −120 |||
| #31877 | −80 |||

**Resolved:** 2026-04-26 — `s/Saivs/Saves/` applied via Edit (sed -i was
silently denied by sandbox; Edit tool replace_all worked). Backup at
`isles.are.pre_saves_fix.bak`. Verified post-copyover: boot at 17:34:05
read isles.are with zero LOAD_MOBILE errors. Released as 0.4.5.

---

### BUG-002: `do_reroll` crashes server (SIGABRT via tell_all)

- **Status:** resolved (neutralized as stub)
- **Severity:** crash
- **Reporter:** Kyle (2026-04-25)
- **Date opened:** 2026-04-25
- **Affects:** `do_reroll` command, server stability

Player typing `reroll` triggers a crash — visible in
`~/ds_watchdog.log` around 14:13:42 (code 134, SIGABRT caught by
`tell_all` signal handler, originally a SIGSEGV). Same crash family as
`do_remort` (neutralized earlier the same day for the same reason):
class re-init touches stubbed `act_combat.c` and stock-ROM `update.c`
tail.

**Resolved:** 2026-04-25 — `neutralize_reroll.py` replaces `do_reroll`
body with a polite-message stub. Original body backed up to
`<source>.pre_reroll_stub.bak`. Long-term fix tracked as IDEA-003
(auto-promote new chars to tier 3 at creation, after skills/spells
stabilise).

---

## Investigating

### BUG-001: Spontaneous SIGABRT (signal 6) crashes

- **Status:** investigating
- **Severity:** crash
- **Reporter:** Kyle (observed during 2026-04-25 playtest)
- **Date opened:** 2026-04-25
- **Affects:** server stability — watchdog respawns within ~3 seconds

Server occasionally dies with signal 6 (SIGABRT) — typically `assert()`
failure or explicit `abort()`. Watchdog respawns ds.new in ~3s so players
just reconnect, but it IS a hard fail of the running process.

**Repro:** non-deterministic so far. Has occurred during normal play
without anyone running known-suspect commands.

**Notes:**
- Likely culprits per `SESSION_STATE.md` Known Issue #6:
  - `area_update`/`update_handler` ticks running on DS-specific player
    state (giants, plague, pyrokinesis curses) the stock-ROM update.c
    tail doesn't recognise.
  - `fight.c` reaching into stubbed `act_combat.c` paths and getting
    inconsistent state back.
  - Clan iteration over the synthesised-empty `clans.lst`.
- Phase B Step 2 (combat verb porting) probably reduces frequency as
  stubs become real implementations. Defer formal diagnosis until
  Phase B is further along; if still occurring, attach gdb under
  `-O0 -g` for stack traces.

---

## Resolved

### BUG-000: Template (delete when first real bug closes)

Empty entry just to anchor the section. Delete me when you close your
first real bug.

