############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################
FROM ubuntu:18.04
MAINTAINER tiago.arasilva@outlook.com

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
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update                                              && \
    apt-get install -y bind9-host                                  \
                       build-essential                             \
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
                       libevent-dev                                \
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
                       postgresql-client-9.6                       \
                       postgresql-server-dev-9.6                   \
                       python-pil                                  \
                       python-urllib3                              \
                       python3-pip                                 \
                       python-pip                                  \
                       python-dev                                  \
                       python3-dev                                 \
                       rsyslog                                     \
                       socat                                       \
                       software-properties-common                  \
                       sudo                                        \
                       supervisor                                  \
                       unattended-upgrades                         \
                       unzip                                       \
                       vim                                         \
                       wget                                     && \
    apt-get clean && apt-get autoclean                          && \
    find /var/lib/apt/lists/ -type f -delete


RUN apt-get -y upgrade

#
# Install Pip Requirements
# upgrade the setuptools from 27.1.2 to 32.3.1.
#
RUN pip3 install pip --upgrade
RUN pip3 install wheel
RUN pip3 install -U setuptools

#
#  Install requirements
#
ADD requirements /var/www/requirements
RUN pip3 install -r /var/www/requirements/common.txt

RUN echo 'alias python=python3' >> ~/.bashrc && echo 'alias pip=pip3' >> ~/.bashrc

# Patch Nginx Config to Disable Security Tokens
RUN sed -i -e 's/# server_tokens off;/server_tokens off;/g' /etc/nginx/nginx.conf

# Add JSON logging formatter for nginx
ADD deploy/nginx/nginx.json-logging.conf /etc/nginx/conf.d/json-logging.conf
