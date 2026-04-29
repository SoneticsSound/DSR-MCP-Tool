# DS Ideas Log

Feature requests, QoL enhancements, "wouldn't it be cool if…" suggestions
from playtesters, the community, Kyle, or anyone else. Add new entries
at the **top** of the Open list (newest first). Move accepted entries
into Planned when they're scheduled, into Done when shipped, or into
Won't-do with a reason.

## Format

```
### IDEA-NNN: Short title

- **Status:** open / planned / in-progress / done / wontfix
- **Source:** who suggested (name / discord handle / "Kyle" / "Code")
- **Date proposed:** YYYY-MM-DD
- **Complexity:** trivial / small / medium / large / huge
- **Affects:** what part of the codebase

Description of the idea. What it would do. Why it'd be nice. Any
constraints or related ideas. Not a spec — just enough that future-you
remembers what was meant.

**Notes:** evolving thoughts, related discoveries.
**Shipped:** YYYY-MM-DD + reference to where it landed (commit, PR, etc.)
```

Complexity rough-cut:
- **trivial** — < 1 hour, single file, no design questions
- **small** — < half day, one or two files, mostly mechanical
- **medium** — 1–3 days, design + code + test, multiple touch points
- **large** — week+, new subsystem or significant refactor
- **huge** — multi-week, architectural changes, new dependencies

ID numbers monotonic.

---

## Open

### IDEA-043: Mud School — new player tutorial area

- **Status:** open
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** large
- **Affects:** new area file (mud school), world map (connection to guildmaster hallway), creation.c (route new characters here on first login)
- **Related:** FTUE_HELPFILES.md, IDEA-042 (back command), IDEA-009 (starter pack), IDEA-010 (auto-spellup)

A physical in-world tutorial area for players who have never played a MUD.
Teaches through exploration and signs (not autoall popups — autoall is default ON so
channel spam is not the right medium). Progressive, not front-loaded.

**Layout spec:**

```
[ Tutorial wing — 3 to 4 rooms per topic ]
  Room 1–4:   Movement (N/S/E/W, LOOK, exits)
  Room 5–8:   Commands (SCORE, SKILLS, INV, EQ, WHO)
  Room 9–12:  Combat basics (attack, flee, recall, safe zones)
  Room 13–16: DS:R premise (PvP economy, Grace/Souls, no mandatory PvP)

[ 5x5 Levelling field — 25 rooms ]
  Populated with copies of levelling-area NPCs (low-mid level, fast respawn)
  Purpose: new players can hit Hero quickly without needing to navigate the world
  Sign at entrance explaining what it is

[ Exit ]
  Central-north room of the field → guildmaster hallway → 1 south of recall temple
```

**Sign system:** Each tutorial room uses an in-room sign object (readable via LOOK
SIGN or EXAMINE SIGN) rather than on-enter messaging, so it works with autoall ON
and doesn't spam players who walk through multiple times.

**Mob source:** NPC copies from existing levelling areas (sprite.are vnums 100–149
is a natural reference — Alecca's level 1–30 area). Mud school mobs should be
statted slightly easier than their source counterparts — this is practice, not a
challenge.

**Vnum range:** TBD — needs to not collide with existing areas. Check SOURCE_INDEX.md
for available ranges before authoring.

**Connection:** Exit from mud school field (central north) connects to the room
1 north of guildmaster hallway, which is 1 south of recall temple. New characters
should be routed here automatically on first login before reaching Solennir.

**Note:** FTUE_HELPFILES.md covers the helpfile layer of the same onboarding goal.
Mud school is the *in-world* complement — players who ignore help files still get
taught by walking through the rooms.

---

### IDEA-042: Character creation `back` command

- **Status:** open
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** medium
- **Affects:** creation.c (character creation state machine)

At each step of character creation (race, class, customization), the player should be
able to type `back` to return to the previous step rather than being forced to
disconnect and reconnect. Discovered during BUG-020 QA — chose a race incompatible
with Sensei to test the gate (gate works correctly), but then had no way to back out
without quitting.

Each creation phase needs to track state so `back` pops to the prior prompt cleanly.
Affects at minimum: race selection, class selection, any stat/customization steps.
Low urgency but high quality-of-life, especially during testing and for new players
who misclick a choice.

**Prompt display requirement:** Every creation prompt must explicitly list available
commands at the bottom, e.g.:

```
  Enter a race, or type 'list' to see all options.
  Type 'back' to return to the previous step.
```

Currently nothing in the prompts hints at navigation options — players have no way
to know commands exist unless told. This applies to ALL creation steps even before
`back` is implemented (list, help, etc. should also be surfaced).

---

### IDEA-041: PVP/Economy system — Essence, Grace, Souls (name TBD)

- **Status:** planned — POST-RESTORATION, Phase 2
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** huge
- **Affects:** fight.c, handler.c, db.c, save.c, clan system, new vendor NPC, new pfile fields

Full design in VISION_PVP_ECONOMY.md. Do not implement until core class restoration and skill ports are stable.

Three-archetype economy: Default (no flag, no loot), Essence Farmer (PVE opt-in, earns Grace buffer + lootable), Soul Collector (PVP opt-in, earns Souls from kills, can loot Grace players). Grace is a TTK modifier on top of Sanctuary powered by mob-kill Essence. Souls buy access from a personal vendor. Essence transfers on death to killer's clan pool. No stat inflation for PVP players — Souls buys access, not power.

**Name needed** — working title "Grace/Chaos system" but needs a proper in-world name. Candidates: Alecca's Covenant (ties to existing "Alecca's Grace" buff name), The Reckoning, The Tribute, The Offering. Kyle to decide.

**Open design questions** (from VISION_PVP_ECONOMY.md):
- Loot scope: all items or worn vs. carried split?
- Default players in clans: do they contribute to clan Essence pool?
- Souls vendor location: Solennir, clan hall, or both?
- Paradox interaction: does Grace modifier change during paradox events?
- New player tutorial hook: veteran NPC or helpfile explaining the system at level 30–40?

**Notes:** Prototype path is ~400–600 lines across fight.c, handler.c, db.c. MVP needs 8 steps listed in VISION_PVP_ECONOMY.md. Wardancer/Seer Grace cap may need to be lower than other classes to prevent evasion-stacking.

---

### IDEA-040: Zone level tiering — proximity = difficulty + gear quality

- **Status:** open
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** large
- **Affects:** area files (mob levels, reset tables), gear tuning, world map design

Closer areas (shorter travel from start) should be lower level and act as levelling zones.
Further areas should be hero-tier with appropriately scaled mobs and better gear rewards.
This creates a natural progression loop: level up → push further out → find better gear.

**Restring pass (tied idea):** All world gear should eventually be restrung for visual appeal —
cool color schemes and evocative names make gear worth farming. The cosmetic layer is part
of the reward loop. Items that look good feel like achievements. Priority after balance pass.

**Notes:** Gear set catalogue (gear_sets.html/pdf) is the reference for what's out there.
AQ veteran sets (IDEA-039) are the 100 AQP floor. Restring work should start with hero-area
BiS pieces since those have the most player visibility.

---

### IDEA-039: AQ Veteran Gear Sets — 100 AQP purchasable starter/veteran gear

- **Status:** done
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** trivial
- **Affects:** quest.c (reward_table)

17 pieces covering all major slots (head/body/about/arms/hands/legs/feet/shield/waist/
neck/finger/wrist/ankle/ear/mark/face/eye) at 100 AQP each. Top HR+DR non-QEQ items
from the world gear catalogue. Lets returning/new heroes skip the farm grind and get
into PVP quickly. Keywords set for `quest buy <slot-keyword>`.

**Shipped:** 2026-04-29 — quest.c reward_table, above the NULL sentinel.

---

### IDEA-038: Rabbit / Skunk / Leech stances — implement as new monk stances

- **Status:** planned
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** small
- **Affects:** act_combat.c (do_stance keyword switch + stance_table), fight.c (stance switch block)

Three stances stubbed/absent in 2003 binary. Design decided 2026-04-29 — see CODE_HANDOFF.md
"Stance designs — rabbit / skunk / leech" section for full spec. Summary:
- **Leech**: HP lifesteal per hit (dam/5). Mirrors WEAPON_VAMPIRIC but always-on.
- **Skunk**: applies plague/rot debuff on hit, attrition stance.
- **Rabbit**: per-round bonus attack chance (NOT full AFF_HASTE — too strong). Optional small AC penalty while active.

---

### IDEA-037: `time` — add formatted uptime line

- **Status:** open
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** trivial
- **Affects:** act_info.c (do_time only)

`do_time` already prints "Devil's Silence started up at X" and "The system time is Y" but makes
the player do the math. Add a third line computing the duration: "Uptime: 2 days, 4 hours, 17 minutes."
`str_boot_time` and `current_time` are both available in the function — just subtract and format.
One sprintf line.

**Note:** IDEA-033 (tick visibility via weather) is the bigger tick-awareness fix. This is the
quick one-liner that should ship first.

---

### IDEA-036: Stance system — confirmed from source (2026-04-29)

- **Status:** open
- **Source:** Kyle (2026-04-29)
- **Date proposed:** 2026-04-29
- **Complexity:** medium (do_stance in disasm queue, 1479b)
- **Affects:** fight.c (weapon flags live), bit.h (slots confirmed), const.c (stance_table confirmed)

**CONFIRMED FROM SOURCE** — all 9 stances exist in bit.h and fight.c. Slot numbers confirmed,
no gaps. Weapon flag mappings recovered directly from fight.c:

| Stance   | Slot | Weapon Flag(s)                   |
|----------|------|----------------------------------|
| Dragon   | 1    | WEAPON_SHOCKING                  |
| Crane    | 2    | WEAPON_VORPAL                    |
| Scorpion | 3    | WEAPON_POISON                    |
| Leopard  | 4    | WEAPON_FROST                     |
| Phoenix  | 5    | WEAPON_FLAMING                   |
| Monkey   | 6    | WEAPON_ROTTING                   |
| Rabbit   | 7    | WEAPON_ACCURSED                  |
| Leech    | 8    | WEAPON_OSMOSIS + WEAPON_VAMPIRIC |
| Skunk    | 9    | WEAPON_JINX                      |

`do_stance` itself is in the disasm queue (1479b at 0x08058b64) — mana costs and any
stat/evasion bonuses are unknown until ported. Combat hook (weapon flag injection in
fight.c) is already live in recovered source. Helpfile drafted — see HELP_STANCES.md.

---

### IDEA-035: `eq <slot>` — show single wear location instead of full equipment list

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial
- **Affects:** `do_wear` or `do_equipment` in `act_obj.c`

When `eq` is typed with a slot argument (e.g. `eq head`, `eq wrist`, `eq finger`), show only what's equipped in that slot rather than the full equipment list. Useful for quickly checking a specific slot mid-session without scrolling through the whole list.

Valid slot names should match the standard wear location names: head, neck, body, about, arms, hands, wrist, waist, legs, feet, finger, shield, hold, float, wield, patch (and any DS customs like ear, eye, face, ankle if present).

No argument: existing behavior (full list) unchanged.

---

### IDEA-034: Guardian `track` — pathfind toward target with movement speed bonus

- **Status:** open — defer until BFS pathfinding (Priority 8) is complete
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** medium (depends on BFS infrastructure)
- **Affects:** `do_track` in act_move.c or act_combat.c, Guardian class only

When a Guardian uses `track <target>`, it auto-walks to the **area entrance** of
whichever area the target is currently in — not directly to the target's room.
The Guardian arrives at the area's starting point (same entry room the travel system
uses as its BFS destination). From there they hunt manually. Movement speed doubled
while tracking. Within 3 rooms of the destination, behavior changes (exact mechanic
unclear from 2003 — possibly speed bonus drops, or switches to direction-only
display). Kyle's memory on the 3-room threshold is fuzzy — investigate disasm.

