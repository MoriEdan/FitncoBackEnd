# -*- coding: utf-8 -*-
import json
import fastjsonschema
from flask import request


class SchemaHelper(object):
    path = 'src/schemas/'

    def get_schema(self, schema):
        try:
            if self.path and schema:
                with open(self.path + schema + '_schema.json', "r", encoding='utf8') as file:
                    data = json.load(file)
                    return data
            else:
                print("Path is INVALID", flush=True)
                return None
        except Exception as e:
            print(e, flush=True)
            return None

    def json_validate_schema(self, schema):
        try:
            data = request.json if request.is_json else request.form
            json_schema = self.get_schema(schema)
            if json_schema and data:
                try:
                    validator = fastjsonschema.compile(json_schema)
                    validator(data)
                    return True, data
                except fastjsonschema.JsonSchemaException as exp:
                    return False, exp
            elif data is None:
                return False, 'Please Fill JSON Object'
            else:
                return False, 'Schema Not Valid'
        except Exception as e:
            return False, e
