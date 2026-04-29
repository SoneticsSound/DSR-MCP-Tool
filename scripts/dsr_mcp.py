"""
dsr_mcp.py — Devil's Silence Resurrected MCP Server
=====================================================
A local MCP server that gives Cowork (Claude) direct access to DS:R
project state without burning tokens on large file reads.

Tools exposed:
    get_briefing()              Current build, bugs, decisions, ideas summary
    get_open_bugs()             Open bugs list with severity
    get_recent_decisions()      Last N design decisions
    get_missing_implementations() Commands wired in interp.c with no source
    query_function(name)        Look up a do_* function location
    query_vnum(vnum)            Which area file owns a vnum
    query_area(filename)        Vnum range + name for an area file
    refresh_index()             Re-scan source tree (after git pull)

Setup:
    pip install "mcp[cli]"
    python scripts/install_mcp.py    (registers with Claude Desktop)

Then restart Claude Desktop — the dsr: tools will appear.
"""

import sys
import os
import json
from pathlib import Path

# ── Path setup — finds dsrlib relative to this file ───────────────────────────
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    from fastmcp import FastMCP
from dsrlib import config
from dsrlib.parse_md import (
    read_file, parse_bugs, parse_ideas,
    parse_decisions, parse_handoff, parse_build_version
)
from dsrlib.generate import briefing as gen_briefing
from dsrlib.scan_source import build_full_index

# ── Server setup ──────────────────────────────────────────────────────────────
mcp = FastMCP("dsr")

# Cache the source index in memory so repeated queries don't re-scan
_index_cache: dict | None = None


def _get_index() -> dict:
    """Return cached source index, building it if needed."""
    global _index_cache
    if _index_cache is None:
        _index_cache = build_full_index(config.SRC_DIR, config.AREA_DIR)
    return _index_cache


# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_briefing() -> str:
    """
    Generate and return the full DS:R session briefing.
    Covers current build version, open bugs, pending Code questions,
    recent design decisions, and ideas backlog summary.
    Use this at the start of any session instead of reading individual .md files.
    """
    return gen_briefing(write=True)


@mcp.tool()
def get_open_bugs() -> str:
    """
    Return all open and staged bugs from BUGS.md.
    Open bugs are sorted by severity (crash first).
    """
    text       = read_file(config.BUGS_MD)
    open_bugs, staged = parse_bugs(text)

    lines = [f"## Open Bugs ({len(open_bugs)})"]
    for b in open_bugs:
        lines.append(f"- {b['id']} [{b['severity']}] {b['title']}")

    if staged:
        lines.append(f"\n## Staged / Needs QA ({len(staged)})")
        for b in staged:
            lines.append(f"- {b['id']}: {b['title']}")

    return "\n".join(lines)


@mcp.tool()
def get_recent_decisions(count: int = 10) -> str:
    """
    Return the most recent design decisions from DECISIONS.md.

    Args:
        count: Number of decisions to return (default 10, max 50)
    """
    count = min(count, 50)
    text  = read_file(config.DECISIONS_MD)
    decisions = parse_decisions(text, top_n=count)

    lines = [f"## Recent Decisions (newest first, showing {len(decisions)})"]
    for d in decisions:
        lines.append(f"- **{d['id']}** ({d['date']}) — {d['title']}")
    return "\n".join(lines)


@mcp.tool()
def get_missing_implementations() -> str:
    """
    Return commands wired in interp.c that have no matching do_* function
    in the workspace source tree.

    Note: functions in act_combat.c will appear missing until Code pushes
    to GitHub and Kyle does a git pull. Call refresh_index() after pulling.
    """
    index   = _get_index()
    missing = index["wired_missing"]

    lines = [
        f"## Missing Implementations ({len(missing)})",
        "*Commands in interp.c with no source in workspace.*",
        "*After git pull, call refresh_index() to update.*\n",
    ]
    for item in sorted(missing, key=lambda x: x["command"]):
        lines.append(f"- `{item['command']}` → `{item['function']}` (trust {item['trust']})")
    return "\n".join(lines)


