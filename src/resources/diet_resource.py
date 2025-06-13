# -*- coding: utf-8 -*-
from flask_jwt_extended import jwt_required
from src.commons.response import ok_result
from src.resources.base_resource import BaseResource
from src.services.diet_service import DietService
from flask import request
from src.commons.auth import authorize


class PlanResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__diet_service = DietService()

    @jwt_required()
    def get(self):
        diet_id = request.args['plan']
        diet_plan = self.__diet_service.get_plan(diet_id)
        return ok_result(data=diet_plan)


class MyPlansResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__diet_service = DietService()

    @jwt_required()
    def get(self):
        page = request.args.get('page', 1)
        pagination = request.args.get('pagination', 10)
        data = self.__diet_service.get_my_plans(int(pagination), int(page))
        return ok_result(data=data)


class MyPlanResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__diet_service = DietService()

    @jwt_required()
    def get(self):
        data = self.__diet_service.get_my_plan()
        return ok_result(data=data)


class HomeResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.__diet_service = DietService()

    @jwt_required()
    @authorize(user_type=['client'])
    def get(self):
        diet_plan = self.__diet_service.home()
        return ok_result(data=diet_plan)


class DietResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._diet_service = DietService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._diet_service.add_diet()
        return ok_result(data=result)


class DeleteDietResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._diet_service = DietService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self._diet_service.delete_diet()
        return ok_result(data=result)


class ClientPlansResource(BaseResource):

    def __init__(self):
        super().__init__()
        self._diet_service = DietService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        page = request.args.get('page', 1)
        pagination = request.args.get('pagination', 10)
        client = request.args.get('client', None)
        result = self._diet_service.get_my_plans(int(pagination), int(page), user_id=client)
        return ok_result(data=result)
