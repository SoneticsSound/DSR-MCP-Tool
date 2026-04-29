# Devil's Silence Resurrected — Discord Patch Notes

Player-facing patch notes, one entry per version. Written for Discord.
Technical details live in CHANGELOG.md — this is the hype doc.

---

## v0.4.43 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.43**

✨ **`spellup` no longer floods your screen, and brand-new characters get a free buff on first login.**

- 🧙 **Spellup is quiet now.** Casting `spellup self` (or on a friend) used to dump a wall of nineteen "you feel..." lines — one per buff. Now it lands as a single line: *"A shimmering aura of magical protections envelops you."* All the same buffs apply; you just don't have to scroll past the recital.
- 🎁 **Auto-spellup for new characters.** When you log in for the first time after creating a character — or after remorting back to level 1 — the world now automatically spellups you so you don't land in TC unbuffed and squishy. Stops firing once you hit level 2, so it's not nagging veterans.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.42 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.42**

🌀 **Paradox events are ticking again.**

The paradox state machine — the one that builds tension, fires, and resolves on its own clock — was sitting fully wired but never ticking. Its update was orphaned in the engine and just… didn't run. Now it does.

- ⏳ **Paradox now counts up, fires, and clears properly** on its built-in cadence. If you've been around long enough to remember paradox actually *happening* — it's back.
- 🛡️ **All existing paradox triggers, durations, and chances** are unchanged from the original 2003 tuning. This is purely a "the gear is now connected to the engine" fix.

*Grace-period suppression (the second half of paradox) is still pending an economy hookup before it can be turned on — a future patch.*

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.41 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.41**

🐛 **Two bug fixes — one big classes, one ancient Alecca todo.**

- 🥋 **Monk, Shaolin, and Sensei are selectable again.** All three classes had been silently locked out at character creation, reroll, and remort — the gate was a single flag deep in the class table. **All 73 monk-family skills work**, and now the classes themselves can actually be picked. If you've wanted to roll a monk, today's the day.
- 🌀 **Cursed players can no longer cheat curse by following someone.** When your master recalls, you used to get pulled along regardless of curse. Now the curse properly forsakes you ("$G has forsaken you.") and you stay put while your master vanishes. NPC pets and charmies still follow recall normally — only mortal cursed PCs are blocked. *Original Alecca todo from 2003, finally fixed.*

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.40 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.40**

⚙️ **Monk multi-kick chain now does what 2003 multi-kick did.**

For monk-family characters using `kick` and `roundhouse`, the chain attack now extends up to **four hits** instead of one:

- 🥋 **Hit 1** — Always lands. Big damage on `roundhouse`, lighter on `kick` (kick is meant to be spammable, so the per-cast damage is half).
- ⚡ **Hit 2** — Only if you have **haste** and the target's still fighting you.
- 🎯 **Hit 3** — Rolls against your **second attack** skill. Halved chance if you're slowed.
- 🎯 **Hit 4** — Rolls against your **third attack** skill. Halved chance if you're slowed.

Each hit checks the fight is still active before swinging — no whiffing at corpses if the target dies mid-chain.

**Practical effect**: monks with high second/third attack and haste now feel meaningfully stronger in melee. Kick spam is still kept in check by the 50% damage scaling. Roundhouse is now the heavy-hitter monk burst.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.39 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.39**

🛡️ **`biomanipulation feedback` now actually grants Sanctuary** — the way it did in 2003.

Until this build, biofeedback's "protective" affect was a placeholder bit that didn't read correctly to the rest of the engine. Damage halving from sanctuary wasn't applying. Now it does — biofeedback is a real defensive cooldown again, exactly as it was originally designed: a mid-combat shield psis can throw on themselves.

🛡️ **`voodoo pin/trip/throw` lockout now flags the victim as voodoo-shielded** — visible in observation tools, accurate for any future game systems that check shield state. The lockout window itself is unchanged.

**Nothing else changes mechanically.** Same mana costs, same lockout durations, same damage, same broadcasts. This is the engine catching up to its own original data model.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.38 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.38**

🔥 **Pyrokinesis is online — Priority 7 Psionics is complete.**

That makes biomanipulation + electrokinesis + telekinesis + pyrokinesis all live, which means **the entire Priority 1-7 combat-port queue is done**. Every combat verb that was a stub at the start of this resurrection effort is now real code.

**New command (the last big psi verb):**
- `pyrokinesis <mode> [target]` (psi class) — four-mode fire palette gated by skill, level, and mana. Type with no arg to see the menu of modes available at your level.
  - **`redsteel`** (always) — Heats the target's wielded weapon. Mana 25. **Requires the target to be wielding something.** On hit: fire damage + ~25% chance to **burn the weapon out of their hand** (drops to the room floor — they can pick it back up).
  - **`flamebolt`** (level 50+) — Single-target flame projectile. Mana 35, move 15. Damage `level..2*level` DAM_FIRE.
  - **`firestorm`** (level 70+) — **Room-AOE fire** that burns everyone (caster excluded). Mana 60, move 60. Damage `2*level..4*level` per target.
  - **`inferno`** (level 91+) — Massive fire explosion. Requires hit/mana/move all 550+ (100 of each on hit, 200 of each on miss). **Primary target takes `3*level..6*level` damage** plus splash damage `2*level..4*level` on everyone fighting either you or the primary target.

