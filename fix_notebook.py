#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from shutil import copy2

if len(sys.argv) != 2:
    sys.exit("Usage: fix_notebook.py <notebook.ipynb>")

path = Path(sys.argv[1]).expanduser()

with path.open(encoding="utf-8") as f:
    notebook = json.load(f)

metadata = notebook.get("metadata", {})

# Fix CodeMirror metadata
metadata.get("language_info", {}).pop("codemirror_mode", None)

# Fix broken Jupyter widget metadata
metadata.pop("widgets", None)

# Remove widget-specific output representations
# while preserving regular outputs
for cell in notebook.get("cells", []):
    for output in cell.get("outputs", []):
        data = output.get("data", {})
        data.pop("application/vnd.jupyter.widget-view+json", None)
        data.pop("application/vnd.jupyter.widget-state+json", None)

# Create backup without overwriting an existing one
backup = path.with_suffix(".ipynb.bak")

if not backup.exists():
    copy2(path, backup)

# Save through a temporary file
tmp = path.with_suffix(".ipynb.tmp")

tmp.write_text(
    json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
)

tmp.replace(path)

print(f"Fixed: {path}")
