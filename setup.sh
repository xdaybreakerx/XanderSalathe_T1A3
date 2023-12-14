#!/bin/bash


if command -v python3 &> /dev/null
then
    echo "Python 3 is installed."
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt 
    deactivate
else
    echo "Python 3 is not installed. It requires installation before running this script."
    echo "https://www.python.org/downloads/"
fi
