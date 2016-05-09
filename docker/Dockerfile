FROM ubuntu:latest

MAINTAINER Marius Magureanu

RUN export DEBIAN_FRONTEND="noninteractive"

RUN apt-get update
RUN apt-get upgrade -y

RUN echo "mariadb-server mariadb-server/root_password password rootpw" | debconf-set-selections
RUN echo "mariadb-server mariadb-server/root_password_again password rootpw" | debconf-set-selections
RUN apt-get -y install mariadb-server-10.0

ENV user zipnish
ENV password secret
ENV db_script /var/db/database.sql

ADD ./init-db.sh /usr/local/bin/init-db.sh
ADD ./database.sql /var/db/database.sql

RUN chmod +x /usr/local/bin/init-db.sh

EXPOSE 3306

CMD ["/usr/local/bin/init-db.sh"]
