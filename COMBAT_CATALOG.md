# Combat Catalog — Phase A Deliverable

**Generated 2026-04-25** from the corrupt-but-readable `act_combat.o`.

## Headline finding

The `.text` section of the original 2003 `act_combat.o` is **completely intact**
(78,123 bytes of clean i386 assembly). Only the `.debug_*` sections were destroyed
by archive corruption. The corruption that prevented linking was limited to
relocation entries pointing into the bad debug data. This means:

- We have **Tier 1 fidelity** for every single combat ability — the actual 2003
  implementation, in assembly, byte-for-byte.
- The `.rel.text` relocation table (4,348 entries) is intact, naming every
  external helper and string each function calls. We have a complete call graph.
- Every player-facing message string in `.rodata` is recoverable verbatim.
- 84 unique external helpers are referenced (`act`, `damage`, `multi_hit`,
  `set_fighting`, `update_pos`, etc.) — all defined in surviving source files.

Practical implication: we don't have to *guess* DS-custom behaviour from the wiki.
We can read the original disassembly and translate it back to C. ROT/ROM source
becomes a *starting template* for vanilla commands, not the only available
reference.

## Symbol totals

- Functions in `act_combat.o`: **102**
- Player-exposed commands: **87**
- Internal helpers (called by other modules): **15**

## How to read the columns

- **Cmd** — what the player types.
- **Pos** — required position (FIGHTING, STANDING, RESTING, SLEEPING, DEAD).
- **Lvl** — minimum player level. `0` = available to all, `20` = high-tier.
- **Size** — bytes in `.text` from disassembly. Rough proxy for porting effort.
- **Source** — recommended porting reference for Phase B.

## BASIC ROM (Priority 1 — port these first)

These exist in stock ROM 2.4. Public source is available; DS's flavour is minor tweaks. Once `do_kill` and `do_flee` work, mob combat, aggro, and baseline PK become testable end-to-end. Do these first.

**Status as of 2026-04-25 evening:** ALL 11 BASIC ROM functions IMPLEMENTED. Step 2 BASIC ROM tier complete.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `do_kill` | hit | FIGHTING | 0 | 231 | ✅ IMPLEMENTED 2026-04-25 |
| `do_kill` | kill | FIGHTING | 0 | 231 | ✅ IMPLEMENTED 2026-04-25 |
| `do_kick` | kick | FIGHTING | 0 | 569 | ✅ IMPLEMENTED 2026-04-25 (knee-breaker / limp side-mechanic verified — affect persistence, not a bug) |
| `do_berserk` | berserk | FIGHTING | 0 | 661 | ✅ IMPLEMENTED 2026-04-25 (Bundle B verified) |
| `do_rescue` | rescue | FIGHTING | 0 | 673 | ✅ IMPLEMENTED 2026-04-25 (Bundle A — deployed, stable, light testing) |
| `do_flee` | flee | FIGHTING | 0 | 852 | ✅ IMPLEMENTED 2026-04-25 |
| `do_backstab` | backstab | FIGHTING | 0 | 857 | ✅ IMPLEMENTED 2026-04-25 (Bundle B verified) |
| `do_backstab` | bs | FIGHTING | 0 | 857 | ✅ IMPLEMENTED 2026-04-25 (Bundle B verified) |
| `do_trip` | trip | FIGHTING | 0 | 970 | ✅ IMPLEMENTED 2026-04-25 (Bundle A — deployed, stable, light testing) |
| `do_gouge` | gouge | FIGHTING | 0 | 998 | ✅ IMPLEMENTED 2026-04-25 (Bundle B verified) |
| `do_disarm` | disarm | FIGHTING | 0 | 1011 | ✅ IMPLEMENTED 2026-04-25 (with `disarm()` helper — weapon-drop verified) |
| `do_dirt` | dirt | FIGHTING | 0 | 1046 | ✅ IMPLEMENTED 2026-04-25 (Bundle B verified) |
| `do_bash` | bash | FIGHTING | 0 | 1606 | ✅ IMPLEMENTED 2026-04-25 (Bundle A — deployed, stable, light testing) |

