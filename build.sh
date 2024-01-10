#!/usr/bin/env bash

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input

# python manage.py makemigrations admin zero
# python manage.py makemigrations accounts
# python manage.py migrate accounts
# python manage.py migrate admin
python manage.py makemigrations
python manage.py migrate