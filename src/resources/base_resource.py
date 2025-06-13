# -*- coding: utf-8 -*-
from flask_restful import Resource
from src.helpers.schema_helper import SchemaHelper


class BaseResource(Resource):
    def __init__(self):
        self.schema_helper = SchemaHelper()
