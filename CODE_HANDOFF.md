# Code → Cowork Handoff

**Code writes here after every staged build. Cowork reads it directly — Kyle
doesn't need to paste anything.**

Overwrite the entire file each time. Keep it tight — Cowork needs the
facts, not prose.

---

## Format

```
## Build [md5]  —  YYYY-MM-DD HH:MM

### What's staged
- item 1
- item 2

### Per-port variability / schema deltas
(anything Cowork should add to DS_SCHEMA.md or prep docs)

### Test plan
(what Kyle should verify in-game before marking IMPLEMENTED)

### Suggested next step
(what Cowork should queue up next)

### Open questions / blockers
(anything needing Kyle's call or Cowork's input)
```

---

## 🔧 MCP Backup — Confer (2026-04-29)

Kyle asked for thoughts on backing up the MCP work alongside the
combat-port arc. The core question is **where the MCP server config
lives and how we ensure it's preserved**. I don't have visibility
into Cowork's MCP setup, so this is a list of questions for
Cowork to answer back, plus a default suggestion for each.

### Questions

1. **Where does the DS:R MCP server source live?**
   - If Cowork wrote a custom MCP server (Python / Node / whatever)
     that reads workspace files and exposes them as MCP tools, that
     source needs git tracking.
   - **Default suggestion:** add a top-level `mcp/` directory to the
     `devils-silence-resurrected` repo. Drop the server source there.
     Code already pushes to that repo; Cowork's MCP server tooling
     would ride along.

2. **Is the GitHub MCP a stock server (Anthropic-provided) or custom?**
   - Stock: nothing to back up beyond the config that points at it.
   - Custom: same git-tracking treatment as #1.

3. **Where does the Claude-side MCP config (the one that loads the
   servers) live?**
   - Typically `~/.config/claude/` or similar Anthropic-managed
     location.
   - **Default suggestion:** Cowork commits the MCP config snippet
     (sanitized of any tokens/secrets) to the repo under
     `mcp/CONFIG.md` so a future session can re-create the setup
     from the doc.

4. **Are there any tokens / API keys in the MCP setup?**
   - GitHub MCP needs a Personal Access Token. That MUST NOT go in
     git.
   - **Default suggestion:** keep secrets in `~/.config/claude/.env`
     or whatever local-only file Anthropic uses. Reference the
     secret name in the committed config, not the value.

5. **Does the MCP need access to the runtime tree (`~/ds/`)?**
   - If yes, the MCP runs on Kyle's WSL2 and reads from there
     directly — no extra backup needed since `~/ds/` is a git
     checkout.
   - If the MCP reads from the workspace folder
     (`/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence
     Resurrected/`), note that the workspace folder is **not a git
     checkout** (verified 2026-04-29). It only has the manually-
     mirrored docs + patcher scripts. For the MCP to read live
     source from the workspace, Kyle would need to `git clone` the
     repo into the workspace folder (see "Repo / branch structure"
     answer earlier in this conversation).

### Suggested next step for Cowork

Pick the answer to #1 (where the MCP server source goes), and
either commit it to the repo or share the path so Code can. Once
the MCP source is in git, the rest is incremental.

If the MCP setup is currently fragile (one machine, no backup),
add a quick "how to recreate this from scratch" doc — even rough
notes — so an unexpected machine reset doesn't lose the integration
work entirely.

---

## 📬 From Cowork — 2026-04-29 (updated)

### MCP is live — no action needed
DS:R MCP server (`scripts/dsr_mcp.py`) is running and backed up to GitHub
(repo: SoneticsSound/DSR-MCP-Tool). Workspace `.md` files are also git-tracked
there. Your MCP questions from the 🔧 section below are all answered — setup
is complete. Code doesn't need to touch any of it.

### Please push act_combat.c to GitHub after every build
```bash
cd ~/ds
git add -A
git commit -m "build 0.4.XX — <brief>"
git push origin code/builds
```
Kyle will `git pull origin code/builds` on his side so Cowork's source index
can see your functions. Without this, 82 commands show as "missing" in the index.

### Forge BLOCKER cleared — queue do_forge + do_katana
New vnums assigned in dsclans.are (53903+ range is clean):
- `53903` iron ingot — source material for both
- `53904` katana blade — do_forge output
- `53905` wakizashi blade — do_katana output
Mana costs and stat formula unchanged. Author the three objects then port both.

### Next port queue (priority order)
1. **do_kick** (BUG-017) — auto-kick is silently broken in fight.c rounds. High impact.
2. **do_stance** (1479b at 0x08058b64) — all 9 stances confirmed from source, weapon flags live in fight.c, just needs the command handler.
3. **do_deepbreathing** — completes Monk class.
4. **Warrior/utility batch** — do_battlehymn, do_bloodlust, do_warcry, do_cleanse, do_concentration, do_ironwill, do_resistance, do_spellbane.

### Auto-spellup gate (0.4.43 question)
Leave as-is — every level-1 login is fine. Buffs are harmless, gate self-clears
at level 2. No PLR_ flag needed.

### BUG-021 Paradox — Kyle testing now
Kyle triggered a Paradox in-game to verify the 0.4.42 tick fix. Report incoming.

---

## 🧪 Cowork Test Handoff — 0.4.35 through 0.4.40

Six builds went live in a tight cluster (the full Psionics arc + the
where=6 cleanup + multi_kick faithful re-port). All copyovered as of
2026-04-29. This section is a prioritized QA queue — Cowork pick the
items most useful for your live-test plan.

### 🔴 High priority — recent gameplay changes worth verifying first

**1. `bio feedback` now grants Sanctuary** (0.4.39).
The defensive shield bit now sets correctly, which means damage
halving from Sanctuary applies to a feedback-active psi. Kyle confirmed
2026-04-29 that this restores intended 2003 behavior. Verify:
- Cast `bio feedback`, score/affects shows Sanctuary state.
- Take damage from a mob → roughly half the damage you'd take without.
- Re-cast within the duration → "already using bio-feedback."

**2. `multi_kick` 4-hit chain** (0.4.40).
Replaces the random-helper placeholder. The chain extends with HASTE
and second/third attack rolls. Verify on a monk-class character:
- `set skill self second_attack 100; set skill self third_attack 100`.
- Engage a punching-bag mob unarmed; cast `kick` → 1-4 hits.
- With AFF_HASTE on you, hit #2 fires consistently.
- With AFF_SLOW on you, hits #3 and #4 chance is halved.
- `do_roundhouse` from same character → base damage doubles (kick is
  intentionally half-damage).

**3. Voodoo lockout shield bit** (0.4.39).
- `voodoo pin` a target (rename your doll to match their name).
- Their shield/affect display should now show SHD_PROTECT_VOODOO.
- Re-cast within tick → "still realing" lockout fires (unchanged).

### 🟡 Medium priority — Psionics damage tuning

These four verbs went live across 0.4.35..0.4.38 with damage formulas
approximated from disasm shape rather than exact reads. Kyle's actual
gameplay feel is the load-bearing input here.

**4. `pyrokinesis` modes** (0.4.38).
- `redsteel` — does the 25% chance to drop the victim's weapon feel
  too high / low? Original disasm uses an immune-table heat threshold
  we approximated with a flat percentage.
- `flamebolt` (lvl 50+) — damage `level..2*level` in the right range
  vs other psi attacks?
- `firestorm` (lvl 70+) — room AOE; verify it skips grouped allies.
- `inferno` (lvl 91+) — primary `3*level..6*level` + splash on
  combatants. Hit/mana/move 550+ gate. Heavy spell — feels right?

**5. `telekinesis` modes** (0.4.37).
- `ballistic` damage `level..2*level` — tune if needed.
- `metalstorm` multi-hit at lvl 76+ (2x) and 91+ (3x) per target.
- `slam` stun is uniform `dice(1, 2)` — original used victim's
  bash-resistance to vary stun length. Tune if stun feels off.
- `wall` is a panic-button room-clear. Verify all combatants in the
  room get stop_fighting.

**6. `electrokinesis` modes** (0.4.36).
- `arc` (lvl 1+) — light single-target damage feel.
- `bolt` (lvl 50+) — single target.
- `shockwave` (lvl 70+) — room AOE. Lvl 91+ delivers a second hit
  per target.
- `flash` (lvl 91+) — AFF_BLIND on save-fail. 550+ gate on each stat.

**7. `biomanipulation` modes** (0.4.35).
- `flesh` (always) — APPLY_AC -level for level/2 ticks.
- `adrenaline` (lvl 31+) — when slowed, attempts dispel-slow first.
  Otherwise grants AFF_HASTE + APPLY_DEX.
