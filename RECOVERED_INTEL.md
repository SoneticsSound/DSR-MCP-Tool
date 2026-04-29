# Recovered Data Intelligence

**Generated:** 2026-04-28  
**Source:** `recovered/devils/` — 1,847 files, 167.5 MB extracted by `recovery_carver.py`  
**Purpose:** Permanent reference so Code and Cowork don't need to rescan raw recovered data.

---

## What Was Recovered (Quick Map)

| Location | Count | Contents |
|---|---|---|
| `recovered/devils/src/*.c` | 67 .c files | Full source — **except act_combat.c** (only .o survived) |
| `recovered/devils/src/*.h` | 17 .h files | All headers intact — merc.h, bit.h, gsn.h, etc. |
| `recovered/devils/data/area/` | 96 .are files | World areas — fully intact |
| `recovered/devils/data/log/` | 306 .log files | Live gameplay session logs from 2003 |
| `recovered/devils/data/player/` | 155 player files | Character save files from 2003 |
| `recovered/devils/data/backup/` | 1,095 files | Player file backups |
| `recovered/devils/data/note/` | 11 .not files | In-game boards: ideas, immnote, chang, notes, etc. |
| `recovered/devils/data/misc/` | 16 files | help.are, help.mhp, coding.txt, todo.txt, mytodo.txt, etc. |
| `recovered/devils/bin/` | 3 binaries | ds, ds.new, ds.tmp — different build snapshots |
| `recovered/devils/bin/ryan/` | 3 binaries | Ryan's build — separate snapshot |
| `recovered/devils/bin/dontdeletethis/` | 2 binaries | **2002-11-08 build** — oldest binary, primary disasm source |

**Critical gap:** `act_combat.c` is permanently lost. `act_combat.o` survived but cannot be decompiled to readable C. All DS custom combat logic is being reverse-engineered from the 2003 binaries via disasm.

---

## Note Boards (`data/note/`)

### `chang.not` — Changelog Board (Imm-posted patch notes)
**Most valuable file in the entire recovered dataset for mechanic research.**

Key entries directly relevant to active work:

**Wary Flag (April 16, 2003 — Leto):**
> "Wary flag. Whenever someone is hit by backstab, ambush, charge, bastion or chromatic salvo
> they will get a flag which prevents anyone else using a similar attack until a number of
> rounds have passed. The flag will also vanish if fighting stops."

This is the canonical definition of the wary flag seen at offset `0x16c bit 0x04` in
`do_throw`'s disasm and `0x17c bit 0x40` in `do_charge`. The flag is **set by** backstab,
ambush, charge, bastion, chromatic salvo. `do_throw` **reads** it but the changelog doesn't
list throw as a setter — meaning a wary victim (recently hit by one of those openers) resists
being thrown. Makes complete sense: if someone just landed a charge or backstab on you, you're
now alert and can't be caught off-guard with a throw.

Other relevant chang.not entries:
- **Apr 22:** "Ambush now does bonus damage wielding spears. Charge does bonus damage if you wield swords."
- **Apr 29:** "Wardancers lost counterattack on Mist Dance. Fleeing: harder to flee, only 5/6 attempts per round."
- **May 9:** "Cleave: moves to once every 2 rounds (like circle)."
- **Various:** Circle damage lowered, berserk (slam) stun frequency reduced, warcry changes.

### `bitch.not` — IMM Meeting Minutes / Internal Notes
Informal meeting minutes and internal discussions. Key combat/skill entries:

- **Shapes getting jab:** "Giving shapes jab. We have no high level shapes, we'll wait to see how they do in pk without it." — Confirms jab was Ninja/Assassin/Shadowen originally; extension to Shapes debated.
- **Jab duration:** "lower both rift and jab to 1 tick (0 in score) 1,0 is too much for hero level" and "Making jab duration same as rift. Measure passes." — Jab was mechanically linked to rift duration at one point. Both were being discussed as too long at hero level.
- **Ambush as a Guardian opener:** "ambush, something for guardians to start fights with. does 1 extra round of damage and maybe adds an entangle affect for 3-5 rounds. or maybe a chance of a stun?"
- **Backstab skills for Shapes:** "I tried to add all their backstab skills...all 4 of em."
- **Rift + jab** mentioned together repeatedly — both are interrupt/silence-family skills.

### `ideas.not` — Player Suggestion Board (Sep 2003)
Player-submitted ideas from the live community. No direct jab/throw mechanic info.
Notable entries:
- Clan PK visibility in genocides (Lagen)
- War flag to identify war participants (Ayperos)
- Item insurance vs. looting (Xeyer)
- Knight-only honed weapons (Einon)
- Throwing daggers need shocking flag for chasing (Mallegar) — *different from do_throw; shuriken/thrown-item skill*