## CLASS ABILITY / ROT 1.4 (Priority 2)

Standard ROT 1.4 class verbs. Public source exists; diff against disasm to catch DS tweaks.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `do_stomp` | stomp | FIGHTING | 0 | 522 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE AOE batch — verified in-game 2026-04-27) |
| `do_legsweep` | legsweep | FIGHTING | 0 | 555 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE AOE sub-anchor — verified in-game) |
| `do_circle` | circle | FIGHTING | 0 | 638 | ✅ IMPLEMENTED 2026-04-25 (Bundle B verified) |
| `do_charge` | charge | FIGHTING | 0 | 833 | ROT 1.4 source + disasm validation |
| `do_jab` | jab | STANDING | 0 | 1080 | ROT 1.4 source + disasm validation |
| `do_throw` | throw | FIGHTING | 0 | 1247 | ROT 1.4 source + disasm validation |
| `do_dance` | dance | FIGHTING | 0 | 1282 | ROT 1.4 source + disasm validation |
| `do_hurl` | hurl | FIGHTING | 0 | 2477 | ROT 1.4 source + disasm validation |

## DS CUSTOM — Monk class (Priority 3a)

Monk ki / breathing / katana suite. The `monk_*` helpers (in HELPER section) are the actual strike implementations called by `multi_kick`.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `do_deepbreathing` | deepbreathing | FIGHTING | 0 | 286 | Hand-decompile from disasm + wiki |
| `do_concentration` | concentration | STANDING | 0 | 375 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — hit roll +250) |
| `do_ironwill` | ironwill | STANDING | 0 | 379 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — RES_CHARM + saves -22) |
| `do_katana` | katana | STANDING | 0 | 748 | Hand-decompile from disasm + wiki |
| `do_buddha_palm` | buddha palm | FIGHTING | 0 | 842 | Hand-decompile from disasm + wiki |
| `do_chi` | chi | FIGHTING | 0 | 1042 | Hand-decompile from disasm + wiki |

## DS CUSTOM — Voodoo class (Priority 3b)

Voodoo curse system. `do_voodoo` is the dispatcher; `voodoo_pin` / `voodoo_throw` / `voodoo_trip` (in HELPER section) are the actions.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `do_voodoo` | voodoo | STANDING | 20 | 274 | Hand-decompile from disasm + wiki |
| `do_jinx_palm` | jinx palm | FIGHTING | 0 | 1096 | Hand-decompile from disasm + wiki |

## DS CUSTOM — Other (Priority 3c, sorted small→big)

