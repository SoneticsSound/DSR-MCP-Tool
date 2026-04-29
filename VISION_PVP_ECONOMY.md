# DS:R — PVP & Economy Vision
**Status:** POST-RESTORATION — do not implement until core revival is stable
**Priority:** Major feature, Phase 2 or later
**Author:** Kyle Webb + session notes, 2026-04-29

---

## The Loop (Canonical Summary)

```
MOB KILLS → Essence
Essence   → Grace buffer (% damage reduction on top of Sanctuary)
Grace     → High TTK, makes you lootable, decays on 8hr played-time idle

INITIATE COMBAT (as Grace player) → costs Grace (15% chunk)
DOGPILE a fight (as Grace player) → costs Grace (50% of current)
BEING ATTACKED                    → costs nothing

KILL a flagged/Grace player       → victim loses their Essence stack
                                    killer's clan gains MULTIPLIED Essence
                                    (victim loses 100, killer clan gains 300-500)
                                    multiplier scales with killer's Souls count
                                    + Souls (personal, yours to keep)
                                    + loot rights on corpse

Essence (clan pool) → clan guards, room upgrades, exclusive clan items
Souls               → personal vendor: gear, consumables, items

PVP players are full strength baseline. Souls buys access, not power.
No stat inflation. No snowball. Balance stays tractable.
```

---

## Core Philosophy

Three player archetypes coexist without forcing anyone into a playstyle they don't
want. Risk is always a choice. The economy ties them together so each archetype
benefits from the others existing, rather than being in pure conflict.

---

## The Three Archetypes

### 1. Default (No Flag)
- Fights freely, kills mobs, does quests
- **Cannot be looted. Cannot loot.**
- Earns no special currency from PVP or farming
- Normal sanctuary, normal character — just plays the game
- No registration required. No timer. No decay.
- The on-ramp. New players, casuals, alts. Safe floor.

### 2. Essence Farmer (PVE Path)
- Opts into the Essence system (command TBD: `essence on`?)
- Earns **Essence** from killing mobs
  - Scaled by mob HP total (hard mobs = more Essence per kill)
  - Diminishing returns on grey/trivial mobs to prevent farming low zones
- Essence decays on a timer — must keep farming to maintain their stack
  - "Alecca's Grace" requires continuous tribute from the world
  - Think of it as a heartbeat tax: stop killing, protection fades
- Essence provides a **% damage reduction modifier on top of Sanctuary**
  - More Essence stacked = stronger Grace modifier (cap TBD, maybe +15% DR max)
  - Runs out: Sanctuary returns to normal, no extra protection
  - Grace modifier visible in score/affects as `Alecca's Grace [████░░]`