### `immnote.not` — Immortal Notices
Administrative notes (renames, promotions, ban handling, meeting times). No combat mechanic content.
Notable: Shade flagged vorpal flag as overpowered vs. sharp — fixed to 5% increase. New Qimms appointed.

### `notes.not`
Spam-filled (bot/advertisement posts). No useful content.

### `wedds.not`, `penal.not`, `questi.not`, `clani.not`, `classifieds.not`
Not scanned for combat content — administrative/social boards unlikely to contain mechanic data.

---

## Misc Files (`data/misc/`)

### `coding.txt` — Coding TODO Board
Imm-posted development tasks (Alecca, ceto). Useful for understanding what was in-flight in 2003:
- Racial affects on affect screen
- War flag system
- Custom bugs causing crashes
- Interactive web/mud integration (help files, skill lists)
- Skill display command (e.g. `skill dirt kicking`)

### `mytodo.txt` / `todo.txt`
Personal notes (Alecca). Mix of dev tasks and personal reminders. No mechanic content.

### `help.are` / `help.mhp`
In-game helpfile database. Scanned for jab/throw:
- **`do_throw` help (line 572):** "Throw is a skill given to Ninjas/Assassins/Shadowens, which allows them to pick up their opponent and basically body slam them into the ground." — No HP condition or prerequisite mentioned.
- **No `do_jab` helpfile exists.** Jab was never given a helpfile entry.
- "Unwary" language appears only in the SKILL_KICK entry (failed kick unbalances an unwary character) — unrelated to do_throw.

---

## Source Files — Combat-Relevant Findings

### `fight.c` — Recovered, Fully Readable
Grepped for: wary, alert, attacker, AFF2, throw, jab, gsn_jab, gsn_throw.

**Findings:**
- **Lines 1371–1373:** Elbow jab in the multi-hit attack sequence — this is a *random attack noun*, NOT `do_jab`.
  ```
  act("You swiftly jab your elbow into $N's face.", ch, NULL, victim, TO_CHAR);
  act("$n swiftly jabs $s elbow into your face!", ch, NULL, victim, TO_VICT);
  act("$n swiftly jabs $s elbow into $N's face!", ch, NULL, victim, TO_NOTVICT);
  ```
- **Line 4588:** `fch->attacker = FALSE;` — PvP attacker bookkeeping, not skill logic.
- **Line 5660:** Comment about negative attacker value — unrelated.
- **No wary, WARY, alert, ALERT, gsn_jab, gsn_throw references anywhere in fight.c.**

Conclusion: All wary flag logic (setting and reading) lives entirely in `act_combat.c`, which is lost.
The flag itself is a CHAR_DATA field read via bit-test in the disassembly.

### `act_combat.c` — LOST (only `.o` compiled object survived)
Primary target of all disasm work. Contains do_jab, do_throw, do_charge, do_backstab,
do_circle, do_ambush, and all other DS-custom combat verbs.

### `merc.h`, `bit.h`, `gsn.h` — Recovered, Fully Readable
Used as the authoritative field-name source for all patcher scripts. See `DS_SCHEMA.md`
for the extracted field layout. No wary/alert flags found in current headers — the field
at disasm offset `0x16c` is not represented in the current struct definition, which is
why the wary flag check couldn't be directly ported.

---

## Log Files (`data/log/`)

**306 total log files.** 2003 live gameplay sessions. Largest: `1485.log` (13 MB).  
Files containing jab/throw/wary/alert strings (per grep scan 2026-04-28):
`1044, 1341, 1362, 1366, 1369, 1370, 1377, 1378, 1380, 1407, 1411, 1414, 1433, 1434, 1442, 1443, 1444, 1449, 1450, 1457` (and more — scan returned 20 before cutoff).

**Not yet extracted:** Actual combat message strings from these log files are unread due to output size limits. When investigating specific messaging (e.g. the wary miss message for throw), target-grep these files:
```bash
grep -h "wary\|too wary\|sensed\|alert" recovered/devils/data/log/*.log | sort -u
grep -h "throws.*ground\|body slam\|slams.*ground" recovered/devils/data/log/*.log | sort -u
grep -h "jabs.*throat\|fist.*throat\|gasping" recovered/devils/data/log/*.log | sort -u
```

---

## Binaries