🎉 **Project milestone:** with this build the full combat catalog from `act_combat.o` is back. ~85+ combat verbs ported from disasm over the resurrection arc — kill, flee, kick, bash, trip, disarm with weapon-drop, rescue, berserk, backstab, circle, gouge, dirt, mock, spellbane, resistance, warcry, concentration, ironwill, battlehymn, bloodlust, warpaint, do_remort, do_reroll, do_storm, do_charge, do_strike_extended, do_garotte, do_cross_slash, do_dhammer, do_stomp, do_whirlwind, do_jab, do_throw, do_dance, do_chaos_blow, do_ambush, do_pinch, do_blackjack, do_caltrops, do_blinding_strike, do_assassinate, do_shield_smash, do_stance, do_roundhouse, do_healing_touch, do_earthbind, do_scream, do_shuriken (+ multi_shuriken), do_feed, do_bastion, do_strangle, do_voodoo + voodoo_pin/trip/throw, do_jinx_palm, the 8 monk_* helpers + multi_kick, do_buddha_palm, do_chi, all four psi verbs… and counting.

The only remaining ports are blocked on Cowork design questions (`do_forge` + `do_katana` material vnums) or post-2003 additions that don't exist in the original binary.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.37 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.37**

Mind over matter — **Telekinesis** is the third of four big psi verbs. One left.

**New command:**
- `telekinesis <mode> [target]` (psi class) — four-mode telekinetic palette gated by skill, level, and mana. Type with no arg to see the menu of modes available at your level.
  - **`ballistic`** (always) — Single-target ballistic projectile. Mana 25, move 25. Damage `level..2*level` DAM_PIERCE.
  - **`metalstorm`** (level 50+) — **Room-AOE shrapnel storm**. Mana 55, move 55. Damage `2*level..4*level` per non-safe target. **Level 76+ adds a second hit per target; level 91+ adds a third.** A maxed character can dump three rounds of shrapnel into the room in one cast.
  - **`slam`** (level 70+) — Single-target shaped-force slam. Mana 25, move 25. **No damage.** Applies the **AFF2_SLAMMED** affect (5–20 ticks) and stuns the victim for 1d2 ticks. "Too careful to be slammed again" if already slammed.
  - **`wall`** (level 91+) — Wall of force. Requires hit/mana/move all 550+, costs 250 of each on a successful cast (500 of each on a fail). **Forces stop_fighting on every combatant in the room** — emergency "everyone back to neutral corners" panic button. Must already be fighting to cast (otherwise "you aren't quite that desperate").

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.36 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.36**

Psionic offense. **Electrokinesis** is the second of four big psi verbs to come online.

**New command:**
- `electrokinesis <mode> [target]` (psi class) — four-mode lightning-attack palette gated by skill, level, and mana. Type with no arg to see the menu of modes available at your level.
  - **`arc`** (always) — Single-target lightning arc. Mana 10. Damage `level/2..level` DAM_LIGHTNING. Falls back to `ch->fighting` if no target.
  - **`bolt`** (level 50+) — Thrown bolt of energy. Mana 25, move 25. Single target. Damage `level..2*level` DAM_LIGHTNING.
  - **`shockwave`** (level 70+) — **Room-AOE**. Mana 60, move 60. Hits everyone in the room (caster excluded, safe rooms/groupies excluded). Damage `2*level..4*level` per target. **At level 91+, every target eats a second hit** of the same range.
  - **`flash`** (level 91+) — Single-target blinder. Requires hit/mana/move all 550+. Costs 50 of each on cast. Saves vs DAM_LIGHTNING — on save-fail applies AFF_BLIND with -4 hitroll for level/4 ticks. Already-blind targets are politely declined.

Each mode has its own roll; failure consumes mana but not damage. Standard wait clamp via skill_table.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.35 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.35**

Psionics class is opening up. **Bio-manipulation** is the first of four big psionic verbs to come online.

