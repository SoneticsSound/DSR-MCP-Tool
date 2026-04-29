# Contributing to Devil's Silence Resurrected

Welcome! This doc is for anyone who wants to help rebuild DS —
whether you're a coder, a writer, or just someone who played the
original and remembers how things worked.

**You do not need to know how to code to contribute meaningfully.**

---

## What this project is

Devil's Silence was a clan-based PvP MUD (text-based multiplayer RPG)
from 2003. We're bringing it back from a corrupted archive. The server
runs, the world loads, players can connect — but about a third of the
combat abilities are still stubbed out ("that ability isn't available
right now"). We're putting them back one by one.

The server runs 24/7 (when Kyle's laptop is on) at:
`7.tcp.ngrok.io:25597` — connect with any MUD client (Mudlet is free)
or via telnet.

---

## The fastest way to contribute right now

### 1. Play and break things

Connect to the server, make a character, try abilities. When something
doesn't work right — wrong message, crash, weird behaviour — type:

```
bug <description of what happened>
```

That writes to a log file Kyle and Claude read. You don't need to know
why it broke, just what you were doing when it did.

### 2. Remember things

If you played the original DS, your memory is a primary source. Things
we need:

- What did `[ability name]` actually do?
- How did the `[class name]` class play?
- What were the class tiers and how did remort work?
- What areas existed and what was special about them?

Drop these in Discord or OOC in-game. They go into the design docs and
directly inform how abilities get rebuilt.

### 3. Write content

Room descriptions, mob flavour text, helpfile rewrites — all plain text,
no coding. We have a full IDEAS log of content work that needs a writer.
If you want to draft something, ask Kyle for the `HELPFILES.md` or
`IDEAS.md` from the repo and pick something.

---

## How the code side works (for coders or the curious)

### The repo structure

The key files you'll interact with:

| File | What it is |
|---|---|
| `SESSION_STATE.md` | Full project status — read this first |
| `COWORK_PROMPT.md` | Current task queue for the AI coding agent |
| `CODE_HANDOFF.md` | What was last built, md5, test plan |
| `COMBAT_CATALOG.md` | Every combat ability — status, size, source |
| `BUGS.md` | Open and resolved bugs |
| `IDEAS.md` | Feature ideas and design notes |
| `DS_SCHEMA.md` | DS-specific struct/field reference |
| `CHANGELOG.md` | Per-version history |
| `*.py` | Patcher scripts — each one makes one surgical change |

The C source lives in WSL2 on Kyle's machine (not in this repo). This
repo is the coordination layer — docs, patcher scripts, and the
AI-to-AI handoff files.

### How abilities get ported

Every combat ability in DS was compiled into a binary in 2003. The
source was lost, but the compiled machine code is intact. The workflow:

1. **Disassemble** the original binary to read the assembly for a function
2. **Translate** the assembly back to C (Claude does this step)
3. **Write a patcher** — a Python script that surgically inserts the
   new C function into the source file
4. **Build and deploy** — compile, copy binary, hot-swap via `copyover`
5. **Test in-game** — Kyle verifies the ability works correctly

You can contribute at any of these steps.

### The patcher pattern

Every patcher script follows the same shape:

```python
# 1. Check sentinel — if already patched, do nothing (safe to re-run)
if SENTINEL in source_text:
    print("Already patched.")
    sys.exit(0)

# 2. Write atomic backup before touching anything
shutil.copy2(SOURCE_FILE, BACKUP_FILE)

# 3. Make one surgical edit — replace stub with real implementation
patched = source_text.replace(OLD_STUB, NEW_IMPLEMENTATION)

# 4. Write the result
SOURCE_FILE.write_text(patched)
```

Sentinels are comment strings embedded in the code that prove the
patch was applied. Backups mean any patch is one `cp` command from
being undone.

---

## How to submit code changes

There are two paths depending on how you work. Both are valid.

### Path A — Edit directly, let Code formalize it (recommended for coders)

If you're comfortable writing C or editing the source files directly:

1. Clone the repo and make your changes to the relevant `.c` files
2. Push to GitHub — just the changed source files, nothing else
3. Tell Kyle what you changed and why (Discord or a short commit message)
4. Kyle tells Code to `git pull` and pick up your changes
5. Code reviews the diff, writes a proper sentinel-checked patcher from
   it, applies it to the WSL2 source, builds, and tests
6. If something's wrong, Code flags it in `CODE_HANDOFF.md` and Kyle
   loops back to you

You don't need to know anything about the patcher pattern. Code handles
the formalization. Your job is just to write correct C.

### Path B — Write a patcher script yourself

If you want full control over exactly what gets applied:

Follow the patcher pattern (see below) and push a `port_yourfeature.py`
to the repo. Kyle runs it in WSL2 after review. This is how Kyle and
Code do it natively, and it's the safest path because the sentinel check
makes the script safe to re-run and the backup means any change is one
`cp` command from being undone.

---

## How to use Claude as your pair programmer

This is the core workflow. You don't write C from scratch — you
describe what you want, Claude reads the codebase, and Claude writes
the patcher. You review and run it.

### Setup

1. Clone the repo to your machine
2. Open [claude.ai](https://claude.ai) or Cowork (if you have it)
3. Point Claude at the repo files — paste relevant docs into the
   conversation or use a tool that can read files

### What to tell Claude

Give Claude context:
- "I'm working on Devil's Silence Resurrected — read SESSION_STATE.md
  and COMBAT_CATALOG.md first"
- "I want to port `do_roundhouse` (339b, DS custom)"
- "Here is what the disasm shows: [paste disasm output]"
- "Write a patcher script following the same pattern as the other
  `port_*.py` files in the repo"

Claude will ask clarifying questions, read the relevant files, and
produce a patcher script you can run in WSL2.

### What you need on your machine to run patchers

- WSL2 (Windows Subsystem for Linux) with Ubuntu
- The DS source tree (Kyle will share access)
- Python 3 (comes with Ubuntu)
- gcc multilib (for building the 32-bit binary)

If you don't have WSL2, you can still write patcher scripts and hand
them to Kyle to run. Claude writes the script, you review it, Kyle
runs it.

---

## Content contributions (no coding at all)

These are always open and always useful:

### Helpfile rewrites

The in-game `help` command has terse 2003 entries. We want to rewrite
them to actually teach new players how to play. If you can write
clearly and remember how abilities worked, this is high-value work.

Format: plain text, one helpfile per ability. See `HELPFILES.md` for
the current entries to use as a reference.

### Area and world content

Room descriptions, mob names, NPC dialogue flavour. The world loads
but a lot of it is sparse 2003 text. If you want to write for a
specific zone, ask Kyle which areas are candidates for polish.

### Ideas and design

Drop ideas into Discord or OOC. They get logged into `IDEAS.md` with
full context. Rex has already contributed several major design ideas
this way — the arena structure, Kensai class design, daze mechanic
rework. No barrier to entry.

---

## Submitting changes via GitHub

1. Fork or clone the repo
2. Make your changes (patcher scripts, doc edits, content files)
3. Submit a pull request with a short description of what changed
4. Kyle reviews before anything touches the live server

For patcher scripts specifically: include a comment at the top
explaining what the patch does and why, following the same format as
the existing `*.py` files.

---

## Questions?

- OOC in-game
- Discord
- Ask Claude directly — paste this file and your question and it'll
  have full context

The project is moving fast. The best thing you can do is show up,
play, and tell us what's broken or what you remember.