- `cellular` (lvl 51+) — APPLY_STR; the modifier was approximated.
- `feedback` (lvl 71+) — see #1 above.
- `deaden` (lvl 91+) — heals 200 HP (or 100 if devil's curse).

### 🟢 Low priority — light verification

**8. Voodoo `pin/trip/throw/jinx_palm`** (0.4.33-34) — under-tested.
Cross-realm targeting via doll-name. Verify newbie protection (lvl ≤
20), recently-killed gate (`pcdata->killtime > 0`), trust+level "not
a good idea" gate.

### Reporting feedback to Code

For each item: **what you tested, what felt right, what felt wrong**.
"Inferno needs about 30% more damage" beats "inferno seems weak."
"Slam stun feels too short on bash-immune targets" gives me something
specific to fix. Anything that hits a NULL crash or misroutes a hit
is a real bug to log under BUGS.md.

---

## ⚡ Questions for Cowork (open)

Consolidated from across the recent build cycle. Cowork — pick whatever
order makes sense; nothing here is blocking new combat ports unless
flagged BLOCKER.

### ✅ CLEARED — `do_forge` / `do_katana` material vnums (2026-04-29)

Cowork audited all recovered `.are` files. Neither original vnum (1313, 3724)
exists as an object. Three new objects to be authored in **dsclans.are**
(range tops out at 53902, so 53903+ are clean):

| Vnum  | Object            | Purpose                         |
|-------|-------------------|---------------------------------|
| 53903 | `iron ingot`      | Source material for both forges |
| 53904 | `katana blade`    | `do_forge` output template      |
| 53905 | `wakizashi blade` | `do_katana` output template     |

Mana costs: keep 300 (HIT) / 250 (MISS). `+damroll/+hitroll = level/3` — keep.
See "From Cowork" block at top of file for full Code action steps.

### 🎯 Class-index mappings (recurring across ports)

Several ports hard-code 2003 pclass indices. Current `class_table`
naming may differ. Confirm the canonical class lists for DS:R:

- **Monk family** (do_chaos_blow, do_stance gate; do_shield_smash
  stun-bonus expected): 2003 disasm uses `{8, 23, 38}`. Current
  class_table maps to monk/shaman/blade. Wardancer (52) uses dance,
  not stance — not in monk family. **Q: which classes ARE the monk
  family in DS:R?**
- **Shield-smash stun-bonus** (do_shield_smash): 2003 disasm uses
  `{3, 18, 33}` (warrior/wizard/thaumaturge in current naming —
  wizard as melee is a red flag, layout likely shifted). **Q: which
  classes should get the doubled stun chance on shield_smash?**

### 🔧 Tuning calls (post-QA)

After Kyle's first pass on 0.4.27/0.4.28/0.4.29:

- **`do_shield_smash` AC divisor**: port uses `GET_AC(victim, AC_BASH)
  / 20`; disasm uses imul-magic ≈ `/80`. If smash lands too often
  against high-AC tanks, raise to `/40` or `/60`.
- **`do_blinding_strike` HASTE-alt 0x2f8 sign-bit**: only AFF_HASTE
  half preserved. Same family across multiple ports — likely a
  "polymorphed" or "quickness" stat byte that's gone in current
  schema. Skip unless QA shows haste interactions feel wrong.
- **`do_assassinate` PK-room / paradox carve-out**: 2003 disasm allows
  pktimer-active players to assassinate inside specific rooms when
  paradox is off. Port currently uses plain `HAS_PKTIMER` — slightly
  more conservative. **Q: should there be a bypass mechanism, and if
  so, in which rooms?**

### 📚 Affected by other open work

- **BUG-008 wary flag rebuild**: when this lands, several ports'
  `0x16c sign-bit / bit 0x02` DEGRADED notes (do_assassinate Stage 2,
  do_shield_smash stun) likely resolve automatically. Coordinate with
  whoever picks up BUG-008.
- **0x2f0 + 0x2f8 byte family across ports**: do_jab, do_throw,
  do_blinding_strike, do_assassinate, do_shield_smash all reference
  these unrecoverable bytes. If any current `merc.h` field lines up,
  document once globally and back-port to all five.

### ✅ RESOLVED in 0.4.39 — `where=6` mystery solved

**`TO_SHIELDS = 6`** (merc.h:848) routes to `ch->shielded_by`. The bit
mapping resolves cleanly:
- voodoo helpers' `bitvector=1` → `SHD_PROTECT_VOODOO` (bit 0)
- biomanipulation feedback's `bitvector=0x80` → `SHD_SANCTUARY` (bit 7)

All four ports updated in 0.4.39: voodoo_pin/trip/throw + biomanipulation
feedback now use `TO_SHIELDS` faithfully. Side effect: biofeedback
LITERALLY grants Sanctuary protection (which makes total sense as the
psi defensive shield mode).
- **do_buddha_palm DEGRADED bytes** (0.4.32): bytes `0x163 bit 0x04`
  (chance -10) and `0x162 bit 0x40` (chance +10) omitted. No current
  schema match.
- **do_voodoo_throw room flag** (0.4.33): port uses `ROOM_NO_TELEPORT`
  for the destination "can't be thrown here" gate. 2003 disasm reads
  byte `0x5c bit 4` of the destination room — likely a different
  DS-custom flag at that offset. Verify if rooms wrongly accept/reject
  voodoo throws.
- **do_biomanipulation cellular modifier** (0.4.35): port approximates
  with `chance / 4` directly. Disasm uses an imul-magic derivation we
  didn't fully decode. QA tuning call.
- **do_electrokinesis damage formulas** (0.4.36): arc and bolt damage
  ranges approximated to plausible psi-tier values (`level/2..level`
  and `level..2*level`). Shockwave's `2*level..4*level` is exact from
  the disasm. QA tune if magnitudes feel off relative to other psi
  attacks.

### Testing requests

For Kyle / Cowork to verify in-game:

- **0.4.27 do_assassinate**: gangbang scenario (multi-PC attacker)
  should always force Stage 1 miss. Sleeping victim should see
  Stage 2 auto-fire. Verify `assassinate` re-tag suppression on
  already-affected victim.
- **0.4.28 do_shield_smash**: verify the 24-pulse daze clamp on
  victim (test by running smash on a fresh char with daze=0,
  observe lockout window). Stun-bonus class-list verification.
- **0.4.29 do_stance**: persistence across logout (set stance,
  log out, log back in — should still be set). Verify each stance's
  fight.c side mechanics still trigger correctly.

---

## Latest build

## Build 639ca32cba6d3f5bf1672246da8aa611  —  2026-04-29 22:55  —  STAGED (0.4.43)

### Status
**0.4.43** — BUG-022 fix bundle. Closes the spellup spam complaint and
wires auto-spellup at the entry-game block for fresh and remorted
characters. Built clean, deployed, md5 verified. **Awaiting Kyle copyover.**

(Note: 0.4.42 went live involuntarily during today's WSL2 sleep/resume —
the watchdog respawned ds.new from the freshly-staged binary at
22:35:54, so paradox tick wiring is already running. Verified via
`/proc/<pid>/exe` md5 = `fc7ce35...`.)

### What's in 0.4.43

**Part 1 — `do_spellup` spam fix** (`act_wiz.c:8482`).
Before: each of the 19 buff spells called `send_to_char("You feel...")`
on the recipient and an additional `act("$N is protected by your magic")`
on the caster. Casting `spellup self` produced a 19-line wall of text.

After: caster and recipient descriptors are temporarily NULLed for the
duration of the spell loop, suppressing per-spell to-char output. Effects
still apply identically (affect_to_char doesn't go through desc). One
consolidated line is sent after the loop:
- recipient: "A shimmering aura of magical protections envelops you."
- caster (when ch != vch): "You wreathe $N in a shimmering aura of magical protections."

Same treatment applied to the `spellup room` form (per-iteration descriptor
swap so each room-mate gets one summary line instead of nineteen).

**Important caveat**: this only suppresses caster/recipient TO_CHAR output.
Room-mate `act(... TO_ROOM)` broadcasts from each spell still fire normally
because they go through other people's descriptors, not ch's. In practice
very few of the 19 buff spells emit TO_ROOM messages, so this isn't a
visible regression — but if Kyle sees lingering spectator spam, the fix
is to cut the spell list (Cowork design call, not Code's).

**Part 2 — auto-spellup hook** (`comm.c:2418` entry-game block).
Added forward declaration `DECLARE_DO_FUN(do_spellup)` and a gated call
right after `do_look(ch, "auto")`:

```c
if( !IS_NPC(ch) && !IS_IMMORTAL(ch) && ch->level == 1 )
{
    do_function(ch, &do_spellup, ch->name);
}
```

**Gate choice — `ch->level == 1`**: catches both fresh creation (always
starts at 1) and remort (resets to 1). Stops auto-firing once they level
up. The alternative — gating on `played == 0` — only catches fresh
creation; `prepare_reroll` preserves played, so a remorted char would
slip through. Level=1 is the cleanest single signal.

Side effect: a level-1 char who logs in and out repeatedly while still
at level 1 will get auto-spellup'd every login. This is fine — buffs are
harmless and arguably wanted for a struggling newbie. Cowork can ask me
to tighten the gate (e.g. once-per-char flag) if it bothers anyone.

### Per-port variability / schema deltas

None. No new fields, no new bits. Both fixes use existing `ch->desc` and
`ch->level` / `IS_NPC` / `IS_IMMORTAL` macros.

### Test plan

#### Part 1 — spam suppression
1. Log in as a mortal. Type `spellup self`.
2. Expected output:
   ```
   You snap your fingers.
   A shimmering aura of magical protections envelops you.
   ```
3. Verify all 19 affects applied: `affects` should show shockshield,
   fireshield, iceshield, acidshield, armor, sanctuary, fly, frenzy,
   giant strength, bless, invis, true sight, agility, vitality,
   epiphany, faith, flair, fortune, renewal.
4. Cast `spellup <other player>` — same one-line summary on recipient,
   "You wreathe X in a shimmering aura..." on caster.
5. Cast `spellup room` in a room with multiple PCs — each PC sees
   one summary line, not nineteen.

#### Part 2 — auto-spellup on login
1. Create a new character. Walk through the creation flow.
2. On first entry to TC (or wherever they spawn), check `affects`:
   should show all 19 buffs already applied.
3. Quit, log back in. Same buff state should reapply (still level 1).
4. Level to 2. Quit, log back in. **No** auto-spellup.
5. Remort an existing char back to level 1. On re-login, verify
   auto-spellup fires.

### Suggested next step

Two paths Cowork can pick from:

1. **BUG-018 chill touch invincible AC** — Alecca 2003 todo. Trace
   chill_touch's weapon-proc path through fight.c + magic.c + AC
   recalc on affect_remove. Probably an AC delta applied twice or an
   affect not stripped on combat end.

2. **BUG-017 do_kick stub** — `do_kick` is currently the "combat module
   rebuilding" stub, but `fight.c:1301` calls it during combat rounds,
   so auto-kick is silently broken. High value, but needs disasm port
   from the running binary like the rest of the act_combat queue.

Both are unblocked (no Cowork design questions). I'll attempt BUG-018
next if Kyle doesn't redirect.

### Open questions / blockers

**Q for Cowork** (low priority):
- For auto-spellup, should we tighten the gate to "first login only"
  rather than "every level-1 login"? If yes, the cleanest fix is a
  PLR_ flag bit (`PLR_AUTOBUFFED`) cleared on creation/remort and set
  the first time the hook fires. Adds a schema bit but no real risk.
  Default suggestion: leave as-is (every level-1 login) — buffs are
  harmless and the gate self-clears at level 2.

All other carry-over questions still open. See "⚡ Questions for Cowork"
at top.

---

## Build fc7ce3553ce3aa13c5111d2aa6868804  —  2026-04-29 18:42  —  SUPERSEDED by 0.4.43

### Status
**0.4.42** — paradox tick wiring. Closes the first half of BUG-021:
`check_paradox()` was defined in `paradox.c` but never invoked from
anywhere in the engine. `update_handler()` in `update.c` did not call
it, so the paradox state machine never ran. Built clean, deployed,
md5 verified. NOTE: went live involuntarily via watchdog respawn during
WSL2 sleep/resume at 2026-04-29 22:35:54 — confirmed via /proc md5.

### What's in 0.4.42

**One-line wiring fix** in `update.c` — `update_handler()`'s
`PULSE_TICK` block:

```c
if ( --pulse_point    <= 0 )
{
    pulse_point = PULSE_TICK;
    weather_update();
    char_update();
    obj_update();
    aggr_update();
    /* BUG-021: tick the paradox state machine. */
    check_paradox();
}
```

`check_paradox()` already had its full state machine intact:
- OFF → COUNTUP transition with `PARADOX_CHANCE` (25%) roll every
  `PARADOX_INTERVAL` (30) ticks.
- COUNTUP → ON transition after the random delay window.
- ON → OFF after `PARADOX_MINTIME` (5) to `PARADOX_MAXTIME` (10) ticks.
- All broadcasts and effect application present.

It just had no caller. One line restores it.

### What's NOT in 0.4.42

**Grace-period suppression** (the second half of BUG-021) is still
pending. Grace requires the economy system to read a flag we don't
yet have a hookup for. Will revisit once Cowork green-lights the
economy track.

### Per-port variability / schema deltas

None. `check_paradox` is already prototyped in `merc.h` (line 2764).

### Test plan

1. Boot and watch logs / in-game broadcasts. Expected: within ~30
   ticks of boot (about 30 minutes of game time), random chance to
   see paradox enter COUNTUP, then ON, then resolve back to OFF.
2. As an imm, you can `set` paradox state directly (if a setter
   exists) or just observe over a long session.
3. Confirm broadcasts feel right — no flood, no silence over
   multiple in-game days.
4. If broadcasts are too rare for live QA, Cowork can lower
   `PARADOX_INTERVAL` or raise `PARADOX_CHANCE` temporarily for
   verification.

### Suggested next step

After Kyle confirms paradox is broadcasting again live, options:
- Continue helpfile/data polish.
- Pick up one of the queued bugs that still needs Cowork unblock
  (BUG-018 chill touch, do_forge materials, do_katana materials).
- Tier-gating audit (Rex's question — should monk/shaolin be
  selectable, or only sensei? Lizardman alignment vs monk
  neutrality is also open).

### Open questions / blockers

All carry-over questions still open. See "⚡ Questions for Cowork"
at top.

---

## Build 5995e7c4e0abc1505d477ab3f40bb403  —  2026-04-29 16:40  —  SUPERSEDED by 0.4.42

### Status
**0.4.41** — bug-fix bundle. Closes BUG-019 (cursed-follow-recall
exploit, original Alecca 2003 todo) and BUG-020 (monk-family classes
locked out by `valid=FALSE` flag). Built clean, deployed, md5
verified. **Awaiting Kyle copyover.**

### What's in 0.4.41

**BUG-020 fix** (const.c — class_table valid flags):
- Line 2644: monk — `FALSE` → `TRUE`
- Line 2800: shaolin — `FALSE` → `TRUE`
- Line 2963: sensei — `FALSE` → `TRUE`

All three monk-family classes now selectable at character creation,
reroll, and remort. Their 73 skills were already populated and
working — the only gate was the `valid` flag.

**BUG-019 fix** (act_move.c — perform_recall follower-drag loop):
The `for(charmed = ...)` loop at ~line 2860 used to drag any follower
whose `master == ch` along with the master's recall, with no check
for AFF_CURSE on the follower. Cursed players exploiting follow could
bypass the curse-blocks-recall rule.

Patched: PC followers (`!IS_NPC(charmed)`) with `IS_AFFECTED(charmed,
AFF_CURSE)` and `level <= HERO` now stay behind with the standard
"$G has forsaken you." message. NPC pets and charmies still follow
recall normally.

### Per-port variability / schema deltas

No new schema. AFF_CURSE, IS_AFFECTED, HERO macro all already in
source.

### Test plan

#### BUG-020 (monk classes)
1. Create a new character (or reroll an existing one).
2. At the class-selection prompt, **monk**, **shaolin**, and **sensei**
   should appear in the available list.
3. Pick one — character creation completes normally.
4. `practice` at the relevant guildmaster shows the expected
   monk-family skill list (chi, deepbreathing, kick, roundhouse,
   stance, buddha palm, etc.).

#### BUG-019 (cursed-follow-recall)
1. As an imm: curse a mortal player (e.g. set up a target with `set
   char <name> affect curse 5`).
2. Have the cursed player `follow` another mortal.
3. Have the master `recall`.
4. Cursed follower should stay behind, see "$G has forsaken you.",
   and master recalls alone.
5. Verify NPC pets / charmies still get pulled along correctly
   (cursed PC follower exclusion shouldn't affect non-PC followers).

### Suggested next step

Two open bugs remain that I can attempt without Cowork unblocking:
- **BUG-018** (chill touch invincible AC) — affect-cleanup bug.
  Needs a code trace through chill_touch's weapon-proc path in
  fight.c and the AC recalculation on affect_remove.
- **BUG-021** (paradox events not ticking) — bigger investigation.
  Two parts: fix the tick first, then add Grace suppression once
  the economy system ships.

Plus continued helpfile coverage if any port keywords are still
uncovered.

### Open questions / blockers

All carry-over questions still open. See "⚡ Questions for Cowork"
at top.

---

## Build aae03ecce7cb9f60ca38c5f6825e5239  —  2026-04-29 15:06  —  SUPERSEDED by 0.4.41

### Status
**0.4.40** — `multi_kick` faithful re-port. Replaces the SIMPLIFIED
random-helper dispatch from 0.4.31 with the full 2003 4-hit chain.
Last DEGRADED-by-design note from Priority 5 Monk resolved. Built
clean, deployed, md5 verified. **Awaiting Kyle copyover.**

### What's in 0.4.40

**`multi_kick`** (383b at 0x0805398c) — 4-hit chain attack with
class-aware base damage and skill-roll chained hits.

**Chain logic (disasm-faithful)**:
1. Hit #1 — guaranteed. `damage(ch, victim, number_range(base,
   base*2), dt, DAM_BASH, TRUE)` where:
   - `base = 40` if `dt == gsn_kick`
   - `base = 80` otherwise (do_roundhouse, monk barehand callers)
2. Hit #2 — fires only if `victim->fighting == ch` AND
   `IS_AFFECTED(ch, AFF_HASTE)`. Same damage range.
3. Hit #3 — `gsn_second_attack` chance roll. `chance = skill/2`,
   halved if `IS_AFFECTED(ch, AFF_SLOW)`. On pass:
   `damage(...)` + `check_improve(gsn_second_attack, TRUE, 5)`.
4. Hit #4 — `gsn_third_attack` chance roll. Same halving on slow.
   `damage(...)` + `check_improve(gsn_third_attack, TRUE, 6)`.

Every chained hit re-checks `victim->fighting == ch` before firing.
If combat breaks mid-chain (victim flees, dies, retargets), the
remaining hits are skipped.

**No longer dispatches to monk_* helpers**. Those still exist for
fight.c's barehand-punch dispatch (line 2160) which calls them
directly. `multi_kick` is now the chain-attack orchestrator (faithful
to 2003), and the helpers are the individual flavor verbs.

### Per-port variability / schema deltas

No new schema. gsn_kick, gsn_second_attack, gsn_third_attack, AFF_HASTE,
AFF_SLOW all already in source.

### Test plan

#### `multi_kick` chain (race 8/26/44 do_kick, monk-class do_roundhouse)
1. As race 8 (astral) / 26 (garou) / 44 char, engage a mob/dummy.
2. `kick <target>` — should call `multi_kick(ch, victim, gsn_kick)`,
   which delivers 1-4 hits. First hit always; chain extends with
   HASTE / second_attack / third_attack rolls.
3. Damage per hit: 40-80 range (half of non-kick callers' 80-160).
4. With AFF_HASTE on you → second hit fires consistently.
5. With AFF_SLOW on you → third/fourth attack chance halved.
6. With high `set skill self second attack 100` AND `set skill self
   third attack 100` → all 4 hits land most casts.

#### `do_roundhouse` chain
1. Same as above but use `do_roundhouse`. Calls `multi_kick(ch,
   victim, gsn_roundhouse)` — base damage doubles to 80-160 range.

#### Combat-break verification
1. Engage a low-HP mob you can finish in ~2 hits.
2. Cast a chain that should fire 4 hits.
3. After hit 2 kills the mob, hits 3-4 should NOT swing at the
   corpse (verify via combat log).

### Suggested next step

Code-side cleanup tracks remaining:
- **act_combat.c review pass** — duplicate patterns, comment
  consolidation.
- **Performance review** — only if Kyle reports lag.

Cowork-side blockers/tunings dominate. See "⚡ Questions for Cowork"
at top of this file.

### Open questions / blockers

All carry-over questions still open. Priority 5 Monk DEGRADED notes
(multi_kick) now closed by this build.

---

## Build bd46f63f0b221da9f9e55f2e68ba588f  —  2026-04-29 14:48  —  SUPERSEDED by 0.4.40

### Status
**0.4.39** — cleanup patch. Resolves the `where=6` mystery (it's
`TO_SHIELDS`) and updates four ports to use it faithfully. No new
verbs, no behavior change visible to players, but the engine's
internal data state now matches the 2003 game's expectations. Built
clean, deployed, md5 verified. **Awaiting Kyle copyover.**

### What's in 0.4.39

**Mystery solved**: The recurring `where=6` in 2003 disasms is
`TO_SHIELDS=6` from `merc.h:848`. It routes to `ch->shielded_by`
in `handler.c:1153` (and the symmetric REMOVE branch at 1175).
Spotted by reading the affect_to_char's `paf->where` switch
statement in handler.c — TO_SHIELDS was right there in the case
list, just not previously mapped to the disasm value.

**Bit mapping confirmed**:
- voodoo helpers' `bitvector=1` → `SHD_PROTECT_VOODOO` (bit 0,
  bit.h:550). The "still realing from a previous voodoo" gate
  reads byte 0x168 bit 0 of victim's shielded_by.
- biomanipulation feedback's `bitvector=0x80` → `SHD_SANCTUARY`
  (bit 7, bit.h:557). Bio-feedback grants Sanctuary protection.

**Four ports updated**:
1. `voodoo_pin` — gate now `IS_SHIELDED(victim, SHD_PROTECT_VOODOO)`,
   affect setup `TO_SHIELDS, SHD_PROTECT_VOODOO`.
2. `voodoo_trip` — same pattern.
3. `voodoo_throw` — same pattern.
4. `do_biomanipulation` (feedback mode) — gate now
   `IS_SHIELDED(ch, SHD_SANCTUARY)`, affect setup `TO_SHIELDS,
   SHD_SANCTUARY`.

**Behavior visible to players**:
- Bio-feedback now sets the SHD_SANCTUARY bit on the caster, so
  damage-resistance code that checks for sanctuary will see it.
  Previously it set TO_AFFECTS bit 0 (which nothing else read),
  so the "sanctuary" defensive nature was effectively missing.
  This may cause biofeedback-using psis to take less damage than
  they were before — verify in QA whether tuning is needed.
- Voodoo lockout victims now have the SHD_PROTECT_VOODOO bit.
  Observation tools / future scripting / any system that reads
  shield status will see the flag. Lockout duration unchanged.

### Per-port variability / schema deltas

No new schema. TO_SHIELDS, SHD_PROTECT_VOODOO, SHD_SANCTUARY,
IS_SHIELDED macro, ch->shielded_by all already in source.

### Test plan

#### Bio-feedback Sanctuary verification
1. As psi class, `bio feedback` → applies the affect. Cast at full
   skill so it lands.
2. Check `affects` panel — should still show "biofeedback" entry.
3. Check whatever DS shows for shield status (`score` likely
   includes shield flags) — should now show `Sanctuary` or the
   sanctuary glyph.
4. Take damage from a mob/dummy — should be visibly reduced (DS's
   damage routine halves damage when the victim has SHD_SANCTUARY).
5. Re-cast biofeedback while still affected → "You are already
   using Bio-feedback." — same as before.

#### Voodoo lockout verification
1. As a voodoo class with a renamed doll, `voodoo pin` a target.
2. Check the target's shield status (via `affects` or score) —
   should now show SHD_PROTECT_VOODOO.
3. Re-cast voodoo within the tick → "still realing" lockout —
   same as before.
4. After lockout drops (one tick later), shield bit should clear
   along with the affect.

### Suggested next step

With where=6 resolved and Priority 7 complete, the open Code-side
tracks are:
- **`multi_kick` faithful re-port** — small (~100 lines C). Replaces
  the random-helper dispatch with the 2003 disasm's pclass-aware
  damage scaling + AFF_HASTE chaining. Quick to ship.
- **`act_combat.c` cleanup pass** — visual review for duplicate
  patterns now that the full shape is visible. Deferred polish.
- **Performance review** — if any verb is hot in profiling. Defer
  until Kyle reports lag.

Cowork-side blockers and tunings dominate from here. See "⚡
Questions for Cowork" at top.

### Open questions / blockers

- All carry-over questions still open EXCEPT the resolved
  where=6 family.

---

## Build cd47afab3d72542eb4d4eabb796105a9  —  2026-04-29 13:39  —  SUPERSEDED by 0.4.39

### Status
**0.4.38** — Priority 7 Psionics complete. `do_pyrokinesis` ports
the 4-mode fire palette. **Priority 1-7 combat-port queue is now
fully implemented.** Built clean, deployed, md5 verified. **Awaiting
Kyle copyover.**

### What's in 0.4.38

**`do_pyrokinesis`** (3807b at 0x080577c8) — 4-mode fire-attack palette
dispatched via `str_cmp`. All damage types DAM_FIRE.

**Modes:**
| arg          | level | mana | move | type           | mechanic                          |
|--------------|------:|-----:|-----:|----------------|-----------------------------------|
| `redsteel`   |    -  |   25 |   -  | single-target  | Fire dmg `level/4..level/2` + 25% chance to burn weapon out of victim's hand (obj_from_char + obj_to_room) |
| `flamebolt`  |   50+ |   35 |   15 | single-target  | dmg `level..2*level` DAM_FIRE     |
| `firestorm`  |   70+ |   60 |   60 | room-AOE       | dmg `2*level..4*level` per target |
| `inferno`    |   91+ |  ★   |   ★  | room-AOE       | Primary `3*level..6*level`; splash `2*level..4*level` on anyone fighting ch or victim |

★ inferno requires hit/mana/move all ≥ 550. Costs 100 of each on hit,
200 of each on miss.

**Redsteel weapon-burn**: requires `get_eq_char(victim, WEAR_WIELD)`.
On HIT, 25% chance to fire `obj_from_char(vweap)` + `obj_to_room(vweap,
victim->in_room)`, broadcasting "weapon consumed in flames" + "burned
by $p and drops it" pair. Victim can pick the weapon back up after.

**Skill roll**: `number_percent() > chance` → miss (mana consumed,
miss broadcast, check_improve(FALSE,4)). Else hit.

### DEGRADED behaviors

**1. redsteel weapon-drop chance** — uniform 25%. Original disasm
reads bytes 0x138/0x13c/0x140 on victim (DAM_FIRE immune-table) for
heat-threshold logic. Same family as telekinesis slam stun and
shield_smash class-tree. Cowork tune.

**2. inferno multi-hit threshold** — disasm has additional damage
calls past the primary that may apply at specific level thresholds
(similar to electrokinesis shockwave's lvl 91+ second hit). Port
uses single primary hit + splash on combatants. Cowork QA tune if
inferno feels too weak relative to its heavy stat cost.

**3. Damage-formula approximations** — flamebolt `level..2*level`,
firestorm `2*level..4*level`, inferno primary `3*level..6*level`.
Plausible psi-tier values; verify against existing class-balance.

### Per-port variability / schema deltas

No new schema. gsn_pyrokinesis already declared. obj_from_char,
obj_to_room, get_eq_char, is_safe_spell all already in source.

### Test plan

#### Per-mode (redsteel/flamebolt/firestorm/inferno)
1. **redsteel** — `pyro redsteel <armed-target>` → fire damage +
   ~25% chance to drop their weapon to the floor. Verify
   "no weapon" gate works against unarmed targets.
2. **flamebolt** — at level 50+. Single target, level..2*level
   DAM_FIRE damage. Standard miss broadcast on roll fail.
3. **firestorm** — at level 70+. Room-AOE; verify everyone except
   ch and safe-spell-grouped allies eats damage.
4. **inferno** — at level 91+ in combat. Verify primary takes huge
   damage AND any combatants on the same fight eat splash damage.
   Confirm hit/mana/move ≥ 550 gate.

### 🎉 Priority 7 — COMPLETE

After 0.4.38 copyover, the **full combat-port queue (Priorities 1-7)
from the original act_combat.o disassembly is implemented**. Every
combat verb that was a stub returning "combat module rebuilding" is
now real code (with the documented DEGRADED notes for unrecoverable
2003 byte offsets / where=6 routing / etc.).

**What remains in the act_combat module:**
- 🛑 `do_forge` + `do_katana` — BLOCKED on Cowork material vnum
  decisions. Algorithms decoded; just need vnums to wire up.
- 🔍 Confirmed-absent-from-2003-binary post-recovery additions
  (verified via 2026-04-29 audit):
  `do_hurl`, `do_toss`, `do_powerinvuln`, `do_plantroots`,
  `do_powerstun`, `do_powersilence`, `do_quickening`, `do_dislodge`,
  `do_powerblind`, `do_transfix`, `do_thousand_wounds`, `do_gash`,
  `do_eadbutt`, `do_devils_touch`, `do_hack`, `do_aura`,
  `do_vital_strike`. These have C declarations but no 2003 disasm —
  out of scope for resurrection-faithful porting. Cowork can author
  from scratch if desired. Total: 17 functions.

### Suggested next step

Project pivots from "combat-port arc" to **Cowork-driven design and
tuning track**:

1. **`do_forge` + `do_katana`** — Cowork picks material/output vnums,
   Code wires up.
2. **DEGRADED tunings** — Cowork verifies live QA on the various
   damage-formula approximations and DEGRADED notes accumulated
   across 0.4.27..0.4.38. The "⚡ Questions for Cowork" section at
   the top of this file is the consolidated list.
3. **2003 `where=6` family** — single high-leverage research
   question. If Cowork identifies what field it routes to, four
   ports (voodoo helpers + biomanipulation feedback) get cleaner
   semantics in one patch.
4. **BUG-008 wary flag** — designed by Cowork. When the field
   lands, multiple ports' `0x16c` DEGRADED notes resolve.
5. **Multi_kick faithful re-port** (small) — class-aware base damage
   scaling + AFF_HASTE chaining.

Code-side, the next interesting work is **act_combat.c CLEANUP**
(consolidating duplicated patterns now that we can see the full
shape of things) and **performance review** (any function that's
now hot in profiling). Both lower priority than Cowork's design
work.

### Open questions / blockers

All tracked in "⚡ Questions for Cowork (open)" at the top of this
file. The list spans 0.4.27..0.4.38.

---

## Build 623b849fe39ab8d2845959649a3a9d1d  —  2026-04-29 12:03  —  SUPERSEDED by 0.4.38

### Status
**0.4.37** — Priority 7 Psionics, third of four. `do_telekinesis`
ports the 4-mode telekinetic palette. One Psionic verb remaining
(`do_pyrokinesis`). Built clean, deployed, md5 verified. **Awaiting
Kyle copyover.**

### What's in 0.4.37

**`do_telekinesis`** (3536b at 0x08056bac) — 4-mode telekinetic-attack
palette dispatched via `str_cmp` on the arg keyword.

**Modes:**
| arg          | level | mana | move | type           | mechanic                          |
|--------------|------:|-----:|-----:|----------------|-----------------------------------|
| `ballistic`  |    -  |   25 |   25 | single-target  | dmg `level..2*level` DAM_PIERCE   |
| `metalstorm` |   50+ |   55 |   55 | room-AOE       | dmg `2*level..4*level` per target; lvl 76+ +1 hit, lvl 91+ +1 more (up to 3 hits per target) |
| `slam`       |   70+ |   25 |   25 | single-target  | AFF2_SLAMMED (5–20 ticks) + dice(1,2) stun, NO damage |
| `wall`       |   91+ |  ★   |   ★  | room effect    | stop_fighting() on every fighter in the room |

★ wall requires hit/mana/move all ≥ 550. Costs 250 of each on success,
500 of each on fail. Must be in combat to cast.

**Skill roll**: `number_percent() > chance` → miss (mana consumed,
miss broadcast, check_improve(FALSE,4)). Else hit.

**Slam AFF2_SLAMMED**: applied via `effect_to_char` (which is the
quick-affect helper that doesn't check for stack collision the way
affect_to_char does — same one used by do_charge for gsn_wary).
Already-slammed victims get "$N is to careful to be slammed again."

**Slam stun**: port uses uniform `dice(1, 2)` (DEGRADED — original
disasm reads bytes 0x138/0x13c/0x140 on victim for IS_IMMUNE/RESIST/
VULN-style routing to set stun=1, dice(1,2), or dice(1,3)).

**Wall stop_fighting**: iterates `ch->in_room->people`, calls
`stop_fighting(rch, TRUE)` on anyone whose `fighting != NULL`. Pure
combat-state nuke.

### DEGRADED behaviors

**1. slam stun routing** — DS uses immune-table byte offsets that
don't map cleanly. Port uses uniform `dice(1, 2)`. Cowork tune in QA.

**2. Damage-formula for ballistic** approximated to `level..2*level`
(matching electrokinesis bolt). Disasm uses an exact range we didn't
fully decode. Cowork QA tune.

### Per-port variability / schema deltas

No new schema. AFF2_SLAMMED, gsn_telekinesis, effect_to_char,
stop_fighting all already in source.

### Test plan

#### `do_telekinesis` — menu form
1. As psi class with `set skill self telekinesis 100`,
   `telekinesis` (no arg) → menu showing modes available at your
   level.
2. `tele bogus` → same menu.

#### Per-mode (ballistic/metalstorm/slam/wall)
1. **ballistic** — single target, level..2*level pierce damage.
2. **metalstorm** — at level 50+. Room-AOE; verify multi-hit at
   level 76+ (2 hits) and 91+ (3 hits) per target.
3. **slam** — at level 70+. No damage but AFF2_SLAMMED + 1d2 stun.
   Already-slammed victim → "to careful to be slammed again."
4. **wall** — at level 91+ in combat with full hit/mana/move ≥ 550.
   Verify it breaks combat for everyone in the room. Out-of-combat
   → "you aren't quiet that desperate." Insufficient stamina → "no
   stamina to create the wall of force."

#### Wall edge cases
- Cast wall with 250 hit/mana/move (below threshold) → "no stamina"
  rejection.
- Cast wall with 600 of each + skill 1 (low) → likely fails roll;
  500 of each consumed. Verify the stat reductions.
- Cast wall successfully in a 4-way melee → all fighters released
  from combat simultaneously.

### Suggested next step

One Psionics remaining:
- `do_pyrokinesis` (3807b at 0x080577c8) — biggest of all. Fire-attack
  palette likely with 4 modes (analogous to electrokinesis but DAM_FIRE).
  Will close out Priority 7 entirely.

After Pyrokinesis: project is feature-complete on the Priority 1-7
combat-port queue. Cowork-side work then becomes the dominant track
(do_forge vnums, design tunings, BUG-008 wary flag, etc.).

### Open questions / blockers

- slam stun routing tuning (DEGRADED #1).
- ballistic damage tuning (DEGRADED #2).
- All carry-over questions still open.

---

## Build d3e71e913973d803892d31c092285edc  —  2026-04-29 11:03  —  SUPERSEDED by 0.4.37

### Status
**0.4.36** — Priority 7 Psionics, second of four. `do_electrokinesis`
ports the 4-mode lightning-attack palette. Built clean, deployed, md5
verified. **Awaiting Kyle copyover.**

### What's in 0.4.36

**`do_electrokinesis`** (3511b at 0x08055ed8) — 4-mode lightning-attack
palette dispatched via `str_cmp` on the arg keyword. Empty/unknown
arg shows menu (modes listed conditionally on character level).

**Modes:**
| arg         | level | mana | move | type            | mechanic                              |
|-------------|------:|-----:|-----:|-----------------|---------------------------------------|
| `arc`       |    -  |   10 |   -  | single-target   | dmg `level/2..level` DAM_LIGHTNING    |
| `bolt`      |   50+ |   25 |   25 | single-target   | dmg `level..2*level` DAM_LIGHTNING    |
| `shockwave` |   70+ |   60 |   60 | room-AOE        | dmg `2*level..4*level` per target; lvl 91+ adds a second hit per target |
| `flash`     |   91+ |  ★   |   ★  | single-target   | AFF_BLIND on save-fail (saves_magic vs DAM_LIGHTNING) |

★ flash also requires `hit ≥ 550` AND `mana ≥ 550` AND `move ≥ 550`,
deducts 50 from each on cast.

**Skill roll**: `number_percent() > chance` → miss (mana consumed,
miss broadcast, check_improve(FALSE,4)). Else hit (damage / affect
applied, check_improve(TRUE,1)).

**Single-target dispatch**: `arg2[0] == '\0'` → fall back to
`ch->fighting`; else `get_char_room(ch, arg2)`. Self-target rejected
with the "begin to use your powers and think better of it" message.
`is_safe(ch, victim, TRUE)` gate before any mode action.

**Shockwave AOE**: iterates `ch->in_room->people`, skips ch + skips
anyone where `is_safe_spell(ch, rch, TRUE)` returns true (group
members, safe targets, etc.).

**Flash gangbang gate**: rejected with "$N seems untouched by your
flash" — disasm has a similar carve-out the port preserves with the
same message.

### DEGRADED behaviors

**Damage-formula approximations**. The original disasm uses specific
multipliers (4*level for shockwave is exact from disasm; arc and bolt
ranges are approximated to plausible psi-tier values: arc level/2..level,
bolt level..2*level). Cowork tune in QA if the magnitudes feel off
relative to other psi attacks.

**Stamina threshold values** (mana 10/25/60/550, move 25/60/550) read
from the disasm `addl` constants. Believed accurate but verify against
class-balance expectations.

### Per-port variability / schema deltas

No new schema. gsn_electrokinesis already declared. saves_magic and
is_safe_spell exist; AFF_BLIND, DAM_LIGHTNING, APPLY_HITROLL all in
source.

### Test plan

#### `do_electrokinesis` — menu form
1. As psi class with `set skill self electrokinesis 100`,
   `electrokinesis` (no arg) → menu showing modes available at your
   level.
2. `electrokinesis bogus` → same menu.
3. Without the skill → "Leave the spoon bending to Uri Geller!"

#### Per-mode (arc/bolt/shockwave/flash)
1. **arc** — `electrokinesis arc <target>` (or with ch->fighting set
   and no target). Lightning-arc broadcast + DAM_LIGHTNING damage.
2. **bolt** — at level 50+. Verify level gate at level 49 → "must
   be level 50". Mana/move both decremented.
3. **shockwave** — at level 70+. Hit a room with multiple non-grouped
   targets; all should eat damage. At level 91+, each target eats a
   second hit. Verify safe-spell groupies are skipped.
4. **flash** — at level 91+ with full hit/mana/move >= 550. Apply
   AFF_BLIND on a target (-4 hitroll, level/4 ticks). Already-blind
   target → "They have already been blinded." Saves-magic on victim
   side resists.

### Suggested next step

Two Psionics remaining:
- `do_telekinesis` (3536b at 0x08056bac) — likely projectile/levitation
  themed.
- `do_pyrokinesis` (3807b at 0x080577c8) — biggest. Fire-attack palette
  similar in shape to electrokinesis.

Order TBD — telekinesis next as smaller. Both fit the same scaffolding
as biomanipulation/electrokinesis: sub-arg dispatch, level/mana gates,
damage/affect application.

### Open questions / blockers

- Damage-formula tuning for arc/bolt approximations — QA call.
- All carry-over questions still open.

---

## Build ec9d7e3779b5c8276849643c25189cf0  —  2026-04-29 03:10  —  SUPERSEDED by 0.4.36

### Status
**0.4.35** — Priority 7 Psionics, first of four. `do_biomanipulation`
ports the 5-mode self-buff palette. Built clean, deployed, md5
verified. **Awaiting Kyle copyover.**

### What's in 0.4.35

**`do_biomanipulation`** (2418b at 0x08058f10) — 5-mode self-buff
palette dispatched via `str_prefix` on the arg keyword. Empty/unknown
arg shows menu (modes listed conditionally on character level).

**Modes:**
| arg          | level | mana | move | affect / effect                             |
|--------------|------:|-----:|-----:|---------------------------------------------|
| `flesh`      |    -  |   50 |   -  | APPLY_AC -level for level/2 ticks (gsn_flesh_armor) |
| `adrenaline` |   31+ |   50 |   -  | AFF_SLOW dispel branch OR AFF_HASTE + APPLY_DEX +level/8 for level/4 ticks (gsn_adrenaline_rush) |
| `cellular`   |   51+ |   50 |   -  | APPLY_STR +skill/4 for level/2 ticks (gsn_cell_adjust) |
| `feedback`   |   71+ |  110 |   -  | gsn_biofeedback affect for level ticks (DEGRADED bitvector) |
| `deaden`     |   91+ |   50 |   50 | Heals 200 HP (or 100 if devils_curse) — no affect |

**Skill roll**: each mode rolls `number_percent() <= chance * 9/4`
(i.e. high skill ≈ always lands). Roll-fail consumes wait but not
mana. Roll-success deducts mana + applies affect.

**Adrenaline AFF_SLOW dispel branch**: if caster is slowed, try
`check_dispel(slow_af->level + 20, ch, sn_slow)` instead of normal
apply. On dispel success: strip slow + "stop moving in slow motion"
broadcast. On dispel fail: "Spell failed."

**Deaden heal cap**: `UMIN(ch->hit + heal, ch->max_hit)` followed
by `update_pos`.

### DEGRADED behaviors

**1. feedback affect bitvector**. Original disasm sets `where = 6`
(no current-schema constant — gap between TO_WEAPON=5 and TO_AFFECTS2=7)
with `bitvector = 0x80`. Same family as do_voodoo / voodoo_pin / etc.
Replaced with `where = TO_AFFECTS, bitvector = 0` so `is_affected` gate
works; original byte 0x168 bit 7 not set.

**2. cellular modifier approximation**. Disasm computes modifier via
a complex `chance / 4` derivation involving the imul magic constant.
Port uses `chance / 4` directly which is close in magnitude.

### Per-port variability / schema deltas

No new schema. All gsns (gsn_biofeedback, gsn_flesh_armor,
gsn_adrenaline_rush, gsn_cell_adjust, gsn_devils_curse,
gsn_biomanipulation) already in source. APPLY_*, AFF_HASTE,
AFF_SLOW, check_dispel, affect_find, affect_strip all already
available.

### Test plan

#### `do_biomanipulation` — menu form
1. As psi class with `set skill self biomanipulation 100`,
   `biomanipulation` (no arg) → menu showing "Flesh" + tier-gated
   modes per character level.
2. `biomanipulation bogus` → same menu.
3. Without the skill → "Leave the spoon bending to Uri Gellar!"

#### Each mode (flesh/adrenaline/cellular/feedback/deaden)
1. `bio flesh` (always available) → "Your skin turns to armor." +
   `affects` panel shows flesh_armor with -level AC, level/2 ticks.
2. Already affected → "Your flesh is already like armor."
3. Insufficient mana → "You haven't the stamina for ..."
4. With `set skill self biomanipulation 1` (low skill) → most casts
   should hit the per-mode "fail" message ("muscles thicken briefly"
   for flesh, etc.).
5. Repeat for adrenaline / cellular / feedback / deaden, gating on
   level requirement (31/51/71/91).

#### Adrenaline dispel branch
1. Get slowed (e.g. cast slow on yourself or have an enemy do it).
2. `bio adrenaline` → roll for the dispel; on success strip slow
   + "stop moving in slow motion." On fail: "Spell failed."
3. If NOT slowed → standard AFF_HASTE + APPLY_DEX application.

#### Deaden heal
1. Take damage to half-HP.
2. `bio deaden` → "The pain lessens." + HP up by 200 (or 100 if
   you have devil's curse on you).
3. Already at max HP → cap, no overflow.

### Suggested next step

Priority 7 Psionics — three remaining:
- `do_electrokinesis` (3511b at 0x08055ed8)
- `do_telekinesis` (3536b at 0x08056bac)
- `do_pyrokinesis` (3807b at 0x080577c8)

Each is similar in shape (multi-mode dispatch with sub-args). One per
build keeps each diff readable. Order TBD — probably electrokinesis
next as smallest.

### Open questions / blockers

- **DEGRADED feedback bitvector** — Cowork: any insight on what 2003
  where=6 routes to? Same family as voodoo where=6. If we identify
  the field, can fix this batch + voodoo together.
- **DEGRADED cellular modifier** — verify magnitude feels right via
  QA. If too weak/strong, tune the `chance / 4` divisor.
- All carry-over questions still open from 0.4.27..0.4.34.

---

## Build 3fd4f29203d7a2065e9943f343e64fca  —  2026-04-29 02:43  —  SUPERSEDED by 0.4.35

### Status
**0.4.34** — `do_jinx_palm` ports the last unported Voodoo verb. Priority
6 Voodoo class is now feature-complete. Built clean, deployed, md5
verified. **Awaiting Kyle copyover.**

### What's in 0.4.34

**`do_jinx_palm`** (1096b at 0x0804d7fc) — barehand DAM_NEGATIVE strike
+ AFF_CURSE on save-fail. Sister to do_buddha_palm (same shape, curse
instead of fire).

- Skill check, must be barehand (WEAR_WIELD empty), target gates,
  self-target ("can't do much damage at close range"), is_safe,
  stunned, check_killtimer.
- Chance: `skill/2 + hand_to_hand/4 + GET_HITROLL(ch)/2 + STR/4 +
  STAT_DEX(ch) - STAT_DEX(victim)/2 + (level diff) + 10 if HASTE(ch)
  - 5 if HASTE(victim)`.
- HIT: 3-line "jinx palm" broadcast + `damage(number_range(level/2,
  level), gsn_jinx_palm, DAM_NEGATIVE, TRUE)` + `check_improve(TRUE,
  2)` + wait clamp via skill_table beats (IMM bypass).
- Curse application: only if `!IS_AFFECTED(victim, AFF_CURSE)` AND
  `!is_affected(victim, gsn_curse)` AND `!saves_spell(level, victim,
  DAM_OTHER)`. Two AFFECT_DATA applied with `type = skill_lookup("curse")`,
  `duration = level/4`, `bitvector = AFF_CURSE`:
    1. APPLY_HITROLL `-level/8`
    2. APPLY_AC `+level/8` (worse defense in DS's AC scheme)
- "You feel unclean." to victim + "$N looks very uncomfortable." to ch.

### Per-port variability / schema deltas

No new schema. GET_HITROLL macro, AFF_CURSE bit, gsn_jinx_palm,
gsn_hand_to_hand, gsn_curse all already in source.

### Test plan

#### `do_jinx_palm`
1. As a voodoo-class char, `set skill self jinx palm 100`,
   `set skill self hand to hand 100`. Remove all eq.
2. Engage a mob/dummy. `jinx palm <target>` → 3-line "concentrates chi
   and hits" broadcast + DAM_NEGATIVE damage in level/2..level range.
3. After damage, ~percentage of HITs (depending on victim's saves)
   should also broadcast "You feel unclean." to victim and "$N looks
   very uncomfortable." to caster. Victim's `affects` panel should
   show "curse" with -level/8 hitroll + +level/8 AC for level/4 ticks.
4. Already-cursed victim → no curse re-applied (standard damage only).
5. Try with weapon wielded → "You can't do that while wielding a
   weapon."
6. `jinx palm self` → "You try, but you can't do much damage at close
   range."
7. No target / not fighting → "But you aren't fighting anyone!"

### Suggested next step

Priority 6 Voodoo is **complete**. Next:
- **Priority 7 Psionics** — biomanipulation/electrokinesis/telekinesis/
  pyrokinesis (largest functions, 2400-3800b each). Will do one per
  build given the size. Start with biomanipulation (smallest).
- **multi_kick faithful re-port** — small but DEGRADED today (random
  helper dispatch). Cowork judgment after monk-barehand QA.
- **Tuning passes** for any 0.4.27..0.4.33 design questions Cowork
  answers.

### Open questions / blockers

- All carry-over questions still open from 0.4.27..0.4.33.
- See "⚡ Questions for Cowork" at top of this file for the
  consolidated list.

---

## Build 84c41a20f0006cee373324041e0d0e18  —  2026-04-29 02:27  —  SUPERSEDED by 0.4.34

### Status
**0.4.33** — Priority 6 Voodoo class foundation. `do_voodoo` dispatcher
+ `voodoo_pin` / `voodoo_trip` / `voodoo_throw` helpers. `do_jinx_palm`
deferred to 0.4.34 (independent). Built clean, deployed, md5 verified.
**Awaiting Kyle copyover.**

### What's in 0.4.33

**`do_voodoo`** dispatcher (274b at 0x0804f854):
- WEAR_HOLD slot must contain item vnum 55 (the voodoo doll). Verified
  vnum 55 exists in `misc.are` — unlike do_forge's dead vnums, this
  works.
- one_argument → match `pin`/`trip`/`throw` → call corresponding helper
  with `doll->name` as the target string.
- Empty arg or unknown arg → syntax + action list.

**`voodoo_pin`** (519b at 0x0804f954) — pin-stick, doubles victim over.
**`voodoo_trip`** (533b at 0x0804fb30) — face-plant trip-slam.
**`voodoo_throw`** (814b at 0x0804fd1c) — wind-throws victim through up
to 5 random exits to a new room (if any work). On failure (already
fighting, bad roll, all exits blocked), wind+wall messages still fire.

**Shared structure across all three helpers**:
- Iterate `descriptor_list`, filter `connected == CON_PLAYING`,
  `can_see` checks, `is_name(arg, FILENAME(victim))` to find target.
- Identical gates: trust+level "not a good idea", `pcdata->killtime > 0`
  "just been killed", `level <= 20` newbie protection,
  `is_affected(victim, gsn_protection_voodoo)` "still realing".
- On success: per-helper broadcast pair + apply 1-tick
  `gsn_protection_voodoo` affect.

**Targeting model**: Player renames their doll to include a victim's
filename (via whatever restring mechanism DS supports). The
`is_name(arg, FILENAME(victim))` test matches any word in the doll
name against the victim's player file name. Cross-realm — works on
any online PC, doesn't require same room.

### Per-port variability / schema deltas

No new schema. WEAR_HOLD, CON_PLAYING, gsn_protection_voodoo,
descriptor_list, FILENAME, is_name, skill_lookup all already in source.

### DEGRADED behaviors

**1. 2003 affect routing `where = 6`**. Original disasm sets the
affect with `where = 6` (no constant in current `merc.h` — gap between
`TO_WEAPON=5` and `TO_AFFECTS2=7`). Likely TO_STATUS or similar
DS-custom routing that sets a specific bit at byte 0x168. Port uses
`TO_AFFECTS=0` instead — `is_affected(victim, gsn_protection_voodoo)`
finds the affect equivalently for the lockout gate, but the byte
0x168 bit 1 the original used isn't set.

**2. 2003 byte 0x128 bit 0 victim "off-limits" gate** — same family
as do_stance's first gate. Unmappable. Omitted.

**3. voodoo_throw room flag check** uses `ROOM_NO_TELEPORT` for the
"can't throw victim here" gate. The original 2003 disasm reads byte
0x5c bit 4 of the destination room — likely a different but related
flag. Cowork: if `voodoo throw` skips obviously-OK rooms or accepts
obviously-bad ones, retune the room-flag check.

### Test plan

#### `do_voodoo` dispatcher
1. Without holding a voodoo doll → "You are not holding a voodoo doll."
2. Hold a voodoo doll (vnum 55 — find one in misc.are or have an imm
   `oload obj 55`).
3. `voodoo` (no arg) → syntax + action list.
4. `voodoo bogus` → recursion to syntax/action display.
5. `voodoo pin/trip/throw` → forwards to helper using doll's name.

#### `voodoo_pin` / `voodoo_trip`
1. Rename your doll (via whatever restring method DS uses) to include
   another online PC's name. E.g. doll name = "doll voodoo Alice".
2. `voodoo pin` → broadcasts pin-stick to your room, "double over"
   message to Alice anywhere on the server, "$n suddenly doubles over"
   to Alice's room.
3. Re-cast immediately → "They are still realing from a previous voodoo."
4. `voodoo trip` after the lockout drops → similar but "feet slide" /
   "trips and faceplants" flavor.
5. Verify newbie protection: try against a level-20-or-under PC →
   "They are a little too young for that."
6. Verify killtime gate: kill someone (or set their killtime > 0
   manually as imm), try `voodoo pin` → "But they have just been
   killed!"

#### `voodoo_throw`
1. Same target setup as pin/trip.
2. `voodoo throw` → broadcasts toss-doll to your room, then **either**:
   - Target gets thrown to a random adjacent room (5 attempts), with
     directional wind broadcast at the OLD room and slam-into-wall at
     the NEW room + auto `look` for them.
   - OR target stays put but sees wind + wall messages anyway (already
     fighting, low roll <=24, or all exits blocked).
3. Verify the lockout still applies after throw (re-throw should hit
   the "still realing" message).

### `do_jinx_palm` — deferred to 0.4.34

`do_jinx_palm` (1096b at 0x0804d7fc) is the largest voodoo verb and
independent of the dispatcher. Disasm decoded but writing a faithful
port deferred to keep this build's scope tight. It uses get_curr_stat,
saves_spell, is_affected, affect_to_char — looks like a curse-attack
similar in shape to do_buddha_palm. Re-queue for 0.4.34.

### Suggested next step

- **`do_jinx_palm`** (0.4.34 next bundle).
- Cowork answers on assassinate/shield_smash design questions.
- **Priority 7 Psionics** — biomanipulation/electrokinesis/telekinesis/
  pyrokinesis (largest functions, 2400-3800b each — one per build).

### Open questions / blockers

- **DEGRADED #1 affect routing where=6** — Cowork: any insight on what
  this routes to in 2003? Worst case the affect doesn't set the byte
  0x168 bit, but the gameplay-visible behavior (lockout) still works.
- **DEGRADED #3 voodoo_throw room flag** — confirm ROOM_NO_TELEPORT is
  the right "can't be thrown here" room flag, or specify alternative.
- All carry-over questions still open. See "⚡ Questions for Cowork"
  at top.

---

## Build a3a708dd0990b9bce5141db35a319b34  —  2026-04-29 01:40  —  SUPERSEDED by 0.4.33

### Status
**0.4.32** — ports `do_buddha_palm` (842b) + `do_chi` (1042b). Skips
`do_katana` (also blocked on `do_forge`'s material vnum question — same
crafting pattern, same dead vnums). Built clean, deployed, md5 verified.
**Awaiting Kyle copyover.**

### What's in 0.4.32

**`do_buddha_palm`** (842b at 0x0804dc14) — barehand DAM_FIRE strike.
- Skill check, **WEAR_WIELD must be empty**, target gates, self-burn,
  is_safe, stunned, check_killtimer.
- Chance: skill/2 + hand_to_hand/4 + STAT_INT(ch)-10 + STAT_DEX(ch)
  - STAT_DEX(victim)/2 + (level diff) + 10 if HASTE(ch) - 5 if HASTE(victim).
- HIT: 3-line "flaming palm" broadcast + `damage(number_range(level/2,
  level), gsn_buddha_palm, DAM_FIRE, TRUE)`. Then 50% chance → 
  `fire_effect(victim, level/2, number_range(1, level/4 + 1), 0)`.
- MISS: damage(0, DAM_FIRE, FALSE) + 3-line miss broadcast.
- Wait clamp via skill_table beats; trust > 102 IMM bypass.

**DEGRADED**: 2003 bytes 0x163 bit 0x04 (chance -10) and 0x162 bit 0x40
(chance +10) on ch — neither maps to a named field in current schema.
Omitted; standard chance modifiers only.

**`do_chi`** (1042b at 0x0804d42c) — stacking meditation.
- Per-cast: skill check, must be fighting, mana > 24, deduct 25 mana.
- Skill-roll failure: visible flicker, no chi gain, return.
- Skill-roll success: find existing chi affect (modifier = current chi
  level). Determine which broadcast applies based on chi + ch->level
  thresholds (0/4/8/12/16/20/24, gating at 0, 19, 39, 59, 79, 99, 100).
- If `chi > 7`: discharge elemental damage at `ch->fighting`:
  - chi == 8 → DAM_COLD via `cold_effect`
  - chi == 12 || 16 → DAM_FIRE via `fire_effect`
  - chi == 20 || 24 → DAM_LIGHTNING via `shock_effect`, dam *= 2
  - dam = `number_range(level/2, level) + chi * 10`
- Strip old chi affect, apply two new ones (APPLY_HITROLL +chi+4 and
  APPLY_DAMROLL +chi+4) for `ch->level` ticks.
- check_improve(TRUE, 2).

### Per-port variability / schema deltas

No new schema. cold_effect/fire_effect/shock_effect, gsn_chi,
gsn_buddha_palm, gsn_hand_to_hand all already in source.

### `do_katana` — BLOCKED (same as do_forge)

`do_katana` (748b at 0x08054790) shares the do_forge crafting pattern
and the same dead material vnums (1313, 3724). It's effectively a
single-output specialization of do_forge (always katana, no
katana-vs-wakizashi choice). Same material-vnum question for Cowork.
Re-queue with do_forge once vnums are picked.

### Test plan

#### `do_buddha_palm` (monk class, barehand)
1. As monk-class char, `set skill self buddha palm 100`,
   `set skill self hand to hand 100`. Remove all eq.
2. Engage a mob/dummy. `buddha palm <target>` → 3-line "flaming palm"
   broadcast + DAM_FIRE damage in level/2..level range.
3. ~50% of HITs should also apply a lingering fire effect (extra
   ticks of fire damage on victim).
4. Try with a wielded weapon → "You can't do that while wielding a
   weapon."
5. `buddha palm self` → "You burn yourself."
6. With no fighting + no arg → "But you aren't fighting anyone!"

#### `do_chi` (monk class, in combat)
1. `set skill self chi 100`. Get into a fight.
2. First `chi` cast → "Your body flickers with energy" (chi=0 → 4).
3. Second cast → if level > 19, "Your body pulses with energy" (chi=4
   → 8), AND DAM_COLD discharge on victim with cold_effect.
4. Third cast (level > 39) → DAM_FIRE discharge.
5. Continue casting until you hit your level cap. Higher chi = more
   damage per discharge, plus stacking HITROLL/DAMROLL on you.
6. Cast at max chi for your level → "Your have already fully focused
   your ch'i."
7. Skill-roll fail (stay sub-100 skill or low chance) → "Your body
   flickers for a second" with no chi change.
8. Out of combat → "You must be fighting to focus your ch'i."
9. Mana < 25 → "Your spirit is too weak."

### Suggested next step

Priority 5 Monk class is **complete** apart from `do_katana` (blocked
with do_forge) and the `multi_kick` faithful re-port (currently
random-helper dispatch).

Next big batches:
- **Priority 6 Voodoo class** — do_voodoo dispatcher, voodoo_pin /
  voodoo_trip / voodoo_throw helpers, do_jinx_palm. Similar
  helper-heavy pattern to Monk. ~3000b total.
- **Priority 7 Psionics** — biomanipulation/electrokinesis/telekinesis/
  pyrokinesis (the four largest functions, 2400-3800b each). Each is
  a substantial port; doing one per build cycle is sensible.
- **multi_kick faithful re-port** — small but DEGRADED today. Cowork
  judgment after monk-barehand QA.

### Open questions / blockers

- **do_forge + do_katana** — Cowork material vnum decisions.
- **multi_kick simplification** — Cowork judgment after QA.
- **Class-tree mapping questions** — still open from 0.4.27..0.4.29.
- All other carry-overs unchanged.

---

## Build 173b2ee7a693f4e6d5207b76f7864531  —  2026-04-29 01:18  —  SUPERSEDED by 0.4.32

### Status
**0.4.31** — Priority 5 Monk class foundation. 8 monk_* helpers ported
from disasm + simplified multi_kick that calls them. Built clean,
deployed, md5 verified. **Awaiting Kyle copyover.**

### What's in 0.4.31

**Eight monk_* helpers ported** (act_combat.c lines ~700-870 region):
- `monk_shinkick`, `monk_palmstrike`, `monk_knee`, `monk_elbow`,
  `monk_thrustkick`, `monk_backfist` (all 113b, identical shape):
  - 1-in-10 chance to fire 3-line flavor broadcast (TO_CHAR + TO_VICT
    + TO_NOTVICT)
  - Always: `one_hit(ch, victim, gsn_<helper>, 0)` for real damage
- `monk_reverse` (192b): 1-in-10 chance for spin+wrap 4-line setup,
  ALWAYS the choking-grip 3-line + `damage(0, TYPE_UNDEFINED, DAM_NONE,
  FALSE)` (fight-state poke, no damage)
- `monk_spinkick` (203b): 1-in-10 chance for berserk AOE — iterates
  ch->in_room->people, anyone fighting ch or the primary victim eats
  `one_hit(gsn_tornadokick, 0)`. Always 3-line + `one_hit(gsn_spinkick,
  0)` on primary victim.

**Signature change**: stubs were `(CHAR_DATA *ch, char *argument)`
(do_fun shape — wrong); real signature is `(CHAR_DATA *ch, CHAR_DATA
*victim)` to match fight.c's prototypes (lines 128-136). Stubs took
the wrong args silently because all they did was send_to_char(...,ch).

**multi_kick SIMPLIFIED port** (act_combat.c, was stub):
- Picks `number_range(1, 8)` and dispatches to the corresponding
  monk_* helper.
- `dt` argument preserved in signature for future use.
- Original 2003 multi_kick (383b at 0x0805398c) had pclass-aware base
  damage scaling (40 vs 80) and an AFF_HASTE-chained second damage
  call. **DEGRADED — replaced with random-helper dispatch.** Cowork
  judgment call after live QA.

### Per-port variability / schema deltas

No new schema. All 8 monk gsns + gsn_tornadokick already in source.

### Test plan

#### Monk barehand punches (fight.c:2152-2173)
1. As a class with IS_MONK true (monk/shaolin/sensei), unarmed
   (`remove all`).
2. Engage a mob/dummy. Each round of barehand punches now randomly
   triggers one of the 7 helpers (monk_reverse not in fight.c
   dispatch — only via multi_kick).
3. Roughly 10% of triggered helpers fire the 3-line flavor broadcast.
4. Confirm damage scales with each helper's gsn (different skills
   may have different damage tables in skill_table).

#### `do_kick` and `do_roundhouse` for races 8/26/44 (formerly stub)
1. Find a character with race == 8 (astral) / 26 (garou) / 44 (?).
2. `kick <target>` or `roundhouse` — should now fire multi_kick which
   randomly picks a helper. No more "combat module rebuilding" message.
3. **Resolves BUG-017** if reproducible by anyone.

#### `monk_spinkick` AOE
1. As a monk, get attacked by 2+ mobs at once (gangbang scenario).
2. Repeat barehand punches until monk_spinkick fires its 1-in-10 path.
3. All attackers should eat a tornadokick hit; primary victim takes
   the standard spinkick on top.

#### `monk_reverse` choking grip
1. Trigger via multi_kick (case 8 in our random dispatch).
2. Always sees the 3-line "{hYour choking grip leaves $N gasping..."
   broadcast.
3. No actual damage from the choking — fight-state poke only.

### Suggested next step

Priority 5 Monk class continues:
- `do_chi` (1042b at TBD) — class skill
- `do_buddha_palm` (842b)
- `do_katana` (748b)
- `do_deepbreathing` (already live in 0.4.12 STRIP-SELF cluster)

After Monk:
- **Priority 6 Voodoo class** — do_voodoo dispatcher + voodoo_pin/trip/throw
  helpers + do_jinx_palm. Similar helper-heavy pattern to Monk.
- **multi_kick faithful re-port** — the 2003 disasm has class-scaling
  + haste chaining we currently approximate. Worth doing once QA
  confirms whether the simplified version feels right.
- **Priority 7 Psionics** — biomanipulation/electrokinesis/telekinesis/
  pyrokinesis (the four largest functions, 2400-3800b each).

### Open questions / blockers

- **multi_kick simplification** — Cowork judgment after QA: keep the
  random-helper dispatch, or invest in the faithful 2003 re-port?
- **BUG-017 do_kick repro** — should resolve with this build for
  race 8/26/44 chars (multi_kick no longer stubs). Confirm post-copyover.
- All carry-over questions still open. See "⚡ Questions for Cowork"
  at top.

---

## Build 431de484d75ca890b539f3a3eb2a85d5  —  2026-04-29 00:16  —  SUPERSEDED by 0.4.31

### Status
**0.4.30** — fixes BUG-011..016 (six bugs from Cowork's Leto-changelog
mining). Built clean, deployed, md5 verified. **Awaiting Kyle copyover.**

### What's in 0.4.30

**BUG-011 fix (do_charge sword bonus).** HIT path of `do_charge` now
saves `ch->damroll`, adds `ch->level / 4` if wielding a sword
(`item_type == ITEM_WEAPON && value[0] == WEAPON_SWORD`), runs
`multi_hit`, restores `ch->damroll`. Disasm-faithful per Leto Apr 22
2003: "Charge does bonus damage if you wield swords."

**BUG-012 fix (do_ambush spear bonus).** Same pattern — `ch->level/4`
damroll bonus in HIT path when wielding `WEAPON_SPEAR`. Per Leto Apr
22 2003: "Ambush now does bonus damage wielding spears."

**BUG-013 fix (do_flee 5/6 gate).** New gate `if (number_range(1,6) == 1)`
between the pre-flight checks and the attempt loop. Failed roll prints
"{rPanic grips you, but you can't find an opening.{x" and returns
without trying any door. Wait clamp already applied above so the
2-tick penalty still hits. Per Leto Apr 29 2003.

**BUG-014 audit (do_quaff fumble — closed, no code change).** `act_obj.c:3599-3611`
already implements 1/15 fumble while fighting (drops potion, extracts,
12-tick wait). Predates the bug report. Marked resolved in BUGS.md.

**BUG-015 fix (silver/wood/iron weapon AC routing).** `fight.c:3068-3076`
extended:
- `DAM_BASH || DAM_WOOD` → AC_BASH
- `DAM_PIERCE` → AC_PIERCE
- `DAM_SLASH || DAM_SILVER || DAM_IRON` → AC_SLASH
- else → AC_EXOTIC

Per Leto Jul 18 2003: "Bash, Pierce, Slash, Iron, Wood and Silver
are weapon. Everything else is magic." Cowork: if iron should route
to AC_BASH instead of AC_SLASH (e.g. iron maces vs swords), one-line
tune.

**BUG-016 fix (TRAVEL_COOLDOWN lowered).** `act_move.c:2989` —
`#define TRAVEL_COOLDOWN` from 1440s (24 min) to 90s. Old comment
"24 ticks x 60 seconds" was wrong arithmetic. Cowork tune as needed.

### BUG-017 (do_kick stub) — appears resolved already, repro requested

`do_kick` IS fully implemented at `act_combat.c:4130` (since 0.4.5).
It uses real damage + knee_breaker affect chain. The "combat module
rebuilding" message Kyle saw probably came from one of:
1. **`multi_kick` stub** — for races 8 (astral), 26 (garou), 44 the
   HIT path routes to `multi_kick` which is still stubbed (Priority 5
   Monk batch). Julian is banshee, not in that race set, so this
   shouldn't have affected him.
2. **Stale binary** — Kyle reported the bug 2026-04-28; if the
   running binary at the time predated 0.4.5, do_kick would have been
   the stub.

**Cowork: please confirm with Kyle whether he can still reproduce
`kick` returning the stub message after 0.4.30 copyover.** If yes,
attach his character class/race so we can trace which branch fires.
Otherwise the bug can be closed.

### Per-port variability / schema deltas

No new schema entries. All fixes use existing fields/macros.

### Test plan

#### BUG-011 (charge sword bonus)
1. Wield a non-sword weapon, `set skill self charge 100`,
   `charge <target>` repeatedly — note baseline damage range.
2. Wield a sword (`wield <sword>`), repeat — damage should be
   visibly higher (level/4 extra damroll on every hit in the chain).
3. Verify damroll restored: `score` after the charge should show
   the same damroll as before.

#### BUG-012 (ambush spear bonus)
Same pattern with spears. Verify other weapon types don't get the
bonus.

#### BUG-013 (flee 5/6 gate)
1. Get into combat, `flee` repeatedly (use a punching-bag mob).
2. Roughly 1 in 6 attempts should print "Panic grips you, but you
   can't find an opening." and consume the wait without moving.
3. Other 5 in 6 attempts should proceed as before.

#### BUG-015 (weapon damage routing)
1. Get hit by a silver weapon — should now be reduced by AC_SLASH,
   not AC_EXOTIC.
2. Damage breakdown via in-game diagnostic command if available;
   otherwise QA on whether silver/wood/iron hits feel less magical.

#### BUG-016 (travel cooldown)
1. `travel <discovered-area>` and arrive.
2. Wait 90+ seconds, then `travel <another-area>` — should work,
   no "still too weary" message.
3. Try `travel` again immediately after arrival — should be blocked
   by cooldown for 90s.

### Suggested next step

Priority 4 BLOCKER (`do_forge`) waiting on Cowork material vnums.
Priority 5 (Monk class) is the next big batch — multi_kick + helper
fns + do_chi/do_buddha_palm/do_katana. Unblocking multi_kick would
also activate the existing do_kick / do_roundhouse race-routes for
race 8/26/44 chars.

### Open questions / blockers

- **BUG-017 do_kick** — needs Kyle/Cowork repro confirmation. See
  section above.
- **BUG-015 iron AC routing** — currently AC_SLASH; verify with
  Cowork whether it should be AC_BASH for iron maces/cudgels.
- **All carry-over questions from 0.4.27..0.4.29** still open.
  See "⚡ Questions for Cowork" at top.

---

## Build 446aa3fa6a4bace29121e34956940bb6  —  2026-04-28 23:38  —  SUPERSEDED by 0.4.30

### Status
**0.4.29** — ports `do_stance` (1479b at 0x08058b64). Bundles 0.4.28
(do_shield_smash) which never copyovered. Built clean, deployed, md5
verified. **Awaiting Kyle copyover.**

### What's in 0.4.29

**`do_stance` port** (1479b at 0x08058b64) — replaces stub. Monk-class
stance toggler.

Six stances + clear:
- `phoenix` → STANCE_PHOENIX (5) — flame fists
- `leopard` → STANCE_LEOPARD (4) — frost
- `crane`   → STANCE_CRANE (2)   — wind
- `scorpion`→ STANCE_SCORPION (3)— talon/poison
- `dragon`  → STANCE_DRAGON (1)  — thunder
- `monkey`  → STANCE_MONKEY (6)  — jungle strength
- `none`    → STANCE_NONE (0)    — clear

Each stance: 2-line broadcast (TO_ROOM + TO_CHAR) + sets
`ch->pcdata->stance`. fight.c's switch on `pcdata->stance` (lines
2573–2581) applies combat-side mechanics per stance — port is a pure
toggler, no combat logic added here.

No-arg form: shows current stance via `stance_table[stance].name`.

Class gate: `pclass ∈ {8, 23, 38}`. In current class_table this maps
to monk/shaman/blade — current names may differ from 2003 layout.
Same indices as the do_chaos_blow Monk-family multi_kick branch.

### `do_forge` — BLOCKED, deferred

`do_forge` (1200b at 0x08053e50) was disasm-decoded and ready to write,
but the algorithm requires hardcoded source-material vnums (`0x521 = 1313`
and `0xe8c = 3724`) which **don't exist in current DS world data**:
- Vnum 1313 in `swamplands.are` is a *room*, not an object.
- Vnum 3724 isn't anywhere in `data/area/*.are`.

The disasm uses `obj->pIndexData->vnum` to compare against these specific
material vnums; if they don't load, the skill always errors with
"That's not the right material."

**Cowork question (BLOCKER for do_forge):**
1. What item vnums should serve as forge source materials in DS:R?
   (Probably want a "raw iron ingot" / "blade-blank" type — DS:R may
    need new objects authored.)
2. What item vnum should be the resulting katana template?
3. Should the wakizashi keep the same template-with-renamed-fields
   approach, or get its own dedicated vnum?
4. Confirmed mana costs: 300 (HIT) and 250 (MISS) — keep, retune?
5. Confirmed +damroll/+hitroll = level/3 on the forged weapon —
   keep, retune?

Until these are decided, `do_forge` stays a stub. Re-queue when ready.

### Per-port variability / schema deltas

No new schema entries. STANCE_* constants and stance_table all live
in current source.

### DEGRADED behaviors (Cowork: design calls)

**1. 2003 byte 0x128 bit 0 silent-return gate.** First gate in
do_stance — silent return if the bit is set on ch. Doesn't map to a
named field in current schema. Omitted.

**2. Class indices 8/23/38 hard-coded.** Same as do_chaos_blow's
Monk-family branch. Cowork: which classes constitute "monk family"
in DS:R?

### Test plan

#### `do_stance`
1. As a monk-family class (pclass 8/23/38), `stance` (no arg) → shows
   "Current stance: Normal" (or whatever current state).
2. `stance phoenix` → "$n stands straight, fists covered in flame."
   (TO_ROOM) and "You glare as the flames dance on your hands."
   (TO_CHAR). pcdata->stance now equals STANCE_PHOENIX (5).
3. Repeat for each of leopard / crane / scorpion / dragon / monkey —
   confirm correct broadcast pair + correct stance value via `score`
   or in-fight behavior (fight.c's stance switch).
4. `stance none` → "$n relaxes from their stance." + "You relax from
   your stance." pcdata->stance back to 0.
5. `stance lava` (or any unknown keyword) → "Thats not a stance..."
6. As a non-monk class → "It's a tough life as a monk - devoted to
   your studies."
7. Stance persistence across logout/copyover — pcdata->stance is
   already saved (save.c:497, load 1816). Verify by setting a stance,
   logging out, logging back in, `stance` (no arg) → same stance.

#### `do_shield_smash` (carry-over from 0.4.28 — first time live with
this copyover)
See 0.4.28 plan in superseded section below.

### Suggested next step

Priority 4 partially complete after 0.4.29:
- ✅ do_roundhouse, do_healing_touch, do_earthbind, do_scream,
     do_shuriken (+ multi_shuriken), do_feed, do_bastion, do_strangle,
     do_chaos_blow, do_ambush, do_pinch, do_blackjack, do_caltrops,
     do_blinding_strike, do_assassinate, do_shield_smash, do_stance
- ⛔ BLOCKED: do_forge (Cowork material-vnum decision needed)
- 🔍 Confirmed absent from 2003 binary (per CODE_HANDOFF earlier
  inventory): do_hurl, do_toss, do_powerinvuln, do_plantroots,
  do_powerstun, do_quickening, do_dislodge, do_powerblind, do_transfix,
  do_thousand_wounds, do_gash, do_eadbutt, do_devils_touch, do_hack,
  do_aura, do_vital_strike

Next concrete priorities:
1. **do_forge** unblocking — Cowork vnum decisions.
2. **BUG-011..015** Leto changelog combat-port deficiencies.
3. **Priority 5 Monk class** — multi_kick + kick helpers, do_chi,
   do_buddha_palm, do_katana, deepbreathing.
4. **Priority 6 Voodoo class** — do_voodoo dispatcher, voodoo_*
   helpers, do_jinx_palm.
5. **Priority 7 Psionics** — biomanipulation, electrokinesis,
   telekinesis, pyrokinesis (the four largest functions).

### Open questions / blockers

- **do_forge BLOCKER** (see dedicated section above).
- **DEGRADED carry-overs** from 0.4.27 (assassinate PK-room/paradox,
  0x16c sign-bit) and 0.4.28 (shield_smash AC divisor, class-tree stun
  indices, 0x16c bit 0x02). All await Cowork tuning calls.
- **Monk-family class indices** (8/23/38) — unify across do_chaos_blow,
  do_stance, future Monk batch. Cowork: canonical list of "monk
  family" classes for DS:R.

---

## Build a6f9511d269b9b465967a0eef60853cf  —  2026-04-28 23:20  —  SUPERSEDED by 0.4.29

### Status
**0.4.28** — ports `do_shield_smash` (1169b at 0x0804cbbc). Built clean,
deployed, md5 verified. **Awaiting Kyle copyover.**

### What's in 0.4.28

**`do_shield_smash` port** (1169b at 0x0804cbbc) — replaces stub.

Shield-bash opener with secondary stun. Requires WEAR_SHIELD.

**HIT path**:
- Clamp `victim->skill_daze`, `spell_daze`, `flee_daze` to ≥ 24 pulses.
- Force `victim->position = POS_RESTING`.
- `damage(ch, victim, number_range(level/2, level) + 2 * shield->value[2],
          gsn_shield_smash, DAM_BASH, TRUE)`.
- check_improve(TRUE, 1).
- Stun roll: chance = get_skill(ch, gsn_stun) / 4 (or /2 if pclass ∈
  {3, 18, 33}). Gangbang zeroes; defender-ganged doubles. If pass, set
  `victim->stunned = dice(1, gsn_stun-skill > rand ? 3 : 2)`. Three-line
  broadcast "{i...stunned...{x" / "{h$N is stunned...{x" / "{k$N having
  trouble...{x". check_improve(gsn_stun, TRUE, 1).

**MISS path**: `damage(0, gsn_shield_smash, DAM_NONE, TRUE)` (default
banner) + `check_improve(FALSE, 1)`.

**Gates** (in disasm order): skill, WEAR_SHIELD weapon, empty arg →
falls back to `ch->fighting` (else "Who do you want to smash with $p?"
using shield obj as $p), `get_char_room`, self-target, `is_safe`,
`stunned > 0`, `gsn_rift`, `can_see`, `check_killtimer`.

**Wait clamp**: skill_table.beats with IMM (>102) bypass — straight
beats, no 2x/3x.

### Per-port variability / schema deltas

No new schema. AC_BASH, GET_AC macro, `is_being_ganged`, gsn_stun,
gsn_rift, gsn_shield_smash all already in source.

### DEGRADED behaviors (Cowork: design calls + tuning)

**1. 2003 byte 0x2f0 asymmetric scaling on chance.** Same unrecoverable
family as do_jab/do_throw/do_assassinate. Omitted (no field maps).

**2. AC contribution to chance — approximation.** 2003 disasm uses an
imul-magic divide of victim->ac that nets approximately `/80` (with a
dexterity-table side contribution when victim is awake). Port uses
`GET_AC(victim, AC_BASH) / 20` which keeps the same direction with a
slightly stronger contribution. **Cowork tuning question:** if testers
report smash landing too often against high-AC targets, lower to /40
or /60. If too rarely, current value is good. Live QA call.

**3. Class-tree stun-bonus indices (3, 18, 33).** 2003 disasm hard-codes
these pclass values for the doubled stun-chance branch. In current
class_table they map to warrior, wizard, thaumaturge — but the 2003
class_table layout may differ from current. Wizard isn't a melee class
in DS lineage; we'd expect warrior/gladiator/knight (3, 21, 39) or
warrior/blade/knight (3, 38, 39). **Cowork question:** which classes
should get the stun-bonus path on shield_smash? Provide the canonical
list by name and we'll map to current indices.

**4. 2003 0x2f8 sign-bit alt-trigger for HASTE.** Same family as prior
ports. Only the AFF_HASTE half preserved.

**5. 2003 byte 0x16c bit 0x02 on victim zeroes stun chance.** Likely
BUG-008-adjacent (wary flag family). Omitted.

### Test plan

#### `do_shield_smash`
1. As a warrior-tree class with the skill (tier 1 warriors, knights,
   etc.), `wear <shield>`, `set skill self shield smash 100`,
   `set skill self stun 100`.
2. `smash <target>` outside combat → expect bash damage + victim
   knocked to "resting" + ~50% chance of stun broadcast (warrior-tree)
   or ~25% chance (other classes).
3. `smash` (no arg) while not fighting → "Who do you want to smash
   with $p?" with $p resolving to your shield's name.
4. Without a shield equipped → "You'll need a shield to smash with."
5. `smash self` → "You try to smash your brains out, but fail."
6. `smash` while `ch->fighting` is set → uses fighting target.
7. With `gsn_rift` on caster → "A magical rift prevents you..."
8. While stunned → "You're still a little woozy."
9. Against an invisible target → "Are they to your left or to your
   right? bleh - better rub."
10. **Daze clamp verification:** smash a target with `skill_daze=0`,
    then check their score / observe — they should be unable to act
    skill/spell/flee for 24 pulses.
11. **Stun verification:** after smashing a non-warrior-tree class, the
    stun should fire ~25% of the time on average. Confirm `victim->stunned`
    increments on stun broadcast lines.
12. **Gangbang scenario** (multi-PC attacker on victim) → stun should
    never fire (chance forced to 0).

### Suggested next step

Priority 4 continues:
- `do_forge` (1200b at 0x08053e50)
- `do_stance` (1479b at 0x08058b64)

Then BUG-011..015 (Leto changelog mining work) and any remaining
DEGRADED tunings from the assassinate/shield_smash ports once Cowork
returns design calls.

### Open questions / blockers

- **DEGRADED #2 (AC divisor)** — Cowork tuning call after QA.
- **DEGRADED #3 (class-tree stun indices)** — Cowork mapping needed.
- **0.4.27 carry-overs** — assassinate's two design questions still
  open. See below.

---

## Build cd2a996b22cfc8b4a2f0f7a57ad81686  —  2026-04-28 22:28  —  SUPERSEDED by 0.4.28

### Status
**0.4.27** — ports `do_assassinate` (1148b at 0x080586b8). Built clean,
deployed, md5 verified. **Awaiting Kyle copyover.**

### What's in 0.4.27

**`do_assassinate` port** (1148b at 0x080586b8) — replaces stub.

**Two-stage opener:**
- **Stage 1**: roll vs full chance (skill + sneak +25 - 40 if AFF2 bit-15
  on victim - 0 if gsn_sever on victim - chance=0 if gangbang). On pass:
  apply `AFF2_ASSASSINATE` (bit 12 = 0x1000, weight `dice(1,5)`,
  APPLY_NONE/0 modifier) via `affect_to_char` if not already affected;
  emit "{GYour weakness has been exposed!{x" to victim + "{G$n's
  weakness has been exposed.{x" TO_ROOM (with ch=victim so $n=victim).
- **Stage 2** (only after Stage 1 success): chance = level/5 + skill/5;
  +25 sneak; chance=0 if `victim->hit < max_hit/3` OR `gsn_rift on ch`
  OR `gsn_sever on victim`. Roll → if pass OR (chance > 1 AND victim
  asleep) → `multi_hit(ch, victim, gsn_assassinate)`.
- **Stage 1 MISS**: 3-line broadcast (TO_CHAR + TO_NOTVICT + TO_VICT
  with distinct flavor strings).
- **Tail (always)**: `damage(ch, victim, 0, gsn_assassinate, DAM_NONE,
  FALSE)` keeps fight-state + pktimer bookkeeping consistent on both
  HIT and MISS paths.

**Gates** (in disasm order): skill check, empty arg → "Assassinate whom?",
`ch->fighting != NULL` → "They are moving to much..." (assassinate is an
opener — refused while already in combat), `get_char_room`, `can_see`,
self → "*shiver*", `HAS_PKTIMER` → "Your heart's pounding to fast!!",
`is_safe`, `WEAR_WIELD` weapon required, `check_killtimer`.

### Per-port variability / schema deltas

No new schema entries. `AFF2_ASSASSINATE` (bit 12 = 0x1000),
`gsn_assassinate`, `gsn_sever`, `gsn_rift`, `paradox_is_on`, `HAS_PKTIMER`
all already in source.

### DEGRADED behaviors (Cowork: design calls)

**1. PK-room + paradox carve-out on the pktimer brake (DEGRADED).**
The 2003 disasm checks `ch->in_room->room_flags` bit (byte 0x5d bit 2)
AND `!paradox_is_on()` to BYPASS the pktimer brake. In current DS bit
order this would map to bit 10 = `ROOM_SAFE`, which is semantically odd
(safe rooms exempting the brake doesn't fit assassinate's intent). More
likely a removed DS-custom flag (e.g. `ROOM_PK_ALLOWED` or similar) at
that offset that was never re-introduced.

Port currently uses `HAS_PKTIMER(ch)` directly — pktimer always brakes
assassinate. This is more conservative than 2003 (one less escape hatch).

**Cowork question:** is there a desired "X room type" where pktimer-active
players SHOULD be allowed to assassinate? If so, what's the room flag
name and which areas have it? If we don't care about reproducing the
2003 carve-out exactly, leave the simple `HAS_PKTIMER` brake.

**2. 2003 byte 0x16c sign-bit chance-zero (DEGRADED).** Same family as
do_throw alert flag (BUG-008). The disasm zeroes Stage 2 chance if the
sign byte at 0x16c on victim is negative — separate from the 0x16c bit
0x04 wary flag tracked under BUG-008. Different bit (0x80 vs 0x04). The
0x16c byte doesn't map cleanly to any current `merc.h` field. Omitted.

**Cowork question:** likely covered by the wary-flag rebuild already
queued under BUG-008. Confirm and link if so.

### Test plan

#### `do_assassinate`
1. As a class with the skill (check `const.c` skill_table — should be
   ninja-tier), `set skill self assassinate 100`. Wield a weapon.
2. `assassinate <visible-target>` outside combat → expect:
   - On Stage 1 hit: "Your weakness has been exposed!" to victim,
     "$n's weakness has been exposed." to room. Affects panel on victim
     shows "assassinate" with 1-5 tick duration.
   - On Stage 2 hit: standard multi_hit damage chain immediately
     after Stage 1.
3. `assassinate <invis-target>` → "You must be able to see to find a
   weak spot."
4. `assassinate self` → "*shiver*" message.
5. While already fighting → "They are moving to much..."
6. Without wielding → "You must wield a weapon to perform this."
7. With pktimer → "Your heart's pounding to fast!!"
8. Sleeping victim (via sleep spell, not stunned) → Stage 2 auto-fires
   if chance > 1 (sleeping-victim auto-hit pattern).
9. Re-assassinate a victim already carrying the assassinate affect →
   no re-tag broadcast, but Stage 2 still rolls.
10. Gangbang scenario (multiple PCs attacking) → Stage 1 should always
    miss (chance forced to 0).

### Suggested next step

Priority 4 continues:
- `do_shield_smash` (1169b at 0x0804cbbc)
- `do_forge` (1200b at 0x08053e50)
- `do_stance` (1479b at 0x08058b64)

Cowork-queued combat-port deficiencies (BUG-011..015) are also good
candidates — they're small additions to existing functions.

### Open questions / blockers

- **DEGRADED #1 (PK-room carve-out)** — Cowork design call needed (see
  above).
- **DEGRADED #2 (0x16c sign-bit alert)** — likely subsumed by BUG-008
  wary-flag work.
- **0.4.26 + 0.4.25 + 0.4.24 carry-overs unchanged** — see below.

---

## Build 285acb5078011e4bebab09c991ca7708  —  2026-04-28 22:05  —  SUPERSEDED by 0.4.27

### Status
**0.4.26** — bundles 0.4.25's travel-crash fixes + ports `do_blinding_strike`.
0.4.25 was never copyovered (Kyle hadn't yet); rolling forward into 0.4.26 means
a single copyover delivers both. Built clean, deployed, md5 verified.

### What's in 0.4.26

**1. `do_blinding_strike` port** (1022b at 0x080506e8) — replaces stub.
Pressure-point strike that applies AFF_BLIND with -4 hitroll for 1 tick.
- skill check → "What do you know about pressure points?"
- empty arg → use `ch->fighting`; else "But you aren't in combat!"
- arg → `get_char_room`; else "They aren't here."
- Already-blind gate → "$E's already been blinded." (TO_CHAR, sees once)
- self → "Easier to just wear a blindfold."
- standard stunned + is_safe gates
- chance: skill + DEX(ch) - 2*DEX(victim) + 10/-25 HASTE + 5*level-diff +
  divisible-by-5 +1 quirk
- HIT path: 3-line broadcast (TO_ROOM victim's-name banner / TO_VICT
  caster-strike / send_to_char victim "eyes go numb"), light damage
  (2-5 HP, DAM_NONE, show=FALSE), check_improve(TRUE,2), apply
  AFF_BLIND via affect_to_char (TO_AFFECTS, gsn_blinding_strike,
  level=ch->level, duration=0, APPLY_HITROLL -4, AFF_BLIND).
- MISS path: damage(0, DAM_NONE, show=TRUE) + check_improve(FALSE,2).
- Wait clamp: skill_table beats; trust > 102 bypass.

**DEGRADED**: 2003 byte offset 0x2f8 on CHAR_DATA — read alongside the
AFF_HASTE bit to gate the +10/-25 chance modifier ("if (sign-bit) OR
AFF_HASTE → apply"). Unrecoverable to current schema (same family as
do_jab/do_throw 0x2f0). Only the AFF_HASTE half of the disjunction is
preserved.

**2. Carry-over from 0.4.25** (rolled into this binary — see superseded
section below for full detail):
- BUG-010 fix (`travel <area name>` crash + Visited save round-trip)
- BFS diagnostic logging via log_string()
- new_room_index BFS-scratch zero-init

### Per-port variability / schema deltas

No new schema entries this round. AFF_BLIND, gsn_blinding_strike,
APPLY_HITROLL, TO_AFFECTS all already in source.

### Test plan

#### `do_blinding_strike`
1. As a class with the skill (lvl 10 sn from const.c:5514 with TRUE/TRUE
   minimums; check skill_table for class gate), `set skill self
   blinding_strike 100`.
2. `blinding strike <target>` against a non-blind mob/dummy → should
   ~always land (high chance), see 3-line broadcast: room-banner "$n is
   struck blind!", to-victim "$n strikes you with blinding speed!", and
   "Your eyes go numb from the impact!" to victim.
3. Verify victim's `affects` shows blinding strike with -4 hitroll.
4. Re-blind a victim already blinded → "$E's already been blinded."
5. `blinding strike self` → "Easier to just wear a blindfold."
6. `blinding strike` (no arg) while not fighting → "But you aren't in combat!"
7. `blinding strike` while ch->fighting set → uses fighting target.
8. With low skill, `blinding strike <strong-DEX target>` → expect MISS;
   default damage banner fires (show=TRUE).

#### Travel (0.4.25 carry-over verification)
Same as 0.4.25 plan: try `travel the sprite village`, confirm no crash.
Walk into areas, log out, log back in, `travel list` should still show them.

### Suggested next step

Priority 4 continues:
- `do_assassinate` (1148b at 0x080586b8 in ds.tmp)
- `do_shield_smash` (1169b at 0x0804cbbc)
- `do_forge` (1200b at 0x08053e50)
- `do_stance` (1479b at 0x08058b64)

Cowork-queued combat-port deficiencies (BUG-011/12/13/14/15) are also
candidates — they're small additions to existing functions, not new
ports. Bundle when convenient.

### Open questions / blockers

- **Travel diagnostic logging is verbose.** Once BUG-010 is verified
  fixed live for ~24h, downgrade `log_string()` calls in `travel_bfs`
  to a debug conditional or remove.
- **Blinding strike's 0x2f8 byte (DEGRADED)** — same unrecoverable
  family as do_jab/do_throw. If QA shows the chance feels off, revisit
  whether some current `merc.h` field can substitute.
- **0.4.25 + 0.4.24 carry-overs unchanged** — see below.

---

## Build cdc1f773fa36deb1742f99ce657fda7c  —  2026-04-28 21:47  —  SUPERSEDED by 0.4.26

### Status
**0.4.25** — emergency fix bundle for BUG-010 (`travel <area>` crashed
the server live on 0.4.24). Built clean, deployed to runtime tree, md5
verified equal staged↔runtime. **Awaiting Kyle copyover.**

### What's in 0.4.25

**1. `do_travel` argument-form crash fix.** Three defects compounded:
- Area matcher used `arg` (= first word from `one_argument`) instead of the
  full argument string. `travel the sprite village` matched whichever
  `"The X"` area came first in `area_first` — non-deterministic and often
  not the area the player meant. Switched to a full-stripped-argument prefix
  match with first-word fallback.
- `TrvlVst` save load was in `case 'R'` of `fread_char` but the keyword
  starts with `T`. Case dispatch by first letter meant the load was never
  reached — boot log's "Fread_char: no match. Error matching word: TrvlVst"
  was the tell. Moved to `case 'T'`.
- `new_room_index` didn't initialise the new `bfs_tag`/`bfs_pvnum`/`bfs_pdir`
  fields. Garbage values shouldn't crash on their own (BFS terminates on
  `bfs_pvnum != -1`), but defensive zero-init eliminates a class of weird
  silent BFS skips/wrong-path-recons.

**2. BFS diagnostic logging.** `travel_bfs` now emits `log_string()`
breadcrumbs at entry, on entrance discovery, on path-out, on bail conditions,
and on any out-of-range `bfs_pdir` (with an early return). If a crash
recurs after 0.4.25, the boot log will pinpoint the branch.

### Test plan

#### BUG-010 verification
1. Repeat the original repro: walk into "The Sprite Village", walk to another
   area, `travel the sprite village`. Should auto-walk, not crash.
2. Try ambiguous-prefix: `travel the` — should pick whichever "The X" area
   matches first (defined behavior with first-word fallback).
3. Try unambiguous: `travel sprite` (substring) → does NOT match because
   `str_prefix` requires exact prefix. Try `travel the s` → matches "The
   Sprite Village" specifically.
4. **Visited persistence (the other half of the fix):** walk into a few
   areas, log out, log back in. `travel list` should still show those areas.
   Formerly the load bug wiped them every login.

#### If a new crash appears
Look for `travel_bfs:` lines in `/tmp/ds_boot.log` to see exactly where
BFS got. Lines printed:
- `travel_bfs: from <vnum> to area '<name>' (vnums <min>-<max>)` — entry
- `travel_bfs: found entrance vnum=<n>` — found a target-area room
- `travel_bfs: path=<dir-string> nsteps=<n> dest_vnum=<n>` — successful exit
- `travel_bfs: bail src=...` — bad src/target_area
- `travel_bfs: BAD bfs_pdir=...` — corrupt scratch field (defensive return)

### Suggested next step

Once Kyle confirms BUG-010 fixed live, return to:
- **Priority 4 — `do_blinding_strike`** (1022b at 0x080506e8). Disasm read,
  string pool extracted, port not yet written. The pause was at the C-emit
  step. Resume cleanly.
- **BUG-011 / BUG-012** (charge/sword + ambush/spear weapon bonuses) per
  Leto's April 22 2003 changelog — Cowork queued these for combat.
- **Priority 8 mprog `mpwalk`** opcode — complete the travel system.

### Open questions / blockers

- **Diagnostic logging is verbose.** Once BUG-010 verified fixed, those
  `log_string()` calls can be removed or downgraded to a debug-only
  conditional. Leave them for at least 24h to catch recurrence.
- **First-word fallback in area match** — could still pick the wrong
  area when the player's full input doesn't prefix-match anything (e.g.
  typo). Monitor in QA.
- **0.4.24 carry-overs unchanged** — see below.

---

## Build c01aa2a650bab3e51b55b39654ed1bfc  —  2026-04-28 18:05  —  SUPERSEDED by 0.4.25

### Status
**0.4.24** — clears the 0.4.23 bastion silent-miss HOLD + finishes the
in-flight travel system + ports `do_caltrops`. Built clean, deployed to
`~/ds/recovered/devils/bin/ds.new`, md5 verified equal between staged
and runtime tree. **Awaiting Kyle copyover.**

This bundle picked up unfinished work from a session that closed mid-edit
on 2026-04-28: the source tree had ~13 modified files (travel system +
caltrops port + ancillary save/recycle/handler hooks) plus the still-pending
0.4.23 bastion HOLD. Resyncing fixed both. Build broke once on a `static`
qualifier hiding `travel_cancel` from `comm.c`'s game-loop hook; repaired
and rebuilt clean.

**0.4.23 (do_pinch + do_blackjack) — never copyovered to live.** Rolled
forward into 0.4.24. Quirks listed in 0.4.23 carry-over still apply.

### What's in 0.4.24

**1. `do_bastion` silent-miss fix (BUG: 0.4.23 HOLD blocker — RESOLVED).**
Miss branch of `do_bastion` now emits:
```
"You lunge but find only air."          → TO_CHAR
"$n lunges hard but finds only air."    → TO_ROOM
```
Disasm-faithful version omitted the broadcast (alert-flag branch we can't
recover); Kyle confirmed live 2026-04-28 the silent miss felt broken.
Comment in source flags the deliberate divergence.

**2. `do_caltrops` port** (act_combat.c:1183, 84-line replacement of stub).
Disasm-derived from 2003 `do_caltraps` symbol at `0x0804f1ac` (2003 typo;
source uses corrected `caltrops`).
- skill check → "Caltraps? Is that a dance step?"
- requires `ch->fighting != NULL` ("You must be in combat.")
- AFF_FLYING bypass — "Their feet aren't on the ground."
- stunned/safe gates
- always-broadcast 2-line spike-throw (TO_CHAR + TO_VICT) — even on miss
- HIT: `damage(number_range(level/2, level), gsn_caltrops, DAM_PIERCE, TRUE)`
  + 1×beats wait (IMM bypass).
- HIT 20% chance (`number_percent() < chance/5`) to apply `AFF2_LIMPING`
  (-4 DEX, duration 1 tick) via `affect_to_char` if not already limping.
- MISS: `damage(0, gsn_caltrops, DAM_PIERCE, TRUE)` + 2×beats wait.

`gsn_caltrops` already declared in `gsn.h:113` and `const.c skill_table`
at line 5514. `AFF2_LIMPING` defined in `bit.h:352` (introduced earlier
for the knee-breaker side-mechanic).

**3. Travel system (Priority 8 — partial, foundation landed).**
- New PC_DATA fields: `travel_path` (char *), `travel_step` (int),
  `travel_dest` (int vnum), `travel_cooldown` (time_t),
  `visited_areas[256]` (int min_vnums), `num_visited` (int).
- New ROOM_INDEX_DATA scratch fields: `bfs_tag` (gen counter),
  `bfs_pvnum` (parent vnum, -1 = source), `bfs_pdir` (DIR_*).
- `do_travel` (act_move.c:3219) — auto-walk to area name (or vnum for imms).
- `do_slash_recall` (act_move.c:3359) — `/` cmd_table entry split off so
  the comm.c travel auto-walk hook doesn't false-trigger on plain `/`.
- `travel_cancel` + `travel_step_char` + `travel_arrive` helpers
  (act_move.c:3018, 3138, 3030).
- `mark_area_visited(ch, area)` called from `char_to_room`
  (handler.c:2771) — tracks visited areas, gates `travel` destinations.
- Cooldown skipped for guardian-class chars; everyone else has
  `TRAVEL_COOLDOWN` between travels (verify exact duration).
- comm.c game_loop_unix() hook: typing anything mid-travel cancels;
  no input → next `travel_step_char()` per pulse.
- Save/load: `TrvlCool` field in player files (save.c:515-516, 1787).
  `Visited` round-trip not yet verified.
- Recycle init zeroes pcdata travel fields (recycle.c:797-800);
  free_string travel_path on destruction (recycle.c:828-829).

### Per-port variability / schema deltas

**Push to DS_SCHEMA.md:**
- PC_DATA gains 6 fields (see merc.h:1640-1647). Char save format expands.
- ROOM_INDEX_DATA gains 3 BFS scratch fields — runtime-only, not persistent.
- New extern: `void mark_area_visited(CHAR_DATA *ch, AREA_DATA *area)`.
- New extern: `void travel_cancel(CHAR_DATA *ch, const char *reason)`,
  `void travel_step_char(CHAR_DATA *ch)` — declared locally in comm.c
  (lines 241-242); should probably move to merc.h for any other caller.

**Compat:** existing player files load with travel_cooldown=0,
visited_areas all 0, num_visited=0. First time the player walks into
an area, `mark_area_visited` populates the list. No migration needed.

### Test plan

#### Bastion silent-miss fix (former 0.4.23 HOLD)
1. As Julian, `set skill self bastion 1` to bias toward miss.
2. Find a non-friendly target out of combat.
3. `bastion <target>` — should produce TO_CHAR "You lunge but find only
   air." and TO_ROOM "$n lunges hard but finds only air." Damage path
   unchanged.

#### `do_caltrops`
1. Engage a mob/dummy (must be in active combat).
2. `caltrops` — always sees the spike-throw broadcast, then either:
   - HIT: pierce damage in `level/2`–`level`. ~20% chance to also see
     "$n starts limping." + "Ouch that hurt! You start limping." with
     -4 DEX in `affects` panel.
   - MISS: damage(0) banner.
3. Re-caltrops a limping victim — should NOT re-apply the affect.
4. Against a flying target → "Their feet aren't on the ground."
5. While not fighting → "You must be in combat."
6. As IMM, no wait clamp.

#### Travel system
1. `travel` (no arg) → usage hint or list of visited areas.
2. `travel <unvisited-area>` → rejected.
3. Walk into a new area normally → `mark_area_visited` adds it.
4. `travel <visited-area>` → auto-walks one step per tick. Watch the
   per-step movement messages.
5. Type any input mid-travel → "You stop traveling." + stop.
6. Get attacked mid-travel → "Combat disrupts your journey!" + stop.
7. Reach destination → "You arrive at your destination..." (guardian
   variant for guardian class).
8. Try `travel` while still in cooldown (non-guardian) → blocked.
9. **Save round-trip:** travel + save + log out + log back in. Confirm
   visited list persists. **THIS IS THE OPEN QUESTION below.**

#### `/` recall
- `/` should still recall as before. (`do_slash_recall` is a thin wrapper
  added so the travel auto-walk hook doesn't tangle with it.)

### Suggested next step

CLASS ABILITY tier complete. Priority 4 advancing.

**Priority 4 next ports per queue:** `do_blinding_strike` (1022b),
`do_assassinate` (1148b), `do_shield_smash` (1169b), `do_forge` (1200b),
`do_stance` (1479b).

**Priority 8 travel** — C foundation landed. Remaining: mprog `mpwalk`
opcode (Bundle B+ from COWORK_PROMPT.md). Note: COWORK_PROMPT anticipated
an `add_pathfind_cmd.py` patcher; this round changed source directly
without one. If Rex needs to replay the changes on a fresh tree, the
patcher will need retrofitting.

### Open questions / blockers

- **`Visited` save round-trip not verified.** save.c:515-516 saves
  `TrvlCool` but I didn't trace the visited_areas array serialization.
  If it's not in the player save format, `mark_area_visited` is
  in-memory-only and resets each login. Quick test in the test plan
  above. If it fails, the visited array needs save/load wiring before
  travel is gameplay-complete.
- **`TRAVEL_COOLDOWN` value** not visible from the diff context. Worth
  confirming it's reasonable (not e.g. an hour).
- **0.4.23 quirks unchanged** — pinch/blackjack 20-HP non-alert-miss
  damage and the do_pinch/do_blackjack mechanical-duplication discussion
  still open. See "Design quirks worth flagging" carry-over below.

### Status
0.4.20 — bundles **`do_shuriken`** (796b, 0x08050b10) +
**`multi_shuriken`** helper (320b, 0x080509d0) + **`do_feed`** (836b,
0x08052e7c). Three replacements (one is a helper unlock). Built
clean. Deployed to `~/ds/recovered/devils/bin/ds.new`. **Awaiting
Kyle copyover.**

**0.4.19 (do_earthbind + do_scream) confirmed LIVE** at 2026-04-28
~13:35 — running binary md5 matched the staged 0.4.19 pre-image
before 0.4.20 replaced it on disk.

**Priority 3 — CLASS ABILITY tier note: `do_hurl` cannot be ported.**
The symbol is registered in `interp.c` and `const.c` (gsn_hurl, level
75 augurer) but **doesn't exist in the 2003 binary `ds.tmp`**. It was
a post-2003 addition for which we have C declarations only — no disasm
to recover. CLASS ABILITY tier is therefore **complete** with do_charge,
do_dance, do_jab, do_throw all live or pending QA. Same situation
applies to `do_toss` (registered, no 2003 disasm). Future work may
implement these from scratch, but they're not part of the resurrection
recovery path.

### What's staged (0.4.23)

**Two Priority 4 ports — `do_pinch` and `do_blackjack` (mechanically
identical, different flavor).**

#### `do_pinch` (984b at 0x0804e890) — `port_pinch.py`

Pressure-point pinch — sister of strangle but with `check_immune(DAM_BASH)`
handling.

Key differences from strangle:
- `check_immune(victim, DAM_BASH)` result drives chance:
    `IS_NORMAL`     → no change
    `IS_IMMUNE`     → chance = 0, immediate "unaffected" broadcast and return
    `IS_RESISTANT`  → chance /= 2
    `IS_VULNERABLE` → chance += chance/3
- Imm-protection: `victim->level > 103 AND ch_mortal AND vict_imm_trust`
  → "It's not smart to mess with gods."
- Bail if `IS_AFFECTED(victim, AFF_SLEEP)` (already asleep).
- **Non-alert MISS deals 20 HP damage** (unique to pinch/blackjack
  in this batch — most ports' non-alert miss is silent or damage(0)).

All other gates + AFF_SLEEP outcome + force-POS_SLEEPING identical
to do_strangle.

#### `do_blackjack` (984b at 0x0804edd4) — `port_blackjack.py`

Mechanically identical to `do_pinch`. Differences:
- Uses `gsn_blackjack` instead of `gsn_pinch`
- Sack-to-the-head broadcasts instead of pressure-point
- Same DAM_BASH immune handling, same alert-flag MISS bifurcation,
  same -60 pktimer brake, same AFF_SLEEP outcome.

---

### Carry-over: 0.4.22 — `do_chaos_blow` and `do_ambush`

#### `do_chaos_blow` (884b at 0x08050e2c) — `port_chaos_blow.py`

Holy-themed power strike with weakening affect.

Mechanics:
- skill check → "Try again when you've mastered your emotions.{x"
- standard arg/target/self/safe/stunned gates
- chance modifiers: `+str_ch -str_vict +con_ch -con_vict`, `+5/-10` HASTE,
  `+(level diff)`, then **divisible-by-5 quirk**: divide by 5, recompute,
  if exactly divisible → `chance += 1`. Preserved disasm-faithful;
  looks like an off-by-one rounding hack.
- HIT: class-aware wait clamp (Monk-family pclass {8,23,38} use 1×beats,
  others use 2×beats). 3-line broadcast (TO_VICT/TO_NOTVICT/TO_CHAR
  in disasm order). `damage(number_range(level/2, level), gsn_chaos_blow,
  DAM_HOLY, TRUE)` — yes "holy", per 2003 disasm. "{DDamn that hurt!{x"
  to victim. check_improve(TRUE, 2). Apply AFF_WEAKEN (-10 STR, duration
  0) via `affect_to_char`.
- MISS: gangbanger-aware wait clamp (2×beats vs 1×beats), `damage(0,
  gsn_chaos_blow, DAM_NONE, FALSE)`, check_improve(FALSE, 2).

#### `do_ambush` (712b at 0x0805979c) — `port_ambush.py`

Stealth opener with TWO hard prerequisites. Sleeping-victim auto-hit
pattern (similar to backstab).

Mechanics:
- skill check → "You need more preparation to do this."
- empty arg → "Ambush whom?"
- `ch->fighting != NULL` → "{hYou are too visible for that.{x"
- get_char_room → "They aren't here."
- `!can_see(ch, victim)` → "You can't see well enough to do that."
- `is_affected(ch, gsn_rift)` → magical rift bail
- self → "There's stupid, then there is you."
- is_safe → bail
- **Wielded weapon required**: `get_eq_char(ch, WEAR_WIELD) == NULL`
  → "{hYou need to wield a weapon to do this.{x"
- HP gate: `victim->hit >= max_hit/3` (same as charge/bastion)
- check_killtimer
- Wait clamp: 2×beats gangbanger else 1×beats; IMM bypass
- Sneak bonus: `chance += 25` if `!can_see(victim, ch)`
- Alert flag (0x16e bit 0x20) → `chance = 0` (DEGRADED, raw byte read)
- **AFF_CAMOUFLAGE required on caster**: `IS_AFFECTED(ch, AFF_CAMOUFLAGE)`
  must be true → "{hYou need to be camouflaged to ambush someone.{x"
  if missing
- HIT condition: `roll < chance` OR (`chance > 1 AND victim->position
  <= POS_SLEEPING`) — sleeping-victim auto-hit
- HIT: check_improve(TRUE), `multi_hit(ch, victim, gsn_ambush)`
- MISS: alert→3-line broadcast vs silent, check_improve(FALSE),
  `damage(0, gsn_ambush, DAM_NONE, FALSE)`

---

### Carry-over: 0.4.21 — `do_bastion` and `do_strangle`

#### `do_bastion` (824b at 0x080524b0) — `port_bastion.py`

Body-slam opener — sister of do_charge.

Mechanics:
- skill check → "You can't do that."
- `ch->fighting != NULL` → "{hYou're too close to do that!{x"
- empty arg → "Bastion whom?"
- `victim==NULL` → "They aren't here."
- `is_affected(ch, gsn_rift)` → magical rift bail (caster lockout)
- self → "You cannot do that to yourself!"
- `is_safe` → bail
- HP gate: `victim->hit >= max_hit/3` (same as do_charge)
- `check_killtimer(ch)`
- Wait clamp: 2x beats gangbanger, 1x else, IMM bypass
- AFF2 bit-15 halver: `chance -= 40` if `(short)(victim->affected_by2 & 0xFFFF) < 0`
- HIT: `check_improve(TRUE)` + `multi_hit(ch, victim, gsn_bastion)`
  — uses normal melee chain for damage
- MISS: silent (alert-branch broadcast omitted) + `damage(0, gsn_bastion,
  DAM_NONE, FALSE)` + `check_improve(FALSE)`

**DEGRADED**: 2003 0x16e bit 0x10 alert flag (chance-zero + 3-line
shrug-out broadcast on miss). Same family as do_throw / do_feed /
do_charge. Omitted — every miss is silent.

#### `do_strangle` (780b at 0x08054ccc) — `port_strangle.py`

Choke-out attack. **Applies AFF_SLEEP and forces POS_SLEEPING on hit.**

Mechanics:
- skill check → "You lack the skill to strangle."
- `get_char_room(ch, argument)` (treats whole arg as name); if NULL:
  wait clamp + "You do not see that person here."
- `is_affected(victim, gsn_strangle)` → silent return (no re-strangle
  while still affected)
- self → "Even you are not that stupid."
- `victim->position <= POS_SLEEPING` → "$N isn't even awake!"
- `affect_strip(victim, gsn_strangle)` — strip prior strangle (re-roll
  support after duration expires)
- `is_safe` → bail
- `check_killtimer(ch)`
- Stat modifiers:
  - `-get_curr_stat(victim, STAT_CON)`
  - `+get_curr_stat(ch, STAT_DEX) / 2`
  - `+10` if `!can_see(victim, ch)` (sneak bonus); `-10` else
  - `-20` if AFF2 bit-15 halver
  - `-60` if `!IS_NPC(ch) && ch->pcdata->pktimer > 0` (pktimer brake)
  - PvP level diff capped at ±20
- alert flag (0x16c bit 0x10): if set, chance = 0 (+ broadcast on miss)
- Wait clamp via skill_table beats; IMM bypass
- HIT: `do_visible(ch)` (un-hide), 3-line broadcast, check_improve(TRUE),
  apply AFF_SLEEP via `affect_join` (where=TO_AFFECTS, type=gsn_strangle,
  duration=1, bitvector=131072=AFF_SLEEP, others 0), force
  `victim->position = POS_SLEEPING` if currently higher.
- MISS: alert→3-line broadcast, non-alert→silent. damage(0, gsn_strangle,
  DAM_NONE, FALSE), check_improve(FALSE).

**DEGRADED**: alert-flag offset (0x16c bit 0x10) maps to `status` byte 0
bit 4 (= STATUS_CHALLENGER) in current layout — semantically wrong. Read
via raw byte access; behavior in current build will be governed by an
unrelated flag.

---

### Design quirks worth flagging (0.4.18 – 0.4.21)

Per Kyle's request: surface gameplay behaviors that are either
disasm-faithful but might *feel* wrong, or where we made a degradation
choice that has visible player-side impact. Cowork: pull these into
IDEAS.md as balance/tuning candidates if any feel worth re-tuning.

| Port | Quirk | Worth discussing? |
|---|---|---|
| `do_roundhouse` | Monk-family multi_kick combo branch is omitted (Monks get the same generic broadcast + bash damage as everyone else, no kick-combo). Will be wrong-feeling for Monks who remember the combo. | Yes — re-port roundhouse once Monk batch lands so multi_kick fires. |
| `do_earthbind` | Effective hit chance is `skill * 3/4` (75% of raw skill). Designed-strict per disasm — earthbind is *meant* to be hard to land. | Confirm intentional vs. typo. Players may complain it feels weak relative to skill %. |
| `do_scream` | Effective hit cap ~50% regardless of skill (HIT requires `roll < chance AND roll <= 49`). Designed as a side-effect attack, not a primary damage source. | Confirm 49 cap is intentional. |
| `do_shuriken` | HIT path uses literal wait clamp of **12 pulses**, not pulled from `skill_table`. If skill_table beats differ from 12 in the current data, post-hit lockout will feel inconsistent vs other skills. | Confirm 12 is canonical. |
| `do_feed` | Minimum 90% effective hit chance — feed almost always lands. POLY_WOLF gives +33% damage bonus. | Both look intentional (it's a sustain skill, not a hit-or-miss). No action. |
| `do_bastion` | **Silent miss** (no broadcast). Players may try `bastion <target>` and see no message — looks broken. Disasm-faithful (the broadcast lives in the omitted alert-flag branch). | Strong candidate: add a generic miss broadcast back, with a comment that it diverges from disasm. |
| `do_strangle` | Pktimer penalty is `-60` chance — recent PvP attackers are almost guaranteed to fail strangle. Designed brake on chain-aggression. | Confirm intent. -60 is brutal. |
| `do_strangle` | Applies AFF_SLEEP with `duration = 1`. Affect drops next tick, but `victim->position` is forced to POS_SLEEPING separately and stays asleep until they take damage or wake manually. **Asymmetric mechanic** — affect and position state diverge after 1 tick. | Confirm this asymmetry is intentional. Could feel buggy to players. |
| `do_chaos_blow` | Damage type is **DAM_HOLY** (10) not "chaos". Either DS treats holy as the chaos elemental color, or the 2003 disasm is doing something we'd read differently in C. Resist/vuln math will follow holy modifiers. | Confirm DAM_HOLY is correct. If wrong, players resistant to holy will tank chaos blow incorrectly. |
| `do_chaos_blow` | "Divisible-by-5 +1" chance quirk — if `chance % 5 == 0`, chance is bumped by 1. Looks like a deliberate off-by-one rounding hack from the original compiler/code. Preserved verbatim but unclear what gameplay impact this has. | Worth confirming intent (or just leaving as compatibility quirk). |
| `do_ambush` | Requires **TWO** simultaneous prerequisites: AFF_CAMOUFLAGE active AND a wielded weapon. Without `camouflage` precast you can't even attempt it. Sleeping victims auto-hit if chance > 1. | Camouflage requirement is a UX gotcha — players will try ambush bare and get rejected. Worth surfacing in `help ambush`. |
| `do_pinch` / `do_blackjack` | Non-alert MISS branch deals **20 HP damage** even though it didn't knock the target out. Unique to these two — most other ports' non-alert miss is silent. May surprise players ("I missed but they took damage?"). | Confirm the 20-HP non-alert-miss damage is intentional. |
| `do_pinch` / `do_blackjack` | Both ports use the **exact same** mechanics — only flavor messages and gsn differ. May feel duplicative as players unlock both. | Cowork could differentiate one (e.g. blackjack does damage, pinch doesn't) if the duplication feels boring. |
| `do_caltrops` (queued) | Inventory miss: 2003 binary has the function under `do_caltraps` (typo) at 0x0804f1ac. Earlier flagged as "absent". Re-queued for next bundle. | None — just a finding. |
| Multiple ports | Several "alert flag" reads use raw 2003 byte offsets that map to unrelated current fields. Behaviors will *fire*, but on the wrong condition. See METHODOLOGY.md "Unrecoverable 2003 behaviors". | Track for cumulative-impact assessment as more ports land. |

**Process**: Code is now logging design quirks per port. If anything in
the table above warrants design discussion, lift it into IDEAS.md as
its own entry; if it warrants source change, queue under bugs.

---

### Carry-over: 0.4.20 — `do_shuriken` + `multi_shuriken` + `do_feed`

#### `multi_shuriken` (320b at 0x080509d0) — helper, called by do_shuriken

Pre-rolls `dam = number_range(level/2, level)`, then:
1. Hit 1 — always: `damage(dam, gsn_shuriken, DAM_POISON, TRUE)`
2. Bail if `victim->fighting != ch`
3. Hit 2 — if caster has `AFF_HASTE`: same damage
4. Bail
5. Hit 3 — chance = `get_skill(ch, gsn_second_attack) / 2`, halved
   again if `AFF_SLOW`. Roll → damage + check_improve(gsn_second_attack,
   TRUE, 5)
6. Bail
7. Hit 4 — chance = `get_skill(ch, gsn_third_attack) / 2`, halved
   if SLOW. Roll → damage + check_improve(gsn_third_attack, TRUE, 6)

**Signature change**: stub took `(ch, char *argument)`; disasm calls
with `(ch, victim)`. New signature is `(CHAR_DATA *ch, CHAR_DATA *victim)`.

#### `do_shuriken` (796b at 0x08050b10) — `port_shuriken.py`

Thrown poisoned shuriken — primary `DAM_PIERCE` + slow affect chained,
multi-hit follow-ups via `multi_shuriken` deliver `DAM_POISON`.

Mechanics:
- skill check → "Huh?"
- empty arg / arg parse / `victim==ch` / safe / stunned gates
- chance modifiers: `+str_ch -str_vict +con_ch -con_vict`,
  `+5/-10` HASTE (caster/victim), `+(level diff)`
- HIT: literal wait clamp 12, IMM bypass; `multi_shuriken(ch, victim)`;
  check_improve(gsn_shuriken, TRUE, 2). Then if `ch->fighting == victim`:
  2-line broadcast + `damage(2-5, DAM_PIERCE, FALSE)` + slow-msg
  to victim + wait clamp `(beats+3)/4` + `affect_join` slow affect
  `(TO_AFFECTS, gsn_shuriken, level, 2 ticks, APPLY_DEX, -1, 0)` +
  `spell_slow(skill_lookup("slow"), level, ch, victim, 0)`.
- MISS: `damage(0, gsn_shuriken, DAM_POISON, TRUE)` + check_improve(FALSE)
  + wait clamp `beats/2`.

#### `do_feed` (836b at 0x08052e7c) — `port_feed.py`

Vampire blood-feed bite. Always-mostly-lands (90% min effective chance).

Mechanics:
- skill check → "Take the fake teeth out of your mouth..."
- empty arg / arg parse gates
- caster blind → "{hYou cannot feed while blind.{x"
- self → "You can't feed off yourself!"
- is_safe → bail
- **kill-stealing gate** (same as do_scream)
- charm-master gate
- `victim->hit < victim->max_hit / 6` → "$N is hurt and suspicious..."
- stunned-woozy gate
- `chance = MAX(get_skill(ch, gsn_feed), 90)` — minimum 90%
- HIT: 3-line bite broadcast, `dam = number_range(level, level*2)`,
  `+33%` if `ch->polyform == 3` (vampiric form). If `ch->fighting == NULL`:
  `multi_hit()`, else `damage(dam, gsn_feed, DAM_PIERCE, TRUE)`.
- MISS: 3-line normal-branch broadcast, `damage(0, gsn_feed,
  DAM_NEGATIVE, TRUE)`, check_improve(FALSE).
- Wait clamp via skill_table beats; trust > 102 bypass.

**DEGRADED**: 2003 0x16d bit 0x10 "blood resistance" alert flag (gates
chance-zero AND alert-vs-normal miss messaging). Same unrecoverable
2003-offset family as `do_throw` 0x16c and `do_charge` 0x17c. Omitted
— always uses normal miss messages.

---

### Open question — RESOLVED: do_feed's polyform == 3 bonus

**Question raised**: do_feed grants +33% damage when `ch->polyform == 3`.
What does polyform 3 represent?

**Answer (found in source, no design call needed)**: POLY_WOLF.

Full polyform table from `merc.h:904-909`:

| Constant       | Value | Likely use |
|----------------|------:|-----------|
| `POLY_NONE`    | 0     | normal form (default) |
| `POLY_MIST`    | 1     | mist / gas form (vampire travel) |
| `POLY_BAT`     | 2     | bat form (vampire flight) |
| `POLY_WOLF`    | 3     | wolf form — feed's +33% bonus form |
| `POLY_LICH`    | 4     | lich form (undead caster) |
| `POLY_WEREWOLF`| 5     | werewolf (separate macro `IS_WEREWOLF`) |

**Supporting clues from grep over the source tree:**

- `act_move.c:3667-3724` — `do_morph`-family verbs map to specific
  vnums per polyform (BAT, WOLF, MIST, LICH branches).
- `handler.c:464-466` — `polyform == POLY_WOLF` unlocks the
  `gsn_bash` and `gsn_stun` melee paths. Strong "wolf = combat form"
  signal.
- `magic.c:604` — `if(ch->polyform == POLY_WOLF)` gate in some
  spell — wolf-specific magic interaction (worth confirming which
  spell once Cowork is on it).
- `effects.c:281` — `victim->polyform == POLY_LICH` — lich-form
  victims get special handling on some effect.
- `fight.c:1750, 1913` — `ch->polyform > 0` (any morph) treated as
  unarmed combat (no wield slot used).
- `fight.c:2131, 2141` — `ch->polyform == 0 || ch->polyform == POLY_LICH`
  — both normal AND lich forms can wield weapons; bat/wolf/mist/were
  cannot.

**Lore-coherent reading**: vampires shapeshift. Wolf is the predator
form, hence the bite damage bonus. Bat = mobility (flight). Mist =
escape/travel. Lich = caster utility (lore-overlap with vampire
necromancy?).

**Action taken**: source updated from `ch->polyform == 3` to
`ch->polyform == POLY_WOLF` (semantically identical, lints cleaner).
Rebuilt as part of the staged 0.4.20 binary above. No copyover impact
beyond what was already pending.

**Open follow-ups for Cowork to confirm in-game / via DS wiki:**

- Which classes/races can take POLY_WOLF? (likely vampire only, but
  worth confirming for the help text.)
- Does any other ability besides feed get a wolf-form bonus? Worth
  scanning act_combat.c against `POLY_WOLF` after the rest of the
  vampire batch lands.
- Is `POLY_LICH` exclusive to vampires (sub-form), or a separate
  class path? `effects.c:281` hints lich gets unique resistances.

---

### Carry-over: 0.4.19 — `do_earthbind` and `do_scream`

#### `do_earthbind` (800b at 0x08055c68) — `port_earthbind.py`

Anti-flight grapple. Yanks airborne targets to the ground.

Mechanics:
- skill check → "You know no such skill.{x"
- empty arg → use ch->fighting; else "But you aren't fighting anyone!"
- arg → get_char_room; if NULL → "They aren't here."
- self → "The tendrils answer your call, then leave as if laughing."
- `IS_AFFECTED(victim, AFF_FLYING)` gate (UNIQUE TO EARTHBIND) →
  "They aren't airborn." if not flying
- is_safe, charm-master, stunned-woozy gates
- PvP attacker bookkeeping
- check_killtimer(ch)
- chance += ch->level - victim->level
- wait clamp via skill_table beats; trust > 102 bypass
- Roll: HIT requires `number_percent() <= chance * 3 / 4`. Stricter
  than typical — earthbind is harder to land than its raw skill %.
- HIT: strip gsn_fly + gsn_levitation + gsn_grow_wings, REMOVE_BIT
  AFF_FLYING from victim, "ripped from the skies" 2-line broadcast,
  damage(number_range(level, level*2), gsn_earthbind, DAM_BASH, TRUE)
- MISS: "tendrils find nothing but air" to ch + room broadcast,
  check_improve(FALSE)

#### `do_scream` (748b at 0x0805597c) — `port_scream.py`

Mind-splitting sound attack. Bypasses physical armor.

Mechanics:
- skill check → "You let out a scream of anguish."
- standard arg/target/self/charm/stunned/safe gates
- **NEW gate — kill-stealing protection**: if `victim->fighting != NULL`
  AND `!is_same_group(ch, victim->fighting)` AND `!IS_NPC(victim->fighting)`
  → "Kill stealing is not permitted." Same gate likely appears in more
  Priority 4 ports.
- PvP attacker bookkeeping
- chance += (ch->level - victim->level)
- chance += chance / 4 (effective chance * 5/4)
- Roll: HIT requires `roll < chance AND roll <= 49` (effective ~50% cap)
- ALWAYS broadcasts 3-line scream (ch/vict/room) regardless of HIT/MISS
- HIT: check_improve(TRUE), wait clamp 1*beats, damage(number_range(10,20),
  gsn_scream, DAM_SOUND, TRUE), then 5% bonus chance to stun the victim
  for `dice(1, 2)` ticks (sets `victim->stunned`).
- MISS: damage(0, ..., show=TRUE), check_improve(FALSE), wait clamp at
  3*beats/2 (50% longer than HIT)

**DAM_SOUND = 19** confirmed via bit.h:210.

---

### Carry-over: 0.4.18 — Two Priority 4 DS Custom ports

#### `do_roundhouse` (339b at 0x080511a0) — `port_roundhouse.py`

#### `do_roundhouse` (339b at 0x080511a0) — `port_roundhouse.py`

Auto-targeting mid-fight kick (no argument — uses `ch->fighting`).

Mechanics:
- skill check → "You better leave the martial arts to monks."
- `ch->fighting == NULL` → "You aren't fighting anyone."
- `ch->stunned > 0` → "You're still a little woozy."
- wait clamp via `skill_table[gsn_roundhouse].beats`; trust > 102 bypass
- HIT: `act("Your roundhouse catches $N off guard!", TO_CHAR)` then
  `damage(number_range(level/2, level), gsn_roundhouse, DAM_BASH, TRUE)`
- MISS: `damage(0, ..., show=TRUE)` + `check_improve(FALSE)`

**DEGRADED**: 2003 disasm forks to `multi_kick(ch, victim, gsn_roundhouse)`
for `pclass in {8, 23, 38}` (Monk-family). `multi_kick` is currently
still a stub (Priority 5 Monk batch, not yet ported); calling it would
print the rebuilding placeholder and deal NO damage to Monk-family
players, which is strictly worse than the unified branch. So all
classes route through the generic broadcast + bash damage. Re-port
roundhouse once `multi_kick` lands.

#### `do_healing_touch` (598b at 0x0804e328) — `port_healing_touch.py`

`htouch [target]` — first real heal verb out of stub. Self-heal if no
arg, target heal otherwise.

Mechanics:
- skill check → "Huh?"; arg parse → `victim = ch` if no arg, else
  `get_char_room`; if NULL → "They are not here."
- `ch->stunned > 0` → "You're still a little woozy."
- `ch->mana <= 54` → "Your spirit is too weak."
- wait clamp; trust > 102 bypass
- mana cost: `ch->mana -= 50`
- self-heal broadcast: `send_to_char` "You focus your energy..." +
  `act("$n concentrates, and magical sparks leap from $s body.", TO_ROOM)`
- other-heal broadcast: 3-line act() block
- heal amount tier:
    `level <= 39: dice(1,8) + level/3`
    `level <= 69: dice(2,8) + level/2`
    `level >= 70: dice(3,8) + level - 10`
  scaled `* chance / 100`, halved if `is_affected(victim, gsn_devils_curse)`
- `victim->hit += heal` (capped at `victim->max_hit`); `update_pos(victim)`
- `send_to_char("You feel better!", victim)`
- `check_improve(ch, gsn_healing_touch, TRUE, 2)` — multiplier 2 for
  bonus learn rate

**No miss branch** — htouch always heals. Skill % only affects amount,
not whether it lands.

---

### Carry-over: 0.4.17 — Two CLASS ABILITY ports — `do_jab` and `do_throw`

#### `do_jab` (1080b at 0x08055544) — `port_jab.py`

Throat-strike attack. **Zero damage.** Applies `AFF2_JAB`
(gasping-for-breath) to the victim with `duration=0`, blocking
re-jab while the affect is up.

Mechanics:
- skill check → "Wanna jab, do 10 rounds with Foreman."
- empty arg → use `ch->fighting`; else "But you aren't fighting anyone!"
- `HAS_PKTIMER` gate ("Your heart's pounding to fast!!")
- `gsn_rift` caster lockout ("A magical rift…")
- victim already gasping → "They are already gasping for breath!"
- self-target → "With deliberate care you jab yourself…"
- standard `is_safe`, `IS_AFFECTED(ch, AFF_CHARM) + master == victim`,
  `ch->stunned > 0`, `can_see` gates
- inline PvP attacker bookkeeping (`ch->attacker = TRUE`,
  `victim->attacker = FALSE`) when both PCs and not in fight
- wait clamp via `skill_table[gsn_jab].beats`; trust > 101 bypass
- chance modifiers: `+2*str`, `-con`, `-dex*4/3`, ±20/-25 HASTE/SLOW,
  ±level-diff for PK
- HIT path: `printf_to_char(victim, "%s jabs their fist into your throat!")`
  with derived attacker name (visible: short_descr if NPC/polymorphed,
  else `get_char_name`; hidden: "An Immortal" if trust > 102, else
  "someone"); then act() to_char and to_notvict; check_improve(TRUE);
  `damage(0, gsn_jab, DAM_BASH, FALSE)`; `affect_to_char` with the jab
  affect.
- MISS path: `damage(0, ..., show=TRUE)` for default miss banner;
  `check_improve(FALSE)`.

#### `do_throw` (1388b at 0x08054fd8) — `port_throw.py`

Wrestling/judo grab-and-throw. **Real damage**: `number_range(level/2,
level)`, `DAM_BASH`. On HIT victim is set to `POS_RESTING` (DS scheme
— no `POS_STUNNED`; 2003 disasm constant 3 maps to `POS_RESTING` in
DS's `bit.h`) and victim's `wait/flee_daze/skill_daze` are clamped to
`>= 24` pulses. On MISS the **caster** is set to `POS_RESTING` and
caster wait clamps to `2*beats` (or `3*beats` if `is_gangbanger`),
trust > 102 bypass.

Mechanics:
- skill check → "Huh?"
- empty arg / arg parse / can_see / `victim->position > POS_SLEEPING`
  / is_safe / stunned / no-self-throw gates
- chance modifiers: `+2*str`, `-con`, `-dex*4/3`, `-10` (approx of
  omitted tabular modifier), ±20/-15 HASTE/HASTE, ±level-diff capped
  at 20
- dodge cap: `chance -= (gsn_dodge_chance - chance) / 2` if victim's
  dodge exceeds caster's chance
- HIT 3-line broadcast → daze clamps → caster wait → victim
  `POS_RESTING` → damage roll → check_improve(TRUE).
- MISS 3-line broadcast → `damage(0, show=FALSE)` →
  check_improve(FALSE) → caster `POS_RESTING` + wait clamp.

### Schema work this round

**2003 binary CHAR_DATA layout differs from current `merc.h`.** Probed
via `gcc -m32 + offsetof()` in `/tmp/probe_offsets.c`. Currently
`level=0xcc, rank=0xc8` (2003 didn't have `rank`); affected_by is at
0x170 current vs 0x162 in 2003. **All ports use field NAMES in C, so
they resolve to current offsets correctly** — disasm-derived offsets
were only used to reverse-engineer the 2003 semantics, never written
into the C output.

Implication for future work: bit-test patterns like `testb $0x4,
0x162(%edi)` need to be decoded as "byte 2 of `affected_by` bit 2 →
bit 18 of int → AFF_CHARM (= S in DS bit.h)" rather than literal byte
offsets. The offset-to-bit table for HASTE (V=21), SLOW (dd=29), CHARM
(S=18) covered all do_jab/do_throw cases — same approach should work
for the rest of the CLASS ABILITY tier.

### Carry-over open questions

- **`gsn_wary` caster-side source** — still unidentified. Likely
  surfaces when `do_dodge` or similar defensive ability lands.
- **2003 CHAR_DATA offset 0x2f0** — same modifier appears in both
  do_jab AND do_throw chance formulas. Looks like a stat field, but
  doesn't map to any current `merc.h` field. Omitted from both ports.
  Could be a removed DS-custom stat (e.g. an old endurance field).
  Flag if QA shows jab/throw too forgiving.
- **2003 offset 0x16c bit 0x04** ("victim alert" flag in do_throw) —
  same family as do_charge's 0x17c bit 0x40. Both are unrecoverable.
  do_throw's chance-zero-on-alert and alert-vs-normal-miss messaging
  are both omitted (always uses the normal miss messages).

### Ngrok ops issue (recurring — happened again 2026-04-28 morning)

**Repeat occurrence on 2026-04-28**: ngrok process was running (PID 489)
with the right CLI shape (`ngrok tcp --url 7.tcp.ngrok.io:25597 5000`)
but its public tunnel was dead — local `:4040` API unresponsive,
`/dev/tcp/7.tcp.ngrok.io/25597` refused connections, log file
zero-bytes since the prior day. Cleanly fixed by `kill -9 489 && nohup
ngrok tcp ... > ~/ngrok.log 2>&1 &`. ds.new was healthy throughout —
the watchdog kept the binary alive on local 5000.

**This is the same family of ops bug as the original incident below.
Recommendations queued from that incident still stand and are now
upgraded to "should ship soon."**

#### Original incident
MUD went down today not because `ds.new` crashed (watchdog kept it up
on ports 5000/5001) but because **6 stale ngrok processes** were stuck
in `Tl` (traced/stopped) state. Symptoms:

- `ps aux | grep ngrok` showed multiple ngrok PIDs all in `Tl` state.
- They had different CLI shapes (`ngrok tcp 5000 --remote-addr ...`,
  `ngrok tcp --url ... 5000`) suggesting accumulation from manual
  re-runs over time.
- `pkill -f ngrok` (without `-9`) does not work on Tl-state processes.
  Recovery required `pkill -9 -f ngrok`, then a clean restart via the
  start script.
- Public tunnel was offline; players couldn't connect even though the
  MUD itself was healthy.

**Recommended fixes for Cowork to queue:**

1. **`run_mud_watchdog.sh` should also watchdog ngrok**, not just
   `ds.new`. Currently if ngrok dies, the public tunnel goes dark
   silently. Watchdog could probe `curl -s http://127.0.0.1:4040/api/tunnels`
   and restart ngrok if it returns no tunnel or doesn't respond.
2. **`start_mud_public.sh` step 3 ("kills any stale ngrok") should use
   `pkill -9 -f ngrok` not plain `pkill`** — Tl-state processes ignore
   SIGTERM. Plain `pkill` silently fails on them.
3. **Document for Kyle: don't Ctrl-Z foreground ngrok processes.**
   That's almost certainly how they got into Tl state. The start
   script backgrounds correctly via `nohup`, but if Kyle ever runs
   `ngrok tcp ...` directly in a terminal and Ctrl-Z's it, that's
   how they pile up. Use the script.
4. **`ds_status_bot.py` already detects external-facing failure** but
   doesn't recover it. Either let it run a restart hook (with rate
   limit) or just keep it as a passive alarm — Kyle's call.

These are ops-layer fixes. No C source changes.

### Per-port variability / schema deltas

**One new entry for DS_SCHEMA.md from this round:**

- **DS POSITION scheme** is non-standard. There is no `POS_STUNNED` /
  `POS_INCAP` constant. From `bit.h:911-917`:
    `POS_DEAD=0, POS_MORTAL=1, POS_SLEEPING=2, POS_RESTING=3,
     POS_SITTING=4, POS_FIGHTING=5, POS_STANDING=6`.
  When 2003 disasm sets `victim->position = 3`, that's `POS_RESTING`
  in DS, NOT `POS_STUNNED` (which doesn't exist). do_throw uses
  `POS_RESTING` for the knock-down semantic.

**Carry-over schema entries (from 0.4.16 do_dance work, still valid):**

- **DS `sh_int = int` (4 bytes), not `short`.** AFFECT_DATA layout is
  `where +16, type +20, level +24, duration +28, location +32,
  modifier +36, bitvector +40`.

- **`where=TO_IMMUNE (2) + bitvector=N`** routes to `imm_flags`.
  **`where=TO_AFFECTS2 (7)`** routes to `affected_by2` (used by
  `do_jab` for AFF2_JAB).

- **`dance_table` struct layout**: `{ char *name, int dance }` = 8
  bytes per entry.

### Test plan (0.4.20 — do_shuriken + multi_shuriken + do_feed)

#### `do_shuriken`
1. `shuriken <victim>` outside combat → uses get_char_room target,
   triggers HIT path with literal 12 wait clamp on success.
2. After HIT, observe up to 4 damage messages (1 guaranteed + 1 if
   you have HASTE + 1 from second_attack roll + 1 from third_attack
   roll). Each is `DAM_POISON`.
3. After multi-hits, if victim still fighting you, see "$n buckles
   under the pain" + "$n throws a shuriken at you" + small DAM_PIERCE
   damage + "You slow down and feel weaker!" message + slow affect
   on victim (-1 dex via `affect_join` + chained `slow` spell).
4. MISS: damage(0) DAM_POISON for show, then half-beats wait.
5. As IMM (trust > 102), wait clamps should be 0 for both branches.
6. With AFF_SLOW, multi_shuriken's hit 3/4 chances should halve.

#### `do_feed`
1. `feed <victim>` while in normal form → 3-line bite + DAM_PIERCE
   damage in `level`–`level*2` range.
2. `feed` while polyform == 3 (vampiric form, set via shape-change
   skill or `set char self polyform 3` if exposed) → damage should
   be ~33% higher than normal-form baseline.
3. `feed` while caster is blind → "{hYou cannot feed while blind.{x"
4. `feed self` → "You can't feed off yourself!"
5. `feed <victim_at_low_HP>` → "$N is hurt and suspicious..."
   (victim must be below 1/6 max_hit).
6. `feed <victim_fighting_other_PC>` (different group) → "Kill stealing
   is not permitted." Same gate as scream.
7. Effective hit chance should be at least 90% even at low skill.
8. Miss → "$n tries to bite you, but hits only air." (the
   resistance-themed alert miss is omitted; only normal branch).

### Test plan (0.4.19 — do_earthbind + do_scream)

#### `do_earthbind`
1. `earthbind <target>` against a non-flying target → "They aren't airborn."
2. Have a target cast `fly` (or use `set` to give them AFF_FLYING),
   then `earthbind <target>` → "ripped from the skies" broadcast,
   AFF_FLYING removed, fly/levitation/grow_wings affects all stripped,
   bash damage in `level`–`level*2` range.
3. `earthbind self` → snarky "tendrils answer your call, then leave"
4. `earthbind` (no arg) while fighting a flying mob → uses ch->fighting
5. MISS feedback: "Your tendrils find nothing but air." + room broadcast
6. Verify `affects` panel — fly should be gone after a successful earthbind

#### `do_scream`
1. `scream <target>` → 3-line broadcast (you/them/room) regardless of
   hit. Damage type is **sound** — armor doesn't reduce it.
2. Repeat scream attempts to confirm the ~50% effective hit cap (even
   at 100% skill, hits roughly half the time).
3. Try to scream a target who's fighting another PC outside your group
   → "Kill stealing is not permitted."
4. After landing several screams, eventually one should additionally
   stun the victim (5% chance per hit). Confirm via `victim->stunned`
   transition / inability to act for 1-2 ticks.
5. Verify miss wait is longer than hit wait (3*beats/2 vs 1*beats).

### Test plan (0.4.18 — do_roundhouse + do_healing_touch)

#### `do_roundhouse` (auto-targets ch->fighting)
1. Engage a mob/dummy and `roundhouse` (no arg) → "Your roundhouse
   catches $N off guard!" + bash damage in `level/2`–`level` range.
2. `roundhouse` while not fighting → "You aren't fighting anyone."
3. `roundhouse` while stunned → "You're still a little woozy."
4. As a class without the skill → "You better leave the martial arts
   to monks."
5. Monk-family character (pclass 8/23/38) — should still get the
   generic broadcast + bash damage (NOT multi_kick combo) until Monk
   batch lands. Flag if Monks notice anything unusual.

#### `do_healing_touch` (target arg or self)
1. `htouch` (no arg) → self-heal, "You focus your energy..." + room
   broadcast + "You feel better!"
2. `htouch <ally>` → 3-line broadcast (you/them/room) + "You feel
   better!" to ally only.
3. `htouch <stranger_in_room>` → still works (no friend gate); aim is
   for healing role-play.
4. `htouch nonexistent` → "They are not here."
5. `htouch` with mana <= 54 → "Your spirit is too weak."
6. `htouch` while stunned → "You're still a little woozy."
7. Heal amounts (verify by spell scaling — at level 60 with 100% skill,
   self-heal of `2d8 + 30 = 32-46` — verify on a damaged character).
8. Heal halved if target has `devil's curse` affect (apply via curse
   spell first).
9. Caster `mana` should drop by 50 per use.
10. As IMM (trust > 102), `htouch` should NOT lock up your wait state.

### Test plan (0.4.17 — do_jab + do_throw)

#### `do_jab` (needs a class with the skill, level 40+ minstrel per
const.c:8696)

1. `jab` with no target while not fighting → "But you aren't fighting
   anyone!"
2. Engage a mob/dummy and `jab` (no arg) → uses ch->fighting; expect
   "You jab their throat" / "$N gasps as you slam your fist…"
   broadcast and a 1-tick AFF2_JAB on the target ("affects" panel
   should show jab).
3. Immediately `jab` again → "They are already gasping for breath!"
4. After the affect drops (~1 tick), re-jab → succeeds again.
5. `jab self` → "With deliberate care you jab yourself till a welt
   forms."
6. `jab notavalidtarget` → "They aren't here."
7. `jab` while pktimered (recent PvP) in a non-safe room → "Your
   heart's pounding to fast!!"
8. `jab` against a charm-master → "But $N is your friend!"
9. As an Immortal (trust > 102) jab a hidden mob → name shown is
   "An Immortal" colorized form.

#### `do_throw` (similar class gate — check skill_table for who has it)

1. `throw <victim>` against a sleeping/resting target → "You'll have
   to let $M get back up first."
2. `throw self` → snarky "There is stupid…" message.
3. `throw <PC>` and HIT → 3-line broadcast, victim drops to RESTING
   position, victim's wait/flee_daze clamped (try moving them
   immediately — should be locked out for ~24 pulses).
4. `throw <PC>` and MISS → 3-line shrug-out broadcast, **caster** drops
   to RESTING, caster's wait clamps to 2*beats (or 3*beats if a
   gangbang situation). Try `look` immediately — caster should be
   "resting" position.
5. As IMM (trust > 102), MISS shouldn't lock you up (wait stays 0).
6. `throw` while ch is stunned → "You're still a little woozy."

**Note on degraded behaviour**: do_throw's "victim alert" flag is
omitted (chance-zeroing + alert-vs-normal-miss messaging always picks
normal). Players whose victim would have been "alert" in 2003 will
see normal miss messages and slightly easier-to-hit chance. Flag if
players notice.

### Suggested next step

CLASS ABILITY tier (Cowork Priority 3) — complete within recovery scope.

**Priority 4 DS Custom Other** progress (smallest → biggest):

| Function | Size | Status |
|---|---:|---|
| `do_roundhouse`     | 339b  | ✅ live 0.4.18 |
| `do_healing_touch`  | 598b  | ✅ live 0.4.18 |
| `do_earthbind`      | 800b  | ✅ live 0.4.19 |
| `do_scream`         | 748b  | ✅ live 0.4.19 |
| `do_shuriken`       | 796b  | ✅ live 0.4.20 |
| `multi_shuriken`    | 320b  | ✅ live 0.4.20 (helper unlock) |
| `do_feed`           | 836b  | ✅ live 0.4.20 |
| `do_bastion`        | 824b  | ✅ live 0.4.21 |
| `do_strangle`       | 780b  | ✅ live 0.4.21 |
| `do_chaos_blow`     | 884b  | ✅ live 0.4.22 |
| `do_ambush`         | 712b  | ✅ live 0.4.22 |
| `do_pinch`          | 984b  | 🟡 staged 0.4.23 |
| `do_blackjack`      | 984b  | 🟡 staged 0.4.23 |
| `do_caltrops`       | 552b  | next (mapped from 2003 `do_caltraps` typo) |
| `do_blinding_strike`| 1022b | |
| `do_assassinate`    | 1148b | |
| `do_shield_smash`   | 1169b | |
| `do_blackjack`      | 1018b | |
| `do_blinding_strike`| 1022b | |
| `do_assassinate`    | 1148b | |
| `do_shield_smash`   | 1169b | |
| `do_forge`          | 1200b | |
| `do_stance`         | 1479b | |

**Confirmed absent from 2003 binary** (registered in current source but
no disasm to recover): `do_hurl`, `do_toss`, `do_powerinvuln`,
`do_plantroots`, `do_powerstun`, `do_quickening`, `do_caltrops`,
`do_dislodge`, `do_powerblind`, `do_transfix`, `do_thousand_wounds`,
`do_gash`, `do_eadbutt`, `do_devils_touch`, `do_hack`, `do_aura`,
`do_vital_strike`. These are post-2003 additions; resurrection path
ignores them.

Code is queuing `do_earthbind` + `do_scream` next bundle (0.4.19).
**`update.c` gap survey** still in task queue as a parallel track.

### Open questions / blockers

- **`gsn_wary` caster-side source** (carry-over from 0.4.15) — still
  unknown. Likely surfaces when `do_dodge` or similar defensive
  abilities get ported.
- **2003 0x2f0 chance modifier** (do_jab + do_throw) — see Carry-over
  open questions above.
- **2003 0x16c "victim alert" flag** (do_throw) — see Carry-over open
  questions above.
- **dance_class auto-detect for bots** — bot personalities don't
  currently know to type `dance storm` before `storm`. If we want
  the BotShade/Fury bots to use storm, they need a personality flag
  and pre-combat dance setup. Defer until bots are spawned as
  dance-class characters (currently warriors).
- **Bot prototype-placement bug** in `add_botspawn_cmd.py` —
  patcher writes prototypes inline in interp.c instead of interp.h
  via DECLARE_DO_FUN. Source tree is fixed manually; patcher itself
  needs regenerating to match. Low priority.
- **Stale comment cleanup** (carry-over from 0.4.7) —
  `act_combat.c:3461` references `multi_hit(ch, victim, 0)` in
  do_cross_slash's comment block. Code is correct; comment is stale.
