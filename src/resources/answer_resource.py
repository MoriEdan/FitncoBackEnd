# -*- coding: utf-8 -*-
from flask_jwt_extended import jwt_required
from src.commons.auth import authorize
from src.commons.response import ok_result
from src.resources.base_resource import BaseResource
from src.services.answer_service import AnswerService


class AnswerResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.answer_service = AnswerService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        result = self.answer_service.get_all()
        return ok_result(data=result)


class NewAnswerResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.answer_service = AnswerService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self.answer_service.new()
        return ok_result(data=result)


class DetailAnswerResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.answer_service = AnswerService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        result = self.answer_service.detail()
        return ok_result(data=result)


class UpdateAnswerResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.answer_service = AnswerService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self.answer_service.update()
        return ok_result(data=result)


class DeleteAnswerResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.answer_service = AnswerService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        result = self.answer_service.delete()
        return ok_result(data=result)
