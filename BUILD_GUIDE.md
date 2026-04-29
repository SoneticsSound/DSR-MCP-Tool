# Devil's Silence — Build & Run Guide

Last updated: April 24, 2026

This folder holds everything recovered from the 2003 `dsmud101803full.tar`
backup plus the tooling needed to rebuild the server on a modern machine.

## What's in this folder

| Thing | What it is |
|---|---|
| `dsmud101803full.tar` | The original corrupted archive. Keep untouched. |
| `recovered/` | Forensically extracted 1,847 files (source, worlds, players, logs). |
| `rebuild_source.py` | Script that patches the recovered C source so it builds on modern Linux. |
| `recovery_carver.py` | The tar carver used to extract files from the damaged archive. |
| `recovery_manifest.csv` | Header-by-header inventory of what was recovered. |
| `RECOVERY_SUMMARY.txt` | Plain-text summary of the recovery. |
| `BUILD_GUIDE.md` | This file. |

## What the build situation is

Out of 66 C source files, 61 compile cleanly on modern gcc. Five need
patches:

* **act_comm.c** — four multi-line string literals missing backslash continuations
* **comm.c** — a stray prototype for `gettimeofday` that clashes with modern glibc
* **olc_reset.c** — uses `struct wear_type` before it's fully declared
* **olc_string.c** — defines its own `getline()`, which POSIX 2008 took over
* **update.c** — the file has binary corruption from line 1,458 onward

`rebuild_source.py` applies mechanical fixes for the first four and
rebuilds `update.c` by keeping its clean prefix and appending stock
ROM 2.4 implementations of the four lost functions
(`char_update`, `obj_update`, `aggr_update`, `area_update`,
`update_handler`). The substitute functions behave like standard ROM — any
DS-specific customisations in the lost section will need to be re-added
later by cross-referencing with the compiled 2003 binary at
`recovered/devils/bin/ds`.

## Milestone 1 — Get it running locally on Windows

You will do all of this inside **WSL2** (Windows Subsystem for Linux).
The server is Linux-only C; WSL2 gives you a real Linux environment
inside Windows. Nothing you install here affects your normal Windows
setup.

### 1. Install WSL2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Reboot if prompted. After reboot you'll get an "Ubuntu" app in the Start
menu. Launch it once, set a Linux username and password (anything you
like, remember the password). You now have a Linux shell.

### 2. Copy this folder into WSL2

From inside the Ubuntu shell:

```bash
mkdir -p ~/ds
cp -r "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/recovered" ~/ds/
cp    "/mnt/c/Users/danbl/Documents/Claude DS/Devil's Silence Resurrected/rebuild_source.py" ~/ds/
cd ~/ds
ls
```

You should see `recovered/` and `rebuild_source.py`.

### 3. Install the build toolchain

```bash
sudo apt update
sudo apt install -y build-essential gcc make libc6-dev
```

That's it. Devil's Silence is plain C with no unusual dependencies.

### 4. Patch the source

```bash
cd ~/ds
python3 rebuild_source.py
```

You should see a sequence of `[ok]` messages ending in
"All patches applied." If you see `[FAIL]`, stop and paste the output
back to me.

### 5. Compile

```bash
cd ~/ds/src_patched
make
```

Expect warning output but no errors. When make finishes you'll have a
file called `ds.new` in the same directory — that's the compiled server.

### 6. Set up the run directory and boot

The server expects a specific layout: the binary runs from `bin/` and
reads world data from `../data/`. The recovered tree already has this.
We just need to drop the freshly compiled binary into `bin/`.

```bash
cd ~/ds
cp src_patched/ds.new recovered/devils/bin/ds
cp src_patched/ds.new recovered/devils/bin/ds.new
cd recovered/devils/bin
./ds 5000 5001
```

Port 5000 is the game port, 5001 is the companion web port. If the
server boots cleanly you'll see a sequence of `reading
../data/area/*.are` messages followed by something like
`Booting database`, `Resetting XYZ area`, and eventually
`Ready to rock at port 5000`.

If it crashes (likely on the first try), note the last "reading ..."
line — that tells us which area file upset it. Paste the output back
and we'll fix.

### 7. Connect from your Windows side

Download a MUD client — **Mudlet** is free and works well
(https://www.mudlet.org). Install, then:

* Add a new profile
* Server name: `localhost`
* Server port: `5000`
* Connect

You should see Devil's Silence's login banner. Create a character,
walk around, confirm the world responds.

### 8. Shut it down cleanly

From inside the game (as whatever character you made):

```
shutdown
```

If you're not an immortal you won't be able to shutdown in-game. In that
case just hit `Ctrl+C` in the WSL2 terminal where `./ds` is running.

## Milestone 2 — Let other people connect

Two options, cleanest first.

### Option A: rent a small Linux VPS (recommended)

Providers: DigitalOcean, Linode, Vultr, Hetzner. A $4–6/month instance
is overkill for a MUD. Steps:

1. Spin up an Ubuntu 22.04 instance
2. SSH in
3. Repeat steps 3–6 above on the VPS
4. Open port 5000 in the provider's firewall / security group
5. Give your friends the VPS's hostname or IP + port 5000

This is what the original Devil's Silence did circa 2003. Your home
network and home IP address stay private; the game runs on a server
that's always on.

### Option B: open a port on your home router

Faster to try, but it exposes your home IP and the MUD will be
scanned by bots within minutes. Not recommended long-term but fine
for a one-hour test with a specific friend.

1. Find your router admin page (usually http://192.168.1.1)
2. Forward external port 5000 to your PC's LAN IP, port 5000
3. Find your public IP at https://whatismyip.com
4. Friend connects to `your.public.ip:5000`

Don't leave this on. The MUD's 2003 code has not been security-audited
in 22 years.

## If something breaks

The patch script is the most brittle piece. If the build fails:

* `rebuild_source.py` should exit cleanly with all `[ok]` lines
* If you see `[FAIL] filename: expected N occurrence(s), found 0` that
  means the script's anchor text doesn't match the recovered source —
  paste the full output back to me
* `make` warnings are fine; errors (lines containing `error:`) are not
* If `./ds` starts but crashes on a specific area file, note the name
  and paste back — we can skip or repair the broken area

## What's next after Milestone 1

1. Re-port any DS-specific behaviour from the old compiled binary back
   into `update.c`'s stock tail (cosmetic — the game is fully playable
   without this).
2. Decide whether to modernise or keep maintaining C. Candidates for a
   rewrite if you want: Python + asyncio (easy to modify, slower),
   Go (fast, simple concurrency), or Rust (maximum performance and safety,
   steeper learning curve). But do it AFTER the C version is stable.
3. Reach out to the old DS Wikidot community — they may have saved
   additional pieces (public_html, clan data, god files) that would
   round out what we have.
