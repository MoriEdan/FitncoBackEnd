# -*- coding: utf-8 -*-
from alembic import op
from flask_script import Manager
from sqlalchemy.schema import Sequence, CreateSequence
from app import app
from src.helpers.sql_helper import db

manager = Manager(app)


def printer(value):
    print("Eklendi:", value)


@manager.command
def demo():
    users()

@manager.command
def users():
    from src.models.root_user_model import RootUser
    result = RootUser(person_national_id='11111111111', password='123456')
    result.save()
    printer(result.person_national_id)

@manager.command
def sequence():
    db.engine.execute(CreateSequence(Sequence('application_id_seq')))
    db.engine.execute(CreateSequence(Sequence('applications_scope_id_seq')))
    db.engine.execute(CreateSequence(Sequence('authorization_type_id_seq')))
    db.engine.execute(CreateSequence(Sequence('domain_id_seq')))
    db.engine.execute(CreateSequence(Sequence('login_type_id_seq')))
    db.engine.execute(CreateSequence(Sequence('oauth2_id_seq')))
    db.engine.execute(CreateSequence(Sequence('root_role_object_id_seq')))
    db.engine.execute(CreateSequence(Sequence('root_user_id_seq')))
    db.engine.execute(CreateSequence(Sequence('root_user_role_id_seq')))
    db.engine.execute(CreateSequence(Sequence('root_user_roles_root_role_object_id_seq')))
    db.engine.execute(CreateSequence(Sequence('root_users_root_user_role_id_seq')))
    db.engine.execute(CreateSequence(Sequence('scope_data_index_id_seq')))
    db.engine.execute(CreateSequence(Sequence('scope_id_seq')))
    db.engine.execute(CreateSequence(Sequence('sms_id_seq')))
    db.engine.execute(CreateSequence(Sequence('user_detail_id_seq')))
    db.engine.execute(CreateSequence(Sequence('user_id_seq')))


if __name__ == '__main__':
    manager.run()
