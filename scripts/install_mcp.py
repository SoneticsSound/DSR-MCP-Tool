#!/usr/bin/env python3
"""
install_mcp.py — Register the DS:R MCP server with Claude Desktop.

Run once:
    pip install "mcp[cli]"
    python scripts/install_mcp.py

Then restart Claude Desktop. The dsr: tools will be available to Cowork.

What this does:
  1. Installs the mcp package if not present
  2. Finds the Claude Desktop config file (claude_desktop_config.json)
  3. Adds the dsr server entry pointing at dsr_mcp.py
  4. Saves the config (backs up the original first)
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPTS_DIR  = Path(__file__).parent
MCP_SCRIPT   = SCRIPTS_DIR / "dsr_mcp.py"

# Claude Desktop config location on Windows
CLAUDE_CONFIG = Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"


def _detect_project_root():
    """
    Auto-detect a likely DSR project root by looking for docs/code_handoff.json
    in common locations. Returns the matching path, or None if nothing found.

    Candidates checked in order:
      - ~/ds/                                        (Linux/WSL home)
      - /mnt/c/Users/danbl/Documents/Claude DS/code-sync/  (Windows mount)
      - ../code-sync/  relative to the MCP-Tool dir   (sibling install)
    """
    candidates = [
        os.path.expanduser("~/ds"),
        "/mnt/c/Users/danbl/Documents/Claude DS/code-sync",
        os.path.join(os.path.dirname(SCRIPTS_DIR), "..", "code-sync"),
    ]
    for c in candidates:
        if os.path.exists(os.path.join(c, "docs", "code_handoff.json")):
            return os.path.abspath(c)
    return None


def install_mcp_package():
    """Install the mcp package if not already present."""
    try:
        import mcp
        version = getattr(mcp, "__version__", "installed")
        print(f"  mcp package already installed ({version})")
        return True
    except ImportError:
        pass

    print("  Installing mcp package...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "mcp[cli]"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR: pip install failed:\n{result.stderr}")
        return False
    print("  mcp package installed.")
    return True


def register_server():
    """Add dsr server to Claude Desktop config."""
    if not CLAUDE_CONFIG.exists():
        print(f"  Creating new config at {CLAUDE_CONFIG}")
        CLAUDE_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        config = {}
    else:
        # Back up before modifying
        backup = CLAUDE_CONFIG.with_suffix(".json.bak")
        shutil.copy(CLAUDE_CONFIG, backup)
        print(f"  Backed up config to {backup}")
        with open(CLAUDE_CONFIG, encoding="utf-8") as f:
            config = json.load(f)

    # Ensure mcpServers key exists
    config.setdefault("mcpServers", {})

    # Detect a sensible DSR_PROJECT_ROOT — the live project tree the MCP should
    # read state from. Briefing/queries pull bugs.json/ideas.json/etc. from
    # there instead of the MCP-Tool's own (typically stale) local copies.
    # Override at install time:  DSR_PROJECT_ROOT=/path/to/project python install_mcp.py
    project_root = os.environ.get("DSR_PROJECT_ROOT") or _detect_project_root()

    server_env = {}
    if project_root:
        server_env["DSR_PROJECT_ROOT"] = project_root
        print(f"  DSR_PROJECT_ROOT = {project_root}")
    else:
        print("  DSR_PROJECT_ROOT not set — MCP will use its own dir for state")
        print("    (briefing will reflect MCP-Tool's local .md files, not your")
        print("     live project. Set DSR_PROJECT_ROOT and re-run to fix.)")

    # Add / overwrite the dsr entry
    config["mcpServers"]["dsr"] = {
        "command": sys.executable,   # whichever python ran this script (python / python3 / py)
        "args": [str(MCP_SCRIPT)],
        "env": server_env
    }

    with open(CLAUDE_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"  Registered 'dsr' server in {CLAUDE_CONFIG}")
    print(f"  Python: {sys.executable}")
    print(f"  Script: {MCP_SCRIPT}")


def main():
    print("DS:R MCP Installer")
    print("=" * 40)

    print("\n[1/2] Checking mcp package...")
    if not install_mcp_package():
        print("\nInstallation failed. Install manually: pip install \"mcp[cli]\"")
        sys.exit(1)

    print("\n[2/2] Registering with Claude Desktop...")
    register_server()

    print("\nDone. Restart Claude Desktop to activate the dsr: tools.")
    print("\nTools you'll have:")
    print("  get_briefing()              — session state summary")
    print("  get_open_bugs()             — open bugs by severity")
    print("  get_recent_decisions()      — latest design decisions")
    print("  get_missing_implementations() — stubs still to port")
    print("  query_function(name)        — look up any do_* function")
    print("  query_vnum(number)          — which area owns a vnum")
    print("  query_area(filename)        — area vnum range + name")
    print("  refresh_index()             — re-scan after git pull")


if __name__ == "__main__":
    main()
