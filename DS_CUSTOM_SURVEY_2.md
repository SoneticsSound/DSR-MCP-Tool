# DS-Custom Mid-Tier Survey (560–700 byte band)

**Generated 2026-04-26** in Claude Code from a static survey of `act_combat.o`.
Eight unported functions in the 568–680 byte range; the band excludes the
already-ported neighbours (`do_kick` 569b, `do_circle` 638b, `do_berserk`
661b, `do_rescue` 673b, `do_garotte` 560b, `disarm()` helper 567b).

Same methodology as `DS_CUSTOM_SURVEY.md`: `readelf -s` for sizes,
`readelf -r` for helper / gsn / string references, no disasm
interpretation beyond what extraction reveals.

## Quick-glance table

| Function | Size | Cluster | Brief |
|---|---:|---|---|
| `do_quickening`     | 568 | STRIP            | anti-cripple buff; strips `gsn_cripple`, applies haste-style affect |
| `do_caltrops`       | 585 | STRIKE-AFFECT    | drop spikes, deal damage + apply `AFF2_LIMPING` to victim |
| `do_healing_touch`  | 598 | UTILITY-TARGET   | heal another char; `dice` roll, `update_pos` to revive |
| `do_storm`          | 610 | STRIKE-PURE      | "storm of blades" — AOE swing, requires Dance state |
| `do_dislodge`       | 631 | STRIKE-DISARM    | knock victim's SHIELD off (DS-specific anti-shield variant of do_disarm) |
| `do_powerblind`     | 641 | STRIKE-DEBUFF    | power-word blind, paired with do_powerstun / do_powersilence |
| `do_strike`         | 660 | STRIKE-PURE      | single-target weapon strike; `multi_hit` flavour, gsn_rift gate |
| `do_gore`           | 680 | STRIKE-PURE      | race-locked horns attack; self-stun on miss |

## Cluster carry-over from Survey 1

These functions extend or fit into clusters already established in the
first survey — port templates can be reused:

- **STRIKE-PURE**: do_storm, do_strike, do_gore join the cluster anchored
  by `do_cleave`. All three share the get_skill / weapon-or-arg / rift /
  stunned / can_see / wait-clamp / chance-roll / hit-or-miss skeleton.
  The remaining cluster batch grows from 6 → 9.
- **STRIKE-DEBUFF**: do_powerblind joins the power-word triad with
  do_powerstun + do_powersilence (already surveyed). All three share:
  consume a `gsn_power_word_X` prime via `affect_strip`, target via arg,
  is_safe + check_killtimer, apply effect to victim via `effect_to_char`,
  nameless-race protection (do_powerblind explicitly, the others
  inferred). 4-function batch when ready.
- **STRIP**: do_quickening joins do_deepbreathing / do_rub /
  do_plantroots in the affect-removal cluster. Slightly different shape
  (does both strip AND apply) — closest to do_plantroots's two-stage
  pattern.

## Cluster details

### STRIP — `do_quickening` (568 b)

**gsns referenced**: gsn_quickening, gsn_cripple, gsn_haste

**helpers**: `affect_strip` (cripple removal), `affect_to_char`
(quickening application), `is_affected` ×2 (gate against re-cast +
check for cripple), `skill_lookup` ("inflict pain" — a tier-related
or class-prereq lookup), standard get_skill/get_trust/check_improve.

**Strings preview**:
- `"Quickening? What the fuck is that?"` (skill-not-known fail)
- `"You're still a little woozy.\n\r"` (stunned gate)
- `"{YYou have been crippled!!!{x"` (special-case path — possibly displayed when ch IS crippled and cleansing applies)
- `"You can't move any faster!"` (already-buffed gate)
- `"You feel yourself quicken."` (success self)
- `"$n is moving less slowly."` (success room — wear-off?)
- `"You feel yourself moving more quickly."` (alt success self?)
- `"$n is moving much quicker."` (alt success room)
- `"You failed.\n\r"` (fail)
- `"inflict pain"` (skill_lookup arg, class-related?)

