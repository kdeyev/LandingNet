#FROM centos:centos7
FROM kostyad/pstgrsql

COPY . /LandingNet

WORKDIR /LandingNet

USER 0

RUN yum -y update; 
RUN yum -y install epel-release;

RUN docker/install_django.sh
RUN docker/install_breakpad.sh

RUN cp docker/landingnet.config.py LandingNet/config.py

EXPOSE 5000

CMD ["./docker/start_landingnet.sh"]