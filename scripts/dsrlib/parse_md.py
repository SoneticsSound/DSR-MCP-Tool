"""
parse_md.py — Markdown document parsers for DS:R project files.

Each parser reads one document and returns structured data (dicts/lists),
never raw text. Scripts and the MCP server both import from here so parsing
logic lives in exactly one place.

Public functions:
    read_file(path)         -> str  (safe read, empty string on missing)
    parse_bugs(text)        -> (open_bugs, staged_bugs)
    parse_ideas(text)       -> (open_count, planned_count, top_open)
    parse_decisions(text)   -> [recent_decisions]   newest first
    parse_handoff(text)     -> (blockers, questions)
    parse_build_version(text) -> str
"""
import re


def read_file(path):
    """Read a file safely. Returns empty string if the file doesn't exist."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        return ""


# ── BUGS.md ───────────────────────────────────────────────────────────────────

def parse_bugs(text):
    """
    Parse BUGS.md.

    Returns:
        open_bugs   : list of {id, severity, title}  — status open/investigating
        staged_bugs : list of {id, title}             — status fix-staged
    """
    entries = re.findall(
        r"### (BUG-\d+): (.+?)\n(.*?)(?=\n### BUG-|\n## |\Z)",
        text, re.DOTALL
    )

    SEVERITY_ORDER = {"crash": 0, "data-loss": 1, "functional": 2, "cosmetic": 3}

    open_bugs, staged_bugs = [], []
    for bug_id, title, body in entries:
        status_m   = re.search(r"\*\*Status:\*\*\s*(\S+)", body)
        severity_m = re.search(r"\*\*Severity:\*\*\s*(\S+)", body)
        status   = (status_m.group(1)   if status_m   else "unknown").lower().rstrip(",")
        severity = (severity_m.group(1) if severity_m else "unknown").lower().rstrip(",")

        entry = {"id": bug_id, "title": title.strip(), "severity": severity}
        if status in ("open", "investigating"):
            open_bugs.append(entry)
        elif status == "fix-staged":
            staged_bugs.append({"id": bug_id, "title": title.strip()})

    # Sort open bugs: crashes first
    open_bugs.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 4))
    return open_bugs, staged_bugs


# ── IDEAS.md ──────────────────────────────────────────────────────────────────

def parse_ideas(text, top_n=5):
    """
    Parse IDEAS.md.

    Returns:
        open_count    : int
        planned_count : int
        top_open      : list of {id, title}  — most recent open ideas, up to top_n
    """
    entries = re.findall(
        r"### (IDEA-\d+): (.+?)\n(.*?)(?=\n### IDEA-|\n## |\Z)",
        text, re.DOTALL
    )

    open_ideas, planned_count = [], 0
    for idea_id, title, body in entries:
        status_m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", body)
        status   = (status_m.group(1).strip().lower() if status_m else "unknown")
        if "open" in status:
            open_ideas.append({"id": idea_id, "title": title.strip()})
        elif "planned" in status or "in-progress" in status:
            planned_count += 1

    return len(open_ideas), planned_count, open_ideas[:top_n]


# ── DECISIONS.md ──────────────────────────────────────────────────────────────

def parse_decisions(text, top_n=5):
    """
    Parse DECISIONS.md.

    Returns:
        list of {id, date, title}  — most recent first, up to top_n
    """
    entries = re.findall(
        r"### (DECISION-\d+): (.+?)\n\*\*Date:\*\*\s*([^\n]+)",
        text
    )
    # File is oldest-first; reverse for newest-first
    entries = list(reversed(entries))
    return [
        {"id": d_id, "date": d_date.strip(), "title": title.strip()}
        for d_id, title, d_date in entries[:top_n]
    ]


# ── CODE_HANDOFF.md ───────────────────────────────────────────────────────────

def parse_handoff(text):
    """
    Parse CODE_HANDOFF.md ⚡ Questions section.

    Returns:
        blockers  : list of str  — unresolved BLOCKER / BUG items
        questions : list of str  — unresolved design questions for Code
    """
    m = re.search(
        r"## ⚡ Questions for Cowork.*?(?=\n## )",
        text, re.DOTALL
    )
    if not m:
        return [], []

    section   = m.group(0)
    blockers, questions = [], []

    for heading in re.findall(r"^### (.+)$", section, re.MULTILINE):
        # Skip anything already resolved or cleared
        if "RESOLVED" in heading.upper() or "CLEARED" in heading.upper():
            continue
        if "BLOCKER" in heading.upper() or heading.strip().startswith("🐛"):
            blockers.append(heading.strip())
        else:
            questions.append(heading.strip())

    return blockers, questions


# ── CHANGELOG.md ──────────────────────────────────────────────────────────────

def parse_build_version(text):
    """
    Extract current build version from CHANGELOG.md.
    Prefers the staged/unreleased entry; falls back to the latest versioned entry.
    """
    m = re.search(r"### (0\.\d+\.\d+) — staged", text)
    if m:
        return m.group(1) + " (staged)"
    m = re.search(r"## \[(0\.\d+\.\d+)\]", text)
    return m.group(1) if m else "unknown"
