# -*- coding: utf-8 -*-
import datetime
import math
import mimetypes
import os
import time
import uuid

from flask import request, current_app
from sqlalchemy import func, desc
from sqlalchemy import or_, and_, text
from werkzeug.utils import secure_filename

from src.commons.exception import NotFoundError
from src.helpers.fcm_helper import fcm_helper
from src.models.base_model import db
from src.models.breakfast_logs_model import BreakfastLogs
from src.models.dinner_logs_model import DinnerLogs
from src.models.lunch_logs_model import LunchLogs
from src.models.messages_model import Messages
from src.models.users_model import Users
from src.models.walking_logs_model import WalkingLogs
from src.services.base_service import BaseService
from src.utils.file_util import allowed_file, upload_file


class MessageService(BaseService):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_file(file_name):
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
        if os.path.exists(file_path):
            return file_path
        return None

    @staticmethod
    def archive(data):
        user = Users.query.filter_by(id=data['client']).first()
        user.archive = bool(int(data['archive']))
        user.save()
        return []

    @staticmethod
    def medias(client):
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        query = Messages.query.filter(or_(Messages.from_user == client, Messages.to_user == client),
                                      Messages.type != 'text', Messages.deleted_at == None).order_by(
            desc(Messages.created_at))
        rows = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()
        items = []
        for row in rows:
            items.append(row.to_message())
        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(rows),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    @staticmethod
    def messages(client):
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        query = Messages.query.filter(or_(Messages.from_user == client, Messages.to_user == client),
                                      Messages.deleted_at == None).order_by(
            desc(Messages.created_at))
        rows = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()
        try:
            Messages.query.filter_by(from_user=client, deleted_at=None).update({"is_seen": True})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            Messages.query.filter_by(from_user=client, deleted_at=None).update({"is_seen": True})
            db.session.commit()
        user = Users.query.filter_by(id=client).first()
        user_inf = user.user_infos[0] if user.user_infos else None
        user_data = user.to_load()
        if user_inf:
            user_data.update(user_inf.to_load())
        if user.timezones:
            user_data.update({'timezone': user.timezones.title})
        items = []
        for row in rows:
            items.append(row.to_message())
        data = {
            'client': user_data,
            'items': items,
            'pagination': {
                "total": total,
                "count": len(rows),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def inbox(self, search, archive=False):
        page = int(request.args.get('page', 1))
        if page == 0:
            page = 1
        pagination = int(request.args.get('pagination', 10))
        fu_query = self.get_inbox_query(Messages.from_user, archive)
        if search is not None and search != '':
            fu_query = fu_query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))

        tu_query = self.get_inbox_query(Messages.to_user, archive)
        if search is not None and search != '':
            tu_query = tu_query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))

        union_query = fu_query.union(tu_query)
        query = union_query.with_entities(func.text(text('client')).label('client'),
                                          func.max(text('created_at')).label('most_recent')).group_by(
            text('client')).order_by(desc(text('most_recent')))
        rows = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()
        items = []
        for row in rows:
            user_id = row.client
            last_message = Messages.query.filter(
                or_(Messages.from_user == user_id, Messages.to_user == user_id), Messages.deleted_at == None).order_by(
                desc(Messages.created_at)).first()
            user = Users.query.filter_by(id=user_id).first()
            user_inf = user.user_infos[0] if user.user_infos else None
            if user_inf and last_message:
                tmp_data = {
                    'id': user.id,
                    'name': f'{user.name} {user.last_name}',
                    'picture': user.pp,
                    'date': datetime.datetime.strftime(last_message.created_at, '%Y-%m-%d %H:%M:%S'),
                    'last': last_message.content,
                    'is_seen': last_message.is_seen if last_message.to_user is None else 1,
                    'vip': user_inf.vip,
                    'type': user_inf.type,
                    'message_type': last_message.type,
                    'info': user_inf.to_json()
                }
                items.append(tmp_data)
        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(rows),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def get_inbox_query(self, column, archive):
        query = Messages.query.filter(Messages.deleted_at == None)
        query = query.join(Users,
                           and_(Users.id == column, Users.type == 'client', Users.archive == archive,
                                Users.status != 2))
        query = query.with_entities(func.max(Users.id).label('client'),
                                    func.max(Messages.created_at).label('created_at')).group_by(column)
        return query

    def multiple_message(self, data):
        for client in data['to']:
            message_to = Users.query.filter_by(id=client).first()
            fcm_helper.fcm_send(message_to.device)
            os.environ['TZ'] = 'Europe/Istanbul'
            if hasattr(time, 'tzset'):
                time.tzset()
            Messages(
                from_user=self.current_user()['id'],
                content=data['content'],
                to_user=client,
                type='text',
                path=None,
                log='none',
                created_at=str(datetime.datetime.now())
            ).save()
        return []

    def my_media(self):
        user_id = self.current_user()['id']
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        query = Messages.query.filter(or_(Messages.from_user == user_id, Messages.to_user == user_id),
                                      Messages.type != 'text', Messages.deleted_at == None).order_by(
            desc(Messages.created_at))
        messages = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()
        res = [x.to_message() for x in messages]
        data = {
            'items': res,
            'pagination': {
                "total": total,
                "count": len(res),
                "per_page": 10,
                "current_page": 1,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def my_message(self):
        user_id = self.current_user()['id']
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        query = Messages.query.filter(or_(Messages.from_user == user_id, Messages.to_user == user_id),
                                      Messages.deleted_at == None)
        messages = query.order_by(desc(Messages.created_at)).offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()
        try:
            Messages.query.filter_by(to_user=user_id, deleted_at=None).update({"is_seen": True})
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            Messages.query.filter_by(to_user=user_id, deleted_at=None).update({"is_seen": True})
            db.session.commit()
        res = [x.to_message() for x in messages]
        data = {
            'items': res,
            'pagination': {
                "total": total,
                "count": len(res),
                "per_page": 10,
                "current_page": 1,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def un_read(self):
        user_type = self.current_user()['user_type']
        user_id = self.current_user()['id']
        if user_type == 'client':
            un_read = Messages.query.filter_by(to_user=user_id, is_seen=False, deleted_at=None).first()
        else:
            query = Messages.query.filter_by(is_seen=False, deleted_at=None)
            query = query.join(Users, Users.id == Messages.from_user).filter(Users.type == 'client')
            un_read = query.first()
        return 1 if un_read is not None else 0

    def delete(self, data):
        user_id = self.current_user()['id']
        user_type = self.current_user()['user_type']
        if user_type == 'client':
            message = Messages.query.filter_by(id=data['message'], from_user=user_id).first()
        else:
            users = Users.query.filter(Users.type != "client", Users.status == 1).all()
            user_ids = [c.id for c in users]
            message = Messages.query.filter(Messages.id == data['message'],
                                            Messages.from_user.in_(user_ids)).first()

        if message:
            self.delete_log(message.log, user_id, datetime.datetime.strftime(message.created_at, '%Y-%m-%d'))
            message.deleted_at = str(datetime.datetime.today())
            message.save()
            return []
        else:
            raise NotFoundError('message_deleted', 'Message Already Deleted')

    def send(self, data):
        data['from_user'] = self.current_user()['id']
        if 'to' in data.keys():
            data['to_user'] = data['to']
            message_to = Users.query.filter_by(id=data['to']).first()
            fcm_helper.fcm_send(message_to.device)
        else:
            users = Users.query.filter(Users.type != "client", Users.status == 1).all()
            for user in users:
                fcm_helper.fcm_send(user.device)

        if 'type' in data and data['type'] != "text" and 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                base_file_name = str(uuid.uuid4()) + '-' + filename
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], base_file_name)
                file.save(file_path)
                data['path'] = current_app.config['API_URL'] + base_file_name
            self.create_log(data['log'])
        else:
            data['log'] = 'none'

        user = Users.query.filter_by(id=data['from_user']).first()
        user.archive = 0
        user.save()
        os.environ['TZ'] = 'Europe/Istanbul'
        if hasattr(time, 'tzset'):
            time.tzset()
        Messages(
            from_user=data['from_user'],
            to_user=data['to_user'] if 'to_user' in data else None,
            type=data['type'],
            content=data['content'] if 'content' in data else None,
            path=data['path'] if 'path' in data else None,
            log=data['log'],
            created_at=str(datetime.datetime.now())
        ).save()
        return data

    def create_log(self, log):
        user_id = self.current_user()['id']
        if log == 'breakfast':
            self.breakfast_upsert(user_id)
        elif log == 'lunch':
            self.lunch_upsert(user_id)
        elif log == 'dinner':
            self.dinner_upsert(user_id)
        elif log == 'walking':
            self.walking_upsert(user_id)

    @staticmethod
    def delete_log(log, user_id, day):
        if log == 'breakfast':
            BreakfastLogs.query.filter_by(user_id=user_id, day=day).delete()
        elif log == 'lunch':
            LunchLogs.query.filter_by(user_id=user_id, day=day).delete()
        elif log == 'dinner':
            DinnerLogs.query.filter_by(user_id=user_id, day=day).delete()
        elif log == 'walking':
            WalkingLogs.query.filter_by(user_id=user_id, day=day).delete()
        # elif log == 'weight':
        #   BreakfastLogs.query.filter_by(user_id=user_id, day=day).delete()

    @staticmethod
    def breakfast_upsert(user_id):
        data = BreakfastLogs.query.filter_by(user_id=user_id, day=datetime.date.today()).first()
        if data is None:
            BreakfastLogs(user_id=user_id, day=datetime.date.today()).save()
        else:
            data.day = datetime.date.today()
            data.save()

    @staticmethod
    def lunch_upsert(user_id):
        data = LunchLogs.query.filter_by(user_id=user_id, day=datetime.date.today()).first()
        if data is None:
            LunchLogs(user_id=user_id, day=datetime.date.today()).save()
        else:
            data.day = datetime.date.today()
            data.save()

    @staticmethod
    def dinner_upsert(user_id):
        data = DinnerLogs.query.filter_by(user_id=user_id, day=datetime.date.today()).first()
        if data is None:
            DinnerLogs(user_id=user_id, day=datetime.date.today()).save()
        else:
            data.day = datetime.date.today()
            data.save()

    @staticmethod
    def walking_upsert(user_id):
        data = WalkingLogs.query.filter_by(user_id=user_id, day=datetime.date.today()).first()
        if data is None:
            WalkingLogs(user_id=user_id, day=datetime.date.today()).save()
        else:
            data.day = datetime.date.today()
            data.save()