**New command:**
- `biomanipulation <mode>` (psi class) — five-mode self-buff palette gated by skill, level, and mana. Type with no arg to see the menu of modes available at your level.
  - **`flesh`** (always available) — Skin turns to armor. Mana 50. Lasts level/2 ticks. APPLY_AC -level (much harder to hit).
  - **`adrenaline`** (level 31+) — Adrenaline pumps quickly. Mana 50. **If you're slowed**, attempts a dispel of the slow first; if it lands, you stop moving in slow motion. **Otherwise** applies AFF_HASTE + APPLY_DEX +level/8 for level/4 ticks.
  - **`cellular`** (level 51+) — Cellular adjustment. Mana 50. APPLY_STR + skill/4 for level/2 ticks. Stacks with giant strength check.
  - **`feedback`** (level 71+) — Bio-feedback. Mana 110. Protective affect for level ticks.
  - **`deaden`** (level 91+) — Deaden pain. Mana 50, move 50. Heals you 200 HP (or 100 if you have devil's curse on you), capped at max HP.

Each mode has its own already-affected gate, fail message, and stamina check. Skill rolls hide a chance multiplier so high skill = nearly always lands. Standard wait clamp via skill_table.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.34 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.34**

Voodoo class is now feature-complete. Time to lay hands on people.

**New commands:**
- `jinx palm <target>` (do_jinx_palm) — barehand DAM_NEGATIVE strike that **applies AFF_CURSE** on a successful save-fail. Required: no weapon wielded. Damage scales `level/2..level`. After the strike, the victim rolls a save vs DAM_OTHER — if they fail, they get hit with the curse affect: **-level/8 hitroll** AND **+level/8 AC** (i.e. worse defense), lasting `level/4` ticks. Already-cursed victims just take the damage without the affect re-applying. Standard chance modifiers via hand-to-hand skill, hitroll, STR/DEX, level diff, HASTE on either side. Falls back to `ch->fighting` if you don't pass a target.

That makes **all five** Voodoo verbs live: `voodoo pin`, `voodoo trip`, `voodoo throw`, and now `jinx palm`. Plus the `voodoo` dispatcher and the underlying lockout via gsn_protection_voodoo. The whole class is in.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.33 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.33**

Voodoo class is online. Find a doll, name it after someone, and start mischief.

**New commands (you must be holding a voodoo doll, item vnum 55):**
- `voodoo pin` — stick a pin in the doll. Your target doubles over with a sudden pain in their gut. No real damage — the value is the brief lockout (and the room sees you do it).
- `voodoo trip` — slam the doll on the ground. Target's feet slide out from under them; they faceplant. Same brief lockout.
- `voodoo throw` — toss the doll into the air. A sudden gust of wind grabs your target and **throws them through one of the exits in their room**, slamming them face-first into the wall of the new room. If they're already fighting or all the exits are blocked, they still get the wind+wall messages but stay put.
- `voodoo` (no arg) — shows the syntax + action list.

**How targeting works:** Each helper takes the **doll's name keyword** as the target string. Rename your doll to include the victim's character name (e.g. via `restring` or whatever your server allows) and the voodoo command will find them anywhere in the realm — they don't have to be in the room. Standard newbie protection (level ≤ 20), recently-killed gate, and a 1-tick "still realing from a previous voodoo" lockout all apply.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.32 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.32**

Two big monk-class verbs out of the stub list — buddha palm and ch'i meditation.

**New commands:**
- `buddha palm <target>` (do_buddha_palm) — barehand DAM_FIRE strike. **Requires no weapon wielded** — palm only. Real damage scaling level/2..level. On hit, **50% chance** to additionally apply a fire effect to the target (lingering burn). Chance formula stacks on the **hand-to-hand** skill — better hand-to-hand makes buddha palm land harder. Other modifiers: STAT_INT, STAT_DEX (yours), -DEX/2 (theirs), level diff, HASTE on either side.
- `chi` (do_chi) — **stacking ch'i meditation**. Each successful cast in combat builds your chi level by 4 (up to 24 at level 100+). Visual broadcast scales with chi: red flicker → blue energy → bright red → power flash → sparks of energy fully focused. **Each level gates by character level** (chi=4 needs level 20+, chi=8 needs 40+, ..., chi=24 needs 100+). Once chi > 7, every subsequent cast also discharges elemental damage at your active target — **cold at chi=8, fire at chi=12/16, lightning at chi=20/24** (lightning gets double damage). Active chi grants stacking +HITROLL and +DAMROLL bonuses (lasts ch->level ticks). Costs 25 mana per cast. Skill-roll fail just makes you flicker briefly with no progress.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.31 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.31**

Monks — your barehand combat just got real.

**What's new:**
- 🥋 **All eight monk martial-arts kicks/strikes now deal real damage and broadcast their flavor.** The `monk_*` helpers (shinkick, palmstrike, knee, elbow, thrustkick, backfist, spinkick, reverse) were stubs that printed "combat module rebuilding". Now each one fires `one_hit` with its own gsn for real damage, and ~10% of the time you'll see the dramatic 3-line broadcast (you / target / room).
- 🥋 **`monk_spinkick` has a real berserk AOE.** When the 1-in-10 narrative fires, everyone in the room who's fighting you (or your primary target) eats an extra `tornadokick` hit. Use carefully — it'll wake up bystanders.
- 🥋 **`monk_reverse` does the choking-grip combo.** Always 3-line broadcast on use; 1-in-10 chance to also deliver the spin+wrap setup. Pure flavor — no damage, just fight-state engagement.
- ⚙️ **`multi_kick` now delivers something real.** Was a stub returning the rebuilding message; now picks one of the 8 helpers at random. This unblocks the existing `do_kick` and `do_roundhouse` race-routes for races 8/26/44 — those characters will see real attacks instead of the stub message.

**Heads up — what's NOT in this build:**
- The 2003 `multi_kick` had pclass-aware base damage scaling (40 vs 80 range) and an AFF_HASTE-chained second hit. This release uses the simpler random-helper dispatch — feels close, but Cowork may want the faithful re-port if QA shows monk damage is off.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.30 — 2026-04-29

🩸 **Devil's Silence Resurrected — v0.4.30**

A handful of fixes pulled straight from the 2003 Leto changelog — small numbers, real impact on combat feel.

**Bug fixes:**
- 🐛 **`charge` does bonus damage when wielding a sword.** Per the original 2003 design — wield a sword, charge in, and your level/4 extra damroll rides through the multi-hit chain. Other weapons unchanged.
- 🐛 **`ambush` does bonus damage when wielding a spear.** Sister fix — spear-wielders get the same level/4 damroll boost on a successful ambush.
- 🐛 **`flee` is now gated to 5/6 attempts per round.** One in six attempts will fail outright with "Panic grips you, but you can't find an opening." — fits the 2003 design that fleeing isn't always automatic. Wait penalty still applies on the failed roll.
- 🐛 **Silver, wood, and iron damage now route as weapon damage.** Previously these three damage types fell through to the EXOTIC armor path (counted as magic). Per Leto's original design they should hit the same AC bucket as bash/pierce/slash. **Wood** → bash AC, **silver** + **iron** → slash AC.
- 🐛 **`travel` cooldown was way too long.** Was 24 minutes (wall-clock); now 90 seconds. Use `travel` again much sooner after a successful walk.

**Already implemented (closing audit):**
- ✅ `quaff` combat fumble — was already in the code at a 1/15 rate. Bug closed; no action needed.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.29 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.29**

Monks, this one's for you.

**New commands:**
- `stance <name>` (do_stance) — toggle between six monk-class combat stances. Each stance changes how `fight.c` resolves your incoming and outgoing combat. **Phoenix** (flame fists), **Leopard** (frost), **Crane** (wind/grace), **Scorpion** (talons + poison), **Dragon** (thunder), **Monkey** (jungle strength), or **None** to clear. Each one fires a 2-line broadcast — your room sees the dramatic shift, you feel the energy lock in. Only monk-family classes can use this; everyone else sees a polite reminder to study harder.
- `stance` (no arg) — show your current stance.

**Heads up on the queue:**
- `do_forge` (the kensai katana/wakizashi crafting skill) is **paused pending a design call from Cowork** — the original 2003 source-material vnums (1313 + 3724) don't exist in current DS world data. Need new vnums chosen before this can ship live.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.28 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.28**

A real shield-bash. Get one in your off-hand and cause some hurt.

**New commands:**
- `smash <target>` (do_shield_smash) — body-checks the target with your **shield**. **You must be wielding a shield in WEAR_SHIELD** for this to work — barehand or two-handed weapon configs get rejected. On hit: real **DAM_BASH** damage scaling `level/2`–`level` plus a bonus from your shield's armor value, the target gets knocked to **resting position**, and their wait/spell/skill/flee timers all clamp up to a 24-pulse minimum (good luck doing anything for the next moment). Then a second roll based on **gsn_stun** (with a fat bonus if you're a warrior-tree class) can stun them for 1d2 or 1d3 ticks on top of the knockdown. Gangbangs zero out the stun roll; defenders being ganged get double the stun chance.