**Structural notes**: Likely two-stage like do_plantroots —
`if (is_affected(ch, gsn_cripple)) affect_strip + early-return-with-cleanse-msg`,
then `if (is_affected(ch, gsn_quickening)) "can't move any faster"`,
then chance roll + apply quickening AFFECT_DATA.

**Anchor candidate**: yes — could be the STRIP-cluster anchor when we
get there. Smaller than do_deepbreathing in helper count, similar
structure.

### STRIKE-AFFECT — `do_caltrops` (585 b)

**gsns referenced**: gsn_caltrops

**helpers**: `damage`, `affect_to_char`, `is_safe`, standard set.

**Strings preview**:
- `"Caltrops? Is that a dance step?"` (skill-not-known)
- `"You must be in combat."` (no-fighting gate)
- `"Their feet aren't on the ground."` (AFF_FLYING gate — same as do_trip)
- `"You're still a little woozy."`
- `"You throw a handful of sharp spikes at the feet of $N."` (success self)
- `"$n throws a handful of sharp spikes at your feet!"` (success vict)
- `"$n starts limping."` ← **identical to do_kick's knee-breaker affect message**
- `"Ouch that hurt! You start limping."` ← **also identical**

**Structural notes**: caltrops applies the SAME `AFF2_LIMPING` affect
that do_kick's knee-breaker secondary uses. The hit path is essentially
the knee-breaker block extracted into its own ability. Damage delivered
via `damage()` (not `one_hit`/`multi_hit`).

**Schema implication**: confirms `AFF2_LIMPING` is the canonical "feet
hurt, can't move well" debuff in DS. When porting, mirror do_kick's
AFFECT_DATA for the limp affect (where=TO_AFFECTS2, location=APPLY_DEX,
modifier=-4, duration=1, bitvector=AFF2_LIMPING).

### UTILITY-TARGET — `do_healing_touch` (598 b)

**gsns referenced**: gsn_healing_touch, gsn_devils_curse

**helpers**: `dice` (healing roll), `update_pos` (revive from dying),
`is_affected` (gsn_devils_curse blocker), `one_argument`, `get_char_room`,
`act`, standard skill set. **No `damage` / `multi_hit` / `one_hit` —
this is healing, not striking.**

**Strings preview**:
- `"Huh?"` (skill-not-known)
- `"They are not here."`
- `"You're still a little woozy."`
- `"Your spirit is too weak."` (mana/move gate)
- `"You focus your energy, and magical sparks leap from your body."` (self-cast self-msg?)
- `"$n concentrates, and magical sparks leap from $s body."` (self-cast room)
- `"You place your hands on $N's head and focus your energy into $M."` (target-cast self)
- `"$n places $s hands on $N's head and concentrates."` (target-cast room)
- `"$n places $s hands on you and concentrates."` (target-cast vict)
- `"You feel better!"` (target post-heal)

**Structural notes**: takes an explicit target via one_argument; if
arg empty, heal self (two distinct message sets — one for self-heal,
one for target-heal). `gsn_devils_curse` blocks healing the cursed
victim. Healing amount via `dice(N, M)` formula. `update_pos(victim)`
to upgrade their position if the heal brought them back from
incap/dying.

**Anchor candidate**: yes — defines a UTILITY-HEAL micro-cluster that
will likely include `do_cleanse` (already in Survey 1 OTHER tier — uses
`check_dispel`).

### STRIKE-PURE — three additions

#### `do_storm` (610 b)

**gsns**: gsn_storm_of_blades

**helpers**: `one_hit`, `is_safe`, `is_same_group` (avoid friendly
fire — AOE iteration over room), `paradox_is_on`, `check_killtimer`.

**Strings preview**:
- `"Huh?"`
- `"You must be in the Dance of the Raging Storm to use this skill."` (precondition: must be in a "dance" state)
- `"You're still a little woozy."`
- `"You can't do that here."` (room-flag gate, probably IS_SAFE)
- `"You are too tired."` (mana/move gate)
- `"Like a raging storm, $n spins around slashing at everybody near him."`
- `"Like a raging storm, you spin around slashing at everybody within reach."`
- `"You failed."`
- `"$n tries to spin like a storm but fails."`

