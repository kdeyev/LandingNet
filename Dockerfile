FROM 192.168.203.109:5000/breakpad

# workdir and user
WORKDIR /LandingNet
USER 0

# copy LandingNet
COPY LandingNet /LandingNet/LandingNet
COPY manage.py /LandingNet/manage.py
COPY requirements.txt /LandingNet/requirements.txt
COPY wsgi.py /LandingNet/wsgi.py

# copy installation script
COPY docker/install_django.sh /LandingNet/docker/install_django.sh
RUN yum -y update; 
RUN yum -y install epel-release;
RUN docker/install_django.sh
RUN pip install jira

# copy a demo
COPY demo /LandingNet/demo

# copy start script
COPY docker/start_landingnet.sh /LandingNet/docker/start_landingnet.sh

# copy config
COPY docker/landingnet.config.py /LandingNet/LandingNet/config.py

VOLUME ["/LandingNet/debug-symbols"]
VOLUME ["/LandingNet/minidumps"]
EXPOSE 5000

CMD ["./docker/start_landingnet.sh"]