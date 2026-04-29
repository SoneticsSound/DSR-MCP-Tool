# DS:R First-Time User Experience — Helpfile Rewrite Plan

**Goal:** Readable, friendly, concise. Teach the player what they need to
survive the first session. Not encyclopedic — every helpfile should answer
ONE question clearly and point to the next one.

**Tone:** Direct. Short paragraphs. No walls of text. Written for someone
who has played games but never a MUD.

**Format per helpfile:**
- One-line summary of what it covers
- Short explanation (3–6 lines max before first break)
- Syntax block (exact commands)
- One "see also" line

Priority order = most likely to be typed by a new player first.

---

## Priority 1 — NEWBIE (or HELP START)

The first thing a lost player types. Must answer: "What is this and what
do I actually DO?" Written for someone who plays Tarkov, Rust, The Isle,
or any open-world survival/PvP game — they understand risk/reward and
player-driven economies. Meet them where they are.

Draft:
```
Welcome to Devil's Silence Resurrected.

DS:R is an open-world RPG with player-versus-player combat and a
living economy. Think of it like an extraction game crossed with a
classic RPG — you level up, find gear, and choose how deep into
dangerous territory you want to go.

You don't have to PvP. Some players focus entirely on progression,
exploration, and building wealth through PvE content. Others live
for the fight. Both playstyles are valid, and both make the world
work better when they coexist.

The basics:
  - Walk using N S E W U D (north, south, east, west, up, down).
  - Type LOOK to see your surroundings and available exits.
  - Type SCORE to see your character stats.
  - Type SKILLS to see your abilities.
  - Safe zones (like Solennir) are marked SAFE -- you cannot be
    attacked here and cannot attack others.

Good first steps:
  1. HELP CLASSES     -- pick a playstyle that suits you.
  2. HELP GUILDS      -- find your trainer and spend your skills.
  3. HELP AREAS       -- where to go to level up and find gear.
  4. HELP TOWN_CENTER -- where players gather and PvP happens.
  5. HELP COMBAT      -- learn how fighting works.
  6. HELP RECALL      -- how to get back to safety when things go wrong.

See also: HELP CLASSES, HELP GUILDS, HELP AREAS, HELP GEAR, HELP TOWN_CENTER, HELP COMBAT, HELP RECALL, HELP PVP
```

---

## Priority 2 — CLASSES

New players pick a class and have no idea what it means.

Draft:
```
CLASSES

Your class determines your abilities and fighting style.
DS:R has three tiers — you start at tier 1 and your class evolves
as you progress. Current tier 3 classes:

  Warrior paths: Gladiator, Berserker, Paladin
  Rogue paths:   Blade, Ninja, Ranger
  Caster paths:  Mage, Cleric, Voodoo
  Special:       Monk, Morpheous

Each class has unique abilities you learn through SKILLS and TRAIN.
Pick based on how you want to fight:
  - High damage, straightforward:  Berserker, Gladiator
  - Stealth, burst damage:         Blade, Ninja
  - Healing, support:              Cleric, Paladin
  - Debuffs, control:              Voodoo, Mage
  - Combo mastery:                 Monk

See also: HELP SKILLS, HELP TRAIN, HELP COMBAT
```

---

## Priority 3 — COMBAT

The core loop. Must be clear without being overwhelming.

Draft:
```
COMBAT

To attack someone, type:  KILL <target>
To stop fighting, type:   FLEE

During combat your skills fire automatically based on what you have
trained. You can also use abilities manually:

  KICK <target>    BASH <target>    TRIP <target>
  DISARM <target>  STRIKE           BACKSTAB <target>

Most abilities have a cooldown (lag) after use — you cannot spam them.

Your HP, MP, and MV are shown in your prompt:
  <<HP/MaxHP  MP/MaxMP  MV/MaxMV>>

When HP reaches 0, you die. You respawn at your recall point
with a short grace period.

See also: HELP SKILLS, HELP FLEE, HELP DEATH
```

---

## Priority 4 — RECALL

