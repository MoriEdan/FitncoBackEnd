# -*- coding: utf-8 -*-
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SqlHelper(db.Model):
    __abstract__ = True

    def __init__(self):
        pass

    @contextmanager
    def transaction_save(self, commit: bool = True):
        session = db.session.add(self)
        try:
            yield
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            commit = False
            return {"session": session, "commit": commit, "error": e}
        return {"session": session, "commit": commit}

    def save(self, commit: bool = True):
        """
        Add a row to the session so that it gets saved to the DB.
        :param commit: whether to issue the commit
        """
        try:
            session = db.session.add(self)
            if commit:
                commit = db.session.commit()
            else:
                commit = False
            result = {"session": session, "commit": commit}
            db.session.flush()
            return result
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            raise e
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            raise e

    def delete(self, commit: bool = True):
        """
        Add a row to the session so that it gets saved to the DB.
        :param commit: whether to issue the commit
        """
        try:
            session = db.session.delete(self)
            if commit:
                commit = db.session.commit()
            else:
                commit = False
            result = {"session": session, "commit": commit}
            db.session.flush()
            return result
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            raise e
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            raise e

