#!/usr/bin/env python3
"""
index_source.py — Generate DS:R source index.
Thin CLI wrapper around dsrlib.generate.source_index().
Run: python3 scripts/index_source.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsrlib.generate import source_index
from dsrlib.config import INDEX_MD, INDEX_JSON

if __name__ == "__main__":
    print("Scanning source and area files...")
    md, data = source_index(write=True)

    missing = data["wired_missing"]
    print(f"  do_* functions:          {len(data['do_functions'])}")
    print(f"  interp.c commands:       {len(data['interp_commands'])}")
    print(f"  Missing implementations: {len(missing)}")
    print(f"  gsn_* declarations:      {len(data['gsn_declarations'])}")
    print(f"  Area files:              {len(data['area_vnums'])}")
    print(f"\nMarkdown: {INDEX_MD}")
    print(f"JSON:     {INDEX_JSON}")

    if missing:
        print(f"\n{len(missing)} commands wired but missing source:")
        for item in sorted(missing, key=lambda x: x["command"]):
            print(f"   {item['command']:20s} -> {item['function']}")
