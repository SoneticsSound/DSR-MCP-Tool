# DS:R Balance Notes
**Source:** Derived from 155 player files + 293 boot logs (Nov 2002 – Oct 2003)
**Hero sample:** 80 level-101 characters across 16 classes
**Last updated:** 2026-04-29

---

## Hero DPS Estimates

Methodology: `attacks_per_round × (avg_damroll + 40)` where 40 approximates a
standard hero-tier weapon base. Hitroll is directional only — the MUD's to-hit
formula is not fully reconstructed. Rankings are relative, not absolute damage values.

| Class      | N  | Avg Atk | Max Atk | Avg HR | Avg DR | Est DPS | Flag      |
|------------|:--:|--------:|--------:|-------:|-------:|--------:|-----------|
| Paladin    | 3  | 7.0     | 7       | 856    | 858    | 6,290   | ⚠️ HIGH   |
| Wardancer  | 7  | 9.0     | 9       | 724    | 610    | 5,853   | ⚠️ HIGH   |
| Knight     | 7  | 8.0     | 8       | 669    | 665    | 5,639   | ✅ OK     |
| Blade      | 17 | 6.2     | 9       | 623    | 658    | 4,309   | ✅ OK     |
| Bishop     | 4  | 5.0     | 5       | 646    | 642    | 3,408   | ✅ OK     |
| Battlemage | 9  | 4.0     | 4       | 580    | 650    | 2,758   | ⚠️ LOW   |
| Elder      | 3  | 6.0     | 6       | 343    | 355    | 2,370   | —         |
| Alchemist  | 8  | 4.0     | 4       | 414    | 411    | 1,803   | —         |
| Seer       | 5  | 3.0     | 3       | 520    | 518    | 1,674   | —         |
| Mage       | 5  | 6.2     | 9       | 119    | 108    | 920     | (outlier) |
| Sorcerer   | 7  | 2.6     | 3       | 321    | 314    | 911     | —         |

> Mage 6.2 avg attacks is skewed by 3 players who trained full melee skill sets.
> True caster mage is 2 attacks. Sorcerer and mage are primarily spell DPS classes.

---

## Balance Flags

### ⚠️ WARDANCER — Attack count ceiling
- **Issue:** 9 attacks per round (highest in game) combined with mist dance evasion
  and cross slash. The dodge layer stacks on top of a very high offensive ceiling.
- **Community signal:** Multiple ideas board posts (Sep–Oct 2003) from experienced
  players (Locke with 800 hit/dam, not landing attacks; Drizzt saying wardancers
  "easy" as blade but hard as other classes).
- **Data:** 7 hero wardancers, 9.0 avg attacks, 610 avg DR. Cross slash trained to
  100% by only 4/12 wardancers total — the level 53 gate was a real friction point.
- **Suggested tweak:** Cap attack chain at 7 for wardancer tier, or require cross slash
  to be trained to use the 7th/8th attack slot. Alternatively, tie mist dance activation
  to a stamina/cooldown mechanic to reduce stacking with high attack count.

### ⚠️ PALADIN — DPS unexpectedly high
- **Issue:** 7 avg attacks + 858 avg damroll puts paladin above knight in raw DPS.
  If cleave fires independently of the attack chain (not counted above), actual output
  is higher still.
- **Data:** Only 3 hero paladins in sample — small n, but numbers are consistent.
  All 3 had enhanced damage maxed, dirt kicking maxed, 4th/5th attack maxed.
- **Suggested tweak:** Verify whether cleave is additive to or replacing an attack in
  the chain. If additive, consider capping paladin at 6 base attacks or reducing
  cleave trigger rate.

### ⚠️ BATTLEMAGE — Attack ceiling too low for DR investment
- **Issue:** Highest average damroll (650) of any class but hard-capped at 4 attacks
  (second + third + dual wield). Results in 2,758 est DPS — less than bishop (3,408)
  despite far higher per-hit damage. Players feel strong in burst, weak sustained.
- **Community signal:** Ideas board: Synistor proposed a battlemage-exclusive buff
  spell (+25 HR/+25 DR); Einon noted battlemagic spells do same damage as combat
  group spells (no differentiation).
- **Suggested tweak:** Allow battlemage access to fourth attack at a high level (95+),
  OR give battlemagic spells a damage premium over combat group spells to reward the
  spell investment. Keep melee at 4 attacks but make each hit matter more.

### ⚠️ BISHOP — Sever creating non-interactive fights
- **Issue:** Sever was so feared that players refused to fight bishops at all.
  Bishop has solid melee (5 attacks, 642 DR) but their win condition being "land sever
  and they can't cast" created binary fight outcomes.
- **Community signal:** Trakanon (a hero bishop) explicitly posted asking for sever to
  be replaced because "no one will fight a bishop."
- **Suggested tweak:** Give sever a duration cap or a resist check based on target's
  WIS/INT, or add a counter mechanic (item, skill, or timer) that lets targets break
  sever after N rounds.

### ⚠️ SEER — Timestop abuse in no-exit rooms
- **Issue:** Timestop spam in rooms with no exits was described as "totally impossible
  to kill" — tstop, deaden, quaff, tstop again before lockout expired.
