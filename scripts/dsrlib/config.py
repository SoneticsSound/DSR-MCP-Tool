"""
config.py — Path constants for dsrlib.

All paths resolve relative to the project root, derived from this file's
location (scripts/dsrlib/config.py → root is two levels up).
Add new paths here rather than hardcoding them in individual modules.
"""
import os

# Project root resolution order:
#   1. DSR_PROJECT_ROOT env var (recommended — point at your live project dir,
#      e.g. ~/ds or the code-sync mount, so the MCP sees current state without
#      a copy step)
#   2. Two directories above this file (scripts/dsrlib/config.py → root),
#      i.e. the MCP-Tool's own dir — used when no env var is set.
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT        = os.environ.get("DSR_PROJECT_ROOT", os.path.dirname(SCRIPTS_DIR))

# Source files
SRC_DIR     = os.path.join(ROOT, "recovered", "devils", "src")
AREA_DIR    = os.path.join(ROOT, "recovered", "devils", "data", "area")

# Project markdown documents (narrative context).
# MCP-Tool's tree historically holds these at ROOT (not docs/) — kept that way
# for backward compatibility. The briefing generator falls back to these when
# the JSON sources below are missing.
BUGS_MD      = os.path.join(ROOT, "BUGS.md")
IDEAS_MD     = os.path.join(ROOT, "IDEAS.md")
DECISIONS_MD = os.path.join(ROOT, "DECISIONS.md")
HANDOFF_MD   = os.path.join(ROOT, "CODE_HANDOFF.md")
CHANGELOG_MD = os.path.join(ROOT, "CHANGELOG.md")

# Project JSON state files (source of truth post-2026-05-02 migration).
# briefing() prefers these; falls back to the .md parsers above if a JSON
# file is missing. Place these alongside the .md files at MCP-Tool ROOT,
# OR override at install time via DSR_PROJECT_ROOT (see __init__.py).
BUGS_JSON          = os.path.join(ROOT, "bugs.json")
IDEAS_JSON         = os.path.join(ROOT, "ideas.json")
CODE_HANDOFF_JSON  = os.path.join(ROOT, "code_handoff.json")
COWORK_PROMPT_JSON = os.path.join(ROOT, "cowork_prompt.json")

# Generated output files
BRIEFING_MD  = os.path.join(ROOT, "BRIEFING.md")
INDEX_JSON   = os.path.join(SCRIPTS_DIR, "source_index.json")
INDEX_MD     = os.path.join(SCRIPTS_DIR, "SOURCE_INDEX.md")
