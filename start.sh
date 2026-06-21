#!/bin/bash
python manage.py migrate
python manage.py seed_products
python manage.py collectstatic --noinput
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    import os
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    User.objects.create_superuser('admin', 'admin@example.com', password)
    print('Admin user created')
else:
    print('Admin user already exists')
"
exec gunicorn bisuteria.wsgi
