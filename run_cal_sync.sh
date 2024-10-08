#!/bin/bash
# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to that directory
cd "$SCRIPT_DIR"

# Source the virtual environment and run the Python script
source "$SCRIPT_DIR/.venv/bin/activate"
python "$SCRIPT_DIR/cal_sync.py"
