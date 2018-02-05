#FROM centos/postgresql-96-centos7
FROM centos:centos7

COPY . /LandingNet

WORKDIR /LandingNet

USER 0

RUN yum -y update; 
RUN yum -y install epel-release;
RUN yum -y install python python-pip; 

RUN yum -y install git svn gcc gcc-c++ make postgresql-devel python-devel;
#RUN yum clean all
RUN pip install -r requirements.txt

#RUN docker/install_python.sh
RUN docker/install_breakpad.sh

RUN cp docker/landingnet.config.py LandingNet/config.py
RUN python manage.py db init
RUN python manage.py db migrate
RUN python manage.py db upgrade

RUN python manage.py setup_demo

EXPOSE 5000

CMD ["python manage.py run"]
#CMD ["uwsgi --socket 0.0.0.0:5000 -w wsgi:app"]