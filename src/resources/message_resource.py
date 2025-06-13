# -*- coding: utf-8 -*-
from flask_jwt_extended import jwt_required
from src.commons.auth import authorize
from src.commons.response import ok_result
from src.resources.base_resource import BaseResource
from flask import request
from src.services.message_service import MessageService


class MessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        data = request.args.get('client', None)
        res = self.message_service.messages(data)
        return ok_result(data=res)


class MediaResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        data = request.args.get('client', None)
        res = self.message_service.medias(data)
        return ok_result(data=res)


class SendMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    def post(self):
        data = request.json if request.is_json else request.form
        res = self.message_service.send(dict(data))
        return ok_result(data=res)


class DeleteMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    def post(self):
        data = request.json if request.is_json else request.form
        res = self.message_service.delete(data)
        return ok_result(data=res)


class UnReadMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    def get(self):
        res = self.message_service.un_read()
        return ok_result(data=res)


class MyMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['client'])
    def get(self):
        res = self.message_service.my_message()
        return ok_result(data=res)


class MediaMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['client'])
    def get(self):
        res = self.message_service.my_media()
        return ok_result(data=res)


class MultipleMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        data = request.json if request.is_json else request.form
        res = self.message_service.multiple_message(data)
        return ok_result(data=res)


class ArchiveMessageResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def post(self):
        data = request.json if request.is_json else request.form
        res = self.message_service.archive(dict(data))
        return ok_result(data=res)


class InboxResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        search = request.args.get('search', None)
        res = self.message_service.inbox(search)
        return ok_result(data=res)


class InboxArchiveResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    @jwt_required()
    @authorize(user_type=['admin', 'dietician'])
    def get(self):
        search = request.args.get('search', None)
        res = self.message_service.inbox(search, True)
        return ok_result(data=res)
