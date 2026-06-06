#!/bin/bash
python manage.py migrate
python manage.py seed_products
exec gunicorn bisuteria.wsgi
