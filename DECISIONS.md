# DS:R Design Decisions

Permanent record of decisions made with rationale. Add here when a
non-obvious call is made so we don't re-litigate it. Reference when
a related question comes up.

Format:
```
### DECISION-NNN: Title
**Date:** YYYY-MM-DD
**Decision:** What was decided.
**Rationale:** Why.
**Affected files / systems:** Where this shows up in code.
```

---

### DECISION-001: do_forge / do_katana — full spec
**Date:** 2026-04-29 (updated 2026-04-29)
**Decision:**
- **Class gate:** Ninja family only — ninja (tier 1), assassin (tier 2), kensai (tier 3).
  Confirmed via skill groups 12/30/50 in const.c, and helpfile SKILL_FORGE_KATANA.
  Helpfile text: "Ninjas and Assassins have the ability to forge katana blades out
  of bars of adamantite."
- **Syntax:** `forge bar katana` → outputs katana. `forge bar wakizashi` → outputs wakizashi.
  Two distinct outputs from the same do_forge dispatcher, branching on arg2.
- **Material vnum:** solennir #8111 (`a bar of adamantite`, type 38 ITEM_FORGE_STONE).
  Shop wired: solennir #8018 apprentice weaponsmith stocks type 38.
- **Output vnums:** katana = #8123 (already exists in solennir.are, weapon type katana,
  10d20 slice). Wakizashi = **#8130** (available, needs object entry added to solennir.are).