The most important survival command. Lost players need this immediately.

Draft:
```
RECALL

If you are lost or in danger, type:  RECALL TEMPLE

This transports you back to Before The Temple in Solennir — the
central hub of the world. It costs movement points and will not
work if you are in combat. (Use FLEE first, then RECALL TEMPLE.)

From Solennir:
  - 1 south = Town Center (players, shops, bots)
  - North hallway = Guild Hall (trainers for your class)

If recall fails: check your MV (movement points). Rest to recover.

See also: HELP COMBAT, HELP FLEE, HELP MAP
```

---

## Priority 5 — SKILLS / TRAIN

Players need to know how to improve.

Draft:
```
SKILLS

Type SKILLS to see all abilities available to your class.
The percentage shown is your current proficiency.

To improve a skill:  TRAIN <skillname>
  Each train costs one training session (shown on your SCORE).
  You gain training sessions by gaining levels.

To use skills in combat most fire automatically. Some must be
typed manually — see HELP COMBAT for the list.

Type PRACTICE to see how many sessions you have remaining.
Type PRAC ALL to spend all sessions at once (recommended at creation).

See also: HELP COMBAT, HELP LEVEL, HELP SCORE
```

---

## Priority 6 — DEATH

Players panic when they die. This should be reassuring.

Draft:
```
DEATH

When your HP reaches 0 you die. Your equipment drops as a corpse
in the room where you fell.

You respawn at your recall point (Before The Temple, Solennir)
with reduced stats. These recover over time as you rest.

Your corpse:
  - Will decay after roughly 10 minutes.
  - Type  GET ALL CORPSE  to retrieve your gear.
  - A trusted player can retrieve it for you if you cannot reach it.

After death from PvP, a short grace timer prevents immediate
re-engagement. Use the time to re-equip and recover.

See also: HELP RECALL, HELP PVP, HELP EQUIPMENT
```

---

## Priority 7 — PVP

The core of DS:R — must be honest and clear about expectations.

Draft:
```
PVP (Player vs Player)

DS:R is a PvP game. Outside of safe zones, players can attack
each other freely.

Safe zones: Solennir, shops, and areas marked SAFE. You cannot
be attacked here and cannot attack others.

To challenge someone to a duel, the convention is:
  BOW <player>   — a formal challenge. Bow back to accept.

Killing another player flags you as a Player Killer (PK) briefly.
This is normal — it is not a punishment, just a status.

Dying in PvP: your corpse drops in place. You respawn in Solennir.
Your killer does not receive your equipment automatically.

See also: HELP DEATH, HELP RECALL, HELP COMBAT
```

---

## Priority 8 — EQUIPMENT / WEAR

Draft:
```
EQUIPMENT

Type EQUIPMENT (or EQ) to see what you are wearing.
Type INVENTORY (or INV) to see what you are carrying.

To wear something:   WEAR <item>
To remove something: REMOVE <item>
To wield a weapon:   WIELD <weapon>
To get items:        GET <item>   or   GET ALL

Shops in Solennir sell starter gear. Walk south to Town Center
to find merchants.

Most classes require a specific weapon type for some abilities —
see HELP CLASSES for your class's preferred weapon.

See also: HELP CLASSES, HELP SHOPS, HELP COMBAT
```

---

## Priority 9 — MAP / NAVIGATION

Draft:
```
NAVIGATION

Move using direction commands:
  N  S  E  W  U  D   (north south east west up down)

Type LOOK to see your current room and visible exits.
Exits are listed as [N] [S] [E] etc.

Key locations from Solennir (your recall point):
  1S  = Town Center (the main hub for players)
  N   = Guild Hall (trainers)

If you get lost: type RECALL TEMPLE to return to Solennir.
If you are in combat: FLEE first, then RECALL TEMPLE.

See also: HELP RECALL, HELP AREAS
```

---

## Priority 10 — SCORE