**Structural notes**: AOE attack — iterates the room's CHAR_DATA list,
calls `one_hit(ch, victim, gsn_storm_of_blades, 0)` for each valid
target. `is_same_group` filter to skip group members. Precondition:
must be in "Dance of the Raging Storm" — likely `is_affected(ch,
gsn_dance_X)` or a `pcdata->dance` field check.

**New schema implication**: AOE-iterate-room pattern. First STRIKE-PURE
that hits multiple targets per call. Will need to confirm the room
iteration idiom (`for (vch = ch->in_room->people; vch != NULL;
vch = vch->next_in_room)` is stock ROM).

#### `do_strike` (660 b)

**gsns**: gsn_strike, gsn_rift

**helpers**: `multi_hit` (HIT path damage), `damage` (MISS path msg),
`get_eq_char`, `can_see`, `is_gangbanger`, `is_affected` (rift +
HP-fraction calc), standard set.

**Strings preview** — full STRIKE-PURE message kit:
- `"You strike a pose."` (skill-not-known)
- `"You must be fighting someone to strike."` (no-fighting)
- `"You'll need a weapon to strike with."` (weapon check)
- `"A magical rift prevents you from attacking $N!"` (rift)
- `"$N is hurt and suspicious ... you can't sneak around."` ← **same string as do_circle's HP-fraction gate**
- `"You're still a little woozy."`
- `"It's not possible to strike when you can't see."` (blind)
- `"{i$n strikes hard and fast.{x"` / `"{hYou strike $N with speed and power.{x"` / `"{k$n strikes $N fast and hard.{x"` (HIT trio)
- `"{i$n strikes, but you easily avoid it.{x"` / `"{h$N avoids your quick strike, $e's quicker than you!{x"` / `"{k$N easily avoids $n strike.{x"` (alert MISS trio)
- `"{i$n strikes, but you dodge just in time.{x"` / `"{h$N dodges your quick strike!{x"` / `"{k$n strikes at $N, but misses.{x"` (standard MISS trio)

**Structural notes**: closest sibling to `do_cleave` in shape — same
gates (skill / fighting / weapon / rift / hurt-suspicious /
woozy / can_see / wait-clamp / alert-flag), same alert-vs-standard
miss-message variant. **Differences**:
- HIT path uses `multi_hit(ch, victim, gsn_strike)` — full melee round —
  vs cleave's `one_hit` single-swing.
- Includes the HP-fraction "hurt and suspicious" gate that cleave skips
  (this is a do_circle / do_backstab borrowing).
