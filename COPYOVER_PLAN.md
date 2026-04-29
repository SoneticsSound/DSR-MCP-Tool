# Copyover — Verify and Test Plan

**Generated 2026-04-25 in Cowork. Surprise finding: copyover already exists.**

---

## What we discovered

When we set out to "add copyover," the assumption was 150-250 lines of porting
from a public ROT/Smaug source. Reality: **DS already has copyover fully
implemented** in the recovered source tree. It survived the corruption.

Files where it lives (in `recovered/devils/src/`):

| File | Lines | What's there |
|---|---|---|
| `act_wiz.c` | 466-540 | `do_copyover` — full implementation |
| `act_wiz.c` | 544-620 | `copyover_recover` — full implementation |
| `comm.c` | 49 | `DECLARE_DO_FUN(do_copyover)` |
| `comm.c` | 329-345 | `main()` argv-flag detection |
| `comm.c` | 347-360 | `init_socket` skip + `copyover_recover()` call |
| `interp.c` | 520 | cmd_table entry: `{ "copyover", do_copyover, 0, POS_DEAD, L3, ... }` |
| `merc.h` | (CON enum) | `CON_COPYOVER_RECOVER 7` |
| `merc.h` | 2345-2346 | `COPYOVER_FILE` and `EXE_FILE` macros |

L3 = `MAX_LEVEL - 3` = level 108 (deity tier). Julian is level 110, so he's
above the threshold and can run it.

## How DS copyover actually works (read once, internalize)

When an immortal types `copyover`:

1. `do_copyover` opens `copyover.data` (in cwd) for writing.
2. It iterates `descriptor_list`. For each connected descriptor:
   - If the player is mid-login (`d->connected > CON_PLAYING`), they get
     "Sorry, we are rebooting" and the socket is closed cleanly.
   - Otherwise: writes `"<fd> <playername> <host>\n"` to copyover.data,
     calls `save_char_obj(och)` to flush the player file, sends them
     `"*** COPYOVER - please remain seated! ***"`.
3. Writes `"-1\n"` as terminator.
4. Closes `fpReserve` (the always-open spare file descriptor).
5. **Calls `execl(EXE_FILE, "ds", port, wwwport, "copyover", control, wwwcontrol, NULL)`.**
   The OS replaces this process image with the new binary. **Same PID, all
   open file descriptors inherited** (sockets, including player connections).
6. If `execl` returns, exec failed — recover gracefully and reopen the
   reserve file. Most failures here are missing-binary or wrong-path issues.

When the new binary boots in copyover mode, in `main()`:

1. Detects `argv[3] == "copyover"`, parses `argv[4]` as `control` socket FD,
   `argv[5]` as `wwwcontrol` socket FD.
2. **Skips `init_socket()`** — those listening sockets are inherited from
   the previous incarnation, no need to recreate.
3. Runs `boot_db()` normally to load world/areas/objects.
4. Calls `copyover_recover()` — opens `copyover.data`, unlinks it (so a
   crash mid-recovery doesn't leave stale state), and for each line:
   - Calls `write_to_descriptor(fd, "\n\rRestoring from copyover...\n\r", 0)`.
     If that write fails, the player has disconnected during the gap; close
     and skip.
   - Allocates a new `DESCRIPTOR_DATA`, attaches the inherited FD.
   - `load_char_obj(d, name)` re-loads the player from disk.
   - Inserts back into `char_list`, places in their saved room (or temple if
     no room), runs `do_look(ch, "auto")`, broadcasts "$n materializes!".
   - If they had a pet, brings the pet to the room too.
5. Drops into the normal `game_loop_unix(control, wwwcontrol)`. Players
   resume play seamlessly.

## Coordination with the watchdog

The current `run_mud_watchdog.sh` watches for ds.new exiting. **Copyover
doesn't exit** — `execl` replaces the process image while keeping the same
PID. The watchdog never sees anything happen. No changes needed there.

If exec fails (e.g., `~/ds/recovered/devils/bin/ds.new` was deleted between
the patch and the copyover), the OLD ds.new continues running because exec
only replaces on success. Players see "Copyover FAILED!" and keep playing
on the old binary. Acceptable failure mode.

If the new binary execs successfully but then crashes during `boot_db` or
`copyover_recover`, ds.new exits with non-zero, the watchdog respawns it
*without* the `copyover` argv flag (it just runs `ds.new 5000 5001`),
so the new instance starts fresh and players get disconnected. This is
the worst-case fallback.

## ngrok tunnel survival

The ngrok tunnel terminates at the listening socket `control`. That FD is
inherited through exec. So the ngrok tunnel keeps working — it doesn't
even know a copyover happened. Good.

## Verify-and-test plan (run from Claude Code in WSL)

### Step 1 — confirm src_patched has the copyover code

```bash
grep -n "do_copyover\|copyover_recover" ~/ds/src_patched/act_wiz.c
grep -n '"copyover"' ~/ds/src_patched/comm.c ~/ds/src_patched/interp.c
grep -n "COPYOVER_FILE\|EXE_FILE" ~/ds/src_patched/merc.h
```

Expected: every line referenced in the table at the top of this doc shows up
in `src_patched/`. If `rebuild_source.py` accidentally stripped any of it,
we copy from `recovered/devils/src/` to `src_patched/`. If everything's
present, move on.

### Step 2 — verify EXE_FILE path against actual deployment layout

The code uses `EXE_FILE = "../bin/ds.new"` which is relative to cwd at the
time `do_copyover` runs. The current launch sequence (per `start_mud_public.sh`)
is:

```bash
cd ~/ds/recovered/devils/bin
./ds.new 5000 5001 ...
```

So cwd is `~/ds/recovered/devils/bin/`. `../bin/ds.new` resolves to
`~/ds/recovered/devils/bin/../bin/ds.new` → `~/ds/recovered/devils/bin/ds.new`.
That's **the same binary** — exec replaces it with itself, just freshly read
from disk. That's exactly what we want for hot-deploying patches: copy the
new ds.new to that path before running copyover.

Confirm with:

```bash
ls -la ~/ds/recovered/devils/bin/ds.new
```

Should show a recent ELF 32-bit executable.

### Step 3 — confirm cwd at runtime

```bash
ls -l /proc/$(pgrep ds.new)/cwd
```

That should print `/home/kwebb/ds/recovered/devils/bin`. If it doesn't (e.g.,
the watchdog launches with a different cwd), `EXE_FILE`'s relative path
won't resolve correctly, and either we change cwd in the launcher or we
edit `EXE_FILE` to an absolute path.

