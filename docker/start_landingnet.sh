#!/bin/bash

sleep 15

#/start_postgres.sh
python manage.py db init
psql -h postgresql -U landingnet landingnetdb -c 'create extension hstore;'
python manage.py db migrate
python manage.py db upgrade

#python manage.py setup_demo

python manage.py run
#CMD ["uwsgi --socket 0.0.0.0:5000 -w wsgi:app"]