**Heads up on quirks:**
- The chance formula respects STR (yours), CON+DEX (theirs), HASTE on either side, and the target's bash-AC.
- `smash` falls back to your current `ch->fighting` if you don't pass a target.
- `rift`-affected casters are blocked from smashing.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.27 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.27**

A new combat verb — and it's the meaty kind.

**New commands:**
- `assassinate <target>` — two-stage stealth opener. **Stage 1**: roll against your full chance to "find a weakness". On success, the victim gets the **assassinate** affect (1d5 ticks) — they're flagged as exposed and the room sees "$n's weakness has been exposed." **Stage 2**: a recomputed chance (level/5 + skill/5 + sneak ±25, zero if they're below 1/3 HP, zero if they're severed, zero if you have a rift on you) decides whether you immediately follow up with a full `multi_hit` chain. Sleeping victims auto-fire stage 2 if any chance survives. Required gates: **must wield a weapon**, **cannot already be in combat**, target must be visible. **Heavy stat scaling**: gangbang situations zero out stage 1 (assassinate is supposed to be a clean opener, not a pile-on tool).

**Heads up on a few quirks worth knowing:**
- Pktimer brakes assassinate — if you've recently been in PvP, you can't assassinate someone fresh.
- The miss path broadcasts a 3-line "tries to find $N's weakness and fails" sequence (different message to caster, room, and victim).
- An assassinated victim already carrying the affect won't re-tag — but stage 2 still rolls and can still chain a multi_hit on success.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.26 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.26**

Bundles the v0.4.25 travel fixes + a new combat port. Single copyover, two improvements.

**New commands:**
- `blinding strike <target>` — pressure-point strike that applies a real **AFF_BLIND** affect (-4 hitroll) to the victim. Light damage on hit (2–5 HP) — the value is the blind, not the damage. Heavy stat scaling: rewards your dex, punishes their dex twice as hard. HASTE on you adds chance, HASTE on them subtracts chance. Targets already blind get a polite "$E's already been blinded" instead of an attempt. Standard combat gates apply (stunned, safe-room, self-target, etc.). Falls back to `ch->fighting` if you don't pass an argument.

