#!/bin/bash

NAME="API_Server"                           # Name of the application
PROJ_ROOT=/webapps/rest_app
APP_ROOT=$PROJ_ROOT/src                     # Django project directory
LOG_DIR=$PROJ_ROOT/logs
SOCKFILE=$PROJ_ROOT/sbin/gunicorn.sock       # we will communicte using this unix socket
USER=api                                    # the user to run as
GROUP=webapps                               # the group to run as
NUM_WORKERS=3                               # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=api.settings         # which settings file should Django use
DJANGO_WSGI_MODULE=api.wsgi                 # WSGI module name

echo "Starting $NAME as `whoami`"
echo "LOG Dir ==> $LOG_DIR"

# Activate the virtual environment
cd $APP_ROOT
# source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$APP_ROOT:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
test -d $LOG_DIR || mkdir -p $LOG_DIR

python $APP_ROOT/manage.py migrate --noinput
echo "from django.contrib.auth.models import User; s = 'Admin User Exists' if User.objects.filter(username='admin') else User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell
# Collect the static files for Nginx server
python $APP_ROOT/manage.py collectstatic --noinput

# Populate master tables
#python $APP_ROOT/manage.py loaddata initial_data.json

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
# --bind=unix:$SOCKFILE  #for socket
# --bind=:8000  #for port
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=:8000 \
  --log-level=debug \
  --log-file=$LOG_DIR/gunicorn.log
