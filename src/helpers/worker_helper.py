# -*- coding: utf-8 -*-
from celery import Celery
from kombu.serialization import register as worker_register

from src.utils.json_util import json_dumps, json_loads
"""
application/x-cje json_util dosyasındaki Custom json encoder anlamına geliyor. 
Celery nin serialize edemediği object_id, datetime gibi objeleri serialize etmek için
worker_register methodu ile celerye register ediyor

"""
worker_register('cje', json_dumps, json_loads,
                content_type='application/x-cje',
                content_encoding='utf-8')

worker = Celery('worker', backend="config.get('CELERY_RESULT_BACKEND')", broker="config.get('CELERY_BROKER_URL')")
