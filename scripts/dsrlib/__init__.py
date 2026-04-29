"""
dsrlib — Devil's Silence Resurrected project toolkit.

Modules:
    config      — path constants, shared across all tools
    parse_md    — parsers for BUGS, IDEAS, DECISIONS, CODE_HANDOFF, CHANGELOG
    scan_source — C source file and area file indexers
    generate    — output generators (BRIEFING.md, SOURCE_INDEX.md)
"""
from . import config, parse_md, scan_source, generate
