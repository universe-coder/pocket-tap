#!/usr/bin/env sh
# First run creates a local Python environment and installs dependencies.
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
fi
exec .venv/bin/python -m pc_remote "$@"
