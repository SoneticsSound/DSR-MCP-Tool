"""
generate.py — Output generators for DS:R tooling.

Builds BRIEFING.md and SOURCE_INDEX.md from parsed/indexed data.
Both functions return the generated text AND write it to disk.

Public functions:
    briefing()      -> str   writes BRIEFING.md
    source_index()  -> str   writes SOURCE_INDEX.md + source_index.json
"""
import json
import os
from collections import defaultdict
from datetime import date

from . import config
from .parse_md import (
    read_file, parse_bugs, parse_ideas,
    parse_decisions, parse_handoff, parse_build_version
)
from .scan_source import build_full_index


# ── Briefing ──────────────────────────────────────────────────────────────────

def _load_json(primary_path):
    """
    Load a JSON file; return None if missing or unparseable.

    Tries the primary path first, then a `docs/` sibling (e.g. ROOT/bugs.json
    then ROOT/docs/bugs.json). The user's project keeps these files in docs/
    while the MCP-Tool's own tree historically holds them at ROOT — checking
    both makes config robust to either layout.
    """
    candidates = [primary_path]
    head, tail = os.path.split(primary_path)
    candidates.append(os.path.join(head, "docs", tail))
    for path in candidates:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
    return None


def _bugs_from_json(data):
    """
    Map bugs.json schema → (open_bugs, staged_bugs) lists.

    Schema (2026-05-02): {"open": [{id, title, severity, status, ...}, ...],
                          "resolved": [...]}

    "Staged" bugs are those whose status is 'fix-staged' or starts with 'staged'
    (treated as needing Kyle QA — same semantic as the old .md parser).
    """
    open_list   = data.get("open", []) if isinstance(data, dict) else []
    open_bugs   = []
    staged_bugs = []
    for b in open_list:
        if not isinstance(b, dict):
            continue
        status = (b.get("status") or "").lower()
        entry = {
            "id":       b.get("id", "?"),
            "title":    b.get("title", b.get("note", "")),
            "severity": b.get("severity", "?"),
        }
        if "staged" in status:
            staged_bugs.append(entry)
        else:
            open_bugs.append(entry)
    return open_bugs, staged_bugs


def _ideas_from_json(data, top_n=5):
    """
    Map ideas.json schema → (open_count, planned_count, top_ideas).

    Schema: {"open": [...], "wontfix": [...], "done": [...]}
    "Planned" = open ideas tagged status='planned' (or fall back to count of all open).
    "top_ideas" = first N open by date_proposed descending (or list order if no date).
    """
    if not isinstance(data, dict):
        return 0, 0, []
    open_list = data.get("open", [])
    open_count = len(open_list)
    planned_count = sum(
        1 for i in open_list
        if isinstance(i, dict) and (i.get("status") or "").lower() == "planned"
    )
    # Sort by date_proposed desc when available; stable for items missing the field.
    sortable = [i for i in open_list if isinstance(i, dict)]
    sortable.sort(key=lambda i: i.get("date_proposed", ""), reverse=True)
    top_ideas = [
        {"id": i.get("id", "?"), "title": i.get("title", "")}
        for i in sortable[:top_n]
    ]
    return open_count, planned_count, top_ideas


def _handoff_from_json(data):
    """
    Map code_handoff.json schema → (blockers, questions).

    Schema: {"queue_for_cowork": [str, ...], "open_questions": [{id, question, blocking}, ...]}
    Blockers = open_questions with blocking=True (queue_for_cowork is informational, not blocking).
    Questions = all open_questions text.
    """
    if not isinstance(data, dict):
        return [], []
    blockers  = []
    questions = []
    for q in data.get("open_questions", []):
        if not isinstance(q, dict):
            continue
        text = f"{q.get('id', '?')}: {q.get('question', '')}"
        questions.append(text)
        if q.get("blocking"):
            blockers.append(text)
    return blockers, questions


