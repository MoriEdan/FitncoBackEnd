# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class Water(BaseModel):
    __tablename__ = 'water'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False, index=True)
    day = db.Column(db.Date, unique=False, nullable=False, index=True)
    unit = db.Column(db.Float, unique=False, nullable=False, index=True)
    users = db.relationship('Users', primaryjoin='Users.id == Water.user_id', back_populates='waters')

    def __init__(self, user_id, day, unit):
        super().__init__()
        self.user_id = user_id
        self.day = day
        self.unit = unit

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'day': str(self.day),
            'unit': self.unit,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'day': self.day,
            'unit': self.unit,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
