#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Collect static files and migrate database