Draft:
```
SCORE

Type SCORE to see your character summary:
  - Level, class, race
  - Strength, Intelligence, Wisdom, Dexterity, Constitution, Charisma
  - HP / MP / MV (hit points, mana, movement)
  - Gold, experience, training sessions remaining
  - Active affects (buffs and debuffs)

Type AFFECTS to see only your active buffs and debuffs with
remaining duration.

Type WORTH to see a shorter financial summary.

See also: HELP SKILLS, HELP TRAIN, HELP AFFECTS
```

---

## Priority 11 — LEVEL

The progression loop. New players need to know what they're working toward
and where to go.

Draft:
```
LEVEL

You gain levels by earning experience points (XP) through combat.
Type SCORE to see your current level, XP, and how much you need to
level up (TNL — "to next level").

When you level up:
  - Your HP, MP, and MV increase automatically.
  - You gain training sessions to spend on skills (type TRAIN).
  - Some abilities unlock at specific levels — check SKILLS after leveling.

Where to gain XP:
  Starting out (levels 1–20): hunt mobs near Solennir.
  Mid-game (levels 20–50):    explore surrounding areas.
  Hero range (level 51+):     hero areas with high-value mobs and gear.

Type WHERE to see what mobs are nearby.
Type AREAS to see a list of zones and their level ranges.

At level 51 you become a Hero. The world opens up — better gear,
tougher fights, and access to Town Center PvP at full strength.

See also: HELP AREAS, HELP SKILLS, HELP TRAIN, HELP SCORE
```

---

## Priority 12 — AREAS

The world map in words. Players need to know where to go.

Draft:
```
AREAS

DS:R is an open world. Type AREAS to see a list of all zones,
their level ranges, and the number of rooms.

How to navigate between areas:
  - Use N S E W U D to walk.
  - Type RECALL TEMPLE to return to Solennir instantly.
  - Ask in chat — veteran players know the routes.

Key locations:
  Solennir          The hub. Safe zone. Shops, guilds, Town Center.
  Surrounding areas Hunting grounds for levels 1–50.
  Hero areas        Level 51+ zones. High danger, high reward.
                    Better gear drops here. PvP can happen anywhere
                    outside safe zones.

Hero areas are where the real gear comes from. If you want to
compete in Town Center, you need what those zones drop.

Danger increases the further you go from Solennir. If you are not
sure you are ready for an area, you probably are not. Come back
when your level and gear say otherwise.

Area resets:
  Mobs respawn on a timer when no players are in the area.
  If you cleared a zone and mobs are gone, move to another area
  and come back — they will have reset. Type HELP AREA_RESET for
  more on how this works.

See also: HELP NAVIGATION, HELP LEVEL, HELP PVP, HELP GEAR, HELP TICK, HELP AREA_RESET
```

---

## Priority 13 — GEAR

How to find, wear, and understand equipment.

Draft:
```
GEAR

Equipment makes a significant difference in DS:R. Better gear means
more damage, more survivability, and more competitive PvP.

Finding gear:
  - Mobs drop equipment when killed. Type GET ALL after a fight.
  - Shops in Solennir sell starter gear — walk south to Town Center.
  - Hero areas (level 51+) drop the best equipment in the game.

Managing your equipment:
  EQUIPMENT (EQ)   — see what you are wearing
  INVENTORY (INV)  — see what you are carrying
  WEAR <item>      — equip something
  REMOVE <item>    — take it off
  WIELD <weapon>   — equip a weapon
  GET <item>       — pick something up

Key stats to look for:
  HR / DR    Hitroll and damroll — how often you hit and how hard.
  AC         Armor class — lower is better. Negative = good.
  HP bonus   Flat HP added on top of your base.
  Saves      Resistance to spells and debuffs. Lower is better.

Some classes require a specific weapon type for certain abilities.
Check HELP CLASSES for your class's preferred weapon.

See also: HELP CLASSES, HELP AREAS, HELP COMBAT, HELP SCORE
```

---

## Priority 14 — TOWN CENTER

The PvP hub. Players need to know what it is and why it matters.

