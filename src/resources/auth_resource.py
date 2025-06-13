# -*- coding: utf-8 -*-
from flask_jwt_extended import jwt_required
from src.commons.response import no_content_result, created_result, ok_result, validation_result
from src.resources.base_resource import BaseResource
from src.services.auth_service import AuthService
from flask import request
from src.commons.auth import authorize
from datetime import datetime


class AuthResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    def post(self):
        success, schema = self.schema_helper.json_validate_schema('auth')
        if success:
            result = self.__auth_service.login(schema=schema)
            return ok_result(result)
        else:
            return validation_result(message=schema if isinstance(schema, str) else schema.message)

    @jwt_required(refresh=True)
    def put(self):
        result = self.__auth_service.set_refresh_access_token()
        return created_result(result)


class LogoutResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    @jwt_required()
    def delete(self):
        self.__auth_service.logout()
        return no_content_result()


class ResetPasswordResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    def post(self):
        email = request.json['email'] if request.is_json else request.form['email']
        self.__auth_service.reset_password(email.strip())
        return ok_result(data=[])


class UpdatePasswordResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    @jwt_required()
    def post(self):
        self.__auth_service.update_password()
        return ok_result(data=True)


class CheckEmailResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    def get(self):
        email = request.args['email']
        status, message = self.__auth_service.check_email(email.strip())
        return ok_result(status=status, message=message)


class SystemResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    def get(self):
        data = self.__auth_service.system_status()
        return ok_result(data=data)

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        json_data = request.json if request.is_json else request.form
        if str(json_data['statu']) not in ['0', '1']:
            return validation_result(message='Statu in 0,1')
        data = self.__auth_service.system_status_update(json_data)
        return ok_result(data=data)

    def patch(self):
        current_timezone = datetime.now().astimezone().tzinfo
        return ok_result(data=str(current_timezone))


class ErrorResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    def post(self):
        error = request.json['error'] if request.is_json else request.form['error']
        data = self.__auth_service.save_error(error)
        return ok_result(data=data)


class WebViewResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__auth_service = AuthService()

    def get(self):
        data = self.__auth_service.web_view()
        return ok_result(data=data)
