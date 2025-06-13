# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class DinnerLogs(BaseModel):
    __tablename__ = 'dinner_logs'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    day = db.Column(db.Date, unique=False, nullable=False)
    users = db.relationship('Users', primaryjoin='Users.id == DinnerLogs.user_id', back_populates='dinners')

    def __init__(self, user_id, day):
        super().__init__()
        self.user_id = user_id
        self.day = day

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'day': str(self.day),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'day': self.day,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
