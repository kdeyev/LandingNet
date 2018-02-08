#!/bin/bash

/start_postgres.sh
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

#python manage.py setup_demo

python manage.py run
#CMD ["uwsgi --socket 0.0.0.0:5000 -w wsgi:app"]