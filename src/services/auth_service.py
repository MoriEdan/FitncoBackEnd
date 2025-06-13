# -*- coding: utf-8 -*-
import datetime
import string
import random
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jti, get_jwt
from src.commons.exception import NotFoundError, ForbiddenError
from src.services.base_service import BaseService
from flask import current_app as app, request
from src.utils.hash_util import check_bcrypt, hash_bcrypt
from src.helpers.cache_helper import CacheHelper
from flask_mail import Message
# Models
from src.models.users_model import Users
from src.models.system_model import System
from src.models.errors_model import Errors
from src.models.webview_model import Webview


class AuthService(BaseService):
    def __init__(self):
        super().__init__()
        self.__cache_helper = CacheHelper()

    def logout_user(self, user_id):
        from app import jwt_redis_blocklist
        data = self.__cache_helper.get(f'jti:{user_id}')
        if data:
            deleted = self.__cache_helper.delete(f'token:{data}')
            jwt_redis_blocklist.set(f'blocked:{data}', "", keepttl=-1)
            self.__cache_helper.delete(f'jti:{user_id}')
            return deleted

    def update_password(self):
        data = request.json if request.is_json else request.form
        user_id = self.current_user()['id']
        user = Users.query.filter_by(id=user_id).first()
        user.password = hash_bcrypt(data['password'])
        user.save()
        return True

    @staticmethod
    def web_view():
        data = Webview.query.first()
        return data.to_json()

    @staticmethod
    def save_error(error):
        error = Errors(error=error)
        error.save()
        return True

    @staticmethod
    def system_status():
        day = datetime.date.strftime(datetime.date.today(), '%a')
        if day == 'Sun':
            return {'statu': 1, 'type': 1}
        system = System.query.filter_by(id=1).first()
        return {'statu': bool(system.statu), 'type': 2}

    @staticmethod
    def system_status_update(data):
        system = System.query.filter_by(id=1).first()
        system.statu = bool(int(data['statu']))
        system.save()
        return True

    @staticmethod
    def check_email(email):
        user = Users.query.filter_by(email=email).first()
        if user is None:
            return True, 'Kayıt olmak için uygun.'
        else:
            return False, 'By email zaten kayıtlı.'

    def logout(self):
        from app import jwt_redis_blocklist
        try:
            jti = get_jwt()["jti"]
            data = self.__cache_helper.delete(f'token:{jti}')
            jwt_redis_blocklist.set(f'blocked:{jti}', "", keepttl=-1)
            self.__cache_helper.delete(f'jti:{self.current_user()["id"]}')
            return bool(data)
        except Exception as e:
            print(e)
            return False

    def login(self, schema):
        user = self.__get_user(schema=schema)
        if user:
            user.device = schema['device']
            user.os = schema['os']
            user.save()
        result = self.__set_create_token(user)
        return result

    @staticmethod
    def __get_user(schema):
        result = Users.query.filter_by(email=schema["email"].strip()).first()
        if not result:
            raise NotFoundError(code="user.not_found", message="User not found")

        if not check_bcrypt(password=schema["password"], password_hash=result.password):
            raise NotFoundError(code="user.not_found", message="User not found")

        # if not result.status:
        #     raise ForbiddenError("module.user.status", "User status is not active")

        return result

    def __token_expires_delta(self):
        days = app.config["API_EXPIRE_TOKEN"]
        if not days:
            return False
        return datetime.timedelta(days=int(days))

    def __set_create_token(self, user):
        expires_delta = self.__token_expires_delta()

        identity = {
            "id": user.id,
            "first_name": user.name,
            "last_name": user.last_name,
            "email": user.email,
            'user_type': user.type
            # "roles": roles,
        }
        access_token = create_access_token(identity=identity,
                                           expires_delta=expires_delta)
        jti = get_jti(access_token)
        self.__cache_helper.set(key='token:' + str(jti), value=1, timeout=-1 if not expires_delta else expires_delta)
        self.__cache_helper.set(key=f'jti:{user.id}', value=str(jti), timeout=-1)
        refresh_token = create_refresh_token(identity=identity,
                                             expires_delta=expires_delta if not expires_delta else expires_delta)
        token = {
            "token": access_token,
            "refresh_token": refresh_token,
        }

        return token

    def set_refresh_access_token(self):
        current_user = get_jwt_identity()
        expires_delta = self.__token_expires_delta()
        access_token = create_access_token(identity=current_user,
                                           expires_delta=expires_delta if not expires_delta else expires_delta)
        self.logout()
        jti = get_jti(access_token)
        self.__cache_helper.set(key='token:' + str(jti), value=1, timeout=-1 if not expires_delta else expires_delta)
        result = {
            'token': access_token,
            'refresh_token': create_refresh_token(identity=current_user,
                                                  expires_delta=expires_delta if not expires_delta else expires_delta)
        }
        return result

    @staticmethod
    def reset_password(email):
        result = Users.query.filter_by(email=email).first()
        if not result:
            raise NotFoundError(code="user.not_found", message="User not found")
        letters = string.ascii_letters + string.digits
        new_pass = ''.join(random.choice(letters) for i in range(6))
        result.password = hash_bcrypt(new_pass)
        result.save()
        try:
            from app import mail
            msg = Message('Şifre Sıfırlama',
                          sender=(app.config['MAIL_FROM_NAME'], app.config['MAIL_USERNAME']),
                          recipients=[email],
                          charset='utf-8')
            msg.body = f"Sisteme giriş yapmak için yeni şifreniz: {new_pass}"
            mail.send(msg)
        except Exception as e:
            print(e)
        return True
