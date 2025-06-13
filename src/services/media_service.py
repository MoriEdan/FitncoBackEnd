# -*- coding: utf-8 -*-
import os.path
from src.commons.exception import NotFoundError
from src.services.base_service import BaseService
from flask import send_file, current_app


class MediaService(BaseService):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_media(path):
        real_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], path)
        if os.path.exists(real_path):
            return send_file(real_path, as_attachment=True)
        else:
            raise NotFoundError('file_not_found', 'File Not Found!!')
