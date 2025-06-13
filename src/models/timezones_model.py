# -*- coding: utf-8 -*-
from src.models.base_model import BaseModel, db
import json


class Timezones(BaseModel):
    __tablename__ = 'timezones'

    id = db.Column(db.BigInteger(), primary_key=True)
    zone = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

    def __init__(self, zone, title):
        super().__init__()
        self.zone = zone
        self.title = title

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'zone': self.zone,
            'title': self.title,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'zone': self.zone,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
