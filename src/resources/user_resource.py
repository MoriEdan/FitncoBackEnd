# -*- coding: utf-8 -*-
import os
from flask_jwt_extended import jwt_required
from src.commons.response import ok_result, validation_result, forbidden_result, not_found_result
from src.resources.base_resource import BaseResource
from src.services.user_service import UserService
from src.helpers.schema_helper import SchemaHelper
from src.commons.auth import authorize
from flask import request, current_app


class RegisterResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__user_service = UserService()

    # def get(self):
    #     self.__user_service.upload()

    # def put(self):
    #     self.__user_service.asdasd()

    def post(self):
        success, schema = self.schema_helper.json_validate_schema('register')
        if success:
            res = self.__user_service.register(schema)
            return ok_result(data=res)
        else:
            return validation_result(message=schema if isinstance(schema, str) else schema.message)


class UserResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    def get(self):
        result = self._user_service.get_user()
        return ok_result(data=result)


class UpdateMeResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['client'])
    def post(self):
        success, schema = SchemaHelper().json_validate_schema('update_me')
        if success:
            result = self._user_service.update_user(schema)
            return ok_result(data=result)
        else:
            if 'pp' in request.files:
                result = self._user_service.update_user_picture()
                return ok_result(data=result)
            return validation_result(message=schema if isinstance(schema, str) else schema.message)


class WaterResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['client'])
    def post(self):
        water = request.json['water'] if request.is_json else request.form['water']
        result = self._user_service.update_user_water(water)
        return ok_result(data=result)


class SportResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['client'])
    def post(self):
        data = request.json if request.is_json else request.form
        result = self._user_service.update_user_sport(data)
        return ok_result(data=result)


class ProfileResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['client'])
    def get(self):
        date = request.args.get('date', None)
        result = self._user_service.user_profile(date)
        return ok_result(data=result)


class ClientProfileResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        date = request.args.get('date', None)
        client = request.args.get('client', None)
        result = self._user_service.user_profile(date, client)
        result["name"] = result["full_name"]
        return ok_result(data=result)


class DieticianResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        order = int(request.args.get('order', 1))
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        search = request.args.get('search', None)
        result = self._user_service.get_dieticians(order, page, pagination, search)
        return ok_result(data=result)


class ApprovalsResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        order = int(request.args.get('order', 1))
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        search = request.args.get('search', None)
        result = self._user_service.get_approvals(order, page, pagination, search)
        return ok_result(data=result)


class ApproveResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        success, schema = SchemaHelper().json_validate_schema('approve')
        if success:
            result = self._user_service.approve(dict(schema))
            return ok_result(data=result)
        else:
            return validation_result(message=schema if isinstance(schema, str) else schema.message)


class PauseResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        data = request.json if request.is_json else request.form
        result, resp = self._user_service.pause(data)
        if result:
            return ok_result(data=resp)
        else:
            return forbidden_result(message="Pasif edilmiş kullanıcının hesabı dondurulamaz. ")


class StatusResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        data = request.json if request.is_json else request.form
        result, resp = self._user_service.status(data)
        if result:
            return ok_result(data=resp)
        else:
            return forbidden_result(message="Hesabı durdurlmuş kullanıcının durumunu değiştiremezsiniz.")


class ClientResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        order = int(request.args.get('order', 1))
        page = int(request.args.get('page', 1))
        pagination = int(request.args.get('pagination', 10))
        search = request.args.get('search', None)
        archive = request.args.get('archive', None)
        result = self._user_service.get_clients(order, page, pagination, search, archive)
        return ok_result(data=result)


class ClientItemResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self, cid):
        result = self._user_service.get_client_by_id(cid)
        if len(result) == 0:
            return not_found_result(data=result, message='Sonuç bulunamadı.')
        return ok_result(data=result)


class NotesResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._user_service.update_user_notes()
        return ok_result(data=result)


class WeightResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._user_service.update_user_logs()
        return ok_result(data=result)


class UpdateWeightResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._user_service.update_weight()
        return ok_result(data=result)


class DeleteWeightResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._user_service.delete_weight()
        return ok_result(data=result)


class TrackingResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        result = self._user_service.tracking()
        return ok_result(data=result)


class RenewalsResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        result = self._user_service.renewals()
        return ok_result(data=result)


class MonthlyResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        result = self._user_service.monthly()
        return ok_result(data=result)


class WeightsResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self, wid):
        result = self._user_service.weights(wid)
        return ok_result(data=result)


class ProfileUpdateResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._user_service = UserService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._user_service.update_profile()
        return ok_result(data=result)
