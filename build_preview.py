#!/usr/bin/env python3
"""Render the real Liquid templates using Ruby (requires liquid and kramdown)."""
from pathlib import Path
import subprocess
import sys

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    sys.exit(subprocess.call(["ruby", str(root / "build_preview.rb")], cwd=root))
