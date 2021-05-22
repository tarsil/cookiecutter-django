#!/usr/bin/env bash

# We want to automte deployments to make sure everything is fine
# and runs smoothly. We need to set some defaults like SERVER_TYPE to activate the roles
# SERVER_TYPE default is asgi
# DEPLOYMENT_ENVIRONMENT default is staging to protect from, mistakes can happen
export SERVER_TYPE=${SERVER_TYPE}
export DEPLOYMENT_ENVIRONMENT=${DEPLOYMENT_ENVIRONMENT}

# We default to asgi if the SERVER_TYPE is empty
if [ -z "${SERVER_TYPE}" ]
then
  echo "No server type provided, defaulting to uwsgi"
  export SERVER_TYPE='uwsgi'
elif [ -z "${DEPLOYMENT_ENVIRONMENT}" ]
then
  echo "No deployment enviroment provided"
  export DEPLOYMENT_ENVIRONMENT='staging'
fi

echo "Starting the server"
invoke -r roles $SERVER_TYPE