def briefing(write=True):
    """
    Generate the session briefing.

    Prefers structured JSON sources (bugs.json / ideas.json / code_handoff.json,
    introduced 2026-05-02). Falls back to the legacy .md parsers if JSON is
    missing or unparseable, so the briefing still works on older trees.

    Args:
        write: if True, writes to config.BRIEFING_MD

    Returns:
        Generated markdown string.
    """
    # ── Bugs (JSON-preferred) ─────────────────────────────────────────────
    bugs_json = _load_json(config.BUGS_JSON)
    if bugs_json is not None:
        open_bugs, staged_bugs = _bugs_from_json(bugs_json)
    else:
        open_bugs, staged_bugs = parse_bugs(read_file(config.BUGS_MD))

    # ── Ideas (JSON-preferred) ────────────────────────────────────────────
    ideas_json = _load_json(config.IDEAS_JSON)
    if ideas_json is not None:
        open_count, planned_count, top_ideas = _ideas_from_json(ideas_json)
    else:
        open_count, planned_count, top_ideas = parse_ideas(read_file(config.IDEAS_MD))

    # ── Handoff blockers / questions (JSON-preferred) ─────────────────────
    handoff_json = _load_json(config.CODE_HANDOFF_JSON)
    if handoff_json is not None:
        blockers, questions = _handoff_from_json(handoff_json)
        # build_ver also lives in JSON build state — prefer it, fall back below
        build_ver = (handoff_json.get("build", {}) or {}).get("live_version")
    else:
        blockers, questions = parse_handoff(read_file(config.HANDOFF_MD))
        build_ver = None

    # ── Decisions (still .md — DECISIONS.md hasn't been migrated to JSON) ─
    decisions_text   = read_file(config.DECISIONS_MD)
    recent_decisions = parse_decisions(decisions_text)

    # ── Build version: prefer JSON, fall back to changelog parser ─────────
    if not build_ver:
        changelog_text = read_file(config.CHANGELOG_MD)
        build_ver      = parse_build_version(changelog_text)

    lines = [
        f"# DS:R Session Briefing — {date.today()}",
        "*Generated by dsrlib.generate.briefing() — do not edit manually.*\n",
        f"## Current Build: {build_ver}\n",
    ]

    if blockers:
        lines.append("## Blockers (Code queue)")
        for b in blockers:
            lines.append(f"- {b}")
        lines.append("")

    lines.append(f"## Open Bugs ({len(open_bugs)} open, {len(staged_bugs)} need QA)")
    if open_bugs:
        for b in open_bugs:
            lines.append(f"- **{b['id']}** [{b['severity']}] {b['title']}")
    else:
        lines.append("- None")
    if staged_bugs:
        lines.append("\n*Staged — needs Kyle QA:*")
        for b in staged_bugs:
            lines.append(f"- {b['id']}: {b['title']}")
    lines.append("")

    if questions:
        lines.append("## Open Questions for Code")
        for q in questions:
            lines.append(f"- {q}")
        lines.append("")

    lines.append("## Recent Decisions (newest first)")
    for d in recent_decisions:
        lines.append(f"- **{d['id']}** ({d['date']}) — {d['title']}")
    lines.append("")

    lines.append(f"## Ideas Backlog: {open_count} open, {planned_count} planned")
    lines.append("*Most recent open:*")
    for idea in top_ideas:
        lines.append(f"- {idea['id']}: {idea['title']}")
    lines.append("")

    lines += [
        "---",
        "*Detail: BUGS.md · IDEAS.md · DECISIONS.md · CODE_HANDOFF.md*"
    ]

    output = "\n".join(lines)
    if write:
        with open(config.BRIEFING_MD, "w", encoding="utf-8") as f:
            f.write(output)
    return output


# ── Source index ──────────────────────────────────────────────────────────────

def source_index(write=True):
    """
    Generate SOURCE_INDEX.md and source_index.json from the recovered source tree.

    Args:
        write: if True, writes to config.INDEX_MD and config.INDEX_JSON

    Returns:
        (markdown_str, index_dict)
    """
    data    = build_full_index(config.SRC_DIR, config.AREA_DIR)
    present = data["wired_present"]
    missing = data["wired_missing"]
    do_fns  = data["do_functions"]
    gsns    = data["gsn_declarations"]
    areas   = data["area_vnums"]

    present_funcs = {c["function"] for c in present}

    lines = [
        "# DS:R Source Index",
        "*Generated by dsrlib.generate.source_index() — do not edit manually.*\n",
        "## Summary",
        f"- **do_* functions in source:** {len(do_fns)}",
        f"- **Commands wired in interp.c:** {len(data['interp_commands'])}",
        f"  - With implementation: {len(present)}",
        f"  - **Missing implementation: {len(missing)}** "
        f"(may include act_combat.c not yet git-pulled)",
        f"- **gsn_* declarations:** {len(gsns)}",
        f"- **Area files:** {len(areas)}\n",
    ]

    if missing:
        lines += [
            "## Wired Commands Missing Source Implementation",
            "*Commands in interp.c with no matching do_* in workspace.*",
            "*If act_combat.c is not synced from GitHub, those will appear here.*\n",
            "| Command | Expected Function | Trust |",
            "|---------|------------------|-------|",
        ]
        for item in sorted(missing, key=lambda x: x["command"]):
            lines.append(f"| `{item['command']}` | `{item['function']}` | {item['trust']} |")
        lines.append("")

    lines.append("## do_* Function Locations")
    by_file = defaultdict(list)
    for func, info in sorted(do_fns.items()):
        by_file[info["file"]].append((func, info["line"]))
    for fname in sorted(by_file.keys()):
        funcs = sorted(by_file[fname], key=lambda x: x[1])
        lines.append(f"\n### {fname} ({len(funcs)} functions)")
        for func, ln in funcs:
            flag = "" if func in present_funcs else " *(not wired)*"
            lines.append(f"- `{func}` line {ln}{flag}")

    if gsns:
        lines.append("\n## gsn_* Declarations")
        by_file2 = defaultdict(list)
        for gsn, info in sorted(gsns.items()):
            by_file2[info["file"]].append((gsn, info["line"]))
        for fname in sorted(by_file2.keys()):
            entries = sorted(by_file2[fname], key=lambda x: x[1])
            lines.append(f"\n### {fname}")
            for gsn, ln in entries:
                lines.append(f"- `{gsn}` line {ln}")

    lines += [
        "\n## Area Vnum Ranges",
        "| File | Name | Min | Max | Count |",
        "|------|------|-----|-----|-------|",
    ]
    for fname, info in sorted(areas.items()):
        lines.append(
            f"| {fname} | {info['name']} | {info['min_vnum']} "
            f"| {info['max_vnum']} | {info['count']} |"
        )

    lines += ["\n---", "*Regenerate: python3 scripts/index_source.py*"]
    output = "\n".join(lines)

    if write:
        os.makedirs(os.path.dirname(config.INDEX_MD), exist_ok=True)
        with open(config.INDEX_MD, "w", encoding="utf-8") as f:
            f.write(output)
        with open(config.INDEX_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    return output, data