- **Community signal:** Drizzt (hero seer player himself) flagged this on the ideas
  board, suggesting the no-cast lockout window needs to be significantly extended.
- **Suggested tweak:** Double the no-recast window on timestop, OR add a room flag
  that prevents consecutive timestop casts in the same room within N ticks.

---

## Universal Hero Skill Floor

Skills trained to 100% by 60%+ of all 80 hero characters — these are effectively
mandatory for any competitive build:

| Skill         | Maxed | Total |
|---------------|------:|------:|
| Dual Wield    | 48    | 80    |
| Second Attack | 48    | 80    |
| Parry         | 48    | 80    |
| Dodge         | 47    | 80    |

**Next tier (40–50%):** Third attack (36), fourth attack (34), enhanced damage (27),
shield block (26), dirt kicking (20).

**Class-specific threshold (10–20%):** Circle (16), trip (16), bash (15), sixth attack (16).

---

## Per-Class Skill Tendencies (Hero Tier)

### Blade (n=17)
- Circle maxed: 10/17. Dual wield: 15/17. 4th + 5th attack: 10/17.
- Most consistent multi-attack class with circle as the primary finisher.
- Earthbind showing up (2/17) suggests some blades were experimenting with utility.
- **Gap:** Enhanced damage only 1/17 — blades skipped it in favor of circle.

### Knight (n=7)
- Enhanced damage maxed: all 9/9 battlemages + 9/13 knights — the defining passive.
- Bash maxed: 7/13. Dual wield: 7/13. 6th + 7th attack: 4/13.
- Knights had the deepest attack chains of any "reliable" class after wardancer.
- Shield smash only 2/13 — either hard to land or not worth the investment.

### Wardancer (n=7)
- Cross slash maxed: 4/12 across all wardancers, even fewer at hero tier.
- Devils touch + counterattack + dislodge showing up — wardancers had the most
  diverse skill spread of any class.
- **Flag:** Attack chain inconsistency — some wardancers at 9 attacks, others at 6.
  The 7th/8th attack skills are not universally trained even at hero level.

### Battlemage (n=9)
- Most uniform build of any class: all 9 had dual wield + enhanced damage at 100%.
- 6/9 maxed second + third attack, parry, and dodge. Cookie-cutter build, no variance.
- **Design note:** Lack of build diversity suggests battlemage has one optimal path
  with no meaningful choices. Consider adding a second viable build direction.

### Sorcerer (n=7)
- Melee investment: 2/7 maxed second attack, 1/7 maxed third. Primarily casters.
- No combat damage skills maxed. Winning via spells not tracked in player files.

### Paladin (n=3, small sample)
- Dirt kicking: 4/5 maxed across all paladins. Trip: 3/3. Disarm: 3/4.
- Heavy utility skill investment alongside high attack count — all-rounder profile.
- **Note:** Small sample, treat DPS ranking with caution until more data available.

---

## Weapon Meta (Hero Tier)

Most wielded weapons at hero tier were daggers and kris-type:
- `#5362` Assassination Kris — 4 heroes
- `#32858` Daggerblast — 4 heroes
- `#5369` Shard Glass — 3 heroes
- `#12808` Martyr's Sting — 3 heroes
- `#33540` Deadly Silver Claw — 3 heroes

Predominantly pierce/slash weapons, which synergize with backstab and circle
(blade mechanics). Suggests the competitive meta weapon type was daggers.

**Implication for forge/crafting economy:** If players are crafting weapons,
daggers and kris-types should be supported in the adamantite forge output.
Currently `do_forge` / `do_katana` outputs to #8123 — verify that covers
dagger types, not just sword/axe.

---

## Community-Sourced Balance Requests (Ideas Board, Sep–Oct 2003)

These are direct player requests — high signal since they came from active heroes:

- **Wardancer dodges:** Locke (800 hit/dam, hitting 7/many attacks) — reduce
  mist dance stacking or add diminishing returns on dodge chains.
- **Blades:** Malacoda proposed removing critical hit from blades, restoring
  enhanced damage, making critical hit a QEQ upgrade. Worth considering.
- **Fabricate (battlemage):** Vorlax suggested skill-% based quality variance.
  Low % = below-average weapon, high % = above-average. Adds build investment value.
- **Cross slash level gate:** Geryon flagged level 53 as too late for wardancers'
  defining skill. Consider moving to level 40–45.
- **Alchemist inventory:** Kelvix — 4 scroll types × 10–20 each + orbs + wands
  leaves no room for potions. Consider a separate scroll/wand pouch slot or
  reducing alchemist default inventory to 125 (from ~170) to force prioritization.
- **Dissolving arrow (sorcerer):** Draccon flagged -50 AC per hit as too strong
  combined with its damage. Consider separating: either reduce AC penalty or
  reduce damage, not both at hero-tier values.

---

## Notes on Data Limitations

- Hitroll and damroll from player files are the stored base values — active buffs
  (haste, bless, strength spells) would add significantly on top.
- DPS estimate does not account for spell damage (sorcerer, seer, mage) which
  is their primary win condition.
- Paladin and elder have small samples (3 each) — treat their rankings as directional.
- Some player files have duplicate skill entries; parser takes the highest value seen.
- PK records (Wind/Killed fields) were all 0 — the registered PK system stored
  records separately and that data is not in the player files.
