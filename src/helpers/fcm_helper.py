# -*- coding: utf-8 -*-
import json
import firebase_admin
from firebase_admin import messaging, credentials, auth
import requests
from flask import current_app
from src.commons.exception import ServiceError
from src.helpers.base_helper import BaseHelper


class FCMHelper(BaseHelper):

    def __init__(self):
        super().__init__()
        creds = credentials.Certificate('fcm.json')
        default_app = firebase_admin.initialize_app(creds)

    @staticmethod
    def fcm_send(device):
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Yeni Mesaj",
                    body="Bir yeni Mesaj",
                ),
                token=device
            )
            response = messaging.send(message)
            return response
        except Exception as e:
            print(e)

fcm_helper = FCMHelper()