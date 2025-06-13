# -*- coding: utf-8 -*-
from src.models.base_model import BaseModel, db
import json


class System(BaseModel):
    __tablename__ = 'system'

    id = db.Column(db.BigInteger(), primary_key=True)
    statu = db.Column(db.Boolean, unique=False, nullable=False, server_default='f')

    def __init__(self, statu):
        super().__init__()
        self.statu = statu

    def to_json(self):
        return json.loads(json.dumps({
            'statu': self.statu,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'statu': self.statu,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