| Binary | Date | Size | Notes |
|---|---|---|---|
| `bin/dontdeletethis/ds` | 2002-11-08 | 2.87 MB | **Oldest build** — primary disasm source for all ports |
| `bin/dontdeletethis/ds.new` | 2002-11-08 | 2.87 MB | Identical to ds |
| `bin/ds` | 2003 | 5.35 MB | Later 2003 build — larger, more features |
| `bin/ds.new` | 2003 | 5.35 MB | Latest recovered build |
| `bin/ds.tmp` | 2003 | 2.77 MB | Intermediate build |
| `bin/ryan/ds` | 2003 | 3.02 MB | Ryan's personal build — unknown divergence |

The 2002-11-08 binary in `dontdeletethis/` is the one Code has been using for disasm.
The larger 2003 builds may contain features not yet ported (do_hurl, etc.) — worth
diffing string tables if a mechanic can't be found in the older binary.

---

## What This Means for Active Work

### BUG-008 (do_throw wary flag)
**Effectively solved by chang.not.** The wary flag is set by backstab/ambush/charge/bastion/
chromatic salvo and prevents "similar attacks." Throw reads this flag — a victim who was just
backstabbed, charged, etc. is alert enough to resist being thrown. The flag is not in current
merc.h/bit.h because it's a lost struct field from act_combat.c.

**Next step for Code:** The wary flag needs to be added to CHAR_DATA as a persistent bit or
timer field, set in do_backstab/do_ambush/do_charge/do_bastion at HIT time, and cleared after
N rounds or when combat ends. Then do_throw and do_charge read it. This is a full mechanic
restoration, not just messaging.

### Log Files for Messaging Research
When you need the *exact* in-game strings for any 2003 mechanic, grep the log files first.
The 20 matched files above are the most likely to contain jab/throw combat output.
Target individual logs by size for broad combat coverage: 1485, 1521, 1442, 1489, 1476.

---

## Action Items — Deferred Until Game Is Stable

These are not blocking. Work through the combat port backlog first. Come back to these
once the CLASS ABILITY tier and update.c gap survey are done.

### 1. Fix `do_time` to show real uptime
**Priority: low / quality of life**
The `do_time` function in `act_info.c` already has the `str_boot_time` string — it was there
in the recovered source but the live build may have lost it. Add or restore the line:
```c
sprintf(buf, "Devil's Silence started up at %s\n\rThe system time is %s\n\r",
    str_boot_time, (char *) ctime(&current_time));
send_to_char(buf, ch);
```
This gives Kyle a reliable in-game uptime check without needing SSH access.

### 2. Extract function list from `act_combat.o`
**Priority: medium — gives us a complete port checklist**
Run `nm -g recovered/devils/src/act_combat.o` to dump every function symbol defined in
the lost source file. This produces a definitive list of every `do_*` function that existed
in act_combat.c — we can cross-reference against what's been ported to know exactly what
remains. No decompilation needed, just symbol names.

### 3. Mine the log files for combat strings
**Priority: medium — fills messaging gaps for any ported verb**
Targeted grep against the 5 largest log files (1485, 1521, 1442, 1489, 1476) for any
skill whose messaging we're uncertain about. Commands that produce useful output:
```bash
grep -h "wary\|too wary\|sensed" recovered/devils/data/log/*.log | sort -u
grep -h "jabs.*throat\|gasping" recovered/devils/data/log/*.log | sort -u
grep -h "throws\|body slam\|slams.*ground" recovered/devils/data/log/*.log | sort -u
```
Extend the pattern for any future skill before writing synthetic messaging.

### 4. Binary string diff — 2002 vs 2003 vs Ryan builds
**Priority: low — discovery only**
Extract string tables from all three binary snapshots and diff them:
```bash
strings recovered/devils/bin/dontdeletethis/ds > /tmp/str_2002.txt
strings recovered/devils/bin/ds.new            > /tmp/str_2003.txt
strings recovered/devils/bin/ryan/ds           > /tmp/str_ryan.txt
diff /tmp/str_2002.txt /tmp/str_2003.txt
diff /tmp/str_2003.txt /tmp/str_ryan.txt
```
Strings only in the 2003 binary = features added after the 2002 snapshot.
Strings only in Ryan's build = his personal additions or a different code branch.
This could surface entire mechanics we don't know exist yet.

### 5. Second-pass tar carving
**Priority: low — diminishing returns likely**
`recovery_carver.py` made one pass. A second pass with a more aggressive block-skip
strategy may recover additional file fragments from the corrupted region. Worth attempting
after everything else — worst case is no new data.

### 6. Investigate Ryan's build
**Priority: low — unknown upside**
`bin/ryan/ds` is 3.02 MB vs the main 5.35 MB binary. We don't know if it's an older
snapshot, a fork, or a test build. String diff against the main binary (action item 4)
will tell us quickly whether it's worth deeper analysis.
