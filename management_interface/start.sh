#!/bin/sh

sh -c "python manage.py migrate
&& python manage.py collectstatic --no-input
&& python manage.py createsuperuser --noinput || true
&& python manage.py runserver 0.0.0.0:8000"