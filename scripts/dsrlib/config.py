"""
config.py — Path constants for dsrlib.

All paths resolve relative to the project root, derived from this file's
location (scripts/dsrlib/config.py → root is two levels up).
Add new paths here rather than hardcoding them in individual modules.
"""
import os

# Project root: two directories above this file (scripts/dsrlib/ -> scripts/ -> root)
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT        = os.path.dirname(SCRIPTS_DIR)

# Source files
SRC_DIR     = os.path.join(ROOT, "recovered", "devils", "src")
AREA_DIR    = os.path.join(ROOT, "recovered", "devils", "data", "area")

# Project markdown documents
BUGS_MD      = os.path.join(ROOT, "BUGS.md")
IDEAS_MD     = os.path.join(ROOT, "IDEAS.md")
DECISIONS_MD = os.path.join(ROOT, "DECISIONS.md")
HANDOFF_MD   = os.path.join(ROOT, "CODE_HANDOFF.md")
CHANGELOG_MD = os.path.join(ROOT, "CHANGELOG.md")

# Generated output files
BRIEFING_MD  = os.path.join(ROOT, "BRIEFING.md")
INDEX_JSON   = os.path.join(SCRIPTS_DIR, "source_index.json")
INDEX_MD     = os.path.join(SCRIPTS_DIR, "SOURCE_INDEX.md")
