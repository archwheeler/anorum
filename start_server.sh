#!/usr/bin/env bash
# start-server.sh
export DJANGO_SETTINGS_MODULE="anorum.production_settings"
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd /anorum; python manage.py createsuperuser --no-input)
fi

(cd /anorum; python manage.py migrate; gunicorn anorum.wsgi --bind 0.0.0.0:8010 --workers 1) &
nginx -g "daemon off;"
