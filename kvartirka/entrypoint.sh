#!/bin/sh

set -e

echo $DATABASE_URL > /app/kvartirka/.env

#Wait Postgresql
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# #Flush DB
# echo "Check FLUSH DB"
# if [ "$DJANGO_FLUSH_DB" ]
# then
#     python3 manage.py flush --noinput
#     echo "DB is flushed"

#     echo "Import ingredients, dimensions, tags"
#     python3 manage.py importingredients

#     #Create super user if env set
#     if [ "$DJANGO_SUPERUSER_USERNAME" ]
#         then
#             python manage.py createsuperuser \
#             --noinput \
#             --username $DJANGO_SUPERUSER_USERNAME \
#             --email $DJANGO_SUPERUSER_EMAIL
#     fi
# fi

python3 manage.py migrate
python3 manage.py collectstatic --noinput

#Load DUMP file of import
DUMP_FILE="fixtures.json"

if test -f "$DUMP_FILE"; 
then
    echo "Load data"
    python3 manage.py loaddata fixtures.json
fi

#RUN Gunicorn
gunicorn --bind 0.0.0.0:8000 kvartirka.wsgi

exec "$@"