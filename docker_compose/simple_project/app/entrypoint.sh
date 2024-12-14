#!/bin/bash

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
python manage.py createsuperuser\
   --noinput\
   --username $DJANGO_SUPERUSER_USERNAME\
   --email $DJANGO_SUPERUSER_EMAIL

uwsgi --strict --ini uwsgi.ini