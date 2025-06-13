# -*- coding: utf-8 -*-
import copy
import datetime
import urllib

import math
import os
import time
import uuid

from dateutil.relativedelta import relativedelta
from flask import request, current_app
from sqlalchemy import desc, func
from sqlalchemy.sql.functions import concat
from werkzeug.utils import secure_filename

from src.commons.exception import NotFoundError
from src.models.breakfast_logs_model import BreakfastLogs
from src.models.delete_approves_model import DeleteApproves
from src.models.diet_images_model import DietImages
from src.models.diets_model import Diets
from src.models.dinner_logs_model import DinnerLogs
from src.models.lunch_logs_model import LunchLogs
from src.models.messages_model import Messages
from src.models.sport_model import Sport
from src.models.timezones_model import Timezones
from src.models.user_infos_model import UserInfos
from src.models.users_model import Users
from src.models.walking_logs_model import WalkingLogs
from src.models.water_model import Water
from src.models.weight_logs_model import WeightLogs
from src.services.auth_service import AuthService
from src.services.base_service import BaseService
from src.utils.file_util import allowed_file, upload_file, download_file
from src.utils.hash_util import hash_bcrypt


class UserService(BaseService):

    def __init__(self):
        super().__init__()

    # def upload(self):
    #     sep_str = '/uploads/'
    #     medias = DietImages.query.all()
    #     for item in medias:
    #         if sep_str in item.image:
    #             file_name = item.image.split(sep_str)[-1]
    #             item.image = download_file(item.image, urllib.parse.unquote(file_name))
    #             item.save()
    #     users = Users.query.all()
    #     for user in users:
    #         if sep_str in user.pp:
    #             file_name = user.pp.split(sep_str)[-1]
    #             user.pp = download_file(user.pp, urllib.parse.unquote(file_name))
    #             user.save()
    #         else:
    #             user.pp = download_file(user.pp, 'fitnco.webp')
    #             user.save()
    #
    def mes(self):
        sep_str = 's3.amazonaws.com'
        date_ = '2024-07-12 22:35:56.645505'
        while True:
            message = Messages.query.filter(Messages.type == 'image',Messages.path.ilike(f'%{sep_str}%'), Messages.updated_at < date_).order_by(desc(Messages.id)).first()
            if not message:
                break
            if message.path and sep_str in message.path:
                file_name = message.path.split('/')[-1]
                new_url = download_file(message.path, file_name)
                if new_url:
                    message.path = new_url
            message.updated_at = date_
            message.save()

    # def test(self):
    #     with open('newfile2.txt', 'r', encoding='utf-8') as file:
    #         all_lines = file.readlines()
    #         for line in all_lines:
    #             lines = line.split(',')
    #             UserInfos.query.filter_by(user_id=lines[0]).update({'notes': lines[1].strip()})
    #             db.session.commit()

    @staticmethod
    def update_weight():
        data = request.json if request.is_json else request.form
        weight = WeightLogs.query.filter_by(id=data['id'], deleted_at=None).first()
        if weight:
            weight.unit = float(data['weight'].replace(',', '.'))
            weight.save()
        return []

    @staticmethod
    def delete_weight():
        data = request.json if request.is_json else request.form
        weight = WeightLogs.query.filter_by(id=data['id'], deleted_at=None).first()
        if weight:
            weight.deleted_at = str(datetime.datetime.today())
            weight.save()
        return []

    @staticmethod
    def weights(user_id):
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 15))
        query = WeightLogs.query.filter_by(user_id=user_id, deleted_at=None)
        weight = query.order_by(desc(WeightLogs.created_at)).offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()
        res = [x.to_weight() for x in weight]
        data = {
            'items': res,
            'pagination': {
                "total": total,
                "count": len(res),
                "per_page": pagination,
                "current_page": page,
                "total_pages": math.ceil(total / pagination if total > 0 else 0)
            }
        }
        return data

    def monthly(self):
        order = int(request.args.get('order', 0))
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 15))
        search = request.args.get('search', None)
        vip = request.args.get('vip', None)
        left = request.args.get('left', None)

        query = Users.query.filter(Users.type == 'client', Users.status == 1)
        query = query.join(UserInfos)

        if search is not None and search.strip() != '':
            query = query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))

        if vip == '1':
            query = query.filter(UserInfos.vip == True)
        elif vip == '0':
            query = query.filter(UserInfos.vip == False)

        if left is not None and left != '0':
            payment_day = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=int(left)), '%d')
            query = query.filter(Users.payment_day == payment_day)
        elif left:
            query = query.filter(Users.payment_day == None)

        if order == 2:
            query = query.order_by(concat(Users.name, ' ', Users.last_name))
        elif order == 1:
            query = query.order_by(desc(UserInfos.vip))

        users = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()

        items = []
        for user in users:
            tmp = user.to_approval()
            user_inf = user.user_infos[0] if user.user_infos else None
            if user_inf is not None:
                tmp.update(user_inf.to_load())
            tmp.update({'date': self.get_day(user.payment_day)})
            items.append(tmp)

        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(users),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    @staticmethod
    def update_profile():
        data = request.json if request.is_json else request.form
        user = Users.query.filter_by(id=data['client']).first()
        if 'pp' in request.files:
            file = request.files['pp']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                base_file_name = str(uuid.uuid4()) + '-' + filename
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], base_file_name)
                file.save(file_path)
                user.pp = current_app.config['API_URL'] + base_file_name
        if 'password' in data:
            user.password = hash_bcrypt(data['password'])
        user.payment_day = data.get('payment_day', user.payment_day)
        user.save()
        user_info = user.user_infos[0]
        user_info.gender = data.get('gender', user_info.gender)
        user_info.age = data.get('age', user_info.age)
        user_info.pp = user.pp
        user_info.type = data.get('type', user_info.type)
        try:
            target = float(data.get('target').replace(',', '.'))
        except Exception as e:
            target = user_info.target
        user_info.target = target
        user_info.vip = True if 'vip' in data and bool(int(data['vip'])) else False
        user_info.can_walk = True if 'can_walk' in data and bool(int(data['can_walk'])) else False
        user_info.begining = data.get('begining', user_info.begining)
        user_info.save()
        ret_data = user.to_load()
        ret_data.update(user_info.to_load())
        return ret_data

    @staticmethod
    def renewals():
        order = int(request.args.get('order', 0))
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 15))
        search = request.args.get('search', None)
        vip = request.args.get('vip', None)
        user_type = request.args.get('type', None)
        left = request.args.get('left', None)

        if page <= 0:
            page = 1
        query = Users.query.filter(Users.type == 'client', Users.status == 1)
        query = query.join(UserInfos)

        if search is not None and search.strip() != '':
            query = query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))

        if vip == '1':
            query = query.filter(UserInfos.vip == True)
        elif vip == '0':
            query = query.filter(UserInfos.vip == False)

        if user_type is not None:
            query = query.filter(UserInfos.type == user_type)

        if left is not None and left != '0':
            diet_end = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=int(left)),
                                                  '%Y-%m-%d')
            query = query.join(Diets).filter(Diets.end == diet_end)

        if order == 0:
            query = query.order_by(concat(Users.name, ' ', Users.last_name))
        elif order == 1:
            query = query.order_by(desc(UserInfos.vip))
        else:
            query = query.order_by(desc(Users.payment_day))

        renewals = query.all()
        total = len(renewals)
        offset = (page - 1) * pagination
        renewals = renewals[offset:pagination + offset]

        items = []
        for user in renewals:
            tmp = user.to_approval()
            user_inf = user.user_infos[0] if user.user_infos else None
            diet = user.diet[0] if user.diet else None
            if user_inf is not None:
                tmp.update(user_inf.to_load())
                tmp.update({'date': None, 'diet_type': None})

            if diet is not None and left != '0':
                tmp.update({'date': datetime.datetime.strftime(diet.end, '%d.%m.%Y'), 'diet_type': diet.type})
            items.append(tmp)

        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(renewals),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    @staticmethod
    def tracking():
        try:
            order = int(request.args.get('order', 0))
            page = int(request.args.get('page', 1))
            pagination = int(request.args.get('pagination', 15))
            search = request.args.get('search', None)
            vip = request.args.get('vip', None)
            can_walk = request.args.get('can_walk', None)
            sport = request.args.get('sport', None)
            walk = request.args.get('walk', None)
            water = request.args.get('water', None)
            meal = request.args.get('meal', None)
            meal_type = request.args.get('type', None)
            control = None
            if page <= 0:
                page = 1
            today = datetime.date.today()
            query = Users.query.filter(Users.type == 'client', Users.status == 1)
            query = query.join(UserInfos)
            if meal is not None:
                if meal == 'breakfast':
                    control = 'breakfasts'
                    query = query.join(BreakfastLogs).filter(BreakfastLogs.day < today)
                elif meal == 'lunch':
                    control = 'lunch'
                    query = query.join(LunchLogs).filter(LunchLogs.day < today)
                elif meal == 'dinner':
                    control = 'dinners'
                    query = query.join(DinnerLogs).filter(DinnerLogs.day < today)

            if search is not None and search.strip() != '':
                query = query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))

            if can_walk == '1':
                query = query.filter(UserInfos.can_walk == True)
            elif can_walk is not None:
                query = query.filter(UserInfos.can_walk == False)

            if vip == '1':
                query = query.filter(UserInfos.vip == True)
            elif vip is not None:
                query = query.filter(UserInfos.vip == False)

            if meal_type is not None:
                query = query.filter(UserInfos.type == meal_type)

            if walk == '1':
                query = query.join(WalkingLogs).filter(WalkingLogs.day == today)
            elif walk == '0':
                control = 'walks'

            if sport == '1':
                query = query.join(Sport).filter(Sport.day == today)
            elif sport == '0':
                control = 'sport'

            if water == '0':
                query = query.join(Water).filter(Water.day <= today)
                control = 'waters'
            elif water is not None:
                query = query.join(Water).filter(Water.unit >= int(water), Water.day == today)

            if order == 0:
                query = query.order_by(Users.id)
            elif order == 1:
                query = query.order_by(desc(UserInfos.vip))
            elif order == 2:
                query = query.order_by(func.concat(Users.name, ' ', Users.last_name))

            # if with_out_pagination:
            # tracking = query.all()
            # else:
            tracking = query.all()
            total = len(tracking)
            offset = (page - 1) * pagination
            tracking = tracking[offset:pagination + offset]
            items = []
            for user in tracking:
                if control:
                    control_data = getattr(user, control)
                    if control_data:
                        continue
                tmp = user.to_tracking()
                user_inf = user.user_infos[0] if user.user_infos else None
                if user_inf is not None:
                    tmp.update(user_inf.to_load())
                items.append(tmp)
                # if len(items) > pagination - 1:
                #     break
            data = {
                'items': items,
                'pagination': {
                    "total": total,
                    "count": len(items),
                    "per_page": str(pagination),
                    "current_page": len(items),
                    "total_pages": math.ceil(total / pagination)
                }
            }
            return data
        except Exception as e:
            print(e)
            return {}

    def update_user_notes(self):
        json_data = request.json if request.is_json else request.form
        user_info = UserInfos.query.filter_by(user_id=json_data['user_id']).first()
        user_info.notes = json_data['notes'] if 'notes' in json_data else user_info.notes
        user_info.save()
        user_data = user_info.users.to_load()
        user_data = self.user_info_updated(user_data, user_info)
        return user_data

    @staticmethod
    def update_user_logs():
        json_data = request.json if request.is_json else request.form
        today = datetime.date.today()
        user_weight = WeightLogs.query.filter_by(user_id=json_data['client'], day=today, deleted_at=None).first()
        if user_weight is not None:
            user_weight.unit = float(str(json_data['weight']).replace(',', '.'))
            user_weight.save()
        else:
            weight = WeightLogs(
                user_id=json_data['client'],
                day=today,
                unit=float(json_data['weight'].replace(',', '.')))
            weight.save()
        return []

    def get_client_by_id(self, cid):
        users = Users.query.filter_by(id=cid).first()
        user_info = UserInfos.query.filter_by(user_id=cid).first()
        if user_info is None and users is None:
            return []
        user_data = users.to_load()
        user_data = self.user_info_updated(user_data, user_info)
        return user_data

    @staticmethod
    def user_info_updated(user_data, user_info):
        if user_info is None:
            user_data.update({
                'age': None,
                'weight': None,
                'height': None,
                'note': None,
                'type': None,
                'gender': None,
                'can_walk': None,
                'vip': None,
                'target': None,
                'begining': None
            })
        else:
            user_data.update(user_info.to_load())
        return user_data

    @staticmethod
    def pause(data):
        user = Users.query.filter_by(id=data['user_id']).first()
        if user.status == 0:
            return False, {}
        if data['pause'] == '1':
            user.payment_day = None
            user.pause_start = data['pause_start']
            user.pause_end = data['pause_end']
        else:
            user.payment_day = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=1), '%d')
            user.pause_start = None
            user.pause_end = None
        user.save()
        user_data = user.to_load()
        user_info = UserInfos.query.filter_by(user_id=user.id).first()
        user_data.update(user_info.to_load() if user_info is not None else {})
        return True, user_data

    @staticmethod
    def status(data):
        user = Users.query.filter_by(id=data['user_id']).first()
        if user.type == 'dietician':
            AuthService().logout_user(data['user_id'])

        if user.pause_start is not None:
            return False, {}

        if int(data['status']) == 1:
            user.payment_day = datetime.datetime.strftime(datetime.date.today(), '%d')
            user.archive = False
        else:
            user.payment_day = None
            user.archive = True
        user.status = int(data['status'])

        user.save()
        user_data = user.to_load()
        user_info = UserInfos.query.filter_by(user_id=user.id).first()
        user_data.update(user_info.to_load() if user_info is not None else {})
        return True, user_data

    def get_dieticians(self, order, page, pagination, search):
        if page <= 0:
            page = 1
        query = Users.query.filter(Users.type == 'dietician')
        if search is not None and search.strip() != '':
            query = query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))
        if order == 1:
            query = query.order_by(func.concat(Users.name, ' ', Users.last_name))
        elif order == 2:
            query = query.order_by(desc(Users.created_at))

        dieticians = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()

        items = []
        for user in dieticians:
            tmp = user.to_load()
            user_inf = UserInfos.query.filter_by(user_id=user.id).first()
            if user_inf is not None:
                tmp.update(user_inf.to_load())
            items.append(tmp)
        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(dieticians),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def get_clients(self, order, page, pagination, search, archive):
        if page <= 0:
            page = 1
        query = Users.query.filter(Users.type == 'client', Users.status == 1)
        if archive is not None:
            query = Users.query.filter(Users.type == 'client', Users.status == 0)

        if search is not None and search.strip() != '':
            query = query.filter((func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))
        if order == 1:
            query = query.order_by(func.concat(Users.name, ' ', Users.last_name))
        elif order == 2:
            query = query.order_by(desc(Users.created_at))
        dieticians = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()

        items = []
        for user in dieticians:
            tmp = user.to_load()
            user_inf = UserInfos.query.filter_by(user_id=user.id).first()
            if user_inf is not None:
                tmp.update(user_inf.to_load())
            items.append(tmp)
        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(dieticians),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def get_approvals(self, order, page, pagination, search):
        if page <= 0:
            page = 1
        query = Users.query.filter(Users.status == 2)
        if search is not None and search.strip() != '':
            query = Users.query.filter(Users.status == 2,
                                       (func.concat(Users.name, ' ', Users.last_name)).ilike(f'%{search}%'))
        if order == 1:
            query = query.order_by(func.concat(Users.name, ' ', Users.last_name))
        elif order == 2:
            query = query.order_by(desc(Users.created_at))
        approvals = query.offset((page - 1) * pagination).limit(pagination).all()
        total = query.count()

        items = []
        for user in approvals:
            tmp = user.to_approval()
            user_inf = UserInfos.query.filter_by(user_id=user.id).first()
            tmp.update({'info': user_inf.to_json() if user_inf is not None else None})
            items.append(tmp)
        # items.reverse()
        data = {
            'items': items,
            'pagination': {
                "total": total,
                "count": len(approvals),
                "per_page": str(pagination),
                "current_page": page,
                "total_pages": math.ceil(total / pagination)
            }
        }
        return data

    def user_profile(self, day, user_id=None):
        if day is None:
            day = datetime.date.today()
        if user_id is None:
            user_id = self.current_user()['id']
        weight = WeightLogs.query.filter_by(user_id=user_id, deleted_at=None).order_by(desc(WeightLogs.day)).first()
        user = UserInfos.query.filter_by(user_id=user_id).first()
        os.environ['TZ'] = user.users.timezones.zone
        if hasattr(time, 'tzset'):
            time.tzset()
        new_time = time.strftime('%H:%M')
        weight_logs_model = WeightLogs.query.with_entities(WeightLogs.unit, WeightLogs.day).filter_by(
            user_id=user_id, deleted_at=None).order_by(desc(WeightLogs.day)).all()
        weight_logs = [{'unit': x.unit, 'day': str(x.day)} for x in weight_logs_model]
        breakfast = BreakfastLogs.query.filter_by(user_id=user_id, day=day).first()
        breakfast_images = self.get_logs_images(user_id, 'image', 'breakfast', day)
        lunch = LunchLogs.query.filter_by(user_id=user_id, day=day).first()
        lunch_images = self.get_logs_images(user_id, 'image', 'lunch', day)
        dinner = DinnerLogs.query.filter_by(user_id=user_id, day=day).first()
        dinner_images = self.get_logs_images(user_id, 'image', 'dinner', day)
        water = Water.query.filter_by(user_id=user_id, day=day).first()
        walking = WalkingLogs.query.filter_by(user_id=user_id, day=day).first()
        walking_images = self.get_logs_images(user_id, 'image', 'walking', day)
        sport = Sport.query.filter_by(user_id=user_id, day=day).first()
        diet = Diets.query.filter(Diets.user_id == user_id,
                                  Diets.start <= day,
                                  Diets.end >= day).first()
        day = self.get_day(user.users.payment_day)
        data = {
            'full_name': user.users.name + ' ' + user.users.last_name,
            'name': user.users.name,
            'pp': user.users.pp,
            'age': user.age,
            'can_walk': user.can_walk,
            'weight': float(weight.unit) if weight else user.weight,
            'begining': str(user.begining),
            'height': user.height,
            'target': user.target,
            'zone': user.users.timezones.title,
            'time': new_time,
            'weights': weight_logs,
            'breakfast': 1 if breakfast else 0,
            'breakfast_image': breakfast_images.path if breakfast_images else None,
            'lunch': 1 if lunch else 0,
            'lunch_image': lunch_images.path if lunch_images else None,
            'dinner': 1 if dinner else 0,
            'dinner_image': dinner_images.path if dinner_images else None,
            'walking': 1 if walking else 0,
            'walking_image': walking_images.path if walking_images else None,
            'water': water.unit if water else 0,
            'sport': sport.to_json() if sport else 0,
            'auto_zone': user.users.auto_zone,
            'vip': user.vip,
            'type': user.type,
            'gender': user.gender,
            'diet_type': diet.type if diet else 2,
            'date': day
        }
        return data

    @staticmethod
    def get_day(day):
        if day:
            if int(time.strftime('%d')) > int(day):
                tmp_time = time.strftime(f'%Y-%m-{day}')
                date_after_month = datetime.datetime.strptime(tmp_time, '%Y-%m-%d') + relativedelta(months=1)
                day = date_after_month.strftime('%Y-%m-%d')
            else:
                day = time.strftime(f'%Y-%m-{day}')
        else:
            day = None
        return day

    @staticmethod
    def get_logs_images(user_id, type, log, day):
        start = f'{day} 00:00:00'
        end = f'{day} 23:59:59'
        image = Messages.query.filter(Messages.from_user == user_id, Messages.type == type,
                                      Messages.log == log, Messages.deleted_at == None,
                                      Messages.created_at.between(start, end)).order_by(desc(Messages.id)).first()
        return image

    def update_user_water(self, water):
        today = datetime.date.today()
        exists = Water.query.filter_by(user_id=self.current_user()['id'], day=today).first()
        if exists:
            exists.unit = float(water.replace(',', '.'))
            exists.save()
        else:
            Water(user_id=self.current_user()['id'], day=today, unit=float(water.replace(',', '.'))).save()
        return True

    def update_user_sport(self, data):
        today = datetime.date.today()
        exists = Sport.query.filter_by(user_id=self.current_user()['id'], day=today).first()
        if exists:
            exists.sport = int(data['sport'])
            exists.during = data['during']
            exists.save()
        else:
            Sport(user_id=self.current_user()['id'], day=datetime.date.today(), sport=int(data['sport']),
                  during=data['during']).save()
        return True

    def get_user(self):
        current_user = self.current_user()
        result = Users.query.filter_by(id=current_user["id"]).first()
        if not result:
            raise NotFoundError("user.service.error", "User not found")
        data = result.to_json()
        user_infos = UserInfos.query.filter_by(user_id=current_user["id"]).first()
        if user_infos is not None:
            data.update({'info': user_infos.to_json()})
        timezone = Timezones.query.filter_by(id=result.timezone).first()
        data['zone'] = timezone.to_json() if timezone is not None else {}
        return data

    def register(self, schema):
        pp = None
        if 'pp' in request.files:
            file = request.files['pp']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                base_file_name = str(uuid.uuid4()) + '-' + filename
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], base_file_name)
                file.save(file_path)
                pp = current_app.config['API_URL'] + base_file_name
        user = Users(
            name=schema['name'],
            last_name=schema['last_name'],
            email=schema['email'].strip(),
            email_verified_at=None,
            password=hash_bcrypt(schema['password']),
            timezone=schema['timezone'],
            pp=pp if pp is not None else '',
            type="client",
            os=schema['os'],
            device=schema['device'],
            parent=schema['parent'] if 'parent' in schema else None
        )
        user.save()
        try:
            weight = float(schema['weight'].replace(',', '.'))
            height = float(schema['height'].replace(',', '.').replace('cm', ''))
            target = float(schema['target'].replace(',', '.'))
        except Exception as e:
            print(e)
            weight = 0
            height = 100
            target = 0
        user_info = UserInfos(
            user_id=user.id,
            type='online',
            vip=False,
            age=schema['age'],
            begining=weight,
            weight=weight,
            height=height,
            target=target,
            gender=schema['gender'],
            can_walk=bool(schema['can_walk']),
            notes=None
        )
        user_info.save()
        data = user.to_json()
        data.update(user_info.to_json())
        return data

    @staticmethod
    def user_fields(item):
        return {
            'id': item.id,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'phone': item.phone,
            'email': item.email,
            'is_admin': item.is_admin,
            'created_at': item.created_at
        }

    def update_user_picture(self):
        file = request.files['pp']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base_file_name = str(uuid.uuid4()) + '-' + filename
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], base_file_name)
            file.save(file_path)
            user = Users.query.filter_by(id=self.current_user()['id']).first()
            user.pp = current_app.config['API_URL'] + base_file_name
            user.save()
        return True

    def update_user(self, schema):
        user = Users.query.filter_by(id=self.current_user()['id']).first()
        user.name = schema['name']
        user.last_name = schema['last_name']
        user.timezone = schema['timezone']
        user.gender = schema['gender']
        user.age = schema['age']
        user.height = schema['height']
        user.auto_zone = int(schema['auto_zone']) if schema['auto_zone'].isdigit() else 0
        user.save()
        user_info = UserInfos.query.filter_by(user_id=user.id).first()
        user_info.age = schema['age']
        user_info.height = schema['height']
        user_info.target = float(schema['target'].replace(',', '.'))
        user_info.gender = schema['gender']
        user_info.save()
        return self.get_user()

    def approve(self, data):
        user = Users.query.filter_by(id=data['user_id']).first()
        try:
            data['begining'] = float(data['weight'].replace(',', '.'))
        except Exception as e:
            print(e)
            data['begining'] = 0
            data['weight'] = 0
        if data['approve']:
            if 'dietician' in data and str(data['dietician']) == '0':
                user_info = UserInfos.query.filter_by(user_id=user.id).first()
                info_data = copy.deepcopy(data)
                del info_data['approve']
                del info_data['name']
                del info_data['last_name']
                del info_data['dietician']
                info_data['vip'] = bool(int(data['vip']))
                info_data['can_walk'] = bool(int(data['can_walk']))
                for key, value in info_data.items():
                    user_info.__setattr__(key, value)
                user_info.save()
            user.name = data['name']
            user.last_name = data['last_name']
            user.status = 1
            user.save()
        else:
            user.status = 3
            user.save()
            DeleteApproves(user.id, datetime.date.today()).save()
        if 'dietician' in data and str(data['dietician']) == '1' and self.current_user()['user_type'] == 'admin':
            user.type = 'dietician'
            user.save()
        user_data = user.to_approval()
        user_inf = UserInfos.query.filter_by(user_id=user.id).first()
        user_data.update({'info': user_inf.to_json() if user_inf is not None else None})
        return user_data
