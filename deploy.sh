#!/bin/bash

# Uruchom migracje
python manage.py migrate

# Zbierz pliki statyczne
python manage.py collectstatic --noinput
