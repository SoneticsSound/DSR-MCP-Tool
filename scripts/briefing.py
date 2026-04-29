#!/usr/bin/env python3
"""
briefing.py — Generate DS:R session briefing.
Thin CLI wrapper around dsrlib.generate.briefing().
Run: python3 scripts/briefing.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsrlib.generate import briefing

if __name__ == "__main__":
    output = briefing(write=True)
    print(output)
    from dsrlib.config import BRIEFING_MD
    print(f"\nWritten to {BRIEFING_MD}")
