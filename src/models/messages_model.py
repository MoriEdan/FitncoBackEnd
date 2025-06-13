# -*- coding: utf-8 -*-
from src.models.base_model import BaseModel, db
import json


class Messages(BaseModel):
    __tablename__ = 'messages'

    id = db.Column(db.BigInteger(), primary_key=True)
    from_user = db.Column(db.ForeignKey('users.id'), nullable=False, index=True)
    to_user = db.Column(db.ForeignKey('users.id'), index=True)
    type = db.Column(db.String, unique=False, nullable=False, index=True)
    content = db.Column(db.String, unique=False, index=True)
    path = db.Column(db.String, unique=False, index=True)
    log = db.Column(db.String, unique=False, nullable=False, index=True)
    is_seen = db.Column(db.Boolean, unique=False, nullable=False, server_default='f', index=True)
    deleted_at = db.Column(db.DateTime)
    from_users = db.relationship('Users', primaryjoin='Users.id == Messages.from_user')
    to_users = db.relationship('Users', primaryjoin='Users.id == Messages.to_user')

    def __init__(self, from_user, to_user, type, content, path, log, created_at=None, is_seen=False):
        super().__init__()
        self.from_user = from_user
        self.to_user = to_user
        self.type = type
        self.content = content
        self.path = path
        self.log = log
        self.is_seen = is_seen
        self.created_at = created_at

    def to_json(self):
        return json.loads(json.dumps({
            'from_user': self.from_user,
            'to_user': self.to_user,
            'type': self.type,
            'content': self.content,
            'path': self.path,
            'log': self.log,
            'is_seen': self.is_seen,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
            'deleted_at': str(self.deleted_at)
        }))

    def to_message(self):
        return json.loads(json.dumps({
            'id': self.id,
            'from': self.from_user,
            'type': self.type,
            'content': self.content,
            'source': self.path,
            'log': self.log,
            'date': str(self.created_at)
        }))

    def to_dict(self):
        return {
            'from_user': self.from_user,
            'to_user': self.to_user,
            'type': self.type,
            'content': self.content,
            'path': self.path,
            'log': self.log,
            'is_seen': self.is_seen,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
