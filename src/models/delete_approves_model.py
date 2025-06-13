# -*- coding: utf-8 -*-
import json
from src.models.base_model import BaseModel, db


class DeleteApproves(BaseModel):
    __tablename__ = 'delete_approves'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    delete = db.Column(db.Date, unique=False, nullable=False)
    users = db.relationship('Users', primaryjoin='Users.id == DeleteApproves.user_id')

    def __init__(self, user_id, delete):
        super().__init__()
        self.user_id = user_id
        self.delete = delete

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'delete': str(self.delete),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'delete': self.delete,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
