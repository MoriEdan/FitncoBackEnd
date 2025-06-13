#!/bin/sh
rm -rf migrations
export FLASK_APP=app
flask db init
flask db migrate
flask extension
flask db upgrade
flask seed run