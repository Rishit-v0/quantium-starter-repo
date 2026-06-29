#!/bin/bash

# ── Soul Foods Dash App — CI Test Runner ──────────────────────────────────────
# Activates the virtual environment, runs the test suite, and returns:
#   exit code 0 → all tests passed
#   exit code 1 → something went wrong

set -e  # Exit immediately on any unexpected error

echo "============================================"
echo "  Soul Foods Dash App — Running Test Suite  "
echo "============================================"

# ── Step 1: Locate the script's directory (project root) ─────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "Working directory: $SCRIPT_DIR"

# ── Step 2: Activate the virtual environment ──────────────────────────────────
VENV_PATH="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Handle both Unix and Windows (Git Bash) activation paths
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"          # Mac/Linux
elif [ -f "$VENV_PATH/Scripts/activate" ]; then
    source "$VENV_PATH/Scripts/activate"      # Windows Git Bash
else
    echo "ERROR: Could not find activate script in venv"
    exit 1
fi

echo "Virtual environment activated."

# ── Step 3: Run the test suite ────────────────────────────────────────────────
echo ""
echo "Running tests..."
echo "--------------------------------------------"

if pytest test_app.py -v; then
    echo "--------------------------------------------"
    echo "SUCCESS: All tests passed."
    exit 0
else
    echo "--------------------------------------------"
    echo "FAILURE: One or more tests failed."
    exit 1
fi