# -*- coding: utf-8 -*-
from src.models.base_model import BaseModel, db
import json


class QuickAnswers(BaseModel):
    __tablename__ = 'quick_answers'

    id = db.Column(db.BigInteger(), primary_key=True)
    message = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'message': self.message,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_message(self):
        return json.loads(json.dumps({
            'id': self.id,
            'message': self.message
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
