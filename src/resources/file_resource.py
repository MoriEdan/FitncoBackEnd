# -*- coding: utf-8 -*-
import mimetypes
from src.commons.response import not_found_result
from src.resources.base_resource import BaseResource
from flask import send_file
from src.services.message_service import MessageService


class FileResource(BaseResource):

    def __init__(self):
        super().__init__()
        self.message_service = MessageService()

    # @jwt_required()
    def get(self, file_name):
        res = self.message_service.get_file(file_name)
        if res:
            mime_type, _ = mimetypes.guess_type(file_name)
            return send_file(res, mimetype=mime_type)
        else:
            return not_found_result(status=False, code=404, message="File not found")