- Includes `is_gangbanger` chance modifier (cleave didn't have it).

**Strong candidate for second STRIKE-PURE batch member** — minor
divergences from cleave, mostly mechanical.

#### `do_gore` (680 b)

**gsns**: gsn_gore

**helpers**: `damage`, `is_safe`, `check_killtimer`, `number_range`,
`get_char_room` (explicit arg target), standard set.

**Strings preview**:
- `"Grow some horns first."` (skill-not-known — race-locked)
- `"But you aren't fighting anyone!"` / `"They aren't here."`
- `"You blindly wave your horns about."` (no-target/blind variant?)
- `"You're still a little woozy."`
- `"I don't think you really want to gore yourself."` (self-target)
- `"You are stunned, and have trouble getting back up!"` ← **same as do_bash's stun message**
- `"$N is stunned by your gore."` / `"$N is having trouble getting back up."`
- `"$n falls over trying to gore $N and stuns $mself."` ← **self-stun on miss**
- `"You fall over and stun yourself."`

**Structural notes**: race-locked (the get_skill 0 message implies a
horn-having race like minotaur). Explicit-target verb (uses
`one_argument` + `get_char_room`). On hit: damage roll with possible
stun secondary (re-uses do_bash's stun affect). On miss: ch self-stuns
("falls over"). Has `check_killtimer` — PvP gate.

**Notable**: this is the **first STRIKE-PURE that can self-affect on
miss** — the falls-over stun applies to ch, not victim. New variability
point for the cluster template.

### STRIKE-DISARM — `do_dislodge` (631 b)

**gsns**: gsn_dislodge, gsn_hand_to_hand

**helpers**: `get_eq_char` ×2 (own weapon + victim's shield), `obj_from_char`,
`obj_to_room` (drop the shield), `get_curr_stat` (probably STR for the
dislodge roll), standard set. **No affect, no damage helper** — this
is purely "remove an item from a slot."

**Strings preview**:
- `"You haven't a clue how to do that."` (skill-not-known)
- `"You must wield a weapon to knock away their shield."` (weapon req)
- `"You aren't fighting anyone."`
- `"You're still a little woozy."`
- `"Your opponent is not using a shield.{x"` (no-shield gate)
- `"Try as you might, $S shield will not budge."` (NOREMOVE block — same as disarm helper's "stuck weapon")
- `"$n tries to dislodge your shield but you have a firm hold."` (vict-side fail)
- `"$n tries to dislodge $N's shield but fails."` (room-side fail)
- `"{Y$n sends your shield flying from your hands, crashing to the floor.{x"` (vict success)
- `"{YYou send $N's shield flying.{x"` (self success)
- `"{Y$n sends $N's shield flying to the ground.{x"` (room success)
- `"You fail to dislodge $N's shield."` (alt fail)
- `"$n tries to dislodge your shield but fails."` (alt vict fail)

**Structural notes**: parallel to `do_disarm` + the lowercase `disarm()`
helper, but for `WEAR_SHIELD` (=11) instead of `WEAR_WIELD` (=16). The
internal mechanics likely mirror disarm(): yank the shield via
`obj_from_char`, drop to room via `obj_to_room`, with NOREMOVE bypass
("won't budge") and the same auto-pickup-by-NPC logic.

**Anchor candidate**: yes for a STRIKE-DISARM micro-cluster. Probably
won't have a 7-function batch behind it; might be a one-off.

### STRIKE-DEBUFF — `do_powerblind` (641 b)

**gsns**: gsn_power_word_blind, gsn_powerblind

**helpers**: `affect_strip` (consume the prime), `effect_to_char`
(apply blind to victim), `is_safe`, `check_killtimer`, `is_affected`
(prime check + already-blind check), `race_lookup`, `damage`, `number_range`.

**Strings preview**:
- `"Huh?"`
- `"You're still a little woozy."`
- `"You must store that power word first."` (no prime)
- `"But you aren't fighting anyone!"` / `"They aren't here."`
- `"nameless"` (race_lookup arg — same nameless-race protection as gouge/dirt)
- `"$n is unaffected by power word blind."` / `"You are unaffected by power word blind."`
- `"Thats not wise."` (self-target?)
- `"You utter a word of power."` / `"$n utters a word of power."`
- `"$N is blinded."` ×2 (TO_CHAR + TO_NOTVICT?)
- `"You are blinded."` (TO_VICT)
- `"{rThe strain of using the power word weakens you{x."` (post-cast self-message — strain damage to ch)

**Structural notes**: completes the power-word triad. Same structural
shape as do_powerstun + do_powersilence (Survey 1 STRIKE-DEBUFF
cluster). Adds: `damage(ch, ?, dam, ...)` for the post-cast strain
weakening — applies a small damage to ch as cost. Triad anchor when
we port this cluster.

## New helpers / references seen for the first time

| Helper / global | First-seen in | Notes |
|---|---|---|
| `update_pos`            | do_healing_touch | Already in DS_SCHEMA helper table — `void update_pos(CHAR_DATA *victim)`. ✓ |
| `dice(N, M)`            | do_healing_touch | Already in schema. ✓ |
| `is_same_group`         | do_storm         | Already used in do_rescue — `bool is_same_group(CHAR_DATA *, CHAR_DATA *)`. ✓ |
| `is_gangbanger`         | do_strike        | Already used in BUFF-SELF / STRIKE-PURE batches. ✓ |
| `gsn_storm_of_blades`   | do_storm         | NEW. Verify in gsn.h. |
| `gsn_quickening`        | do_quickening    | NEW. Verify in gsn.h. |
| `gsn_cripple`           | do_quickening    | NEW. Verify in gsn.h. |
| `gsn_devils_curse`      | do_healing_touch | NEW (also referenced in act_wiz.c per earlier grep). Verify gsn.h. |
| `gsn_caltrops`          | do_caltrops      | NEW. |
| `gsn_dislodge`          | do_dislodge      | NEW. |
| `gsn_strike`            | do_strike        | NEW. |
| `gsn_gore`              | do_gore          | NEW. |

No fundamentally new helper signatures uncovered — this band sticks to
the same call surface as Survey 1.

## New schema deltas implied by the survey

(To be confirmed during the actual ports; flagging here so future-Cowork
and future-Code don't re-derive.)

1. **`AFF2_LIMPING` is the canonical limp debuff** — used by both
   `do_kick`'s knee-breaker AND `do_caltrops`. Same AFFECT_DATA shape:
   `where=TO_AFFECTS2, type=gsn_X, location=APPLY_DEX, modifier=-4,
   duration=1, bitvector=AFF2_LIMPING`. Likely also re-used by other
   leg-targeted verbs we haven't surveyed yet.
2. **AOE iteration via room → people list** — first appears in
   `do_storm`. Stock-ROM idiom: `for (vch = ch->in_room->people;
   vch != NULL; vch = vch_next) { vch_next = vch->next_in_room; ... }`.
   Worth a schema note when porting do_storm.
3. **Self-stun-on-miss pattern** — `do_gore` applies stun to CH (not
   victim) when the chance roll fails. Similar mechanic exists in
   `do_bash`'s self-fall path but bash uses position-change, not stun.
   New variability point for STRIKE-PURE template.
4. **"Strain damage" post-cast pattern** — `do_powerblind` deals a
   small `damage(ch, ch, ...)` to the caster after a successful blind,
   with a "weakens you" message. New pattern for STRIKE-DEBUFF cluster
   — verify do_powerstun / do_powersilence have it too.
5. **Two-stage strip-then-buff** — `do_quickening` removes
   `gsn_cripple` if present (returning a cleanse-flavour message),
   then applies `gsn_quickening` AFFECT. Same shape as do_plantroots.

## Recommended porting order

After the current STRIKE-PURE batch (do_dhammer, do_stomp, do_cross_slash,
do_whirlwind, do_legsweep, do_garotte from Survey 1) lands:

1. **STRIKE-PURE batch extension**: add `do_strike` and `do_gore` to
   the cluster batch. They share ~95% of cleave's structure with two
   small variability bumps (HP-fraction gate, self-stun-on-miss).
2. **`do_caltrops`** standalone (STRIKE-AFFECT, single — can re-use
   the do_kick knee-breaker AFFECT_DATA pattern verbatim).
3. **STRIKE-DISARM**: `do_dislodge` standalone (mirror of disarm()
   helper; likely a clean copy-and-modify).
4. **STRIKE-DEBUFF (power-word triad)**: anchor `do_powerinvuln` (from
   Survey 1 — already classified as STRIKE-DEBUFF self-variant), then
   batch do_powerstun + do_powersilence + **do_powerblind**.
5. **STRIP additions**: extend the STRIP cluster (do_deepbreathing
   anchor planned in Survey 1) with `do_quickening` as a second entry.
6. **UTILITY-HEAL micro-cluster**: anchor `do_healing_touch` (598b),
   then revisit Survey 1's `do_cleanse` (uses `check_dispel`).
7. **AOE pioneer**: `do_storm` standalone — first AOE in the project,
   establishes the room-iteration idiom for future psionics / area
   spells.

## Survey-2 functions NOT in this band (for awareness)

The catalog has additional unported functions just outside the 560–700
window that may be worth surveying next:

- 701b `do_transfix`
- 704b `do_thousand_wounds`
- 748b `do_gash` / `do_katana`
- 771b `do_eadbutt`
- 776b `do_devils_touch`
- 797b `do_earthbind`
- 801b `do_scream`
- 812b `do_shuriken`
- 813b `do_feed`
- 814b `voodoo_throw`

These cross into the 700–820 band — a third survey may be appropriate
when the current backlog clears.