- **Mana costs:** 300 HIT / 250 MISS (disasm values, keep).
- **Stats:** +level/3 HR and DR on the forged weapon.
**Rationale:** Original disasm vnums 1313/3724 don't exist in area files. #8111 is the
only ITEM_FORGE_STONE in recovered areas. #8123 already templated as katana. #8130 is
next available open vnum in solennir object range.
**Affected:** do_forge, do_katana, solennir.are (add #8130 wakizashi object, #8018 shop).

---

### DECISION-002: Class indices (monk and gladiator families)
**Date:** 2026-04-29
**Decision:** Verified global class_table indices from `//N` comments
in const.c and skill group array positions:
- Monk family: monk=8, shaolin=26, sensei=44
- Gladiator family: warrior=3, gladiator=21, knight=39
- Progression: warrior→gladiator→knight (tier 1→2→3)
**Rationale:** Earlier sessions had wrong values (18/36/54 and 13/31/49).
Corrected by direct source inspection. Skill group 54-element arrays
confirm: position 8 per tier = monk archetype.
**Affected:** do_stance, do_chaos_blow (monk gate), do_shield_smash
(gladiator stun bonus).

---

### DECISION-003: Monk/Shaolin/Sensei valid flag
**Date:** 2026-04-29
**Decision:** Set `valid=TRUE` for all three. Skills are fully populated
(73 skills across all three tiers). Sensei has exclusive tier-3 skills
(polearm, bladebarrier, spell groups).
**Rationale:** Classes were flagged `valid=FALSE` at original shutdown —
unfinished marker, not a balance decision. Skills were already complete.
**Affected:** const.c lines 2644 (monk), 2800 (shaolin), 2963 (sensei).

---

### DECISION-004: Re-enable push / drag / chameleon / grow arms
**Date:** 2026-04-29
**Decision:** Removed from disabled.txt. fight.c WEAR_THIRD/FOURTH
uncomment queued for Code.
**Rationale:** All four have complete implementations. push/drag have
safe-room gating (`is_safe_push`) — cannot be used to force players
into or out of safe zones. grow arms requires level 80+ and is a
morpheous-class ability gating WEAR_THIRD/FOURTH slots.
polymorph stays disabled (imm-only, L7 trust, already gated in
interp.c).
**Affected:** data/misc/disabled.txt, fight.c ~L695 (uncomment).

---

### DECISION-005: AQ veteran gear at 100 AQP
**Date:** 2026-04-29
**Decision:** 17 veteran gear pieces added to AQ reward_table at 100
AQP each. Covers all major wear slots. Gear selected from existing
high-stat items in the area files.
**Rationale:** Players need a baseline path back to competitive gear
after dying/looting without having to re-farm hero areas. 100 AQP is
accessible but not trivial.
**Affected:** recovered/devils/src/quest.c reward_table (L45–69).

---

### DECISION-006: PVP economy system — Grace + Souls + Essence
**Date:** 2026-04-29
**Decision:** POST-RESTORATION feature. Full design in VISION_PVP_ECONOMY.md.
Do not implement until core class restoration, skill ports, and stability
are complete. Design is settled in principle — do not re-litigate the loop.
**Summary:** Three archetypes (Default / Essence farmer / Soul collector).
Essence earned from mobs → Grace buffer (TTK + lootable). Souls earned from
PK kills → clan Essence multiplier on kill + personal vendor access.
No stat inflation for PVP players. Balance stays tractable.
**Rationale:** Original opt-in PK design superseded by full economy vision.
**Affected:** fight.c, handler.c, db.c, clan system, new vendor NPC — Phase 2.

---

### DECISION-007: do_assassinate PK-room carve-out
**Date:** 2026-04-29
**Decision:** No general exception to safe room rules in normal game world.
The 2003 carve-out was likely scoped to the chaos/team arena room only
(the room where backstab was enabled during arena events). Imm-level
bypass may have existed but is not confirmed. Current port (plain pktimer
brake, no bypass) is correct for the open world. Revisit only if arena
room needs it explicitly wired.
**Rationale:** Kyle: "in the normal game world I don't think there's ever
an exception to the safe room rule."
**Affected:** do_assassinate DEGRADED #1. Low priority.

---

### DECISION-008: do_shield_smash AC divisor
**Date:** 2026-04-29
**Decision:** Use disasm value (~`/80`), not port's current `/20`.
**Rationale:** Always defer to disasm. High AC should meaningfully counter
a shield smash — `/20` lands too easily on tanky targets, `/80` matches
original intent. Kyle: "that makes sense, high AC would help you counter it."
**Affected:** do_shield_smash in act_combat.c. Code to apply next pass.

---

### DECISION-009: voodoo_throw room restriction
**Date:** 2026-04-29
**Decision:** Keep the room restriction. Use ROOM_NO_TELEPORT OR add an
explicit safe-room check — whichever is tighter. Do NOT allow throwing
players out of safe rooms.
**Rationale:** The feature was disabled originally because players used it
to throw AFK players out of safe, exposing them to PK. Kyle confirmed this.
**Affected:** voodoo_throw in act_combat.c. Add `IS_SAFE(ch, victim)` style
check on destination room before executing the throw.

---

### DECISION-010: 0x16c victim alert flag family
**Date:** 2026-04-29
**Decision:** Defer. Let BUG-008 (wary flag rebuild) land first.
**Rationale:** Kyle: likely position-based (sitting/tripped) OR the wary
flag. The wary fix will probably resolve the most visible cases. If skills
still feel off after BUG-008, revisit with fresh disasm comparison.
**Affected:** do_throw, do_assassinate, do_shield_smash DEGRADED notes.

---

### DECISION-011: 0x2f8 HASTE modifier in jab/throw/blinding_strike
**Date:** 2026-04-29
**Decision:** Treat as a HASTE success rate bonus — same mechanic as how
dirt kick boosts disarm/trip success. Current ports only implement AFF_HASTE
half of the disjunction. Acceptable for now; revisit if haste characters
feel no benefit on these skills during QA.
**Rationale:** Kyle: "sounds like it was a success modifier for those skills
just like disarm or trip might be dirt kick."
**Affected:** do_jab, do_throw, do_blinding_strike DEGRADED notes.

---

### DECISION-012: Lootability scope in Grace/Souls economy
**Date:** 2026-04-29
**Decision:** Only opted-in players (Grace farmers and Soul Collectors) are lootable. Default (unflagged) players cannot be looted under any circumstances — they simply lose their Essence stack on death. No items change hands for Default players. Grace-flagged players are lootable on death (they opted into the risk). Soul Collectors are lootable by other Soul Collectors on death.
**Rationale:** Kyle: "lootability for anyone not flagged PK/PVP on the chaos side cannot be looted they just lose essence." Keeps the safe floor genuinely safe — Default players face zero item loss risk. Loot risk is always a voluntary choice made by opting into the economy.
**Affected:** VISION_PVP_ECONOMY.md, fight.c death handler, IS_GRACE / IS_SOUL flags.

---

### DECISION-013: Paradox suspends Grace defensive bonuses
**Date:** 2026-04-29
**Decision:** When a Paradox event is active, Alecca's Grace damage reduction modifier is fully suspended for all players. Everyone fights at normal TTK during Paradox. Grace stacks are preserved — they just don't apply. Bonus resumes when Paradox ends.
**Rationale:** Kyle: "everyone should be killable in a Paradox." Paradox is an intentional world escalation — a moment where the rules shift and no one is safe. Grace protecting players during Paradox would undermine that. This is also the answer to the open question in VISION_PVP_ECONOMY.md #7.
**Affected:** Grace damage modifier in fight.c — add `if (IS_PARADOX_ACTIVE(world)) skip grace calc`. BUG-021 (Paradox not ticking) must be fixed first.
