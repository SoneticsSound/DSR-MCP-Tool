# DS Bots — Operator's Guide

PvP combat bots for Devil's Silence Resurrected. Three pre-configured
personalities (`BotWarden`, `BotShade`, `BotFury`) that log in over
telnet, walk Town Center, accept challenges via `bow`, and fight using
class-appropriate combat rotations.

This is the operator's helpfile. For player-facing patch-note copy use
`PATCH_NOTES.md`. For implementation details read `ds_bot.py` directly
— it's well-commented.

---

## What's included

| File | Role |
|---|---|
| `ds_bot.py` | The bot itself — telnet client, combat rotation, patrol state machine |
| `bot_personality.py` | Personality templates + skill-tier variance + fight memory |
| `create_bots.py` | First-run helper for batch-creating all three bot characters |
| `add_botspawn_cmd.py` | Patcher that adds the in-game `botspawn` imm command |
| `start_bots.sh` | Launch all (or a named) bot in patrol mode, detached, logged |
| `stop_bots.sh` | Kill all (or a named) running bot process |

All five live at the workspace folder root and get copied to `~/ds/`
in WSL2 before running.

---

## First-time setup

You only do this once per bot character.

### 1. Set passwords

Open `ds_bot.py`, find `BOT_ROSTER` (around line 192). Each bot has a
`"password"` field — set it to whatever you want. Same password is
fine across all three; nobody else logs into them.

### 2. Verify the creation class names

Each bot's `creation_class` field maps to a class in `const.c`. The
defaults (`warrior`, `thief`, `berserk`) are tier-1 ROM classes —
verify by name match if you want a different class:

```bash
grep -A1 "class_table" ~/ds/src_patched/const.c | grep '^\s*"' | head -40
```

For tier-3 morpheous, see `CHANGELOG.md` 0.4.9 — `class_table[47]` is
on, but bots can't remort during creation; pick a tier-1 class and
have Kyle/Julian remort the bot manually if you want a tier-3 bot.

### 3. Run each bot once to create the character

```bash
cp /mnt/c/Users/danbl/Documents/Claude\ DS/Devil*/ds_bot.py ~/ds/
cp /mnt/c/Users/danbl/Documents/Claude\ DS/Devil*/bot_personality.py ~/ds/
python3 ~/ds/ds_bot.py --bot BotWarden
```

The bot will:
1. Connect to `7.tcp.ngrok.io:25597`
2. Send the bot name → confirm with Y
3. Set the password (twice for new chars)
4. Pick sex / race / class from the roster config
5. Accept the first stat roll
6. Type `add all` and `done` to leave the gen-groups screen
7. **Halt with creation-success message** including a list of the
   imm commands you need to run

The bot prints something like:

```
═════════════════════════════════════════════════════════════
  BotWarden created. Run these as Julian:
    advance BotWarden 101
    set char BotWarden skill all 100
    set char BotWarden hp 2500
    set char BotWarden mana 1200
    set char BotWarden move 800
  Re-run: python3 ds_bot.py --bot BotWarden
═════════════════════════════════════════════════════════════
```

Log into the MUD as Julian and run those four `set char` lines, then
re-run the bot script. From this point on it's a normal login.

Repeat for each of the three bots.

> Tip: `create_bots.py` automates the python-launch step for all three
> in sequence — run it once to create-and-halt all bots, then do the
> imm `set char` block in-game once for each.

---

## Day-to-day operations

### Start all three bots in patrol mode

```bash
~/start_bots.sh           # or wherever you put it — keep it alongside ds_bot.py
```

Each bot runs detached as a background `python3 ds_bot.py --bot Botxxx
--patrol` process. Logs land in `/tmp/ds_bot_<Name>.log`.

### Start one bot

```bash
~/start_bots.sh BotShade
```

### Stop everything

```bash
~/stop_bots.sh            # or ~/stop_bots.sh BotShade for a specific one
```

Uses `pkill -f` to find the right process by command-line.

### Watch a bot live

```bash
tail -f /tmp/ds_bot_BotWarden.log
```

You'll see every command the bot sends (`>>`) and every line it
parses (`<<`).

---

## In-game `botspawn` (imm-only)

Once `add_botspawn_cmd.py` has been run + the binary rebuilt + copyover'd,
imms (level 107+) can spawn a bot at their current location:

```
botspawn BotWarden          ← spawns at your room in patrol mode
botspawn BotShade
botspawn BotFury
botspawn list               ← list running bot PIDs
```

This is a thin C wrapper around `popen("python3 ~/ds/ds_bot.py --bot
<Name> --patrol --spawn-room <vnum> &")`. The bot still runs as a
host-side Python process; the MUD just kicks it off without you
needing a shell window.

The patcher itself is sentinel-checked — re-running it after a
successful apply is a no-op.

---

## Bot roster

| Bot | Class | Style | Flee | Notes |
|---|---|---|---|---|
| **BotWarden** | warrior | heavy fighter | 20% HP | Stacks all four buffs (berserk → warcry → bloodlust → ironwill), then commits to bash + kick + trip. Doesn't flee until near death. |
| **BotShade** | thief | stealth rogue | 32% HP | Garotte/backstab opener, then circle/gouge/dirt/strike loop. Rubs off blindness via `do_rub`. Flees earlier and re-engages. |
| **BotFury** | berserk | berserker | 15% HP | Pure aggression. Rebuilds full buff stack mid-fight if stripped. Battlehymn instead of bloodlust. Only flees at 15%. |

Each rotation is a list of `(condition_lambda, command, base_lag)`.
The bot walks the list every tick and fires the first command whose
condition is true and whose skill tier allows it.

