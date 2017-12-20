############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################
FROM ubuntu:16.04
MAINTAINER tiago.arasilva@goutlook.com

ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

#
# Install Apt Packages
#
RUN apt-get update                                                                                           && \
    apt-get upgrade -y                                                                                       && \
    apt-get install curl -y                                                                                  && \
    apt-get clean && apt-get autoclean                                                                       && \
    find /var/lib/apt/lists/ -type f -delete                                                                 && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update                                              && \
    apt-get install -y bind9-host                                  \
                       curl                                        \
                       geoip-bin                                   \
                       gettext                                     \
                       git-core                                    \
                       gawk                                        \
                       imagemagick                                 \
                       iputils-ping                                \
                       language-pack-en                            \
                       less                                        \
                       libcurl4-openssl-dev                        \
                       libffi-dev                                  \
					   libgeos-c1v5                                \
                       libmagickwand-dev                           \
                       libmemcached-tools                          \
                       libxml2-dev                                 \
                       libxslt-dev                                 \
                       memcached                                   \
                       net-tools                                   \
                       nginx-extras                                \
                       perl                                        \
                       pgbouncer                                   \
                       postgresql-client-9.4                       \
                       postgresql-server-dev-9.4                   \
                       python-imaging                              \
                       python-chardet                              \
                       python-colorama                             \
                       python-distlib                              \
                       python-html5lib                             \
                       python-pip                                  \
                       python-requests                             \
                       python-setuptools                           \
                       python-six                                  \
                       python-urllib3                              \
                       python-dev                                  \
                       rsyslog                                     \
                       socat                                       \
                       software-properties-common                  \
                       sudo                                        \
                       supervisor                                  \
                       gunicorn                                    \
                       telnet                                      \
                       unattended-upgrades                         \
                       unzip                                       \
                       vim                                         \
                       wget                                     && \
    apt-get clean && apt-get autoclean                          && \
    find /var/lib/apt/lists/ -type f -delete

RUN apt-get -y upgrade

RUN add-apt-repository -y ppa:jonathonf/python-3.6 && \
	apt-get update && apt-get install -y python3.6

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

#
# Install Pip Requirements
# upgrade the setuptools from 27.1.2 to 32.3.1.
#
RUN pip3 install -U setuptools
ADD requirements /var/www/requirements
RUN pip3 install -r /var/www/requirements/common.txt

#
# Make Python3 the default python
# Make pip3 the default pip
#
RUN echo 'alias python=python3' >> ~/.bashrc && echo 'alias pip=pip3.6' >> ~/.bashrc
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

RUN sed -i -e 's/# server_tokens off;/server_tokens off;/g' /etc/nginx/nginx.conf
