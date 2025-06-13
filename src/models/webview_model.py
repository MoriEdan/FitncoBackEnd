# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class Webview(BaseModel):
    __tablename__ = 'webview'

    id = db.Column(db.BigInteger(), primary_key=True)
    link = db.Column(db.Text, unique=False, nullable=False, index=True)

    def __init__(self, link):
        super().__init__()
        self.link = link

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'link': self.link,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'link': self.link,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
