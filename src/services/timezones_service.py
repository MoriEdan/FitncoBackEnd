# -*- coding: utf-8 -*-
from src.services.base_service import BaseService
from src.models.timezones_model import Timezones


class TimezonesService(BaseService):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_timezones(title):
        try:
            rows = Timezones.query.filter(Timezones.title.ilike(title)).all()
            json_data = [row.to_json() for row in rows]
            return json_data
        except Exception as e:
            print(e)
            return []
