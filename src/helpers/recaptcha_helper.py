# -*- coding: utf-8 -*-
import json
import ssl
from urllib.request import urlopen

from src.helpers.base_helper import BaseHelper


class RecaptchaHelper(BaseHelper):
    
    def __init__(self, recaptcha_public_key: str, recaptcha_private_key: str):
        super().__init__()
        self._recaptcha_public_key = recaptcha_public_key
        self._recaptcha_private_key = recaptcha_private_key

    def validate(self, key):
        url = 'https://www.google.com/recaptcha/api/siteverify?'
        url = url + 'secret=' + self._recaptcha_private_key
        url = url + '&response=' + str(key)
        context = ssl._create_unverified_context()

        json_obj = json.loads(urlopen(url, context=context).read())
        if json_obj['success']:
            return True
        else:
            return False
