"""
scan_source.py — C source and area file indexers for DS:R.

Scans the recovered source tree and area files, returning structured data
about function locations, command wiring, skill numbers, and vnum ranges.

Public functions:
    scan_do_functions(src_dir)      -> {func_name: {file, line}}
    scan_interp_commands(src_dir)   -> {cmd_name: {function, trust, line}}
    scan_gsn_declarations(src_dir)  -> {gsn_name: {file, line}}
    scan_area_vnums(area_dir)       -> {filename: {name, min_vnum, max_vnum, count}}
    build_cross_reference(funcs, cmds) -> (wired_present, wired_missing)
    build_full_index(src_dir, area_dir) -> complete index dict
"""
import re
import os
from collections import defaultdict


# ── Source file helpers ───────────────────────────────────────────────────────

def _c_files(src_dir):
    """Return sorted list of .c file paths in src_dir."""
    if not os.path.isdir(src_dir):
        return []
    return [
        os.path.join(src_dir, f)
        for f in sorted(os.listdir(src_dir))
        if f.endswith(".c")
    ]


def _read(path):
    """Safe file read; returns empty string on error."""
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


# ── Scanners ──────────────────────────────────────────────────────────────────

def scan_do_functions(src_dir):
    """
    Find all `void do_*` function definitions across all .c files.

    Returns dict: { "do_forge": {"file": "skills.c", "line": 1823} }

    Note: if act_combat.c is not in the workspace (Code built it server-side),
    those functions will be absent. This is expected until Code pushes to GitHub
    and Kyle does a git pull.
    """
    functions = {}
    pattern   = re.compile(r"^void\s+(do_\w+)\s*\(", re.MULTILINE)

    for fpath in _c_files(src_dir):
        fname   = os.path.basename(fpath)
        content = _read(fpath)
        for m in pattern.finditer(content):
            func = m.group(1)
            line = content[:m.start()].count("\n") + 1
            functions[func] = {"file": fname, "line": line}

    return functions


def scan_interp_commands(src_dir):
    """
    Parse the command dispatch table from interp.c.

    Returns dict: { "forge": {"function": "do_forge", "trust": "1", "line": 286} }
    """
    content  = _read(os.path.join(src_dir, "interp.c"))
    commands = {}
    pattern  = re.compile(
        r'\{\s*"(\w+)"\s*,\s*(do_\w+)\s*,\s*\d+\s*,\s*(\w+)\s*,'
    )
    for m in pattern.finditer(content):
        line = content[:m.start()].count("\n") + 1
        commands[m.group(1)] = {
            "function": m.group(2),
            "trust":    m.group(3),
            "line":     line
        }
    return commands


def scan_gsn_declarations(src_dir):
    """
    Find `extern int gsn_*` declarations in header files.
    Falls back to scanning for `int gsn_*` assignments if externs are absent.

    Returns dict: { "gsn_forge": {"file": "interp.h", "line": 42} }
    """
    gsns = {}
    # Try extern declarations first (clean header style)
    extern_pat = re.compile(r"extern\s+int\s+(gsn_\w+)\s*;")
    # Fall back: int gsn_xxx = -1; style (defined in C files)
    define_pat = re.compile(r"\bint\s+(gsn_\w+)\s*=")

    for fname in ["interp.h", "skills.h", "merc.h"]:
        fpath   = os.path.join(src_dir, fname)
        content = _read(fpath)
        if not content:
            continue
        for m in extern_pat.finditer(content):
            name = m.group(1)
            if name not in gsns:
                gsns[name] = {"file": fname, "line": content[:m.start()].count("\n") + 1}

    # If extern scan came up empty, try C files
    if not gsns:
        for fpath in _c_files(src_dir):
            fname   = os.path.basename(fpath)
            content = _read(fpath)
            for m in define_pat.finditer(content):
                name = m.group(1)
                if name not in gsns:
                    gsns[name] = {"file": fname, "line": content[:m.start()].count("\n") + 1}

    return gsns


def scan_area_vnums(area_dir):
    """
    Line-by-line scan of .are files for vnum ranges (avoids slow regex on large files).
    Grabs lines matching exactly `#NNN` (object/mob vnum markers).

    Returns dict: { "solennir.are": {"name": "Solennir", "min_vnum": 8000,
                                      "max_vnum": 8199, "count": 87} }
    """
    areas     = {}
    vnum_re   = re.compile(r"^#(\d+)$")

    if not os.path.isdir(area_dir):
        return areas

    for fname in sorted(os.listdir(area_dir)):
        if not fname.endswith(".are"):
            continue

        vnums      = []
        area_name  = fname.replace(".are", "")
        in_header  = False
        hdr_count  = 0

        try:
            for line in open(os.path.join(area_dir, fname),
                             encoding="utf-8", errors="replace"):
                line = line.rstrip()

                if line == "#AREA":
                    in_header, hdr_count = True, 0
                    continue

                if in_header:
                    hdr_count += 1
                    if "~" in line and hdr_count <= 4:
                        candidate = re.sub(r"\{[^\}]*\}", "", line.split("~")[0]).strip()
                        if candidate:
                            area_name = candidate
                    if hdr_count > 5:
                        in_header = False
                    continue

                m = vnum_re.match(line)
                if m:
                    v = int(m.group(1))
                    if v > 0:
                        vnums.append(v)
        except Exception:
            continue

        if vnums:
            areas[fname] = {
                "name":     area_name,
                "min_vnum": min(vnums),
                "max_vnum": max(vnums),
                "count":    len(vnums)
            }

    return areas


def build_cross_reference(do_functions, interp_commands):
    """
    Cross-reference wired commands against found do_* implementations.

    Returns:
        wired_present : list of {command, function, file, line, trust}
        wired_missing : list of {command, function, trust}
            — commands in interp.c with no matching source function
              (either stubs or in act_combat.c not yet synced from GitHub)
    """
    present, missing = [], []
    for cmd, info in sorted(interp_commands.items()):
        func = info["function"]
        if func in do_functions:
            present.append({
                "command":  cmd,
                "function": func,
                "file":     do_functions[func]["file"],
                "line":     do_functions[func]["line"],
                "trust":    info["trust"]
            })
        else:
            missing.append({
                "command":  cmd,
                "function": func,
                "trust":    info["trust"]
            })
    return present, missing


def build_full_index(src_dir, area_dir):
    """
    Run all scanners and return a single index dict.
    This is the primary entry point for scripts and the MCP server.

    Returns dict with keys:
        do_functions, interp_commands, gsn_declarations,
        area_vnums, wired_present, wired_missing
    """
    do_functions    = scan_do_functions(src_dir)
    interp_commands = scan_interp_commands(src_dir)
    gsns            = scan_gsn_declarations(src_dir)
    areas           = scan_area_vnums(area_dir)
    present, missing = build_cross_reference(do_functions, interp_commands)

    return {
        "do_functions":     do_functions,
        "interp_commands":  interp_commands,
        "gsn_declarations": gsns,
        "area_vnums":       areas,
        "wired_present":    present,
        "wired_missing":    missing,
    }
