#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 'Kernel Name' /path/to/venv" >&2
  exit 2
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv is not installed or not on PATH." >&2
  exit 1
fi

display_name=$1
env_path=$2
kernel_name=$(printf '%s' "$display_name" | LC_ALL=C tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')

if [[ -z "$kernel_name" ]]; then
  echo "Error: kernel name must contain letters or numbers." >&2
  exit 2
fi

if [[ ! -f "$env_path/pyvenv.cfg" ]]; then
  if [[ -e "$env_path" ]]; then
    echo "Error: '$env_path' exists, but is not a virtual environment." >&2
    exit 1
  fi
  echo "Creating virtual environment: $env_path"
  uv venv "$env_path"
fi

env_path=$(cd "$env_path" && pwd -P)
python="$env_path/bin/python"

if [[ ! -x "$python" ]]; then
  echo "Error: Python executable not found at '$python'." >&2
  exit 1
fi

echo "Installing Jupyter kernel and pip into: $env_path"
uv pip install --python "$python" ipykernel pip

echo "Registering Jupyter kernel: $kernel_name"
"$python" -m ipykernel install --user \
  --name "$kernel_name" \
  --display-name "Python ($display_name)"

printf '\nDone! Select "Python (%s)" in Zed.\n' "$display_name"
printf 'Kernel interpreter: %s\n' "$python"
printf 'Inside notebooks, use %%pip install PACKAGE (not !pip).\n'
