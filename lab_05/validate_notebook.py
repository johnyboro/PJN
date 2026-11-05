import json
import nbformat

path = "5 - Transformers, część 2_ architektura - PJN.ipynb"

with open(path, encoding="utf-8") as f:
    notebook = json.load(f)

try:
    nbformat.validate(notebook)
    print("Notebook is valid!")
except nbformat.ValidationError as e:
    print("Problem at:", list(e.absolute_path))
    print("Invalid value:", repr(e.instance))
    print("Error:", e.message)
