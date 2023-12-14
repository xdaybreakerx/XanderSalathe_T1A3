#!/bin/bash

venv_path=".venv"

if [ -d "$venv_path" ]; then
    source .venv/bin/activate
    python3 main.py
    deactivate
else
    echo "Please run 'setup.sh' first before trying to run the application."
fi