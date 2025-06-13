# -*- coding: utf-8 -*-
from src.models.base_model import BaseModel, db
import json


class UserInfos(BaseModel):
    __tablename__ = 'user_infos'

    id = db.Column(db.BigInteger(), primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    weight = db.Column(db.Float, unique=False, nullable=False, index=True)
    height = db.Column(db.Float, unique=False, nullable=False, index=True)
    notes = db.Column(db.String, unique=False, index=True)
    type = db.Column(db.String, unique=False, nullable=False, index=True)
    gender = db.Column(db.String, unique=False, nullable=False, )
    can_walk = db.Column(db.Boolean, unique=False, nullable=False, server_default='f')
    vip = db.Column(db.Boolean, unique=False, nullable=False, server_default='f')
    target = db.Column(db.Float)
    begining = db.Column(db.Float)
    users = db.relationship('Users', primaryjoin='Users.id == UserInfos.user_id',  back_populates='user_infos')

    def __init__(self, user_id, age, weight, height, notes, type, gender, can_walk, vip, target, begining):
        super().__init__()
        self.user_id = user_id
        self.age = age
        self.weight = weight
        self.height = height
        self.notes = notes
        self.type = type
        self.gender = gender
        self.can_walk = can_walk
        self.vip = vip
        self.target = target
        self.begining = begining

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'notes': self.notes,
            'type': self.type,
            'gender': self.gender,
            'can_walk': self.can_walk,
            'vip': self.vip,
            'target': self.target,
            'begining': self.begining,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_load(self):
        return json.loads(json.dumps({
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'note': self.notes,
            'type': self.type,
            'gender': self.gender,
            'can_walk': self.can_walk,
            'vip': self.vip,
            'target': self.target,
            'begining': self.begining
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'notes': self.notes,
            'type': self.type,
            'gender': self.gender,
            'can_walk': self.can_walk,
            'vip': self.vip,
            'target': self.target,
            'begining': self.begining,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
