# -*- coding: utf-8 -*-
import datetime
import mimetypes
import os
import math
import uuid

from sqlalchemy import desc

from src.commons.exception import NotFoundError
from src.services.base_service import BaseService
from flask import current_app as app, request
from src.utils.file_util import upload_file
from werkzeug.utils import secure_filename

# Models
from src.models.diets_model import Diets
from src.models.diet_repeats_model import DietRepeats
from src.models.diet_images_model import DietImages
from src.models.breakfast_logs_model import BreakfastLogs
from src.models.lunch_logs_model import LunchLogs
from src.models.dinner_logs_model import DinnerLogs
from src.models.water_model import Water
from src.models.walking_logs_model import WalkingLogs
from src.models.sport_model import Sport
from src.models.user_infos_model import UserInfos
from src.models.users_model import Users
from src.models.base_model import db


class DietService(BaseService):
    def __init__(self):
        super().__init__()

    @staticmethod
    def delete_diet():
        data = request.json if request.is_json else request.form
        diet = Diets.query.filter(Diets.id == data['plan']).first()
        if diet:
            diet_repeats = DietRepeats.query.filter_by(diet_id=diet.id).all()
            for itm in diet_repeats:
                DietImages.query.filter_by(repeat_id=itm.id).delete()
                itm.delete()
            db.session.commit()
            diet.delete()
            return []
        else:
            raise NotFoundError('not_found_error', 'Diet Not Deleted')

    @staticmethod
    def add_diet():
        try:
            json_data = request.json if request.is_json else request.form
            time_format = '%Y-%m-%d'
            end_time = datetime.datetime.strptime(json_data['end'], time_format)
            start_time = datetime.datetime.strptime(json_data['start'], time_format)
            delta = end_time - start_time
            old_diet = Diets.query.filter_by(user_id=json_data['user_id']).first()
            day = delta.days + 1
            if old_diet is None:
                user = Users.query.filter_by(id=json_data['user_id']).first()
                payment_day = datetime.datetime.strptime(json_data['start'], time_format)
                payment_day = datetime.datetime.strftime(payment_day + datetime.timedelta(days=1), '%d')
                user.payment_day = payment_day
                user.save()
            old_diet = Diets.query.filter_by(user_id=json_data['user_id'], start=json_data['start'],
                                             end=json_data['end']).first()
            if old_diet is None:
                diet = Diets(
                    user_id=json_data['user_id'],
                    start=json_data['start'],
                    end=json_data['end'],
                    type=json_data['type'],
                    days=day
                )
                old_diet = diet
            else:
                old_diet.user_id = json_data['user_id']
                old_diet.start = json_data['start']
                old_diet.end = json_data['end']
                old_diet.type = json_data['type']
                old_diet.days = day
            old_diet.save()
            delete_repeats = DietRepeats.query.filter_by(diet_id=old_diet.id).all()
            for itm in delete_repeats:
                itm.delete()
            for index in range(len(request.files)):
                diet_repeat = DietRepeats(
                    diet_id=old_diet.id,
                    repeat=json_data[f"repeats[{index}]"]
                )
                diet_repeat.save()
                images = request.files[f'images[{index}][]']
                filename = secure_filename(images.filename)
                base_file_name = str(uuid.uuid4()) + '-' + filename
                pp = os.path.join(app.config['UPLOAD_FOLDER'], base_file_name)
                images.save(pp)
                diet_image = DietImages(
                    repeat_id=diet_repeat.id,
                    image=app.config['API_URL'] + base_file_name,
                )
                diet_image.save()
        except Exception as e:
            print(f'Diet Add: {e}')
        return []

    def get_my_plan(self):
        user_id = self.current_user()['id']
        today = datetime.date.today()
        diet = Diets.query.filter(Diets.user_id == user_id,
                                  Diets.start <= today,
                                  Diets.end >= today).first()
        if diet is None:
            return []
        return diet.to_json()

    def get_my_plans(self, per_page, page=1, user_id=None):
        if per_page is None:
            per_page = 10
        if user_id is None:
            user_id = self.current_user()['id']
        diets = Diets.query.filter_by(user_id=user_id).order_by(desc(Diets.end)).offset((page - 1) * per_page).limit(per_page).all()
        total = Diets.query.filter_by(user_id=user_id).count()
        pagination = {
            "total": total,
            "count": len(diets),
            "per_page": per_page,
            "current_page": page,
            "total_pages": math.ceil(total / int(per_page))
        }
        return {'items': [x.to_plan() for x in diets], 'pagination': pagination}

    def home(self):
        user_id = self.current_user()['id']
        today = datetime.date.today()
        user = UserInfos.query.filter_by(user_id=user_id).first()
        active_plan = Diets.query.filter(Diets.user_id == user_id,
                                         Diets.start <= today,
                                         Diets.end >= today).first()
        breakfast = BreakfastLogs.query.filter_by(user_id=user_id, day=today).first()
        lunch = LunchLogs.query.filter_by(user_id=user_id, day=today).first()
        dinner = DinnerLogs.query.filter_by(user_id=user_id, day=today).first()
        water = Water.query.filter_by(user_id=user_id, day=today).first()
        walking = WalkingLogs.query.filter_by(user_id=user_id, day=today).first()
        sport = Sport.query.filter_by(user_id=user_id, day=today).first()
        data = {
            "registered": str(user.users.created_at),
            "target": user.target,
            "active_plan_id": active_plan.id if active_plan is not None else None,
            "active_plan_start": str(active_plan.start) if active_plan is not None else None,
            "active_plan_end": str(active_plan.end) if active_plan is not None else None,
            "active_plan_type": active_plan.type if active_plan is not None else None,
            "breakfast": 0 if breakfast is None else 1,
            "lunch": 0 if lunch is None else 1,
            "dinner": 0 if dinner is None else 1,
            "water": water.unit if water is not None else 0,
            "walking": 0 if walking is None else 1,
            "sport": 0 if sport is None else 1,
            "pp": user.users.pp,
            "ad": user.users.name,
            "soyad": user.users.last_name,
            "vip": user.vip,
            "type": user.type,
            "can_walk": user.can_walk,
        }
        return data

    @staticmethod
    def get_plan(diet_id):
        diet = DietRepeats.query.filter_by(diet_id=diet_id).all()
        if len(diet) > 0:
            data = diet[0].diets.to_json()
            data['repeats'] = []
            i = 0
            for item in diet:
                data['repeats'].append(item.to_json())
                dm = DietImages.query.filter_by(repeat_id=item.id).first()
                data['repeats'][i]['images'] = [dm.to_json()]
                i += 1
            return data
        return {}