All remaining DS-specific abilities. Sorted by size — smallest first is the easier place to start practising the disasm→C workflow.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `do_mock` | mock | RESTING | 0 | 183 | ✅ IMPLEMENTED 2026-04-25 (DS-custom anchor — workflow proof-of-concept) |
| `do_spellbane` | spellbane | FIGHTING | 0 | 302 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF anchor — verified via in-game affects panel) |
| `do_resistance` | resistance | STANDING | 0 | 322 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — save vs spell -22) |
| `do_resistance` | resistance | FIGHTING | 0 | 322 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — save vs spell -22) |
| `do_roundhouse` | roundhouse | FIGHTING | 0 | 339 | Hand-decompile from disasm + wiki |
| `do_target` | target | FIGHTING | 0 | 344 | ✅ IMPLEMENTED 2026-04-26 (UTILITY-TARGET anchor — verified in-game) |
| `do_target` | target | FIGHTING | 0 | 344 | ✅ IMPLEMENTED 2026-04-26 (UTILITY-TARGET anchor — verified in-game) |
| `do_warcry` | warcry | STANDING | 0 | 376 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — hit/dam roll +55) |
| `do_powerinvuln` | powerinvuln | FIGHTING | 0 | 428 | Hand-decompile from disasm + wiki |
| `do_battlehymn` | battlehymn | STANDING | 0 | 429 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — save vs spell -22) |
| `do_cleanse` | cleanse | STANDING | 0 | 444 | Hand-decompile from disasm + wiki |
| `do_dhammer` | dhammer | FIGHTING | 0 | 473 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE AOE batch — verified in-game 2026-04-27) |
| `do_bloodlust` | bloodlust | FIGHTING | 0 | 475 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — hp +500, saves +15) |
| `do_plantroots` | plantroots | FIGHTING | 0 | 500 | Hand-decompile from disasm + wiki |
| `do_warpaint` | warpaint | STANDING | 0 | 503 | ✅ IMPLEMENTED 2026-04-25 (BUFF-SELF batch — skull requirement queued for removal per IDEA-004) |
| `do_powerstun` | powerstun | FIGHTING | 0 | 529 | Hand-decompile from disasm + wiki |
| `do_cross_slash` | cross slash | FIGHTING | 0 | 536 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE single-target batch — verified in-game 2026-04-27) |
| `do_whirlwind` | whirlwind | FIGHTING | 0 | 537 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE AOE batch — verified in-game 2026-04-27) |
| `do_powersilence` | powersilence | FIGHTING | 0 | 551 | Hand-decompile from disasm + wiki |
| `do_rub` | rub | FIGHTING | 0 | 552 | Hand-decompile from disasm + wiki |
| `do_cleave` | cleave | FIGHTING | 0 | 559 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE anchor — disasm-verified, tested in-game) |
| `do_garotte` | garotte | FIGHTING | 0 | 560 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE single-target batch — verified in-game 2026-04-27) |
| `do_quickening` | quickening | FIGHTING | 0 | 568 | Hand-decompile from disasm + wiki |
| `do_caltrops` | caltrops | FIGHTING | 0 | 585 | Hand-decompile from disasm + wiki |
| `do_healing_touch` | htouch | STANDING | 0 | 598 | Hand-decompile from disasm + wiki |
| `do_storm` | storm | FIGHTING | 0 | 610 | Hand-decompile from disasm + wiki |
| `do_dislodge` | dislodge | FIGHTING | 0 | 631 | Hand-decompile from disasm + wiki |
| `do_powerblind` | powerblind | FIGHTING | 0 | 641 | Hand-decompile from disasm + wiki |
| `do_strike` | strike | FIGHTING | 0 | 660 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE single-target — single-weapon gate, HP-frac /10, alert-flag dual MISS) |
| `do_gore` | gore | FIGHTING | 0 | 680 | ✅ IMPLEMENTED 2026-04-26 (STRIKE-PURE single-target — race-locked, direct damage not multi_hit, self-stun on miss) |
| `do_transfix` | transfix | STANDING | 0 | 701 | Hand-decompile from disasm + wiki |
| `do_thousand_wounds` | thousand wounds | FIGHTING | 0 | 704 | Hand-decompile from disasm + wiki |
| `do_gash` | gash | FIGHTING | 0 | 748 | Hand-decompile from disasm + wiki |
| `do_eadbutt` | eadbutt | FIGHTING | 0 | 771 | Hand-decompile from disasm + wiki |
| `do_devils_touch` | devils touch | FIGHTING | 0 | 776 | Hand-decompile from disasm + wiki |
| `do_earthbind` | earthbind | FIGHTING | 0 | 797 | Hand-decompile from disasm + wiki |
| `do_scream` | scream | FIGHTING | 0 | 801 | Hand-decompile from disasm + wiki |
| `do_shuriken` | shuriken | FIGHTING | 0 | 812 | Hand-decompile from disasm + wiki |
| `do_feed` | feed | FIGHTING | 0 | 813 | Hand-decompile from disasm + wiki |
| `do_bastion` | bastion | FIGHTING | 0 | 815 | Hand-decompile from disasm + wiki |
| `do_strangle` | strangle | STANDING | 0 | 825 | Hand-decompile from disasm + wiki |
| `do_chaos_blow` | chaos blow | FIGHTING | 0 | 870 | Hand-decompile from disasm + wiki |
| `do_toss` | toss daggers | FIGHTING | 0 | 892 | Hand-decompile from disasm + wiki |
| `do_hack` | hack | FIGHTING | 0 | 959 | Hand-decompile from disasm + wiki |
| `do_ambush` | ambush | DEAD | 0 | 967 | Hand-decompile from disasm + wiki |
| `do_pinch` | pinch | STANDING | 0 | 1018 | Hand-decompile from disasm + wiki |
| `do_blackjack` | blackjack | STANDING | 0 | 1018 | Hand-decompile from disasm + wiki |
| `do_blinding_strike` | blinding strike | FIGHTING | 0 | 1022 | Hand-decompile from disasm + wiki |
| `do_assassinate` | assassinate | STANDING | 0 | 1148 | Hand-decompile from disasm + wiki |
| `do_shield_smash` | smash | FIGHTING | 0 | 1169 | Hand-decompile from disasm + wiki |
| `do_forge` | forge | SLEEPING | 0 | 1200 | Hand-decompile from disasm + wiki |
| `do_aura` | aura | STANDING | 0 | 1452 | Hand-decompile from disasm + wiki |
| `do_stance` | stance | FIGHTING | 0 | 1479 | Hand-decompile from disasm + wiki |
| `do_vital_strike` | vital strike | FIGHTING | 0 | 1690 | Hand-decompile from disasm + wiki |

