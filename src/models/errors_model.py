# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class Errors(BaseModel):
    __tablename__ = 'errors'

    id = db.Column(db.BigInteger(), primary_key=True)
    error = db.Column(db.Text, unique=False, nullable=False)

    def __init__(self, error):
        super().__init__()
        self.error = error

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'error': self.error,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'error': self.error,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
