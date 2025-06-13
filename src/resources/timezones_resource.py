# -*- coding: utf-8 -*-
from src.commons.response import ok_result
from src.resources.base_resource import BaseResource
from src.services.timezones_service import TimezonesService
from flask import request


class TimezonesResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.timezones_service = TimezonesService()

    def get(self):
        search = request.args['search']
        result = self.timezones_service.get_timezones(f'%{search}%')
        return ok_result(data=result)

