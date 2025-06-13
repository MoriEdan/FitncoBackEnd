# -*- coding: utf-8 -*-
from flask_jwt_extended import get_jwt_identity
from flask import current_app


class BaseService:
    def __init__(self):
        pass

    @staticmethod
    def current_user():
        return get_jwt_identity()

    @staticmethod
    def current_user_name():
        jwt_data = get_jwt_identity()
        return jwt_data['user_name']

    @staticmethod
    def current_user_details(user_service):
        user = get_jwt_identity()
        return user_service.get_user(id=user['id'])

    @staticmethod
    def get_medias(owner_id):
        from src.models.medias_model import Medias
        media = Medias.query.filter_by(owner_id=owner_id).all()
        medias = []
        for row in media:
            medias.append({'src': row.src, 'title': row.title, 'type': row.type})
        return medias

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    @staticmethod
    def array_simplify(array, key):
        try:
            new_array = [dict(t) for t in {tuple(d.items()) for d in array}]
            sorted_list = sorted(new_array, key=lambda d: d[key], reverse=True)
        except Exception as e:
            print(e)
            return []
        return sorted_list
