#!/usr/bin/env bash

set -e

PROJECT_BASE_PATH='/usr/local/apps/rest-api-photonic-qc'

git pull
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic #--noinput
supervisorctl restart cdl_rest_api

echo "DONE! :)"