Draft:
```
TOWN_CENTER

Town Center is one step south of your recall point in Solennir.
It is the social and competitive heart of DS:R.

What you will find there:
  - Other players — the main gathering spot.
  - Training bots — AI sparring partners named BotWarden, Shade,
    and Fury. Attack them to practice combat without risking death.
    They hit back. They will kill you if you are not careful.
  - Shops and services nearby.

Town Center is NOT a safe zone. Players can attack each other here.
If you are not ready to PvP, stay aware of who is around you.

The bots are there for a reason: use them to learn your abilities,
test your gear, and measure your output before you challenge a
real player. They respawn and reset — fight them as much as you want.

See also: HELP PVP, HELP BOTS, HELP COMBAT, HELP RECALL
```

---

## Priority 15 — GUILDS

Trainers and how to improve your character.

Draft:
```
GUILDS

Your Guild Hall is north of your recall point in Solennir.
Each class has its own guildmaster who trains your abilities.

To improve a skill:
  SKILLS           — see all available abilities and your proficiency
  TRAIN <skill>    — spend a training session to improve a skill
  PRACTICE         — see how many training sessions you have left
  PRAC ALL         — spend all sessions at once (fastest at creation)

Training sessions come from leveling up. The more you level, the
more sessions you accumulate.

Your guildmaster only trains skills available to your class.
Skills not on your list cannot be trained regardless of level.

Some abilities unlock at specific levels — keep leveling even if
your current skills feel maxed out.

See also: HELP SKILLS, HELP LEVEL, HELP CLASSES, HELP SCORE
```

---

## Priority 16 — TICK

Veterans use it as a clock. New players are confused by it. Explain both.

Draft:
```
TICK

The world runs on a timer called a tick. Roughly every 40–60 seconds
the server pulses — this is the tick.

What happens on tick:
  - Your HP, MP, and MV regenerate. Resting speeds this up.
  - Area resets occur for zones with no players in them.
  - Certain buffs and debuffs count down by one tick.
  - A hint message may appear with a gameplay tip.

You will see "You feel a strange sensation." when a tick occurs —
this is normal. Veterans use it to track regen timing.

If your HP/MP/MV are low: find a safe room, type REST, and wait
for a tick or two. You will recover faster than standing.

See also: HELP AREA_RESET, HELP AFFECTS, HELP SCORE
```

---

## Priority 17 — AREA RESET

Critical for new players who clear a zone and wonder where the mobs went.

Draft:
```
AREA_RESET

Mobs in DS:R respawn automatically — but only when no players are
in their area.

How it works:
  1. You clear a zone — all mobs are dead.
  2. Leave the area entirely (move to a different zone).
  3. Wait for a tick (40–60 seconds).
  4. Return — the mobs have respawned and can be killed again.

If you stay in the area, mobs will NOT respawn. You have to leave.
This is by design — it prevents single players from farming a zone
indefinitely while blocking others.

Practical tip: if you are levelling and run out of mobs, move to
a nearby zone, kill a few mobs there, then return. By the time
you come back your original zone will have reset.

See also: HELP TICK, HELP AREAS, HELP LEVEL
```

---

## Deferred (write after core content is live)

- HELP AFFECTS — buff/debuff system
- HELP SHOPS — buying and selling
- HELP COMMANDS — full command reference
- HELP CHAT — communication channels (say yell tell)
- HELP BOTS — the AI sparring partners in Town Center (BotWarden/Shade/Fury)
- HELP HINT — the tick broadcast tip system (verify do_hint exists in command table first)
- HELP WARDANCER — dance system, stance names, storm chain

---

## Implementation notes

- These replace the terse 2003 stubs currently in the DS help system.
- File location: find with `grep -r "NEWBIE\|newbie" ~/ds/recovered/devils/data/`
- Patch via a patcher that finds each helpfile entry by keyword and
  replaces the body — same surgical edit pattern as other patchers.
- Do NOT patch until the gameplay they describe is actually working.
  HELP COMBAT should not reference abilities that are still stubs.
- Write new helpfiles in UPPER CASE for the title, mixed case for body
  (matches DS convention from existing files).
