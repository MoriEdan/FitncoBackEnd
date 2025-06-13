# -*- coding: utf-8 -*-
from src.helpers.sql_helper import SqlHelper, db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BaseModel(SqlHelper):
    __abstract__ = True

    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), server_onupdate=db.func.now())