### Personality system (per-session variance)

Each bot session generates a fresh `BotPersonality` from a deterministic
archetype (same bot name = same archetype) plus a per-session skill
roll on a normal distribution:

- **noob** (~10% of sessions) — only knows basic commands, big lag
  multiplier
- **scrub** (~30%) — most commands available, small lag penalty
- **normal** (~45%) — full rotation, neutral lag
- **killer** (~15%) — full rotation, lag bonus

Plus per-fight memory: each bot remembers up to 10 prior outcomes
against named opponents. Bots bumped flee threshold +5% per prior loss
to that name; +session-win-rate adjustment on top. So fighting BotFury
twice in a row, the second fight will see slightly more cautious play
if you won the first.

This is all in `bot_personality.py` — the generator is deterministic
on `bot_name + session_seed`, so you can reproduce a roll for
debugging if needed.

---

## Modes

### Arena (default — no `--patrol` flag)

Bot logs in, navigates to the arena challenge room (vnum 2600), and
periodically challenges other bots via `bow <name>`. Use this for
controlled stress-testing — fights are confined to the arena.

### Patrol (`--patrol`)

Bot logs in, recalls to "Before The Temple" (vnum 8084), steps south
into Town Center (vnum 8097), and walks the patrol route:

- 6 east → east gate (8091) → 6 west → center
- 6 west → west gate (8103) → 6 east → center
- 30–75s pause at center (randomised — looks natural)
- Repeat

The bot **avoids going north from TC** — that route leads into the
cots (vnum 8071, in `PATROL_EXCLUSIONS`). Every ~12 patrol steps the
bot shouts a personality-specific taunt.

If a player bows at the bot, it bows back (giving the player first
strike) and engages combat. After the fight, it `rest`s for 12
seconds, recalls, and resumes patrolling.

---

## Adding a new bot

1. Pick a name with the `Bot` prefix (so players can recognise them
   instantly). Generic-class names: `BotXxxxx`. Player-derived names:
   `BotJulian`, `BotLlanos` are reserved for imm-clones.
2. Write a `_yourname_rotation()` function returning the
   `[(lambda, command, lag), ...]` tuple list.
3. Add an entry to `BOT_ROSTER` with password, creation_class,
   creation_race, creation_sex, style, greet_emote, rotation, taunts.
4. (Optional but recommended) Add the name to `BOT_NAMES` in
   `add_botspawn_cmd.py` and re-run that patcher so the C command
   accepts it.
5. (Optional) Add the name to `start_bots.sh`'s `ALL_BOTS` array if
   you want it bulk-launched.

The personality archetype hash will assign one of the existing
templates automatically based on the new bot's name. To pin a specific
archetype, edit `BotPersonality.generate()` in `bot_personality.py`
and add an explicit name → archetype map.

---

## Troubleshooting

**Bot logs in but never moves.** Check `SOLENNIR_RECALL_ROOM` and
`PATROL_ROUTE` in `ds_bot.py` — vnums and direction sequences must
match the actual area layout. Defaults are verified for the current
DS world; if the area is re-authored these may drift.

**Bot hangs at the Y/N name confirmation.** Login flow assumes DS's
specific creation prompts — if `act_wiz` or `comm.c` get a creation-
prompt rewrite, the `_login_or_create()` keyword list in `ds_bot.py`
may need updating. Look for `_wait_for_any(["assword", "Y/N", ...])`.

**Bot dies and never comes back.** `handle_death()` sleeps 12s then
sends an empty newline to dismiss the corpse-screen prompt. If the
death prompt format changes (e.g. an `(Press ENTER)` becomes `(Press
SPACE)`), this needs tuning. Check `/tmp/ds_bot_<Name>.log` for the
last lines before the hang.

**Bot won't accept challenges.** `BOW_RE` in `ds_bot.py` looks for
exactly `"<name> bows before <name>."` — if DS's bow social string
changes (color codes, punctuation), update the regex.

**Three bots conflict at login.** `start_bots.sh` already sleeps 1.5s
between launches; if you're seeing weird state, increase that delay.
The MUD's login handler is single-threaded.

**Server crashes mid-fight.** All three bots will reconnect after the
watchdog respawns. The `fight_memory` ring buffer is in-memory only,
so it resets across reconnects — bots forget who beat them. If you
want persistence, serialize `MudBot.fight_memory` to disk and reload
on `_run_session()` start.

---

## Bot roster naming reservations

For consistency:

- `BotXxxxx` — generic class-based bots (current: BotWarden, BotShade, BotFury).
- `Bot<PlayerName>` — imm-clones (future: BotJulian, BotLlanos, BotRex).
  These should mirror the player's actual class + style and serve as
  "shadow" sparring partners.
- Anything else — discuss before adding so we don't end up with
  `BotMarketingDept` or similar.

---

## Reading the bot's mind

If you `tail -f` a bot's log during a fight you'll see something like:

```
[18:42:11] BotWarden:   << Llanos bows before BotWarden.
[18:42:11] BotWarden: Accepting challenge from Llanos — first strike is theirs.
[18:42:12] BotWarden:   >> bow Llanos
[18:42:14] BotWarden:   >> kill Llanos
[18:42:14] BotWarden:   << You hit Llanos.
[18:42:15] BotWarden:   >> berserk
[18:42:18] BotWarden:   >> warcry
[18:42:21] BotWarden:   >> bash
```

`>>` is what the bot sends; `<<` is what the bot reads. The 3-second
gaps between commands are the `base_lag` from the rotation tuple. If
you see the bot spam-sending faster than that, something's broken
with `set_lag()` — file a bug.
