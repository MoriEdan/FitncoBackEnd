# -*- coding: utf-8 -*-
"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    LOG_FILE_PATH = "logs/transaction_{0}.log"
    LOG_DATE_FORMAT = "%d/%m/%Y %I:%M:%S %p"
    LOG_FORMAT = '%(asctime)s\t%(levelname)s\t%(levelno)s\t%(filename)s\t%(funcName)s\t%(lineno)d\t%(module)s\t' \
                 '%(pathname)s\t%(process)d\t%(processName)s\t%(thread)d\t%(threadName)s\t%(name)s\t%(message)s'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_QUERY_STRING_NAME = "token"
    JWT_TOKEN_LOCATION = ['query_string', 'headers']
    CACHE_KEY_PREFIX = ""
    API_EXPIRE_TOKEN = False  # Süresiz yapmak için false vermek gerekiyor
    PROPAGATE_EXCEPTIONS = True
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_ACCEPT_CONTENT = ['cje', 'application/json']
    BROKER_CONNECTION_TIMEOUT = 10
    CELERY_TASK_SERIALIZER = 'cje'
    CELERY_RESULT_SERIALIZER = 'cje'
    TIMEZONE = 'Europe/Istanbul'
    CELERYD_HIJACK_ROOT_LOGGER = False
    SQLALCHEMY_PRE_PING = True
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    LOGGING = {
        'handlers': {
            'celery_sentry_handler': {
                'level': 'ERROR',
                'class': 'core.log.handlers.CelerySentryHandler'
            }
        },
        'loggers': {
            'celery': {
                'handlers': ['celery_sentry_handler'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
    CACHE_DEFAULT_TIMEOUT = environ.get('CACHE_DEFAULT_TIMEOUT')
    CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')
    REDIS_HOST = environ.get('REDIS_HOST')
    REDIS_PORT = environ.get('REDIS_PORT')
    REDIS_PASSWORD = environ.get('REDIS_PASSWORD')
    REDIS_DB = environ.get('REDIS_DB')
    CACHE_TYPE = environ.get('CACHE_TYPE')
    SENTRY_DSN = environ.get('SENTRY_DSN')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    LOG_LEVEL = environ.get('LOG_LEVEL')
    LOG_STATUS = environ.get('LOG_STATUS')
    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
    API_URL = environ.get('API_URL')
    API_EXPIRE_TOKEN = environ.get('API_EXPIRE_TOKEN') if environ.get('API_EXPIRE_TOKEN') else False
    ALLOWED_EXTENSIONS = set(environ.get('ALLOWED_EXTENSIONS').split(','))
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
    APPLICATION_ROOT = environ.get('APPLICATION_ROOT')
    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = environ.get('AWS_DEFAULT_REGION')
    AWS_BUCKET = environ.get('AWS_BUCKET')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT'))
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_FROM_NAME = environ.get('MAIL_FROM_NAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True if environ.get('MAIL_USE_TLS') == 'True' else False
    MAIL_USE_SSL = True if environ.get('MAIL_USE_SSL') == 'True' else False
    MAIL_SUPPRESS_SEND = True if environ.get('MAIL_SUPPRESS_SEND') == 'True' else False
    MAIL_DEBUG = environ.get('MAIL_DEBUG')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    FCM_KEY = environ.get('FCM_KEY')


class TestingConfig(Config):
    pass


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
    CELERY_ALWAYS_EAGER = True
    CACHE_DEFAULT_TIMEOUT = environ.get('CACHE_DEFAULT_TIMEOUT')
    CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')
    REDIS_HOST = environ.get('REDIS_HOST')
    REDIS_PORT = environ.get('REDIS_PORT')
    REDIS_PASSWORD = environ.get('REDIS_PASSWORD')
    REDIS_DB = environ.get('REDIS_DB')
    CACHE_TYPE = environ.get('CACHE_TYPE')
    SENTRY_DSN = environ.get('SENTRY_DSN')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    LOG_LEVEL = environ.get('LOG_LEVEL')
    LOG_STATUS = environ.get('LOG_STATUS')
    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
    API_URL = environ.get('API_URL')
    API_EXPIRE_TOKEN = environ.get('API_EXPIRE_TOKEN') if environ.get('API_EXPIRE_TOKEN') else False
    ALLOWED_EXTENSIONS = set(environ.get('ALLOWED_EXTENSIONS').split(','))
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
    APPLICATION_ROOT = environ.get('APPLICATION_ROOT')
    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION = environ.get('AWS_DEFAULT_REGION')
    AWS_BUCKET = environ.get('AWS_BUCKET')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT'))
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_FROM_NAME = environ.get('MAIL_FROM_NAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True if environ.get('MAIL_USE_TLS') == 'True' else False
    MAIL_USE_SSL = True if environ.get('MAIL_USE_SSL') == 'True' else False
    MAIL_SUPPRESS_SEND = True if environ.get('MAIL_SUPPRESS_SEND') == 'True' else False
    MAIL_DEBUG = environ.get('MAIL_DEBUG')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    FCM_KEY = environ.get('FCM_KEY')


