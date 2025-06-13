# -*- coding: utf-8 -*-
from src.services.base_service import BaseService
from flask import request
from src.models.quick_answers_model import QuickAnswers


class AnswerService(BaseService):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_all():
        answers = QuickAnswers.query.order_by(QuickAnswers.id).all()
        ret = [x.to_message() for x in answers]
        return ret

    @staticmethod
    def new():
        data = request.json if request.is_json else request.form
        new_answer = QuickAnswers(message=data['message'])
        new_answer.save()
        return new_answer.to_message()

    @staticmethod
    def detail():
        data = request.json if request.is_json else request.args
        ans = QuickAnswers.query.filter_by(id=data['id']).first()
        return ans.to_json()

    @staticmethod
    def update():
        data = request.json if request.is_json else request.form
        ans = QuickAnswers.query.filter_by(id=data['id']).first()
        ans.message = data['message']
        ans.save()
        return ans.to_json()

    @staticmethod
    def delete():
        data = request.json if request.is_json else request.form
        ans = QuickAnswers.query.filter_by(id=data['id']).first()
        ret = ans.to_message()
        ans.delete()
        return ret
