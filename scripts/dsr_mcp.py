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


# ── gsn database ──────────────────────────────────────────────────────────────

_gsn_db_cache: dict | None = None


def _load_gsn_db() -> dict:
    """
    Load the gsn database (built by scripts/build_gsn_db.py).

    Tries <ROOT>/docs/gsn_db.json first (the user's project layout when
    DSR_PROJECT_ROOT is set), then <ROOT>/gsn_db.json (MCP-Tool's
    historical root layout). Cached after first successful load.

    Returns {"meta": {...}, "gsns": {gsn_name: {...}}} or {} if missing.
    """
    global _gsn_db_cache
    if _gsn_db_cache is not None:
        return _gsn_db_cache

    candidates = [
        Path(config.ROOT) / "docs" / "gsn_db.json",
        Path(config.ROOT) / "gsn_db.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    _gsn_db_cache = json.load(f)
                    return _gsn_db_cache
            except (OSError, json.JSONDecodeError):
                continue
    _gsn_db_cache = {}
    return _gsn_db_cache


def _format_gsn_entry(symbol: str, entry: dict) -> str:
    """Pretty-print one gsn_db entry to a single multi-line block."""
    skill   = entry.get("skill_name", "?")
    addr    = entry.get("address",    "?")
    refs    = entry.get("referenced_in", []) or []
    helpkey = entry.get("help_entry")
    words   = entry.get("help_words", 0) or 0

    lines = [
        f"  {symbol}",
        f"    skill:    {skill}",
        f"    address:  {addr}",
    ]
    if helpkey:
        lines.append(f"    helpfile: {helpkey}  ({words} words)")
    else:
        lines.append(f"    helpfile: ⚠ MISSING  (0 words)")
    if refs:
        lines.append(f"    refs:     {', '.join(refs)}")
    else:
        lines.append(f"    refs:     —")
    return "\n".join(lines)


@mcp.tool()
def query_gsn(name: str = "", missing: bool = False, refs: str = "") -> str:
    """
    Query the gsn (global skill number) database.

    The gsn database is the rosetta stone for DS binary archaeology —
    it cross-references every gsn_* symbol in the live binary against
    its skill name, every .c file that touches it, and its helpfile
    entry (if one exists). Lets you map "what skill does this do_*
    function touch" and "what code touches this gsn" in one query.

    Three modes (use exactly one):

    1. **By name** — query_gsn(name="hack")
       Looks up a single gsn by skill name, gsn_<name>, or do_<name>.
       Returns its address, skill name, source files that reference it,
       and helpfile entry. Substring-match: query_gsn(name="aura") will
       return all gsn_aura_of_*.

    2. **--missing** — query_gsn(missing=True)
       Lists every gsn with no helpfile entry. Gap report for Cowork
       to know which skills need helpfile authoring.

    3. **--refs <file>** — query_gsn(refs="update.c")
       Lists every gsn referenced anywhere in a .c file. Substring
       match (e.g. refs="update" hits update.c too). Useful for "what
       skills does the per-tick handler touch" research.

    Returns a formatted multi-entry summary, or a "no gsns found"
    message. Run scripts/build_gsn_db.py to refresh the underlying
    database after adding new gsns.
    """
    db = _load_gsn_db()
    gsns = db.get("gsns", {})

    if not gsns:
        return ("gsn_db.json not found or empty. Run "
                "`python3 scripts/build_gsn_db.py` against the project "
                "to populate it.")

    # Mode dispatch — only one of {name, missing, refs} should be set.
    used_modes = sum(1 for v in (bool(name), missing, bool(refs)) if v)
    if used_modes > 1:
        return ("Pick one mode: name=, missing=True, OR refs=. "
                "Combining modes is not supported.")

    # Mode 3: --refs <file>
    if refs:
        needle  = refs.lower()
        matches = []
        for sym, entry in gsns.items():
            for ref in entry.get("referenced_in", []) or []:
                if needle in ref.lower():
                    matches.append((sym, entry))
                    break
        matches.sort(key=lambda p: p[0])
        if not matches:
            return f"  0 gsns referenced in files matching '{refs}'."
        out = [f"  {len(matches)} gsns referenced in files matching '{refs}':", ""]
        for sym, entry in matches[:80]:
            out.append(_format_gsn_entry(sym, entry))
            out.append("")
        if len(matches) > 80:
            out.append(f"  …and {len(matches) - 80} more.")
        return "\n".join(out)

    # Mode 2: --missing
    if missing:
        gaps = sorted(
            sym for sym, entry in gsns.items()
            if not entry.get("help_entry")
        )
        if not gaps:
            return "  All gsns have helpfile entries. Nothing missing."
        head = f"  {len(gaps)} gsns with no helpfile entry."
        # Paginate — 60 per call to avoid token blowup
        return head + "\n  " + ", ".join(gaps[:60]) + (
            f"\n  …and {len(gaps) - 60} more." if len(gaps) > 60 else ""
        )

    # Mode 1: name lookup
    if not name:
        return ("Specify a mode: name=<skill>, missing=True, OR refs=<file>. "
                "See `query_gsn` docstring for details.")

    needle = name.lower().strip()
    # Strip "do_" if user passed a function name
    if needle.startswith("do_"):
        needle = needle[3:]
    # Try exact gsn_<needle> first
    exact = f"gsn_{needle.replace(' ', '_')}"

    matches = []
    if exact in gsns:
        matches.append((exact, gsns[exact]))
    # Then substring search (skip the exact match we already added)
    for sym, entry in gsns.items():
        if sym == exact:
            continue
        skill_name = (entry.get("skill_name") or "").lower()
        if needle in sym.lower() or needle in skill_name:
            matches.append((sym, entry))

    if not matches:
        return f"  No gsns found matching '{name}'."

    out = [f"  {len(matches)} gsn(s) found:", ""]
    for sym, entry in matches[:25]:
        out.append(_format_gsn_entry(sym, entry))
        out.append("")
    if len(matches) > 25:
        out.append(f"  …and {len(matches) - 25} more (refine the query).")
    return "\n".join(out)


# ── helpfile database ─────────────────────────────────────────────────────────

_help_db_cache: dict | None = None


def _load_help_db() -> dict:
    """
    Load the helpfile database (built by scripts/build_help_db.py).

    Tries <ROOT>/docs/help_db.json first then <ROOT>/help_db.json.
    Cached after first successful load.

    Returns {"meta": {...}, "helps": {keyword: {...}}} or {} if missing.
    """
    global _help_db_cache
    if _help_db_cache is not None:
        return _help_db_cache

    candidates = [
        Path(config.ROOT) / "docs" / "help_db.json",
        Path(config.ROOT) / "help_db.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    _help_db_cache = json.load(f)
                    return _help_db_cache
            except (OSError, json.JSONDecodeError):
                continue
    _help_db_cache = {}
    return _help_db_cache


def _format_help_entry(key: str, entry: dict, full: bool = False) -> str:
    """Pretty-print one help_db entry. full=True returns the body verbatim."""
    keywords = entry.get("all_keywords") or [entry.get("primary_keyword", key)]
    words    = entry.get("word_count", 0)
    source   = entry.get("source", "?")
    text     = entry.get("text", "") or ""

    lines = [
        f"  [{key}]",
        f"      keywords: {' | '.join(keywords)}",
        f"      words:    {words}",
        f"      source:   {source}",
        f"      ─────────────────────────────────────",
    ]
    body = text if full else (text[:300] + ("…" if len(text) > 300 else ""))
    for ln in body.splitlines():
        lines.append(f"      {ln}")
    return "\n".join(lines)


@mcp.tool()
def query_helpfile(term: str = "", full: bool = False) -> str:
    """
    Query the helpfile database — find helpfile entries by keyword or
    body-text substring.

    The helpfile database is built by scripts/build_help_db.py from
    every #HELPS section across area/*.are, data/area/*.are,
    data/misc/*.are, and data/misc/*.mhp. Cross-referenced with
    gsn_db.json so spells/skills find their helpfile by SKILL_<NAME> or
    SPELL_<NAME> automatic key lookup.

    Args:
        term: Keyword (case-insensitive), or substring to match in
              the entry's text body. Examples:
                term="hack"        → finds SKILL_HACK, etc.
                term="continual"   → finds SPELL_CONTINUAL_LIGHT
                term="treant"      → finds RACE_TREANT
                term="vital"       → finds SKILL_VITAL_STRIKE
                term=""            → returns the gap-list summary
                                     (count of unkeyed helpfiles).
        full: True returns the entry body verbatim (default False:
              first 300 chars per match).

    Returns a formatted multi-entry summary, or a "no helpfiles found"
    message. Entries match in the order: exact key, prefix-of-key,
    keyword-contains, then body-text-contains. Caps at 25 results
    (refine the term to narrow further).
    """
    db = _load_help_db()
    helps = db.get("helps", {})

    if not helps:
        return ("help_db.json not found or empty. Run "
                "`python3 build_help_db.py --area ~/ds/Resurrected/area/ "
                "--pretty` against the project to populate it.")

    # Empty term — return summary
    if not term:
        meta = db.get("meta", {})
        return (
            f"  help_db summary: {len(helps)} entries\n"
            f"  source files: {meta.get('source_files', meta.get('total_helps', '?'))}\n"
            f"  Pass term=<keyword> to query, or term=<substring> to search "
            f"keyword AND body text."
        )

    needle = term.lower().strip()

    # Search in priority order: exact key, prefix, keyword-contains,
    # body-contains. Dedupe across categories.
    seen    = set()
    matches = []

    # 1. Exact key (case-insensitive)
    for k in helps:
        if k.lower() == needle and k not in seen:
            matches.append((k, helps[k])); seen.add(k)

    # 2. SKILL_<NEEDLE> / SPELL_<NEEDLE> shorthand
    for prefix in ("SKILL_", "SPELL_", "RACE_", "CLASS_"):
        candidate = (prefix + needle.upper().replace(" ", "_")).strip()
        if candidate in helps and candidate not in seen:
            matches.append((candidate, helps[candidate])); seen.add(candidate)

    # 3. Substring of key (excluding what we already matched)
    for k in helps:
        if k in seen:
            continue
        if needle in k.lower():
            matches.append((k, helps[k])); seen.add(k)

    # 4. Substring in keywords list (for compound-keyword entries)
    for k, v in helps.items():
        if k in seen:
            continue
        kws = v.get("all_keywords") or []
        if any(needle in str(kw).lower() for kw in kws):
            matches.append((k, v)); seen.add(k)

    # 5. Substring in body text — only if we have <5 hits so far
    #    (body search is slow + noisy)
    if len(matches) < 5:
        for k, v in helps.items():
            if k in seen:
                continue
            body = (v.get("text") or "").lower()
            if needle in body:
                matches.append((k, v)); seen.add(k)

    if not matches:
        return f"  No helpfiles found matching '{term}'."

    out = [f"  {len(matches)} helpfile(s) found:", ""]
    for k, v in matches[:25]:
        out.append(_format_help_entry(k, v, full=full))
        out.append("")
    if len(matches) > 25:
        out.append(f"  …and {len(matches) - 25} more (refine the term).")
    return "\n".join(out)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