## DS CUSTOM — Psionics (Priority 4 — biggest functions, do last)

These are the four largest functions in `act_combat.o`. They implement the elemental psionic system Devils were known for. Heavy decompile work — leave for after the easier wins.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `do_biomanipulation` | biomanipulation | FIGHTING | 0 | 2418 | Hand-decompile from disasm + wiki |
| `do_electrokinesis` | electrokinesis | FIGHTING | 0 | 3511 | Hand-decompile from disasm + wiki |
| `do_telekinesis` | telekinesis | FIGHTING | 0 | 3536 | Hand-decompile from disasm + wiki |
| `do_pyrokinesis` | pyrokinesis | FIGHTING | 0 | 3807 | Hand-decompile from disasm + wiki |

## Internal Helpers (no command interface)

Called from other modules — not from the cmd_table. They get linked when we port the corresponding command. The `monk_*` set are individual strike implementations called by `multi_kick`. The `voodoo_*` set are called by `do_voodoo`. `disarm` (lowercase) is called by combat code when a weapon is knocked out of the wielder's hand. `check_killtimer` is the kill-timer decay called by `update.c` ticks.

| Function | Cmd | Pos | Lvl | Size | Source |
|---|---|---|---|---:|---|
| `check_killtimer` | (helper) | - | - | 59 | Hand-decompile from disasm + wiki |
| `monk_backfist` | (helper) | - | - | 113 | Hand-decompile from disasm + wiki |
| `monk_elbow` | (helper) | - | - | 113 | Hand-decompile from disasm + wiki |
| `monk_knee` | (helper) | - | - | 113 | Hand-decompile from disasm + wiki |
| `monk_palmstrike` | (helper) | - | - | 113 | Hand-decompile from disasm + wiki |
| `monk_shinkick` | (helper) | - | - | 113 | Hand-decompile from disasm + wiki |
| `monk_thrustkick` | (helper) | - | - | 113 | Hand-decompile from disasm + wiki |
| `monk_reverse` | (helper) | - | - | 192 | Hand-decompile from disasm + wiki |
| `monk_spinkick` | (helper) | - | - | 203 | Hand-decompile from disasm + wiki |
| `multi_shuriken` | (helper) | - | - | 341 | Hand-decompile from disasm + wiki |
| `multi_kick` | (helper) | - | - | 383 | Hand-decompile from disasm + wiki |
| `voodoo_pin` | (helper) | - | - | 519 | Hand-decompile from disasm + wiki |
| `voodoo_trip` | (helper) | - | - | 533 | Hand-decompile from disasm + wiki |
| `disarm` | (helper) | - | - | 567 | Hand-decompile from disasm + wiki |
| `voodoo_throw` | (helper) | - | - | 814 | Hand-decompile from disasm + wiki |