**Carry-forward from 0.4.25 (now live with this copyover):**
- 🐛 `travel <area name>` no longer crashes the server.
- 🐛 Discovered areas persist across logout for real (the save format had a typo'd load path that wiped them every login).

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.25 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.25**

Travel fixes — the v0.4.24 launch surfaced a hard crash on the argument form. Rolled out same day.

**Bug fixes:**
- 🐛 **`travel <area name>` no longer crashes the server.** The matcher was only looking at the first word of what you typed, so `travel the sprite village` was sometimes picking a totally different "The X" area and the pathfinder hated it. Now the full area name (case-insensitive prefix) is what gets matched.
- 🐛 **Discovered areas now persist across logout for real.** A typo in the save format meant your `Visited` list looked saved but never loaded back — every login wiped it. Fixed; once you walk into an area, your character remembers it forever.

**Other:**
- Pathfinding adds a small log breadcrumb on each `travel` call (server-side only; you won't see it). If anything else crashes, the log will show exactly where.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.24 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.24**

Travel system, a new combat verb, and a fix for the silent `bastion` miss everyone noticed.

**New commands:**
- `travel <area>` — auto-walk pathfinder. Pick an area name and your character starts walking there one step per tick until you arrive. Type anything during travel to cancel. Has a cooldown (skipped for guardian-class characters). You can only travel to areas you've actually walked into at least once — recall-spamming won't open them up.
- `caltrops` — out of the stub. Throw sharp spikes at the feet of whoever you're fighting. Real damage scaling with your level. **Flying targets are immune** ("their feet aren't on the ground"). On hit there's a chance to apply a **limping** affect (-4 DEX for a tick), same effect the knee-breaker side-mechanic uses. Misses still broadcast the spike-throw to the room and lengthen your recovery.

**Bug fixes:**
- 🐛 **`bastion` no longer silently misses.** Trying `bastion` and missing used to produce *zero output* — looked totally broken. Now you'll see "You lunge but find only air." (and the room sees "$n lunges hard but finds only air."). Damage roll unchanged.

**Under the hood:** your character now remembers which areas you've explored, persistently across logouts. That's what feeds `travel`'s destination list.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.23 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.23**

Two knockout-type skills — different flavors, identical mechanics.

**New commands:**
- `pinch <target>` — pressure-point pinch. On hit applies **AFF_SLEEP** and forces the target to a sleeping position (same outcome as `strangle`, but with armor/resistance handling on top). Strong stat scaling: rewards your dex, punishes their con. Visibility matters: +10 chance if they can't see you, -10 if they can. **Pktimer brake**: -60 chance if you have an active pktimer. **DAM_BASH check_immune handling**: if the target's immune to bash, pinch fails outright with a "you are unaffected" broadcast and no damage. Resist halves chance, vuln gives +33%.
- `blackjack <target>` — lead-filled sack to the back of the head. **Functionally identical to pinch** — same gates, same stat scaling, same AFF_SLEEP outcome, same DAM_BASH immune handling, same -60 pktimer brake. The only differences are the broadcast flavor and which skill it learns from.

**Pinch + blackjack quirk:** the "alert flag" branch (when victim is on guard) blocks the knockout AND fires a 3-line "unaffected" broadcast. The non-alert MISS branch is silent EXCEPT it deals 20 HP damage anyway — so failing a pinch on an off-guard target still chips them. Kept disasm-faithful; flag if it feels weird.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.22 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.22**

A holy-tinged power strike and a stealth opener with sharp prerequisites.

**New commands:**
- `chaos blow <target>` — spiritual power strike. Damage scales `level/2`–`level` and is dealt as **DAM_HOLY** (not "chaos" — preserved disasm-faithful, flagged for design review). On hit it also slaps an **AFF_WEAKEN** (-10 STR) affect on the target, dropping their melee output. Strong stat scaling: rewards your str+con, punishes theirs, HASTE shifts ±5/-10. Monk-family classes (pclass 8/23/38) get a lighter wait clamp on hit (1×beats vs 2×beats for everyone else). Misses are silent — flagged for re-tuning.
- `ambush <target>` — stealth opener with **two hard prerequisites**: you need **AFF_CAMOUFLAGE** active ("you need to be camouflaged") AND a wielded weapon ("you need to wield a weapon"). Cannot fire while in combat. Sleeping victims auto-hit if you have any chance at all (sleeping-victim auto-hit pattern, same as backstab). Sneak bonus (+25 chance) if the victim can't see you. On hit it kicks off a real `multi_hit` chain. Misses use the alert-vs-silent broadcast pattern.

**Heads up on chaos blow:** the damage type is `DAM_HOLY` per the 2003 disasm. That might just be a 2003 quirk (chaos magic flavored as holy) or a misread we can't verify without running both side-by-side. Flagged for QA — if the resist/vuln math feels backwards on chaos blow, that's why.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.21 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.21**

A body-slam opener and a choke-out — two PK skills that punch above their damage numbers.

**New commands:**
- `bastion <target>` — body-slam opener. Cousin of `charge` and `garotte` — can't fire while in combat, requires the target to be above 1/3 HP, blocked by the same magical-rift caster lockout. On hit it kicks off a real `multi_hit` chain (so the damage uses your normal melee profile rather than a flat number). Gangbang piles double the recovery time. Misses are silent right now (the missing-broadcast branch is the same kind of unrecoverable alert flag as on `throw` and `feed` — flagged for re-tuning).
- `strangle <target>` — choke-out. **Applies AFF_SLEEP to the victim and forces them to a sleeping position on hit.** No damage on hit — the value is the lockout. Re-strangle is blocked while the affect is up; once it drops you can re-roll. Heavy stat scaling: rewards your dex, punishes their con, +10 if they can't see you coming, -10 if they can. **Pktimer penalty: -60 chance** if you have an active pktimer — strangle is meant to be a setup tool, not a chain-aggression weapon.

**Strangle quirk worth knowing:** the AFF_SLEEP affect lasts only 1 tick, but the position change persists until the victim takes damage or wakes manually. So you get a brief affect-tag plus a longer state-change. Designed-in or forgotten 2003 detail — flagged for QA observation.

**Tracking degradations:** added a new "Unrecoverable 2003 behaviors" section to METHODOLOGY.md. Each port that omits or approximates a 2003 detail (because the offset doesn't map cleanly to current `merc.h`) is now logged with a re-attention trigger. We'd rather know what we're missing than assume the live game matches the 2003 game.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.20 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.20**

A poisoned blade and a vampire's bite. Plus a quietly-ported helper that makes the multi-hit shuriken combo finally fire.

**New commands:**
- `shuriken` — thrown poisoned blade. The HIT path lands a guaranteed first strike, then chains into bonus hits gated by your **second/third attack** skills (with HASTE adding an extra free hit between). The combo is `DAM_POISON` damage. After the multi-hits, if your target's still up and engaged with you, a final `DAM_PIERCE` hit lands AND a slow affect locks onto them (-1 dex, plus a fresh `slow` spell chained on top). Misses still apply `DAM_POISON` for show. Min wait on hit is 12 pulses; miss is half the standard skill wait.
- `feed` — vampire blood-bite. **Effective minimum 90% hit chance** — feed is meant to land. Damage scales `level`–`level*2` and gets a **+33% bonus while shapeshifted into wolf form** (the predator form — vampires also get bat for flight and mist for travel). Won't fire if you're blind, can't hit a target below 1/6 HP ("hurt and suspicious"), and respects the new kill-stealing protection. Miss banner is the standard "hits only air" set.

**Helper unlock:** the multi-hit shuriken helper (`multi_shuriken`) is now real, not a stub. Anything else in the codebase that calls into it now actually does damage instead of printing the rebuilding placeholder.

**Known degradation worth flagging:** feed has a 2003 "blood resistance" alert flag that we couldn't recover (it lived at a `CHAR_DATA` offset that doesn't exist in the current source layout — same family as the alert flags we omitted on `throw` and `charge`). The resistance branch of feed's miss messaging is gone — you'll always see the standard "hits only air" set, never the resistance-themed alternative. Functionally inert; cosmetic only.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.19 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.19**

Two more out of stub — one anti-flight grapple and one sound attack that bypasses armor.

**New commands:**
- `earthbind` — yanks an airborne target out of the sky. Requires the victim to actually be flying (otherwise: "They aren't airborn."). On hit: strips `fly`, `levitation`, and `grow wings` affects + clears the flying bit, broadcasts a "ripped from the skies" line, and deals `level`–`level*2` bash damage. Effective hit chance is your skill `× 3/4` — it's deliberately stricter than its raw skill % suggests.
- `scream` — mind-splitting sound attack. **DAM_SOUND** type, so it bypasses physical armor. Damage is modest (`10`–`20`) but every cast also rolls a 5% chance to **stun** the victim for 1–2 ticks. The scream itself broadcasts to everyone in the room regardless of hit/miss — even when you whiff, people hear it. Has an effective ~50% hit cap regardless of skill (it's a side-effect attack, not a primary damage source). Misses cost 50% extra wait time.

**New gate worth knowing about:** `scream` includes a **kill-stealing protection** — if your target is currently fighting another PC who isn't in your group, you'll get "Kill stealing is not permitted." Same gate will probably surface on more port-in attacks as we work through Priority 4.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.19 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.19**

Two more combat commands — one punishes flyers, one punishes everyone in earshot.

**New commands:**
- `earthbind` — yanks an airborne target to the ground. Only works if they're actually flying (levitate, fly spell, wings). Strips the flight affect, deals bash damage, and brings them down hard. If they're not airborne you'll get told "They aren't airborne." — no wasted attempt.
- `scream` — mind-splitting sound attack. Bypasses physical armor entirely (`DAM_SOUND`). Always broadcasts the scream regardless of hit or miss, so everyone in the room knows it happened. Land it and there's a 5% chance the target gets stunned for a tick or two on top of the damage. Miss it and your own recovery is 50% longer than if you'd hit.

**Kill-steal protection added.** Scream (and likely more skills going forward) now refuses to fire if the target is already fighting someone who isn't in your group. "Kill stealing is not permitted." — enforced at the skill level.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.18 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.18**

Two more combat verbs out of stub — and one of them is the first real heal.

**New commands:**
- `roundhouse` — auto-targets your current opponent (no argument). Mid-fight kick that lands for `level/2`–`level` bash damage on hit. Miss it and you eat the standard miss banner. Get woozy from a stun and you'll get told to wait it out.
- `htouch [target]` — healing touch. Skip the target name and you heal yourself; name a target and you heal them. **Costs 50 mana** and you need at least 55 to even start. Heal amount scales hard with your level: `1d8 + level/3` until 39, `2d8 + level/2` to 69, then `3d8 + level - 10` at 70+. Skill % scales the result, and `devil's curse` halves it.

**Roundhouse note:** Monk-family classes will eventually call into the multi-kick combo on hit (different damage pattern). That fork is wired in the 2003 code but the helpers aren't ported yet — Monks currently get the same broadcast + bash damage as everyone else. Will re-tune when the Monk batch lands.

**Combat roster so far:** more out of stub, more PvP variety landing each patch.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.17 — 2026-04-28

🩸 **Devil's Silence Resurrected — v0.4.17**

Two CLASS ABILITY tier ports — neither hits hard but both reshape a fight.

**New commands:**
- `jab` — throat-strike. **Zero damage**, but it slaps a "gasping for breath" affect on the target. While they're gasping you can't re-jab them — they have to recover first. Use it to interrupt or just to mess with someone's tempo. PvP-aware: pktimer blocks it, charm-master gates it, and you can't jab yourself (well — you can, but you'll just give yourself a welt).
- `throw` — wrestling-style grab and throw. **Real bash damage** plus the victim is knocked to a resting position with a 24-pulse daze (their move/skill/flee timers all clamp). Miss it and **you** end up on the ground instead, locked up for double the wait (triple if you're being gangbanged). Trust > 102 (Exec) bypasses both wait clamps.

Both ports come with the standard DS gates: skill check, can't-target-self, can't-target-while-stunned, charm protection, etc.

**Two ops notes from this patch cycle:**
- The watchdog kept the binary alive through the early-morning ngrok hiccup. Public tunnel was the only thing offline. We've got a fix queued for the launcher.
- The 2003 binary uses a slightly different `CHAR_DATA` layout than the current source — we now decode-by-field-name rather than by raw offset, so all future ports are immune to that drift.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.16 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.16**

The Wardancer has stances now.

**New command:**
- `dance <none/mist/storm/predator/cobra/devil>` — Wardancer-only stance dispatcher. Sets your active dance which gates other Wardancer abilities (`storm` requires `dance storm` first). Each dance has its own broadcast. **Devil dance** also attaches a permanent affect (visible on `affects`) — the others are pure stance toggles. `dance` with no argument shows your current dance. `dance none` stops dancing entirely.
- Mid-fight dance switching costs at least 12 wait pulses (IMM bypass via trust > 101).
- Non-Wardancer classes get "You shake that ass."

**Wardancer chain unlocked:** with `dance storm` set, the existing `storm` AOE now works for Wardancers end-to-end.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.15 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.15**

First CLASS ABILITY port — the combat opener that makes you hard to target.

**New command:**
- `charge` — body-slam opener. Explicit target, can't use while already in combat. Works like `garotte` in shape — sleeping targets get auto-hit, HP-frac check, gang pile-up doubles recovery time. Two things make it DS-unique: if you've recently been charged, backstabbed, or ambushed you have a **wary flag** — charge is blocked until it clears. And if the charge connects, **the victim gets wary-flagged too**, so they can't immediately be hit by the same class of opener again. IMMs bypass the wary gate.

**What this unlocks:** charge is the first skill that interacts with the wary system — a mechanic that runs through backstab, ambush, charge, and eventually throw. Understanding it opens up how the full opener-lockout tier works.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.14 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.14**

Storm is live for Wardancers.

**New command:**
- `storm` — AOE attack that chains through everyone in the room, same multi-hit pattern as `whirlwind` (1 hit always, a second if your skill is over 50%, a third if it's over 90%). Costs **150 mana** — this is a magical-style AOE, not a pure weapon-skill. Gate: requires `dance storm` to be active first (Wardancer only). Non-dancers can't cast it regardless of mana.

**Wardancer chain complete:** `dance storm` → `storm` now works end-to-end.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.13 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.13**

The bots got smart. Also: an in-game command to spawn them.

**Bot system overhaul:**
- Bots now react when they're *being* hit, not just when they land a hit — they'll enter combat mode the moment someone opens on them.
- Death and recovery works: bots walk to cots after dying, sleep until 95% HP, then head back to patrol.
- Corpse retrieval works: after death-lag clears, bots walk the patrol corridor looking for their own corpse and re-equip everything.
- Bots now challenge players proactively — if you walk into their room while they're patrolling, there's a 40% chance they'll bow at you. Bow back and it's on.
- Taunt/flame cadence slowed way down. 60–90s random intervals instead of every 10s.
- Bots clean-quit on shutdown — no more ghost link-dead characters after `botquit`.

**New in-game command:**
- `botspawn <name>` (IMM 107+) — spawns a bot without needing a shell. `botquit <name>` or `botquit all` to shut them down. See `help botspawn` in-game.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.12 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.12**

Three utility skills out of stub, plus Morpheous skills are now actually buyable.

**New commands:**
- `rub` — clears blindness caused specifically by dirt kicking, fire breath, blinding strike, or headbutt. Dex and haste affect the success rate. Other sources of blindness ("Rubbing your eyes won't help that injury.") — use a spell.
- `deepbreathing` — toggle buff. Rolls a check to enter the state; the buff stays until you toggle it off. Harder to activate while in combat.
- `cleanse` — 200-mana dispel chain. Costs mana, not skill. Clears poison at any skill level; plague if your effective level clears 30; curse if it clears 50. Each removal gets its own broadcast.

**Morpheous fix:** the six morpheous skills enabled last patch (`chameleon`, `dopple`, `grow parts`, `form memory`, `advanced dopple`, `mutate body`) weren't showing up in `practice` or costing CP correctly — a rating field was set to zero, silently filtering them from the buy system. That's fixed. If you created a Morpheous and couldn't spend CP on anything, those skills are now live.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.11 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.11**

Morpheous tuning and character creation quality of life.

**Morpheous skills are now buyable.** The six morph skills enabled last patch (`chameleon`, `dopple`, `grow parts`, `form memory`, `advanced dopple`, `mutate body`) weren't showing up in `practice` or costing CP in gen-groups — a rating field left at zero was silently filtering them out. That's fixed. If you started a morpheous and couldn't practice anything, those skills are now available.

**`add all` works properly.** Character creation's bulk-buy command now picks up everything — no more silent drops on skills like `rescue`, `warcry`, or `trip` depending on class. XP per level also now caps at 10,000 regardless of total skills purchased, so you won't see absurd TNL numbers on a fully loaded build.

**No change to the combat roster** — still 30 commands live. Next patch adds more.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.10 — 2026-04-27

🩸 **Devil's Silence Resurrected — v0.4.10**

Character creation quality of life and Morpheous unlocked.

**`add all` fully fixed.** The bulk-buy command now picks up every available skill and group without silently dropping any — including `rescue`, `warcry`, `trip`, and other skills that were being skipped depending on class. XP per level also now caps at 10,000 regardless of how loaded your build is, so you won't see absurd TNL numbers after a full creation.

**Morpheous skills are live.** The six morph skills added last patch are now available in `practice` and cost CP correctly at character generation.

**No change to the combat roster** — 30 commands still live. Next patch adds more.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.9 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.9**

Two more combat verbs and a new playable class.

**New commands:**
- `strike` — single-weapon power attack. Hit your target on guard and they sidestep; hit them off-guard and they barely have time to dodge. The miss messages are different depending on whether they saw it coming. Land it and you swing at full melee speed.
- `gore` — horns required (currently means tier-3 morpheous, but `set char self skill gore 100` works for testing). Level-scaled raw damage — `level × 2` to `level × 4` plus a +100 floor — and a chance the impact stuns your target for a tick or two. Miss badly and you'll faceplant and stun yourself.

**Morpheous class enabled.** Rex flipped the morpheous (tier-3) class on for character selection. After `remort` to tier 3, `morpheous` is now a valid class pick. Skill table is fully wired (morpheous basics + morpheous default groups) — pick it up and let us know what's broken.

**Combat roster so far:** 30 commands live.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.8 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.8**

Two quality of life fixes.

**`spellup` is now available to all players.** Previously restricted to IMMs. Type `spellup` standing (not mid-fight) to bulk-cast your buff suite. No more asking an immortal to buff you.

**Lights no longer burn out.** DS-format light objects were losing their fuel and crumbling because the item format stores fuel at zero by default — the stock ROM protection wasn't catching them. Fixed. Lights now last permanently. Ones that are supposed to have fuel still burn down normally via character update.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.7 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.7**

Bug fixes and remort restored.

**`remort` and `reroll` are back.** Both commands were disabled after a server crash on first use. The crash was caused by class re-init touching combat code that hadn't been ported yet. With ~22 combat verbs now ported, that path is no longer hollow — tested live, no crash. Morpheous (tier 3) is now reachable.

**Combat hit messages fixed.** `cross slash` and `garotte` were generating ~75 log errors per minute of combat due to a wrong skill ID being passed internally. No gameplay impact — hits landed for the right damage — but the server log was filling up fast. Fixed.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.6 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.6**

Two new single-target combat commands — and one of them is a stealth opener.

**New commands:**
- `cross slash` — dual-wield only. Both weapons need to be equipped or it won't fire. When it lands it's a full melee round's worth of damage delivered in one strike. Footwork matters — if your target is nearly dead you can't get enough angle.
- `garotte` — whip required, target must be named, and you **cannot** be in combat when you use it. This is your opener. Catch someone sleeping and it's a guaranteed hit. Get caught mid-fight and you'll hear "You're facing the wrong end." Gang up on someone and the recovery time doubles — by design.

**Combat roster so far:** 20 commands live. Closing in on the full suite.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.5 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.5**

Quick data-file fix, no binary change.

**Isles mobs got their saving throws back.** A typo in the area file (`Saivs` instead of `Saves`) had been silently dropping the saving-throw line on 14 Isles mobs since the rebuild — meaning all of them defaulted to 0 saves, taking spells like cloth. Fix is live: those mobs now have the resistances the area was always supposed to give them. Casters will notice spells failing more often in the Isles — that's the original 2003 balance restored, not a nerf.

The big one: vnum 30004 was authored with **−1000 saves**. It is now functionally spell-immune by design. Bring a weapon.

Server: `7.tcp.ngrok.io:25597`

---

## v0.4.4 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.4**

Big combat update. Three AOE abilities are live, two bugs squashed, and character creation is no longer a pain.

**New AOE combat commands:**
- `dhammer` — call down a divine strike that chains through everyone in the room. Requires a weapon. Each target gets hit separately — and then lit on fire.
- `stomp` — plant your feet and send a shockwave through the floor. Costs move. Everyone in the fight eats it. You'll see it coming; they won't.
- `whirlwind` — spin out and catch every target in the room. High luck gets you two or even three hits per person. Costs move.

These join `legsweep` (from last patch) as the full AOE roster. Group fights just got a lot messier.

**`add all` now works properly** — during character creation you can type `add all` to buy every available skill in one shot. Previously it only grabbed spell groups. Now it grabs everything.

**Bug fixes:**
- New characters no longer vanish during a copyover. Level 1 chars were being silently dropped on hot-reload — fixed.
- Crash diagnostics improved. The server now captures full stack traces on crash so we can actually read them.

**Combat roster so far:** 18 commands fully live. Closing in on the full PvP suite.

Server: `7.tcp.ngrok.io:25597` — any MUD client, Mudlet recommended.

---

## v0.4.3 — 2026-04-26

🩸 **Devil's Silence Resurrected — v0.4.3**

Two new combat commands live, plus quality of life for new players:

**New commands:**
- `cleave` — rear back and put your full weight into a swing. Requires a wielded weapon. Miss and you look foolish. Land it and your weapon stats do the talking.
- `target` — swap who you're swinging on mid-fight without dropping combat. Essential for PvP when someone jumps in.

**Changes:**
- `warpaint` no longer consumes a skull. Paint up whenever.
- New characters now start with `auto all`, `brief`, and a real prompt already set. No more blank line on login.

**Combat roster so far:** 24 commands out of stub and working. The PvP suite is filling in.

Server: `7.tcp.ngrok.io:25597` — any MUD client works, Mudlet recommended.

---

## v0.4.0–0.4.2 — 2026-04-25 (launch patch)

🩸 **Devil's Silence Resurrected — Launch**

The resurrection is live. 22 combat commands ported back from the 2003 binary:

`kill` · `flee` · `kick` · `bash` · `trip` · `disarm` · `rescue` · `backstab` · `berserk` · `circle` · `gouge` · `dirt` · `mock` · `spellbane` · `resistance` · `warcry` · `concentration` · `ironwill` · `battlehymn` · `bloodlust` · `warpaint`

Public hosting via ngrok. Friends can connect from any MUD client.
Watchdog auto-restarts the server on crash — we stay up.

Server: `7.tcp.ngrok.io:25597`
