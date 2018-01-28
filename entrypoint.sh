#!/bin/bash
set -e


if [ -z "$@" ]; then
  echo "Running app in production mode!"
  nginx && uwsgi --ini /app/app.ini

fi

exec "$@"
