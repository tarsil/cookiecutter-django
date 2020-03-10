############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################
FROM ubuntu:20.04
MAINTAINER tiago.arasilva@outlook.com

ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

#
# Install Apt Packages
#
RUN apt-get update -y && apt-get install -y gnupg2 synaptic software-properties-common

RUN apt-get update                                                                                           && \
    apt-get upgrade -y                                                                                       && \
    apt-get install curl -y                                                                                  && \
    apt-get clean && apt-get autoclean                                                                       && \
    find /var/lib/apt/lists/ -type f -delete                                                                 && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update -y                                           && \
    apt-get install -y postgresql postgresql-contrib               \
                       bind9-host                                  \
                       build-essential                             \
                       curl                                        \
                       geoip-bin                                   \
                       gettext                                     \
                       git-core                                    \
                       gawk                                        \
                       iputils-ping                                \
                       language-pack-en                            \
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
                       pgbouncer                                   \
                       postgresql-11                               \
                       python-pil                                  \
                       python-urllib3                              \
                       python-pip                                  \
                       python-dev                                  \
                       python3-dev                                 \
                       python3-pip                                 \
                       rsyslog                                     \
                       socat                                       \
                       sudo                                        \
                       supervisor                                  \
                       unattended-upgrades                         \
                       unzip                                       \
                       vim                                         \
                       wget                                     && \
    apt-get clean && apt-get autoclean                          && \
    apt-get autoremove -y                                       && \
    find /var/lib/apt/lists/ -type f -delete                    && \
    apt-get -y update


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
