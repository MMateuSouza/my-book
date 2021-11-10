#!/bin/bash

while ! mysqladmin ping -h'mysql' -P'3306' --silent; do
    echo 'Aguardando MySQL inicializar...'
    sleep 1
done

python manage.py makemigrations;

python manage.py migrate;

python manage.py collectstatic --noinput;

uwsgi --ini infra/uwsgi/my-book_uwsgi.ini;