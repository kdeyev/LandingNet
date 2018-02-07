# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
#   https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
#   scollier <scollier@redhat.com>

FROM centos:centos7
MAINTAINER The CentOS Project <cloud-ops@centos.org>

RUN yum -y update; yum clean all
RUN yum -y install sudo epel-release; yum clean all
RUN yum -y install postgresql-server postgresql postgresql-contrib supervisor pwgen; yum clean all

ADD ./postgresql-setup /usr/bin/postgresql-setup
ADD ./supervisord.conf /etc/supervisord.conf
ADD ./start_postgres.sh /start_postgres.sh
ADD ./create_extension.sh /create_extension.sh

ENV POSTGRES_USER landingnet
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB landingnetdb

#Sudo requires a tty. fix that.
RUN sed -i 's/.*requiretty$/#Defaults requiretty/' /etc/sudoers
RUN chmod +x /usr/bin/postgresql-setup
RUN chmod +x /start_postgres.sh

RUN /usr/bin/postgresql-setup initdb

ADD ./postgresql.conf /var/lib/pgsql/data/postgresql.conf

RUN chown -v postgres.postgres /var/lib/pgsql/data/postgresql.conf

#RUN echo "local  all  landingnet trust" > /var/lib/pgsql/data/pg_hba.conf
#RUN echo "host  all   landingnet 0.0.0.0/0  trust" >> /var/lib/pgsql/data/pg_hba.conf 
#RUN echo "host  all   landingnet ::/0 trust" >> /var/lib/pgsql/data/pg_hba.conf

RUN echo "local  all  all trust" > /var/lib/pgsql/data/pg_hba.conf
RUN echo "host  all   all 0.0.0.0/0  trust" >> /var/lib/pgsql/data/pg_hba.conf 
RUN echo "host  all   all ::/0 trust" >> /var/lib/pgsql/data/pg_hba.conf

#RUN echo "local	all	all	trust" >> /var/lib/pgsql/data/pg_hba.conf
#RUN echo "host	all	127.0.0.1/32	trust" >> /var/lib/pgsql/data/pg_hba.conf

#RUN echo "host    all             all             0.0.0.0/0               md5" >> /var/lib/pgsql/data/pg_hba.conf

VOLUME ["/var/lib/pgsql"]

EXPOSE 5432

#USER postgres
CMD ["/bin/bash", "/start_postgres.sh"]