**Design notes:**
- This is a Guardian identity feature — fast pursuit is their thing. Ties into the
  PvP risk/reward ecosystem: track makes recalling (and the travel cooldown reset)
  more meaningful, since a Guardian can pursue anyone who doesn't make it out.
- BFS infrastructure from Priority 8 (pathfind + mpwalk) is the natural foundation.
  Don't port this until `do_pathfind` and the mob walk system are working.
- The 3-room threshold likely uses a BFS depth check — trivial once BFS is in.
- Movement speed bonus: either halve the move cost per step, or fire two steps per
  pulse. Check how haste interacts with movement to pick the right approach.
- Guardian exemption from travel cooldown (already in do_travel) is thematically
  consistent with this — Guardians are the pursuit class.

---

### IDEA-033: Tick visibility via weather flavor text

- **Status:** open — preferred implementation
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial
- **Affects:** `weather_update()` in `update.c`, outdoor room check

Piggyback on the existing weather system to give players a passive tick clock. Every tick, fire one weather-appropriate flavor line to all outdoor characters. No new UI, no command — just ambient world feedback that doubles as a tick signal.

**Implementation:**
- In `weather_update()`, after updating weather state, iterate all chars.
- For each char in an outdoor room (not `ROOM_INDOORS`, not `IS_NPC`), send one line.
- Pick flavor based on current `weather_info.sky` state:
  - `SKY_CLOUDLESS` — "A warm breeze drifts through the air.", "Sunlight falls across the land.", "The sky stretches clear and still overhead."
  - `SKY_CLOUDY` — "Clouds drift slowly overhead.", "The wind picks up for a moment, then settles.", "A gust stirs the treetops."
  - `SKY_RAINING` — "Rain patters steadily around you.", "A cold drop finds the back of your neck.", "The rain hisses softly against the ground."
  - `SKY_LIGHTNING` — "Distant thunder rolls across the sky.", "Lightning flickers on the horizon.", "The storm churns overhead."
  - Snow/cold variants if DS has seasonal weather states.
- Rotate through flavor strings per state (use a static index or `number_range`) so it doesn't repeat the same line every tick.
- Indoors: no message fires. Underground rooms: no message. Already-sleeping chars: skip or send anyway (your call).

**Why this works:** Players get a natural rhythm without any new system. It also adds life to outdoor areas that currently have no ambient feedback between combat events.

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial–small
- **Affects:** `act_info.c` (new command) and/or prompt system

In-game time (day/night cycle) advances on a separate pulse from the actual tick (`char_update`). They're related but not the same — a tick fires on `PULSE_TICK` intervals regardless of in-game time. Kyle wants some way to feel ticks passing without guessing.

**Options (pick one or combine):**

1. **`tick` command** — prints time elapsed since last tick and estimated time to next. ROM already tracks `pulse_tick` globally; simple subtraction gives time remaining. Trivial to add.
2. **Prompt variable** — add a `%T` or `%k` prompt tag showing ticks elapsed since login, or current tick count mod N. One extra field in the prompt formatter.
3. **Broadcast on tick** — already partially covered by Bundle A+ (hint system investigation). If the hint system fires on tick, that's a natural clock. Restore it and populate with FTUE tips.
4. **`time` command enhancement** — the existing `time` command shows in-game day/hour. Add a line showing real-time tick interval (e.g. "Next tick in approximately 34 seconds.").

**Note:** The hint system (Bundle A+ in COWORK_PROMPT.md) is worth investigating first — if it broadcasts every tick, that already solves the visibility problem and adds FTUE value at the same time. Add the `tick` command only if the hint system isn't present or is disabled.

---

### IDEA-032: `do_assassinate` — flavor text when attacking a pre-tagged target

- **Status:** open
- **Source:** Kyle (2026-04-28, playtest)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial
- **Affects:** `do_assassinate` in `act_combat.c`

When a victim already carries `AFF2_ASSASSINATE` and you assassinate them again, you just get regular attacks with no special messaging. Should probably have a brief line acknowledging the exposed weakness is already being exploited — something like "You press the advantage on $N's exposed weakness!" or similar. Low priority, cosmetic.

---

### IDEA-031: `ROOM_CHAOTIC` flag — warzone/arena rooms bypass pktimer brake on openers

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** small
- **Affects:** `merc.h` room flags, `do_assassinate` (and any other opener with a pktimer brake), area files

New room flag `ROOM_CHAOTIC` (or `ROOM_WARZONE`) that designates a room as a free-PK zone where pktimer-active players can still use openers like assassinate. Restores the 2003 carve-out from the disasm.

**Initial areas to flag:**
- wararena.are, newarena.are, endarena.are, kingofhill.are, battle.are, tournament.are
- quest.are (confirmed by Kyle — used for team arenas)

