# -*- coding: utf-8 -*-
from flask.cli import FlaskGroup
from app import app, db

cli = FlaskGroup(app)


@cli.command("extension")
def extension():
    db.engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    print('UUID extension create successfully')


if __name__ == '__main__':
    cli()
