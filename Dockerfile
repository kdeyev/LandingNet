#FROM centos/postgresql-96-centos7
FROM centos:centos7
#FROM kostyad/pstgrsql

COPY . /LandingNet

WORKDIR /LandingNet

USER 0

RUN yum -y update; 
RUN yum -y install epel-release;

RUN docker/install_django.sh
#RUN docker/install_breakpad.sh

RUN cp docker/landingnet.config.py LandingNet/config.py
#RUN python manage.py db init
#RUN python manage.py db migrate
#RUN python manage.py db upgrade

#RUN python manage.py setup_demo

EXPOSE 5000

CMD ["python manage.py run"]
#CMD ["uwsgi --socket 0.0.0.0:5000 -w wsgi:app"]