@mcp.tool()
def query_function(name: str) -> str:
    """
    Look up a do_* function by name.

    Args:
        name: Function name, e.g. "do_forge" or just "forge"

    Returns location (file + line), whether it's wired in interp.c,
    and what command name triggers it.
    """
    # Normalise — accept "forge" or "do_forge"
    if not name.startswith("do_"):
        name = "do_" + name

    index    = _get_index()
    do_fns   = index["do_functions"]
    present  = {c["function"]: c for c in index["wired_present"]}
    missing  = {c["function"]: c for c in index["wired_missing"]}

    if name not in do_fns:
        # Check if it's wired but just not in workspace
        if name in missing:
            m = missing[name]
            return (f"`{name}` — NOT FOUND in workspace source.\n"
                    f"Wired in interp.c as command `{m['command']}` (trust {m['trust']}).\n"
                    f"Likely in act_combat.c — needs git pull from Code's branch.")
        return f"`{name}` — not found in source and not wired in interp.c."

    info = do_fns[name]
    result = [f"`{name}` — {info['file']}, line {info['line']}"]

    if name in present:
        p = present[name]
        result.append(f"Wired in interp.c as command `{p['command']}` (trust {p['trust']}, line {p['line']})")
    else:
        result.append("Not wired in interp.c (internal helper or not yet registered)")

    return "\n".join(result)


@mcp.tool()
def query_vnum(vnum: int) -> str:
    """
    Find which area file owns a given vnum.

    Args:
        vnum: The object/mob/room vnum to look up

    Returns the area file, area name, and full vnum range.
    """
    index = _get_index()
    areas = index["area_vnums"]

    matches = []
    for fname, info in areas.items():
        if info["min_vnum"] <= vnum <= info["max_vnum"]:
            matches.append((fname, info))

    if not matches:
        return f"Vnum {vnum} not found in any indexed area file."

    lines = [f"## Vnum {vnum}"]
    for fname, info in matches:
        lines.append(
            f"- **{fname}** ({info['name']}) — range {info['min_vnum']}–{info['max_vnum']}"
        )
    return "\n".join(lines)


@mcp.tool()
def query_area(filename: str) -> str:
    """
    Return vnum range and metadata for an area file.

    Args:
        filename: Area filename, e.g. "solennir.are" (or just "solennir")
    """
    if not filename.endswith(".are"):
        filename += ".are"

    index = _get_index()
    areas = index["area_vnums"]

    if filename not in areas:
        # Fuzzy match on name
        needle = filename.replace(".are", "").lower()
        matches = [(f, i) for f, i in areas.items()
                   if needle in f.lower() or needle in i["name"].lower()]
        if not matches:
            return f"Area file `{filename}` not found."
        filename, info = matches[0]
    else:
        info = areas[filename]

    return (
        f"## {filename}\n"
        f"- Name: {info['name']}\n"
        f"- Vnum range: {info['min_vnum']} – {info['max_vnum']}\n"
        f"- Indexed entries: {info['count']}"
    )


@mcp.tool()
def refresh_index() -> str:
    """
    Re-scan the source tree and area files, clearing the cached index.
    Call this after Kyle does a git pull to pick up Code's latest changes
    (especially new functions in act_combat.c).
    """
    global _index_cache
    _index_cache = None
    index = _get_index()  # Rebuild

    missing = index["wired_missing"]
    present = index["wired_present"]

    return (
        f"Index refreshed.\n"
        f"- do_* functions found: {len(index['do_functions'])}\n"
        f"- Commands wired: {len(index['interp_commands'])}\n"
        f"- With implementation: {len(present)}\n"
        f"- Missing implementation: {len(missing)}\n"
        f"- Area files: {len(index['area_vnums'])}"
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