**Design notes:**
- Reusable across any opener that has a pktimer brake — add the `ROOM_CHAOTIC` check once in each gated skill rather than duplicating logic.
- Could also suppress the PK registration requirement (registerpk) in these rooms — if you're in a warzone, consent is implied.
- Longer term: tie into IDEA-023 (PvE/PvP opt-in toggle) — chaotic rooms could auto-flag both parties as PvP for the duration.

---

### IDEA-030: `area` command — sort by name and filter by level for new players

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial–small
- **Affects:** `do_areas` in `act_info.c`

Two quality-of-life improvements to the `area` command output:

1. **Sort alphabetically** — currently areas list in load order (area.lst order). Sort by `area->name` before printing so players can scan the list quickly.
2. **Level filter** — area headers already contain level ranges entered by the original builders (quality varies — treat as approximate). Hide areas whose min level exceeds the player's current level. Intended to reduce noise for new players, not to wall off content from veterans.

**Design notes:**
- Use the existing level range fields in area headers directly. Don't gate on anything else — if the builder left them blank or wrong, that's a data problem to fix separately.
- **Do not filter helpfiles.** `help <area name>` should always work regardless of player level — if they already know it's there and look it up, show it. The filter is only for the `area` browse list.
- IMMs/admins see the full unfiltered list regardless.
- `area all` argument overrides the filter — lets any player browse above their range if they want to.
- Ties into `travel list` (IDEA-027) — same filter logic could apply there too.

---

### IDEA-029: `blinding strike` — add small visible damage component

- **Status:** open
- **Source:** Kyle (2026-04-28, playtest observation)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial
- **Affects:** `do_blinding_strike` in `act_combat.c`

The 2003 port uses `damage(2-5 HP, DAM_NONE, show=FALSE)` — the hit is intentionally cosmetic (debuff delivery, not a damage skill). In practice this means the skill fires with no visible damage number, which can feel like a miss even when it lands.

**Options:**
- Switch `show=TRUE` so the standard damage banner fires (tiny number but visible confirmation).
- Or add a separate `DAM_BASH` hit (say `1d4`) with `show=TRUE` alongside the existing hidden hit.
- Or leave as-is — the AFF_BLIND message already confirms it landed. Low priority, more feel than function.

---

### IDEA-028: ASCII map — render a radius of rooms around current position

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** medium
- **Affects:** new `do_map` in `act_info.c`, BFS scratch fields on `ROOM_INDEX_DATA`

A `map` command (or `map <radius>`) that flood-fills outward from the player's current room up to N steps and renders a 2D ASCII grid showing connected rooms, exits, and the player's position.

**Example output (radius 2):**
```
     [ ]
      |
[ ]-[ ]-[ ]
      |
     [*]       <- you are here
      |
     [ ]
```

**Design notes:**
- BFS infrastructure already exists on `ROOM_INDEX_DATA` (`bfs_tag`, `bfs_pvnum`, `bfs_pdir`) from the travel system — reuse the same flood-fill for the radius scan.
- Only N/S/E/W exits map cleanly to 2D. Up/Down could be indicated with a `U`/`D` marker inside the room bracket rather than a spatial direction.
- Room coloring possibilities: current room highlighted, rooms with mobs present in red, safe rooms in green, unexplored (known exit but never entered) dimmed.
- Default radius probably 3–4. IMMs could get a larger cap.
- Sector type could influence the room character — `[~]` for water, `[^]` for mountain, `[ ]` for indoor, etc.
- Blind/dark room handling: either blank the map or show only the current room.

**Longer term:**
- Tie into `visited_areas[]` — grey out rooms the character has never entered vs. rooms they've passed through.
- The coordinate/layout data built here feeds directly into IDEA-022 (Mudlet automapper) and IDEA-016 (Unreal client map layer). Build it once, reuse the room-position logic everywhere.

---

### IDEA-027: `travel map` — list visited areas the character knows how to reach

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial
- **Affects:** `do_travel` in `act_move.c`, `visited_areas[]` on PC_DATA

When a player types `travel` with no argument (or `travel map`), display a formatted list of every area in their `visited_areas[]` array — the areas they have walked to and can now fast-travel back to. Currently `do_travel` with no arg shows a usage hint; this would replace or extend that with the actual visited list.

**Notes:**
- Data is already there — `visited_areas[256]` stores area min_vnums, `num_visited` is the count. Just needs a display loop that resolves each vnum to its area name.
- Could sort alphabetically (pairs with IDEA-026 spirit) or by order visited.
- Flavor angle: frame it as the character's mental map — "You recall the paths to the following lands:" — fits the travel-as-knowledge concept.
- Natural companion to the `help travel` helpfile already written.

**Travel system design intent:**
Travel is a time-gated convenience — it lets a player move area-to-area without
recalling through TC first. The 10-tick cooldown is the tax for skipping that
exposure. A player who recalls instead pays with TC vulnerability (visible, resting,
catchable); reward that by resetting their cooldown on successful recall. Do not
erode this tradeoff — it gives TC relevance and makes travel a meaningful choice.

---

### IDEA-026: Alphabetize the `commands` output

