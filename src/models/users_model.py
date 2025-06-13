# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import func

from src.models.base_model import BaseModel, db
import json


class Users(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    email_verified_at = db.Column(db.TIMESTAMP, unique=False, index=True)
    password = db.Column(db.String, unique=False, nullable=False, index=True)
    email_token = db.Column(db.String, unique=False, index=True)
    timezone = db.Column(db.ForeignKey('timezones.id'), unique=False, nullable=False, index=True)
    pp = db.Column(db.String, unique=False, nullable=False, index=True)
    type = db.Column(db.String, unique=False, nullable=False, index=True)
    os = db.Column(db.String, unique=False, nullable=False, index=True)
    status = db.Column(db.SMALLINT, unique=False, nullable=False, server_default='2')
    auto_zone = db.Column(db.SMALLINT, unique=False, nullable=False, server_default='0')
    remember_token = db.Column(db.String, unique=False)
    pause_start = db.Column(db.Date, unique=False, index=True)
    pause_end = db.Column(db.Date, unique=False, index=True)
    payment_day = db.Column(db.Integer, unique=False, index=True)
    parent = db.Column(db.String, unique=False, index=True)
    archive = db.Column(db.Boolean, unique=False, nullable=False, server_default='f')
    device = db.Column(db.String, unique=False, nullable=False, index=True)
    elasticid = db.Column(db.String, unique=False, index=True)
    timezones = db.relationship('Timezones', primaryjoin='Users.timezone == Timezones.id')
    user_infos = db.relationship('UserInfos', primaryjoin='Users.id == UserInfos.user_id', back_populates='users')
    walks = db.relationship('WalkingLogs',
                            primaryjoin='and_(Users.id == WalkingLogs.user_id, WalkingLogs.day == func.current_date())',
                            back_populates='users')
    breakfasts = db.relationship('BreakfastLogs',
                                 primaryjoin='and_(Users.id == BreakfastLogs.user_id, '
                                             'BreakfastLogs.day == func.current_date())',
                                 back_populates='users')
    dinners = db.relationship('DinnerLogs',
                              primaryjoin='and_(Users.id == DinnerLogs.user_id, DinnerLogs.day == func.current_date())',
                              back_populates='users')
    lunch = db.relationship('LunchLogs',
                            primaryjoin='and_(Users.id == LunchLogs.user_id, LunchLogs.day == func.current_date())',
                            back_populates='users')
    sport = db.relationship('Sport', primaryjoin='and_(Users.id == Sport.user_id, Sport.day == func.current_date())',
                            back_populates='users')
    waters = db.relationship('Water', primaryjoin='and_(Users.id == Water.user_id, Water.day == func.current_date())',
                             back_populates='users')
    weight = db.relationship('WeightLogs',
                             primaryjoin='and_(Users.id == WeightLogs.user_id, WeightLogs.day == func.current_date())',
                             back_populates='users')
    diet = db.relationship('Diets', primaryjoin='and_(Users.id == Diets.user_id, Diets.start <= func.current_date(), '
                                                'Diets.end >= func.current_date())', back_populates='users')
    monthly = db.relationship('Diets', primaryjoin='Users.id == Diets.user_id', order_by='Diets.id', overlaps="diet,users")

    def __init__(self, name, last_name, email, email_verified_at, password, timezone, pp, type, os, parent, device,
                 email_token=None, status='2', auto_zone='0', remember_token=None, pause_start=None, pause_end=None,
                 payment_day=None, archive=False, elasticid=None):
        super().__init__()
        self.name = name
        self.last_name = last_name
        self.email = email
        self.email_verified_at = email_verified_at
        self.password = password
        self.email_token = email_token
        self.timezone = timezone
        self.pp = pp
        self.type = type
        self.os = os
        self.status = status
        self.auto_zone = auto_zone
        self.remember_token = remember_token
        self.pause_start = pause_start
        self.pause_end = pause_end
        self.payment_day = payment_day
        self.parent = parent
        self.archive = archive
        self.device = device
        self.elasticid = elasticid

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'email_verified_at': str(self.email_verified_at),
            'timezone': self.timezones.title,
            'pp': self.pp,
            'type': self.type,
            'os': self.os,
            'status': self.status,
            'auto_zone': self.auto_zone,
            'remember_token': self.remember_token,
            'payment_day': self.payment_day,
            'pause_start': str(self.pause_start),
            'pause_end': str(self.pause_end),
            'archive': self.archive,
            'parent': self.parent,
            'device': self.device,
            'elasticid': self.elasticid,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }))

    def to_load(self):
        return json.loads(json.dumps({
            'id': self.id,
            'full_name': self.name + ' ' + self.last_name,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'timezone': self.timezones.title,
            'picture': self.pp,
            'type': self.type,
            'pause': 0 if self.pause_start is None else 1,
            'pause_dates': {'start': str(self.pause_start) if self.pause_start is not None else None,
                            'end': str(self.pause_end) if self.pause_end is not None else None},
            'active': False if self.status == 0 else True,
            'parent': self.parent,
            'registered': datetime.datetime.strftime(self.created_at, '%d.%m.%Y'),
        }))

    def to_tracking(self):
        return json.loads(json.dumps({
            'id': self.id,
            'pp': self.pp,
            'name': f'{self.name} {self.last_name}',
            'diet': self.diet[-1].days if len(self.diet) > 0 else None,
            'diet_type': self.diet[-1].type if len(self.diet) > 0 else None,
            'note': self.user_infos[0].notes if self.user_infos[0].notes else "",
            'diet_end': datetime.datetime.strftime(self.diet[-1].end, '%d.%m.%Y') if len(self.diet) > 0 else None,
            'walking': str(len(self.walks)) + "/" + str(self.diet[-1].days if len(self.diet) > 0 else 0),
            'breakfast': len(self.breakfasts),
            'lunch': len(self.lunch),
            'dinner': len(self.dinners),
            'sport': len(self.sport),
            'walk': len(self.walks),
            'can_walk': self.user_infos[0].can_walk if self.user_infos[0].can_walk else None,
            'vip': self.user_infos[0].vip if self.user_infos[0].vip else None,
            'type': self.user_infos[0].type if self.user_infos[0].type else None,
            'meal': self.diet[-1].type if self.diet else None,
            'water': self.waters[-1].unit if self.waters else None,
        }))

    def to_approval(self):
        return json.loads(json.dumps({
            'id': self.id,
            'full_name': self.name + ' ' + self.last_name,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'picture': self.pp,
            'date': datetime.datetime.strftime(self.created_at, '%d.%m.%Y'),
        }))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'email_verified_at': self.email_verified_at,
            'timezone': self.timezone,
            'pp': self.pp,
            'type': self.type,
            'can_walk': self.can_walk,
            'vip': self.vip,
            'os': self.os,
            'status': self.status,
            'auto_zone': self.auto_zone,
            'remember_token': self.remember_token,
            'pause_start': self.pause_start,
            'pause_end': self.pause_end,
            'archive': self.archive,
            'parent': self.parent,
            'device': self.device,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
