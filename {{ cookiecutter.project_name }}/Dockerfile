############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

#
# Install Apt Packages
#
RUN apt clean                                           && \
    apt update -y                                       && \
    apt install -y gnupg2 synaptic software-properties-common

RUN apt update                                                                                               && \
    apt upgrade -y                                                                                           && \
    apt install curl -y                                                                                      && \
    apt clean && apt autoclean                                                                               && \
    find /var/lib/apt/lists/ -type f -delete                                                                 && \
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -                                  && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" >> /etc/apt/sources.list.d/pgdg.list

RUN apt update -y                                               && \
    apt install -y postgresql                                      \
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
                       libssl-dev                                  \
                       libffi-dev                                  \
                       libgeos-c1v5                                \
                       libmagickwand-dev                           \
                       libmemcached-dev                            \
                       zlib1g-dev                                  \
                       libmemcached-tools                          \
                       libxml2-dev                                 \
                       libxslt-dev                                 \
                       memcached                                   \
                       net-tools                                   \
                       nginx-extras                                \
                       pgbouncer                                   \
                       python-pil                                  \
                       python3-pip                                 \
                       python-is-python3                           \
                       rsyslog                                     \
                       socat                                       \
                       supervisor                                  \
                       unattended-upgrades                         \
                       unzip                                       \
                       wget                                     && \
    apt clean && apt autoclean                                  && \
    apt autoremove -y                                           && \
    find /var/lib/apt/lists/ -type f -delete                    && \
    apt -y update



#
#  Install requirements
#
ADD requirements /var/www/requirements
RUN pip3 install -r /var/www/requirements/common.txt

RUN ln /usr/local/bin/dramatiq /usr/bin/dramatiq

# Patch Nginx Config to Disable Security Tokens
RUN sed -i -e 's/# server_tokens off;/server_tokens off;/g' /etc/nginx/nginx.conf

# Add JSON logging formatter for nginx
ADD deploy/nginx/nginx.json-logging.conf /etc/nginx/conf.d/json-logging.conf