- **Can be looted** while Grace is active (they've opted into risk for the reward)
- Grace-active players are flagged visibly so PVP players can identify them
- Clan members in the same clan can see each other's Grace stacks (escort incentive)

### 3. Soul Collector (PVP Path)
- Opts into the Souls system (PK flag: `pkflag on`)
- Earns **Souls** from:
  - High value: landing the killing blow on a flagged/Grace player
  - Low modifier: damage dealt to flagged players (per-tick accumulation)
  - (Souls cannot be farmed from Default players — no reward for ganking casuals)
- Can **loot** Grace-flagged players on kill
- Can **be looted** by other Soul collectors on death
- Buys exclusive gear or QEQ upgrades from a Souls-only vendor
- PK flag stays active for N minutes after last combat with a flagged player
  - Prevents flag-drop to escape pursuit mid-fight (original DS pktimer mechanic)

---

## Grace and Combat — What Costs Grace

Grace is drained by **choice**, not by circumstance. The rule is simple:

| Situation | Grace cost |
|-----------|-----------|
| Being attacked (you're the target) | None |
| A clanmate initiates combat in your room | None — you just stand there |
| You initiate combat (first offensive action) | Flat chunk (~15% of current Essence) |
| You join an existing fight your clanmate started (dogpile) | Half your current Essence |

**No per-round drain.** Grace is about the decision to fight, not the duration.
Once you've paid the initiation cost, your remaining Grace still protects you
for the rest of that fight. A Grace player who gets jumped keeps their full TTK
advantage — they paid nothing to be attacked.

**Clanmate initiation:** If your clanmate swings first, you're a bystander.
Your Grace is untouched. The moment you throw a hit of your own, you're choosing
violence — that's when the dogpile cost fires. Half current Essence is steep
enough to be meaningful, not so steep that helping a clanmate in a crisis feels
suicidal.

**Two Grace players fighting:** Both pay the initiation cost when they throw
their first hit. Their TTK advantage works on each other, so the fight takes
longer than normal PVP. Both are choosing to erode their own protection.
That's the price of the duel.

---

## Grace as a TTK Mechanic (Not Just a Buff)

Grace is a **communication signal as much as a stat modifier.** A high Grace stack
says to the world: "I am not here to fight." The mechanical consequence is that
killing a Grace player takes significantly longer — giving clanmates time to respond.

This is intentional:
- **High TTK discourages opportunistic ganking.** A PVP player doing the math
  realizes a full-Grace farmer is a long, risky fight with uncertain outcome.
- **It rewards organized PVP.** Killing a Grace player should require coordination —
  a solo attacker burning through a long TTK is exposed the entire time.
- **Double Souls on Grace kill** — when a Soul collector kills a Grace player,
  they earn 2× the normal Souls payout. This keeps the incentive alive. Grace
  farmers are high-value targets, not untouchable ones. High risk, high reward.
- **The chase window extends** — because Grace players are harder to drop, fleeing
  works more often. A Grace farmer who gets jumped has a real chance to run, call
  for help, or survive long enough for a clanmate to arrive. That's the entire
  social dynamic: escort duty is meaningful because the farmer isn't just a
  one-shot on sight.

---

## The Mutual Dependency (Why This Works)

This is the key design question: **what makes PVP players care whether PVE farmers exist?**

Options (not mutually exclusive — pick one or combine):

### Option A: Clan Essence Pool
- Grace Essence farmed by clan members contributes a % to a **clan pool**
- Clan pool funds clan upgrades, guards, or a passive clan-wide bonus
- Soul collectors in the same clan are incentivized to protect their farmers
- Farmers want to be in a strong clan for protection; fighters want active farmers
- Creates genuine clan economy without forcing anyone to do both

### Option B: Essence-to-Souls Conversion (Trade)
- Soul collectors can buy Essence from farmers (platinum or direct trade)
- Essence can boost a temporary damage buff or hitroll modifier for PVP players
  (separate from Sanctuary — call it "World Attunement" or similar)
- Creates a player-driven market: farmers produce, fighters consume
- Risk: could be exploited by the same player farming and fighting on alts

### Option C: Zone Control / Sanctified Ground
- High-Essence zones become "sanctified" — give a passive bonus to all players inside
- Soul collectors want to control or patrol high-value farming zones
- Farmers pull fighters toward dangerous areas naturally (not forced, but incentivized)
- Closest to the The Isle "herd vs predator" dynamic Kyle described
- Requires zone tagging system (simpler than it sounds — flag a room vnum range)

**Recommended starting point:** Option A (Clan Pool) because it uses existing
clan infrastructure, requires the least new code, and creates the natural escort/
protection relationship without needing a market or zone system.

---

## Alecca's Grace — Technical Sketch

```
// Essence stored on character as a decaying integer
// pfile field: Essence <int>

// Decay rate: lose X Essence per tick (real-time tick, ~75 seconds)
// Gain rate: Y * (mob_max_hp / 100) per kill, capped at Z per kill

// Grace modifier applied in damage_modifier():
// if (ch->essence > 0 && IS_AFFECTED(ch, AFF_SANCTUARY))
//     dam = dam * (100 - grace_bonus(ch->essence)) / 100;

// grace_bonus(essence):
//     returns 0–15 based on essence stack (linear or curve TBD)

// Grace flag visible: affects list shows "Alecca's Grace" with bar
// Lootable flag: IS_GRACE(ch) — set when essence > 0 and opted in
```

---

## Souls Currency — Technical Sketch

```
// Souls stored on character: Souls <int>
// No decay — souls are permanent until spent

// Gain on kill:  souls += victim->level * SOUL_KILL_MULT
// Gain on damage: souls += (damage / SOUL_DMG_DIVISOR)
//   (only when victim is Grace or Soul flagged)

// Vendor: special NPC in Solennir (or clan hall)
//   `buy <item> souls` — checks ch->souls balance
//   Items: exclusive weapon flags, QEQ alternatives, cosmetic titles

// Souls display in score: "Souls: 1,247"
```

---

## Death — Essence Transfer

On death, the victim's **full current Essence stack transfers to the killer.**

This is the complete economy loop:

```
Farmer kills mobs → earns Essence → builds Grace buffer (TTK)
Fighter kills farmer → gains victim's Essence + double Souls + loot rights
Fighter spends Essence → clan upgrades, clan items
Fighter spends Souls → personal Chaos buff + exclusive vendor gear
```

**Why full transfer (not partial):**
- Makes the kill meaningful. A full-Grace farmer is a walking Essence piñata —
  high TTK to reach, but worth it.
- Clans now have a direct economic reason to hunt rival clans, not just for
  honor or loot, but to drain their Essence income and redirect it to themselves.
- Protecting your clan's farmers isn't altruism — their Essence feeds your
  clan's upgrade pool. Escort duty has real stakes on both sides.

**Souls — purchasing currency, not a power modifier:**
- Souls is the personal PVP currency earned by killing flagged/Grace players.
- **PVP players do not get stronger through Souls.** They are already full
  strength. Souls buys access, not power — exclusive gear, consumables, and
  items available only to those who've earned them through combat.
- This keeps balance clean. There is no "500-Soul player vs 200-Soul player"
  tuning problem. Two fighters are just two fighters.
- Souls cannot be transferred or looted — personal combat history only.
- Death costs nothing in Souls. Lose the fight, keep your record.

**Essence as clan currency:**
- Essence earned by any clan member can be deposited into the **clan pool**
  (voluntary, or auto-contributed at a %).
- Clan pool funds: guards, room upgrades, clan-exclusive items, clan Sanctuary
  spell (as suggested on the original ideas board).
- Killing a rival clan member transfers their Essence to YOUR clan pool
  directly — inter-clan warfare has economic teeth.
- Default players and unclanned players keep their Essence personal (no pool).

---

## Open Questions (Decisions Not Yet Made)

1. **Essence decay rate** — DECIDED:
   - Decay is measured in **played time**, not real-time wall clock.
   - Grace falls to zero after **8 hours of played time** since the last
     Essence-earning mob kill.
   - Decay **pauses** while the player is actively PVE-ing (earning Essence).
     Only ticks down during played time where no Essence is being generated.
   - Logging off pauses decay entirely — this is not a login-to-maintain system.
   - Effect: casual farmers who play 2–3 hours a week will see Grace fade between
     sessions. Active farmers maintain it indefinitely. Neither is punished harshly.
   - Implementation: store `last_essence_earned` as a played-time timestamp.
     Each tick, if player is online and not in combat with a mob, increment a
     `grace_drain_timer`. At 8 hours accumulated drain, Essence hits zero.

2. **Grace lootability** — are ALL items lootable, or just non-QEQ?
   Original DS had noloot as a server flag. Grace could restore lootability
   to a subset: carried items yes, worn items no? Or everything?

3. **Can Default players join clans?** — if clan pool needs farmers, does a
   Default player contribute? Probably yes at a reduced rate to incentivize
   opting in to Grace.

4. **Souls vendor location and stock** — Solennir (central, risky to reach for
   flagged players) or clan hall (private, safer)? Both?

5. **Alt abuse** — player farming Essence on one char, transferring value to
   PVP char. Mitigations: no Essence transfer, Souls only generated from
   damage to flagged chars, not tradeable.

6. **New player experience** — Default is the safe floor, but there's no
   tutorial pointing toward the economy. Need a veteran NPC or help file
   that explains Grace and Souls at level 30–40 range.

7. **Paradox interaction** — during paradox events, does Grace modifier change?
   (Ideas board: several players wanted paradox to mean something more.
   Turning off Grace during paradox could be a natural escalation mechanic.)

---

## The Isle Parallel

Kyle's reference: The Isle forces players out of safe spots through hunger/thirst.
Herd animals need to feed continuously or they stop growing. Predators get value
from hunting active prey, not parked targets.

The Essence decay mechanic maps directly:
- Farmer who stops farming loses their Grace bonus (stops growing)
- Farmer must stay in dangerous mob territory to maintain their stack
- Natural clustering: farmers group up for mob efficiency + mutual defense
- Predators (Soul collectors) follow the farmers into dangerous zones
- Safe zone becomes a recovery area, not a permanent home

The key difference from The Isle: **players can always opt out** (Default path).
Nobody is forced into the ecosystem. But the rewards are only available to those
who engage with it.

---

## Prototype Path (Minimum Viable Version)

If we want to test the concept before full implementation:

1. Add `Essence` field to pfile
2. Add mob kill hook that increments Essence by (mob_hp / 100)
3. Add tick handler that decays Essence by flat amount
4. Add Grace modifier to sanctuary damage calc (simple % lookup table)
5. Add `IS_GRACE` flag that enables loot on death
6. Add `souls` field to pfile
7. Add kill/damage hook for Souls accumulation (PK only)
8. Add one vendor NPC with 2–3 placeholder items

This is roughly 400–600 lines of new C across fight.c, handler.c, db.c, and
act_wiz.c. No new area files required for MVP. Solennir vendor can be added
to existing shop structure.

---

## Related Decisions

- DECISION-006: PVP flag opt-in (approved in principle, this doc supersedes)
- BALANCE_NOTES.md: Wardancer/seer balance flagged — Grace system should not
  amplify existing imbalances (a wardancer with 9 attacks + full Grace = even
  harder to kill). Consider: Grace modifier caps lower for melee-heavy classes,
  or Grace modifier only applies to a character's passive mitigation (sanc, AC),
  not to active evasion skills (dodge, parry, mist dance) — this keeps the
  "hard to kill" intent without making evasion-heavy classes nearly invincible.
