#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

# Add this line to explicitly prepare migrations for your app:
python manage.py makemigrations expenses

python manage.py migrate
