#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from shutil import copy2

path = Path(sys.argv[1]).expanduser()

with path.open(encoding="utf-8") as f:
    notebook = json.load(f)

# Usuń problematyczne metadane
notebook.get("metadata", {}).get("language_info", {}).pop("codemirror_mode", None)

# Kopia zapasowa
copy2(path, path.with_suffix(".ipynb.bak"))

# Zapis przez plik tymczasowy
tmp = path.with_suffix(".ipynb.tmp")
tmp.write_text(
    json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
)
tmp.replace(path)

print(f"Naprawiono: {path}")
