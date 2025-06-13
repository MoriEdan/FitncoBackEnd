# -*- coding: utf-8 -*-
from flask_injector import FlaskInjector
from injector import Binder

"""depency injection için class loader"""


def injects_config(app):
    def configure(binder: Binder):
        pass

    FlaskInjector(app=app, modules=[configure])