- **Status:** open
- **Source:** Trikeri (community member, 2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** trivial
- **Affects:** `do_commands` in `interp.c` or `act_info.c`

Sort the commands list alphabetically so players can scan it predictably rather than getting whatever order the `cmd_table` happens to be in. Right now the list reflects the order commands were added to `cmd_table`, which is meaningful to the developer and meaningless to the player.

**Notes:**
- `cmd_table` itself shouldn't be reordered — binary searches or index assumptions may depend on its current layout. Instead, build a temporary sorted copy of visible command names for display only.
- Simple approach: collect all visible command names into an array, `qsort` with `strcmp`, print the sorted array. No changes to command lookup logic.
- Pairs well with IDEA-001 (grey out unusable commands) — both are display-only changes to the same output. Could ship together as one small patch.

---

### IDEA-025: Area reorganization — tiered by distance, difficulty, and gear meta

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** huge (design + audit + world edits)
- **Affects:** all .are files, area.lst, AREAS helpfile, world graph

**Design vision:**

Distance from Town Center should map to danger. The further you walk from
TC, the harder it gets. This creates natural PvP hunting lanes — heroes
chasing levellers have to travel with them, and levellers grinding toward
hero are visibly vulnerable the whole way.

**Three tiers:**

| Tier | Level range | Distance from TC | Gear meta | Notes |
|---|---|---|---|---|
| 1 — Easy | 1–30 | Close, 1–5 rooms | Level 30 camper gear | Safe-ish. XP lockers camp here. Heroes can hunt but it's risky close to TC. |
| 2 — Medium | 31–85 | Mid-range | Level 85 grind gear | The vulnerable stretch. Heroes actively hunt here. High tension zone. |
| 3 — Hard | 86–Hero | Far out, hard to navigate | Best gear in game, multiple items per mob | Hero-only. Multiple valuable drops. Long walk = more exposure. |

**Gear meta intention:**
- Level 30 campers: full tier-1 gear set available in nearby areas
- Level 85 campers: full tier-2 set in mid areas — reward the grind
- Hero: best-in-slot gear spread across hard areas, no single farm spot

**Area audit needed:**
Many original DS areas made no sense geographically or difficulty-wise.
Some hero-level mobs were minutes from TC. Some low-level areas were deep
in the world. All areas need to be categorized:
- Easy / Medium / Hard navigation (maze-like vs. linear vs. open)
- Appropriate mob level range
- Gear quality vs. intended tier
- Distance from TC adjusted if needed (exit wiring changes, not area moves)

**XP lock meta acknowledgment:**
Players will XP lock at 30 and 85 intentionally. This is not a bug —
design around it. Level 30 campers griefing levellers is part of the
tension. Tier 2 is the dangerous grind precisely because heroes are
hunting AND 30-campers are griefing from below.

**Notes:** This is a multi-week design + world editing project. Start with
the audit spreadsheet — categorize all 80+ areas before touching anything.
`build_world_graph.py` output + `AREAS` in-game list is the starting data.
Cowork can generate the audit template when ready.

---

### IDEA-024: Player count in Discord server status post

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** small
- **Affects:** ds_status_bot.py, possibly a MUD-side player count export

Show live player count in the Discord status embed alongside UP/DOWN.
Implementation options (simplest to most robust):
1. MUD writes player count to a temp file on tick — bot reads it.
   Requires a small C change to `update.c` to write `/tmp/ds_playercount`.
2. Bot does a lightweight telnet probe and parses WHO output — no C changes
   but fragile if WHO format changes.
3. Bot reads a named pipe or socket the MUD writes to.

Option 1 is cleanest. Embed would show:
  🟢 Devil's Silence Resurrected — ONLINE
  3 players connected · Last checked: Mon Apr 28, 7:05 PM

**Notes:** Defer until VPS migration — temp file approach works on same
machine but needs path coordination if bot and MUD ever run separately.

---

### IDEA-023: PvP toggle — opt-in points mode

- **Status:** open
- **Source:** Kyle (2026-04-28)
- **Date proposed:** 2026-04-28
- **Complexity:** large
- **Affects:** new flag on CHAR_DATA, combat.c, fight.c, economy layer

Opt-in mode where players choose whether their kill/death stats count. You remain attackable either way — this is not a safety flag. It's a stakes flag.

**Core mechanic (Kyle confirmed 2026-04-28):**
- Toggle PvP "on" → your kills and deaths record to the leaderboard/pk records
- Toggle back to PvE → your points **reset** — you made the choice to farm instead
- No damage modifiers. No invulnerability. Just whether your stats count.
- Visible in WHO list so everyone knows what mode you're in.

**Design intent:** Forces a meaningful choice. You can farm safely (stats don't count, no pressure) or compete (stats count, you're invested). Switching back costs your record — the stakes feel real without making anyone unkillable.

**Toggle rules:**
- Cannot toggle in combat
- Toggle cooldown TBD (probably a few ticks to prevent rapid flipping)
- Visible on WHO and SCORE

**Notes:** Much simpler than the original sanctuary-style idea. No damage math changes needed — just a flag on PC_DATA and a kill/death recording gate. Low implementation cost, high design clarity. Pairs naturally with PK registration concept from Leto's original changelog (registerpk at City Hall) — could reuse that framing for flavor.

---

### IDEA-022: Mudlet profile package + Lua client framework

- **Status:** open
- **Source:** Kyle (2026-04-27)
- **Date proposed:** 2026-04-27
- **Complexity:** medium (profile build) / ongoing (feature additions)
- **Affects:** new `ds_profile/` folder in workspace, distributable `.mpackage` file, eventual Electron client

Mudlet's Lua framework as an intermediate client layer before a full custom client. Distributable as a `.mpackage` file — players install Mudlet once, import the package, and get DS pre-configured. Features to implement in priority order:

**Tier 1 — ship immediately:**
- HP/MP/MV gauge bars parsed from Kyle's prompt format `<<%h/%Hhp %m/%Mmp %v/%Vmv $%pp/%gg>>`. ~20 lines of Lua, visual health readout in a sidebar.
- Combat text highlighting — red for incoming damage, green for your hits, yellow for misses. Makes fights readable.
- Auto-connect to DS ngrok address on launch.

**Tier 2 — high value:**
- Automapper seeded from `world_graph.json` — entire DS world pre-mapped so players open Mudlet and the map is already there. Mudlet's mapper API stores vnums natively.
- Channel routing — pull yell/say/tell/gossip into separate mini-windows so combat doesn't scroll chat.
- Buff/affect timer tracking — parse `affects` output, display active buffs with countdowns. Alert when bloodlust/haste drops.
- PK flag detection — visual warning + sound on PK flag trigger.

**Tier 3 — depth features:**
- Combat rotation keybinds — F1–F8 mapped to bash/kick/trip/disarm/strike etc.
- Death stats tracker — kills/deaths/K:D per session in a sidebar widget.
- Session logging with timestamps.

**Sound layer (most relevant to Kyle's Wwise background):**
Mudlet's `playSoundFile()` can trigger audio on any text pattern match. This maps directly to Wwise play events — one trigger per game event (combat start, death, level up, zone entry, low HP alert). Design the reactive audio system here first in Lua, then port the event map to Wwise when the Unreal/Electron client is ready. The trigger logic is the same; only the audio engine changes. This is a genuine portfolio piece — nobody is doing Wwise-style reactive audio in the MUD client space.

**Eventual path:**
Mudlet profile → Electron app (xterm.js + Node telnet, custom branding, EXE via electron-builder) → full custom client with rendered map and Wwise integration. The Lua trigger logic and event map developed in Mudlet informs the Electron and Wwise design directly.

**Notes:**
- Mudlet is free, open source, cross-platform. Profile package is a single file to share.
- The automapper seed from `world_graph.json` is the killer feature — no other DS client will ship with the full world pre-mapped.
- Sound triggers are the design prototype for Stage 1 of IDEA-016 (Unreal/Wwise port). Build them here, document the event map, reuse it later.
- Related: IDEA-011 (browser web client), IDEA-016 (Unreal/Wwise port path).

---

### IDEA-021: Ability tuning / buff pass — make weak abilities worth using

- **Status:** open
- **Source:** Kyle (2026-04-27)
- **Date proposed:** 2026-04-27
- **Complexity:** medium (per-ability, iterative)
- **Affects:** `act_combat.c` (damage formulas, wait states, secondary effects per ability), balance spreadsheet from IDEA-019

Some ported abilities are technically correct — the disasm matches — but the 2003 tuning makes them nearly useless in actual play. `do_cleave` is the canonical example: it deals moderate damage with no secondary effect, a notable wait state, and no situational advantage that would make a player choose it over auto-attacks. Getting ported faithfully doesn't mean getting tuned well.

The goal of this idea is a deliberate pass over every ported ability after the stress-testing phase (IDEA-018) surfaces actual numbers, asking: "Would a player actually use this? If not, why not, and what would make it worth a slot?"

**Design principles for the tuning pass:**
- Every ability should have a clear answer to "when do I use this?" — a niche, a matchup, a situation. If the answer is "never," the ability needs work.
- Damage-only abilities at low numbers are almost always traps. If an ability deals 40 damage and applies no status, it needs either significantly more damage OR a meaningful secondary effect to compete with auto-attacks.
- `do_cleave` specifically: consider adding a defensive debuff on the target (reduce their parry/dodge for 1–2 rounds), or a positioning effect (breaks their combat stance), or simply scaling the damage formula more aggressively. A two-handed weapon requirement with real damage upside would give it an identity.
- Secondary effects (stun chance, stat debuff, position change, affect strip) are more interesting than raw damage bumps — they create decision points.
- Wait state (lag) is a hidden cost players feel even if they don't calculate it. Abilities with high lag need proportionally higher payoff.

**Process:** run each ability through IDEA-019's balance framework, then tune formula constants (not logic) via patcher scripts. Logic stays faithful to disasm; numbers are a design call.

**Notes:**
- Do NOT tune during porting. Port accurately first, tune in a dedicated pass after stress testing gives real data.
- Tuning is cosmetically invisible to the disasm — just changing constants in C expressions, not restructuring control flow.
- Related: IDEA-015 (affect visibility) should land before tuning so players can actually perceive what secondary effects are doing.
- Cleave is the first candidate but almost certainly not the last. Build the tuning pass as a repeatable process, not one-off fixes.

---

### IDEA-020: Accessibility — contextual error messages with requirements

- **Status:** open
- **Source:** Kyle (2026-04-27)
- **Date proposed:** 2026-04-27
- **Complexity:** small (per-ability, iterative)
- **Affects:** `act_combat.c` gate/reject paths, `interp.c` level-gate message, helpfile references

Right now when a player can't use an ability, they get a generic rejection: "You can't do that." or "You don't have that skill." These messages tell the player nothing. What they need to know is *why* and *how to fix it*.

**Examples of what this looks like in practice:**
- `garotte` with no whip equipped → currently just "You need a whip for that." — should also add "Type `help garotte` for more." or "A whip must be wielded in your main hand."
- `cross slash` with only one weapon → name both slots: "You need weapons in both hands for cross slash."
- `gore` with no gore skill → "That ability requires a race with natural horns. Type `help gore` to see which races qualify."
- Ability that requires FIGHTING position when standing → "You need to be in combat first. Attack someone with `kill <target>`."
- Level gate → "You need to be level X to use that." (stock ROM does this; confirm DS hasn't stripped it)

**Scope:** this is not a one-shot patch. It's a standard to apply progressively — each new ability port and each tuning-pass visit is an opportunity to improve the rejection string at that callsite. Build a short style guide for what a good error message looks like and apply it during each pass.

**Helpfile hook:** every ability's rejection path should end with "Type `help <command>` to learn more." even if the helpfile is still the 2003 stub. That plants the expectation that `help` is useful — then IDEA-015's helpfile rewrite pays off.

**Notes:**
- This is deliberately scoped as "small per-ability" — it's ongoing polish, not a dedicated sprint. Treat it as a code quality standard, not a feature.
- The most impactful targets are the weapon-requirement gates (garotte, cross slash, cleave) and the race/class gates (gore, katana) — those are the ones new players will hit first and bounce off.
- Related to IDEA-015 (affect visibility and helpfile rewrite) — complementary but distinct. IDEA-015 is about *during* combat. IDEA-020 is about *entry to* combat abilities.

---

### IDEA-019: Balance planning framework — metrics, spreadsheet, process

- **Status:** open
- **Source:** Kyle (2026-04-27)
- **Date proposed:** 2026-04-27
- **Complexity:** medium (framework design) / ongoing (usage)
- **Affects:** new `BALANCE.md` reference doc, stress test data (IDEA-018), tuning pass (IDEA-021)

Before tuning any ability, establish what "balanced" means for DS. Without a framework, every tuning decision is a guess that creates a new problem somewhere else.

**What the framework needs to answer:**
1. What is the expected DPS of a max-level character in a typical fight?
2. What is the expected TTK (time-to-kill) in a 1v1 between two max-level characters of similar class?
3. What is the expected contribution of a single ability use vs. an auto-attack round?
4. What proc rates feel good vs. feel broken? (e.g. a 25% stun proc on a 2-second wait ability is very different from 25% on a 0-lag ability)

**Deliverables:**
- `BALANCE.md` — a reference document with the above targets set as design goals, updated as we learn more from playtesting.
- A spreadsheet (xlsx) tracking each ported ability: damage formula output at level 10/50/101, wait state, secondary effect and proc rate, and a "role" tag (damage, debuff, utility, opener, finisher). Built from SKILL_TABLE.md + disasm findings.
- A process for the tuning pass: stress test → measure → compare to targets → adjust constants → re-test.

**Notes:**
- Don't set targets before stress testing (IDEA-018). The targets should be informed by what the current system actually produces, not invented from first principles.
- The TTK question is the most important one for PvP balance. Everything else flows from it.
- This framework is the prerequisite for IDEA-021 (tuning pass) being principled rather than arbitrary.
- Rex's note on daze (IDEA-015) is the right instinct: reduce variance first, *then* tune the mean. High-variance abilities are impossible to balance because their effective proc rate varies wildly in practice.

---

### IDEA-018: Bot players and automated stress testing

- **Status:** open
- **Source:** Kyle (2026-04-27)
- **Date proposed:** 2026-04-27
- **Complexity:** medium
- **Affects:** new Python bot script(s), potentially a `bots.are` or spec_fun extension on existing dummies (IDEA-005)

Two related goals bundled together: automated stress testing (can the server handle N concurrent connections without degrading?) and scripted bot players (can we simulate real player behavior for balance measurement?).

**Stress testing:** a Python script that opens N simultaneous telnet connections, logs in with pre-created test accounts, and runs a scripted combat loop for a set duration. Captures: connection stability, server tick rate under load, whether any SIGABRT triggers appear under sustained combat (BUG-001 investigation angle), and whether memory footprint grows unboundedly (leak check).

**Bot players for balance data:** bots that fight each other in a controlled environment — two max-level characters of specified classes, each using their class's full ability rotation, for N rounds. Script captures damage dealt per round, TTK, which abilities fired how often, and whether any ability is never chosen by the rotation. This is the stress-test data that feeds IDEA-019's balance framework.

**Dummy extension (vs IDEA-005):** IDEA-005's dummies are passive — they stand there and take it. Bots are active — they fight back, use abilities, and expose timing/priority bugs that passives can't catch. Both are needed. The dummies validate individual abilities; the bots validate the system under real combat conditions.

**Implementation path:**
1. Start with the stress test script — just N connections doing `kill dummy` in a loop. This is 1–2 hours of Python.
2. Extend to a basic rotation bot once the stress test is stable.
3. Add per-class rotation logic when there's enough abilities to make it meaningful.

**Notes:**
- Requires IDEA-005 (test dummies) to be live first so bots have something to fight.
- Bot accounts need to be pre-created with imm-set skills at 100% and max level to eliminate skill-training variability from the data.
- The stress test alone is useful immediately after the Phase B combat port sprint finishes — run it before the server goes wider public.

---

### IDEA-017: Class bug fixing phase — post DS Custom sprint

- **Status:** open
- **Source:** Kyle (2026-04-27)
- **Date proposed:** 2026-04-27
- **Complexity:** medium (scope unknown until classes are playable)
- **Affects:** class-specific paths in `act_combat.c`, `const.c`, `creation.c`, `fight.c`, `update.c`

Once the DS Custom sprint finishes (all non-Psionic abilities ported), every class will have its full ability set active for the first time since 2003. That's the moment class-specific bugs become visible — interactions that couldn't surface while abilities were stubs.

**What to expect:**
- Class abilities that compile and run but interact incorrectly with each other (e.g. a stance that assumes a resource pool that `update.c`'s stock tail doesn't regenerate).
- Monk chi / wind resource not regenerating because the DS-specific regen code is in the missing `update.c` tail.
- Voodoo curse timing bugs — durations wrong because the DS tick layer is gone.
- Psionic elemental type interactions with resist/vuln tables — these were complex in 2003 and probably have edge cases.
- Race-gated abilities (gore, katana, eadbutt) firing incorrectly for off-race characters who got skills via imm `set`.

**Process:** dedicated playtesting session per class after DS Custom lands. Each class gets run through its full ability set against the test dummies (IDEA-005) and one live opponent. Bugs go to BUGS.md; fixes are batched per class rather than per ability.

**Notes:**
- Rex owns Morpheous — his bug reports from that class are the model for how this process should work.
- The Monk suite is probably the most fragile: `multi_kick` calls eight `monk_*` helpers, and if any one of them has a bad secondary effect, the whole suite is suspect.
- Psionic bugs are deferred to after the Psionic port sprint (Priority 4) — they can't be tested until the abilities exist.
- This phase is also when IDEA-020 (accessibility) and IDEA-021 (tuning) can be applied systematically — you'll be reading every ability path anyway.

---

### IDEA-013: Modular game structure — PvE funnel into arena PvP

- **Status:** open
- **Source:** Rex (DionyzRex, 2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** large (design) / medium (implementation per phase)
- **Affects:** game design philosophy, area layout, balance tuning,
  potentially a separate arena ruleset layer

Break the game into two distinct phases with a clean handoff point:

**Phase 1 — PvE / solo experience:** levelling, gearing, and learning
your class in a self-contained single-player loop. No PvP pressure.
Players build their character, learn their skills, and hit a natural
ceiling (e.g. level 101 Hero). This phase is essentially a tutorial
that produces a battle-ready character.

**Phase 2 — Arena:** players bring their Phase 1 character into a
tightly controlled 1v1 PvP environment. The arena becomes the
competitive layer — balanced, matchmade, spectatable. Because everyone
arrived through the same PvE funnel, gear and level variance is
bounded, making balance tractable.

**Why this matters:** classic DS's biggest balance problem was that
PvP was available everywhere at all times, so a min-maxed veteran
could grief new players constantly. Separating the two phases removes
that friction and lets the dev team focus balance effort on a single
controlled context (1v1 arena) rather than open-world PvP with
infinite variables.

**Notes:**
- The Battle Arena area (`battle.are`, vnums 2600–2699) already
  exists in the recovered world — it's a blank-room deathmatch space.
  Could be the foundation for the structured arena.
- "Extremely tight 1v1 balance" is a separate workstream from combat
  porting — you need all abilities working before you can tune them.
  This idea is a north star for *why* we port every stub, not a
  near-term implementation target.
- Long-term: if DS ever ports to Unreal/Wwise, this modular structure
  maps cleanly — solo campaign as one mode, arena as another, shared
  character progression between them.
- Related: IDEA-005 (test dummies) serves both phases — PvE players
  use dummies to learn abilities, arena players use them to practice
  matchup theory.
- Related: IDEA-014 (Kensai) — Rex and Kyle both want Kensai to be a
  featured arena class. The combo-finisher system is a natural fit for
  the tight 1v1 context where stance and sequencing decisions matter.

---

### IDEA-016: Unreal/AAA port path — MUD as game server, Wwise throughout

- **Status:** open
- **Source:** Rex (DionyzRex) + Kyle (Sonetics), 2026-04-26
- **Date proposed:** 2026-04-26
- **Complexity:** huge (full port) / medium (stage 1 Wwise layer)
- **Affects:** web client, new structured event layer, long-term Unreal
  client, Wwise project

The MUD is already a game server — all logic (combat, stats, world
state, room positions) lives server-side. The telnet client is a dumb
display layer. That separation is the architectural foundation for a
full visual port.

**Stage 1 — Wwise in the MUD client (near term)**
The web client (IDEA-011) parses combat text output for keywords
("bash", "dazed", "flees", "slash", etc.) and fires Wwise events.
Sound design layer lives entirely in the client — MUD source
unchanged. Ambient audio tied to area, combat SFX tied to combat
strings. Kyle's domain entirely. Nobody is doing this in the MUD
space. Achievable as soon as the web client exists.

**Stage 2 — Structured event layer (medium term)**
MUD currently emits human-readable strings only. Add a parallel
sidecar output channel that emits structured events alongside text:
`{"event":"bash","attacker":"Julian","target":"Byrok","hit":true}`.
Text clients ignore it. Visual clients consume it. This is the
bridge — hard but solvable. The sidecar pattern from IDEA-012
(Oracle AI) is the same infrastructure.

**Stage 3 — Unreal client (long term)**
Unreal reads structured events, renders the world in 3D. MUD stays
as authoritative server. Text players and 3D players coexist in the
same game simultaneously. Two people fighting in text can be spectated
in 3D — Kyle's exact vision. Rooms need spatial coordinates
assigned (a mapping/authoring problem, not a logic problem). Combat
events need animation triggers.

**Why Kensai helps the port:** discrete named builder moves (`slash`,
`thrust`, `chop`) map 1:1 to named animations. Cleaner translation
than generic "you swing at the enemy" text. Kensai was designed
for text but is inherently animation-friendly. See IDEA-014.

**Rex's framing:** "Could you imagine an MMO that people could play
like WoW, but running on top of a MUD that you could play in pure
text if you wanted?" That's Stage 3. The MUD is the prototype and the
server simultaneously.

**Notes:**
- Stage 1 is a portfolio piece on its own. A Wwise-enabled MUD web
  client demonstrates the entire Wwise API integration pipeline in a
  novel context.
- The C MUD doesn't need to know about Unreal at all — the bridge
  layer translates. Keep the MUD clean.
- Furcadia was mentioned as a reference point (GUI layer over text
  world). Same basic architecture, different aesthetic direction.
- Stage 2's structured event layer is also what the Oracle AI
  (IDEA-012) needs for context injection — player state events.
  Building it once serves both ideas.

---

### IDEA-015: Combat feedback legibility — expose mechanics through combat text

- **Status:** open
- **Source:** Rex (DionyzRex) + Kyle (Sonetics), 2026-04-26
- **Date proposed:** 2026-04-26
- **Complexity:** medium
- **Affects:** combat message strings across `act_combat.c`, `fight.c`,
  spell failure paths, daze/stun affect application, helpfile rewrites

Right now the combat system is a black box. Players see "your spell
fails" but don't know if it failed because their skill is under 100%,
because the target bashed them, because the target has spellbane active,
or because of the target's saving throws. The cause is invisible. Even
experienced players are guessing.

Rex's framing: daze has a love/hate relationship — the mechanic is
arcane and hard to gauge the exact value of *even if you're familiar
with it*. "Did his spell fail because he didn't get it to 100 or
because of my bashing?" That's a question that should never need to
be asked.

**Two-layer fix:**

**Layer 1 — combat strings that name what happened:**
When a mechanic fires, the text should say so. Examples:
- Spell interrupted by bash → "You lose your concentration as $N's
  bash staggers you!" (not just the generic fail string)
- Daze proc → "$N's eyes go glassy — $E looks dazed." on application;
  something visible on expiry too.
- Spellbane deflecting → a distinct string, not the same as a resist.
- Saving throw success → flavor that implies active resistance ("$N
  shrugs off the effect") vs random miss ("the spell fizzles").

**Layer 2 — helpfiles and FTUE rewrite:**
Kyle: "The more you understand your character / how to counter classes,
the more you realize the depth." Current helpfiles are terse 2003
snippets. A full rewrite as part of a first-time user experience pass
— written to teach, not just document. Pairs with IDEA-012 (Oracle AI)
for the cases where static help isn't enough.

**Notes:**
- Start with daze since it's the specific mechanic Rex flagged. Map
  every place daze is applied in `fight.c` / `act_combat.c` and
  audit the strings at each site.
- Spellbane, bash interrupt, and saving throw results are the next
  highest-value candidates.
- String changes are low-risk — no logic changes, surgical edits.
  Can be done alongside any combat port without a dedicated patcher.
- **Rex's core design note:** the real sticking point isn't just
  visibility — it's variance. Daze is too random to reason about.
  Even if you can see it happening, you can't predict or plan around
  it if the proc rate and duration are noisy. Fix candidate: reduce
  the variance first (tighter proc window, more consistent duration),
  *then* expose it clearly through text. A predictable mechanic that's
  visible is one players can build strategy around. A random mechanic
  that's visible is just noise with a label.
- The Oracle AI (IDEA-012) handles the "explain how it works"
  question dynamically; this idea handles the "show me it happening"
  question in real time during combat. Both are needed.
- Helpfile rewrite is a content task, not a code task — Kyle or Rex
  can draft these in `HELPFILES.md` and they get patched in later.

---

### IDEA-014: Kensai — combo/stance class with finisher system

- **Status:** open
- **Source:** Rex (DionyzRex) + Kyle (Sonetics), 2026-04-26
- **Date proposed:** 2026-04-26
- **Complexity:** huge (new class, new combat subsystem)
- **Affects:** new class definition, new stance/combo tracking on
  `pc_data`, new `do_*` commands for each builder move, finisher
  dispatcher, `fight.c` auto-attack integration

Original DS concept — a class Rex was designing before the project
went dormant. Revived here. Reference point: LotRO's Warden class
(spear/shield tank) is described as "almost 1:1 what I wanted Kensai
to be."

**Core design — builder/finisher loop:**

Players manually input attack sequences ("builders") rather than
relying on auto-attacks alone. Each builder is a named move: `slash`,
`thrust`, `chop`, etc. Executing a sequence of builders fills "slots"
with symbols. The finisher's effect is determined by the combination
of symbols in those slots — so different sequences produce different
outcomes.

Example (3-slot tier):
- `slash slash thrust` from Stance 1 → specific damage + effect,
  leaves you in Stance 2.
- `chop thrust slash` from Stance 1 → different damage + different
  effect, leaves you in Stance 3.

As the character levels up, more slots unlock. At 3 slots you get
a personal effect. At 6+ slots you unlock group-wide buffs. The
player can "read" what the current finisher will do before committing,
and choose to keep building if the current combo isn't what they want.

**Auto-attack stance:** Kyle's take — not fully zero-lag (that may be
a gimmick/trap per Rex). Low autos remain (maybe third attack and
offhand), but the combo loop is the primary damage and effect delivery
system. Parry and shield block stay as passive defensive skills.

**Affects on finishers:** daze, stun, or other status effects are
natural finisher payloads. "If you fill slots X-Y-Z you get a
stun finisher" adds real decision-making to the sequence choice.

**Comparisons noted in conversation:**
- LotRO Warden — closest existing implementation. Spear/shield tank,
  builder/finisher loop, stance transitions.
- FFXIV Gunslinger (Machinist?) — combo weaving rhythm is similar.
- DS `do_stance` (1479b, already in act_combat.o) — the stance
  machinery may already be partially decompilable from the original
  binary. Worth reading before designing from scratch.

**Why the arena context matters for this class:** Kensai's depth comes
from sequencing decisions under pressure. That's only interesting when
your opponent is also making decisions — it's a 1v1 class by design.
Open-world PvE would trivialise the combo system; the arena is the
right home for it. See IDEA-013.

**Implementation path (long-term):**
1. Port `do_stance` from disasm first — understand what stance
   machinery DS already had.
2. Design the slot/symbol data structure on `pc_data`.
3. Implement 3-4 builders as new `do_*` commands.
4. Implement the finisher dispatcher that reads the slot state.
5. Add stance transitions as finisher side effects.
6. Tune in the arena context against a dummy and then live 1v1.

---

### IDEA-012: In-game AI help system ("The Oracle")

- **Status:** open
- **Source:** Kyle (2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** large
- **Affects:** new `do_ask` command in `act_info.c`, new Python sidecar
  daemon, named pipe / Unix socket IPC layer, server tick for response delivery

New players type `ask <question>` in-game and receive a contextual
answer from an LLM (Claude API) delivered as a tell from a thematic NPC
("The Oracle" or similar). The AI knows DS mechanics via a system prompt
built from `HELPFILES.md`, `SKILL_TABLE.md`, and wiki content. Per-player
context (class, level, skill percentages) is injected per call so answers
are personalised.

Architecture: sidecar pattern — `do_ask` writes question + player context
to a named pipe and returns immediately (non-blocking for the MUD's
single-threaded loop). Python daemon reads the pipe, calls the API, writes
the response back. MUD delivers it on the next tick as a tell.

**Notes:**
- Rate-limit per player (e.g. 10-second cooldown) to control API cost.
  For a small friend group this costs cents per session.
- System prompt can be auto-built from existing docs at daemon startup.
- Defer until combat is stable and player onboarding basics (dummies,
  commands, stability) are solid. This is a polish feature, not a
  prerequisite for gameplay.
- Demo pitch: "The help system has an AI that knows the game. New players
  ask questions in plain English and get answers tailored to their
  character."

---

### IDEA-011: Browser-based web client + PWA

- **Status:** open
- **Source:** Kyle (2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** medium
- **Affects:** new Python/Node WebSocket bridge script, static HTML/JS
  client (xterm.js), optional ngrok or domain exposure of WS port

Players visit a URL in any browser — desktop or mobile — and play without
downloading or configuring a MUD client. A small WebSocket bridge (≈50
lines) proxies browser WS connections to the MUD's TCP port 5000. Frontend
is xterm.js (well-maintained browser terminal library).

Once the web client exists, wrapping it as a PWA (manifest + service
worker) lets mobile players add it to their home screen with DS branding —
no App Store, no review process.

**Notes:**
- Solving mobile and "no install" in one shot. The web client IS the
  no-install story — share a URL, click, play.
- WebSocket port exposed via ngrok (same paid plan already in use) or a
  cheap custom domain.
- Prototype is one Python script + one HTML file — could be a single
  afternoon session once combat and stability are solid.
- Discord bridge (MUD ↔ Discord channel) is a related but separate idea —
  low friction for recruiting, limited for actual play. Can be a follow-on.
- Defer until combat commands and stability are in good shape. This is the
  right second milestone after gameplay is solid.

---

### IDEA-010: Auto-spellup on new character spawn

- **Status:** open — queue after combat ports complete
- **Related bug:** BUG-022 (spellup spam + no auto-trigger — fix that first)
- **Source:** Kyle (2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** small
- **Affects:** character creation completion point (`creation.c` / `nanny()`),
  spell/affect application helpers

New characters should spawn pre-buffed with their class's basic spell
stack rather than entering the world naked. Either apply the affects
directly at creation (pre-affected approach, simpler) or trigger a
silent `do_spellup` equivalent on first entry.

**Notes:**
- Pre-affected approach is cleaner — no spell failure rolls, no mana
  cost, just set the AFFECT_DATA stack directly at creation. Same
  pattern as IDEA-007's flag-setting at the end of creation_nanny().
- Spells to include are class-dependent — each class has a baseline
  buff stack (armor, bless, haste equivalents etc.). Need to map
  which affects each class gets by default.
- Duration should be long enough that a new player isn't immediately
  debuffed before they find their footing.
- Related to IDEA-003 (auto-tier-3 at creation) — if that ever ships,
  the spellup stack may need to expand to match tier-3 baseline buffs.

---

### IDEA-009: New characters start with starter pack equipped

- **Status:** open — queue after STRIKE-PURE batch
- **Source:** Kyle (2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** small
- **Affects:** character creation completion / first-entry handler,
  object wear/wield helpers

New characters currently receive their starter pack items in inventory
but unequipped. They should spawn with gear already worn and a
class-appropriate weapon already wielded.

**Notes:**
- Weapon should match the class's natural weapon (e.g. sword/whip for
  warrior, staff for mage, dagger for thief/ninja). Need to map
  class → default weapon vnum from the object database.
- Wear slots: armour pieces should be auto-worn, weapon auto-wielded.
  Use `equip_char(ch, obj, wear_loc)` or equivalent at the end of
  creation — same location as IDEA-007 defaults.
- Watch for wear restrictions (level req, class req, weight) on the
  starter items — make sure the starter gear actually passes the
  equip checks for each class.
- If starter pack vnums vary by class, this becomes slightly more
  complex — may need a class → starter weapon vnum table.

---

### IDEA-008: `add all` shorthand in character creation skill group screen

- **Status:** open
- **Source:** Kyle (2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** trivial
- **Affects:** character creation handler (`creation.c` or `nanny()` in `comm.c`), wherever `do_add` / the `add` command is handled during creation

During character creation, players spend Creation Points (CP) on skill groups
one at a time (`add dagger`, `add kick`, etc.). This is tedious — the real
decision is *how many groups to buy* (more groups = fewer trains left for HP
gains), not *which specific groups* to type. Add an `add all` shorthand that
purchases every available group in one command, spending all remaining CP.

**Notes:**
- The CP trade-off vs HP trains is intentional and should be preserved —
  `add all` just removes the typing friction, not the resource decision.
- Find where the `add` command is parsed during creation and add an `all`
  branch that iterates available groups and calls the existing add logic for each.
- Existing `train all` and `prac all` shorthands confirm the pattern is
  already established in the codebase — find those and mirror the approach.

---

### IDEA-007: Default new character preferences (auto all, brief, scroll 0)

- **Status:** in-progress
- **Source:** Kyle (2026-04-26)
- **Date proposed:** 2026-04-26
- **Complexity:** trivial
- **Affects:** `comm.c` (CON_CREATION handler in `nanny()`), new patcher `set_new_char_defaults.py`

New characters should start with `auto all`, `brief`, `scroll 0`, and
a sensible default prompt already set — no manual configuration needed.

**Default prompt string (Kyle's format):**
```
<<%h/%Hhp %m/%Mmp %v/%Vmv $%pp/%gg>>
```
Produces e.g.: `<<2573/2573hp 1349/1349mp 1233/1233mv $107p/86g>>`

**Notes:**
- Flag names need to be grepped from DS source (`do_brief`, `do_auto`,
  `do_scroll`, `do_prompt`) — DS may differ from stock ROM naming.
- Prompt stored as string field on char (likely `ch->prompt` or
  `ch->pcdata->prompt`) — check `do_prompt` for the field name.
- Should only apply to new character creation, not existing characters.

---

### IDEA-006: In-game `version` command shows project version

- **Status:** open
- **Source:** Kyle (2026-04-25 — paired with CHANGELOG.md introduction)
- **Date proposed:** 2026-04-25
- **Complexity:** trivial
- **Affects:** wherever DS's existing `version` command lives (likely
  `act_info.c` or `act_comm.c`), `merc.h` for a constant

Stock ROM has a `version` command. We should overload it (or extend it)
to print the current project version per `CHANGELOG.md`, so players
typing `version` in-game see e.g. "Devil's Silence Resurrected 0.4.2 —
2026-04-25". Pairs the in-game state with the changelog so when
something breaks, the version-string is immediately diagnosable.

**Notes:**
- Define `DS_VERSION_STRING` in merc.h as a `#define`, bumped per
  copyover (could be auto-generated from CHANGELOG.md by a small
  script during `make`).
- `do_version` / `do_who` / motd display the string somewhere
  player-visible.
- Trivial complexity but high diagnostic value — when a friend says
  "I tried X and got weird behaviour," version-string in their report
  immediately tells us which build they were on.

---

### IDEA-005: Test-dummy area for combat-verb validation

- **Status:** open (specced 2026-04-25; implementation queued for after Phase B Step 2)
- **Source:** Kyle (2026-04-25)
- **Date proposed:** 2026-04-25
- **Complexity:** medium (single area file + possibly a few new spec_funs)
- **Affects:** new `dummies.are` file, `area.lst`, possibly `special.c` for behavioural spec_funs

Dedicated training-dummy area where each dummy stresses a specific
mechanic, so combat verbs (and eventually class abilities) can be
tested against known-behaving opponents instead of random world mobs.
Long-term: opens the door to player-runnable PvP simulation against
tactical dummies, not just PvE against passive NPCs.

**Location:** near the newbie school exit OR the guildmaster hall
near Solennir (Kyle's call when implementing).

**Suggested vnum range:** 9000-9099 (likely free; verify against
existing area assignments before committing).

**Roster — each dummy isolates one mechanic:**

| Vnum (suggested) | Dummy | Mechanic tested |
|---:|---|---|
| 9001 | Hit pillow | Raw HP — 10,000+ hp, no offence, no defence. Stamina/damage-output tests. |
| 9002 | Armored | Very low AC — to-hit % validation, parry/dodge math against well-armored target. |
| 9003 | Saves dummy | High saving throws — magic-vs-physical balance, spell resistance. |
| 9004 | Heavy hitter | High hitroll/damroll — defensive verbs (parry, dodge, shield block). |
| 9005 | Disarmable | Wields a basic weapon — `do_disarm` target practice. |
| 9006 | Disarming dummy | Wields a weapon AND has spec_disarm-equivalent — bidirectional disarm test (you can lose your weapon to it). |
| 9007 | Dispeller | Casts dispel magic on attackers — Sanctuary/buff-stripping resistance test. |
| 9008 | Sanctuary-protected | Casts Sanctuary on self at spawn/restock — our `dispel` target. |
| 9009 | Small (SIZE_TINY) | Bash chance bonus testing. |
| 9010 | Huge (SIZE_HUGE) | Bash chance penalty testing. |

**Implementation notes:**

- For the "tries to disarm you / tries to dispel" dummies, we need
  spec_funs (or mob programs / mprogs). DS likely has some — check
  `special.c` for `spec_*` definitions. If `spec_disarm` /
  `spec_cast_dispel` exist, point the dummy's spec_fun at them.
  If not, write minimal mprogs or extend special.c.
- Each dummy should have a brief long_descr that hints at its
  purpose (e.g., "A heavily-armored dummy stands here, daring you to
  hit it.") so testers know what they're testing.
- Reset rules in the area file should respawn dummies on restock so
  they're always available — they shouldn't permanently die.
- Consider `ACT_NOEXP` and `ACT_NOLOOT` flags so killing dummies
  doesn't grant XP/coins (prevents farming-as-feature).
- Player-runnable summoning eventually: a "summon dummy" command at
  the dummy area's hub room that spawns the requested type into the
  player's room. Trivial extension once the area exists.

**Why this matters now:** Kyle keeps hitting "I don't have a good
test mob" friction. Static dummies fix that for current verbs. Once
porting reaches DS-custom abilities (psionics, voodoo curses), the
varied roster lets us validate behaviour-specific quirks in a
controlled environment. Once we want PvP simulation, the same
roster can be extended with mprog tactics.

---

### IDEA-004: Remove skull requirement from `do_warpaint`

- **Status:** done
- **Source:** Kyle (2026-04-25, after BUFF-SELF batch verification)
- **Date proposed:** 2026-04-25
- **Complexity:** trivial
- **Affects:** `do_warpaint` in `act_combat.c`

The current port faithfully implements the 2003 disasm: warpaint
requires a skull object (OBJ_VNUM_SKULL = 56) which gets consumed via
`extract_obj` whether the painting succeeds or fails. Per Kyle's call,
this requirement isn't fun and should be removed — strip the
`get_obj_carry(skull)` check and the `extract_obj` calls so warpaint
behaves like the other BUFF-SELF abilities (mana/move cost only).

**Notes:**
- This is a **deliberate divergence from the 2003 original**, not a
  bug fix. Document the divergence in the function's leading comment
  block so future-Kyle and future-Claude don't re-port the
  skull-requirement back in by accident.
- Skull testing was also blocked by skulls decaying very fast in
  general — separate concern (object decay timers in update.c). Not
  pursuing as a bug for now since removing the skull requirement
  sidesteps it.
- Pattern flag: this is the first port-level design decision diverging
  from the 2003 original. Worth establishing the convention now —
  divergences get a leading comment explaining the design call,
  reference the IDEA number, dated. Keeps the "what did Kyle change vs
  what's faithful" question answerable forever.

---

### IDEA-003: Auto-promote new characters to "third tier" classes at creation

- **Status:** open
- **Source:** Kyle (2026-04-25)
- **Date proposed:** 2026-04-25
- **Complexity:** medium
- **Affects:** character creation flow (probably in `nanny()` in
  `comm.c` or wherever DS handles `CON_CREATION`), `pcdata->tier`,
  related class re-init code

Once `do_remort` and `do_reroll` are both neutralized (they are, as of
2026-04-25), new players can't access higher class tiers through the
normal in-game progression. Rather than re-port reroll/remort properly
in the short term, **auto-set new characters to tier 3 at creation** —
that gives players the equivalent of what remort would have promoted
them to, with no class-re-init path to crash on.

**Notes:**
- Defer this until after skills/spells are stable per Kyle's preference
  (2026-04-25). Premature implementation risks the same crash family
  do_remort hit, since auto-tier-setting touches the same class re-init
  code.
- When implemented: probably a small patcher that adds a single
  `pcdata->tier = 3;` write to the new-character handler, plus any
  associated stat resets / skill-grants the original remort flow did.
- Relates to BUG-001 indirectly — every "advanced character mechanic"
  that touches stubbed combat code is a potential crash vector. Auto-
  tier-set lets us defer the full reroll/remort port indefinitely.

---

### IDEA-002: Pull in-game `bugs`/`idea`/`typo` submissions into BUGS.md / IDEAS.md

- **Status:** open
- **Source:** Kyle (2026-04-25)
- **Date proposed:** 2026-04-25
- **Complexity:** small
- **Affects:** new helper script (likely `import_ingame_logs.py`),
  `data/log/bugs.txt` / `data/log/typos.txt` / `data/log/ideas.txt`
  (if exists)

DS's `bugs` command (and likely `ideas`/`typos` companions) writes player
submissions to text files under `data/log/`. We already have those files
recovered from the 2003 archive — they accumulate during play and
nobody reads them. A small importer script could:

1. Read `data/log/bugs.txt` (and the others), parse each entry's date +
   reporter + body.
2. For each entry not yet in `BUGS.md` (matched by a hash or date+title),
   stage as a draft entry under `## Open` with `Source: in-game (player
   name)`.
3. Same for ideas → `IDEAS.md`.
4. Optionally: rotate the in-game files (move processed entries to a
   `processed_<date>.txt` archive) so the script doesn't re-import.

**Notes:**
- Same agent-boundary artifact pattern as `reset_character.py` and the
  patcher series — narrow scope, one job, deployable artifact.
- Players get a tighter feedback loop because their submissions actually
  land in the tracked docs rather than gathering dust in a log file.
- Could be a scheduled task (cron / systemd timer) once it's stable, so
  the import is automatic.

---

### IDEA-001: Grey out unusable commands in `commands` output

- **Status:** open
- **Source:** Kyle's buddy (community member, 2026-04-25)
- **Date proposed:** 2026-04-25
- **Complexity:** medium
- **Affects:** `interp.c` (do_commands), maybe `act_info.c` for the
  rendering helper, ANSI colour conventions

When a player types `commands`, commands they can't use (gated by
class, level, trust, or position) should be visually de-emphasised —
greyed out via dim ANSI codes — instead of shown the same as usable
commands or hidden entirely. Players see the full set, learn what
exists, and immediately know which they can actually use.

**Notes:**
- Implementation likely walks the `cmd_table` once per request,
  checks each entry's `level`, `class_bits` (if DS uses class
  gating in cmd_table), and `position` against the requesting char,
  applies a `{D` or similar dim escape if not usable.
- Could be extended to `wizhelp` and any other listing of commands.
- Thoughtful: if DS's commands output already filters by trust,
  the greyed-out ones might be a discovery surface — players notice
  high-level abilities and aspire to them. UX-positive side effect.
- Worth pairing with: a hover/help convention that shows WHY a
  command is unusable (level too low, wrong class, etc.) — could be
  another idea entry.

---

## Planned

_(none yet)_

---

## In progress

_(none yet)_

---

## Done

### IDEA-000: Template (delete when first real idea ships)

Empty entry just to anchor the section. Delete me when you close your
first real idea.

---

## Won't-do

_(none yet — entries here should include a brief reason, e.g., "out of
scope for the C version, revisit after rewrite")_