### Step 4 — compile and deploy a noticeable change

To verify copyover *is* doing what it claims, make a trivial change that
players will see. Edit `act_comm.c` (a survived file) and find the MOTD or
any commonly-seen text. Add or change one word. Rebuild and deploy:

```
/build-deploy
```

Don't restart the MUD via the watchdog cycle — leave the OLD binary running.

### Step 5 — run copyover from Julian (level 110)

In a Mudlet/telnet client, log in as Julian. Confirm you can see the
*old* MOTD/text. Then type:

```
copyover
```

Watch carefully:
- Your client should briefly see "*** COPYOVER - please remain seated! ***"
- After ~1-2 seconds, "Restoring from copyover..." then "Copyover recovery complete."
- A fresh `look` happens automatically.
- The MOTD/text you changed in step 4 should now show the NEW value.

In a separate WSL terminal, watch:

```bash
watch -n 0.5 'pgrep -fa ds.new'
```

The PID should NOT change — same process, replaced image. That's how you
know copyover worked vs. the watchdog respawning a fresh instance.

### Step 6 — verify the copyover.data file was created and removed

```bash
ls -la ~/ds/recovered/devils/bin/copyover.data
```

Right after `copyover` runs, this file briefly exists, then `copyover_recover`
unlinks it. So a fresh `ls` should say "no such file." If it lingers, the
recovery path failed — diagnose by reading `/tmp/ds_boot.log`.

## Test sequence summary (copy-paste version)

```bash
# Step 1
grep -c "do_copyover" ~/ds/src_patched/act_wiz.c

# Step 2-3
ls -la ~/ds/recovered/devils/bin/ds.new
ls -l /proc/$(pgrep ds.new | head -1)/cwd

# Step 4 - make a visible change, then:
# /build-deploy from Claude Code

# Step 5 - in Mudlet as Julian:
# copyover

# Step 6 - in WSL, immediately after:
ls -la ~/ds/recovered/devils/bin/copyover.data 2>&1 | head -1
pgrep -fa ds.new
```

## Rollback plan (if copyover crashes the server)

If copyover triggers a SIGSEGV or SIGABRT (the spontaneous signal-6 issue
we already know about could rear up here):

1. The watchdog will respawn ds.new in ~3 seconds.
2. Players reconnect via Mudlet.
3. **Don't run copyover again** until we diagnose. Treat as a known bad path.
4. Disable the cmd_table entry by either bumping its level to 999 in
   `interp.c`:
   ```c
   { "copyover", do_copyover, 0, POS_DEAD, 999, 1, LOG_ALWAYS, 0 },
   ```
   or by stubbing `do_copyover` similarly to how we stubbed `do_remort`.

Treat copyover as "test once, leave alone if it works" until Phase B is
mature enough that we want hot-deploys regularly.

## Files to copy across (Cowork → WSL)

```bash
cp "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/COPYOVER_PLAN.md" ~/ds/
```

Then in Claude Code:

```
Read COPYOVER_PLAN.md and walk me through verify-and-test, one step at a time.
```
