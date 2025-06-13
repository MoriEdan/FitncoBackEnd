#!/bin/sh
. venv/bin/activate
#export FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1
#nohup flask run --host=0.0.0.0 > logs/audit.log &
nohup python wsgi.py > logs/audit.log &