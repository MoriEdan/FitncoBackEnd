# -*- coding: utf-8 -*-
import datetime
import json
from src.models.base_model import BaseModel, db


class Diets(BaseModel):
    __tablename__ = 'diets'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False, index=True)
    start = db.Column(db.Date, unique=False, nullable=False, index=True)
    end = db.Column(db.Date, unique=False, nullable=False, index=True)
    days = db.Column(db.Integer, unique=False, nullable=False, index=True)
    type = db.Column(db.SMALLINT, unique=False, nullable=False, index=True)
    users = db.relationship('Users', primaryjoin='Users.id == Diets.user_id', back_populates='diet')

    def __init__(self, user_id, start, end, days, type):
        super().__init__()
        self.user_id = user_id
        self.start = start
        self.end = end
        self.days = days
        self.type = type

    def to_plan(self):
        return json.loads(json.dumps({
            'id': self.id,
            'date': datetime.datetime.strftime(self.start, '%d.%m.%Y'),
            'start': datetime.datetime.strftime(self.end, '%d.%m.%Y'),
            'type': self.type
        }))

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'days': self.days,
            'start': str(self.start),
            'end': str(self.end),
            'type': self.type,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'days': self.days,
            'start': self.start,
            'end': self.end,
            'type': self.type,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