## Recommended porting order

1. **`do_kill`, `do_flee`** (231 + 852 bytes, vanilla ROM)
   The smallest possible patch that turns the MUD from un-playable to
   playable for mob combat. Everything downstream depends on them being correct.
2. **`do_kick`, `do_bash`, `do_trip`, `do_disarm`, `do_rescue`** (vanilla ROM)
   Standard combat repertoire. Each is small (300–1,600 bytes).
3. **`do_backstab`, `do_circle`, `do_gouge`, `do_dirt`, `do_berserk`**
   The classic class verbs. ROT 1.4 reference; validate vs. disasm.
4. **First DS-custom hand-decompile: `do_mock` (183 bytes — smallest)**
   Use this as the workflow proof-of-concept. If we can faithfully translate
   183 bytes of asm to C and reproduce the same player-facing messages, we
   know the larger ones are tractable.
5. **Small DS-custom batch (200–500 bytes each):** do_voodoo wrapper,
   do_spellbane, do_deepbreathing, do_resistance, do_target, do_warcry,
   do_ironwill, do_concentration, do_powerinvuln, do_battlehymn, do_cleanse,
   do_dhammer, do_bloodlust, do_plantroots, do_warpaint, do_stomp,
   do_powerstun, do_cross_slash, do_whirlwind, do_powersilence, do_rub,
   do_legsweep, do_cleave, do_garotte.
6. **Medium DS-custom (500–1,500 bytes):** the large remaining set.
7. **Heavy DS-custom (1,500+ bytes):** do_aura, do_stance, do_bash, do_vital_strike,
   do_biomanipulation, do_hurl.
8. **The four psionics** (3,500–3,800 bytes each):
   do_electrokinesis, do_telekinesis, do_pyrokinesis, do_biomanipulation.
   Save these for last — they're the most work, but also the most distinctively
   DS, so they're worth the careful effort.

## Hand-decompile workflow (for DS-custom abilities)

For each function, repeat:

1. `objdump -d -j .text --no-show-raw-insn act_combat.o | sed -n '/<NAME>/,/^$/p'`
   Pull just that function's disassembly.
2. Cross-reference `.rel.text` to identify which call sites resolve to which
   helpers (`act`, `damage`, `send_to_char`, etc.).
3. Pull all `.rodata` strings the function uses — these give you the exact
   player-facing message text.
4. Translate stack frames into C locals. Track which fields of `CHAR_DATA`
   are accessed at which offsets (e.g., `0x5c` is `ch->pcdata`, `0xf0` is
   `ch->position`, etc.). We'll build a struct-offset cheat sheet from `merc.h`
   once we hit our first decompile.
5. Compare behaviour against the wiki spec at http://dsmud.wikidot.com/.
6. Compile, deploy (with copyover if/when we have it), playtest.

## Notes

- The 2003 deployed binary `recovered/devils/bin/ds` is **stripped** — `nm`
  returns no `do_*` symbols. So the previously-planned 'cross-reference the
  binary disasm' fallback isn't trivially available. The `.o` file is the
  much better source anyway — it has both symbols and clean disasm.
- `do_remort` is in `act_comm.c`, not `act_combat.c` — already neutralized per
  Session State Known Issue #2.
- `do_reroll` is also outside this catalog. Treat as suspect until tested.
