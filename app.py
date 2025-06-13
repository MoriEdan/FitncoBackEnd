# -*- coding: utf-8 -*-
import datetime
import logging
import redis
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.commons.handlers import response_handlers_config, exception_handlers_config, \
    json_schema_handlers_config
from src.helpers.cache_helper import global_cache
from src.helpers.sql_helper import db
from src.routes import routes
from src.utils.config_util import config
from src.utils.dict_util import get_value
from flask import Flask, request
from os import environ, path
from dotenv import load_dotenv
from flask_migrate import Migrate
#from flask_seeder import FlaskSeeder
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from flask_mail import Mail

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
sentry_sdk.init(
    dsn=environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration(), SqlalchemyIntegration(), RedisIntegration()],
    environment=environ.get('SENTRY_ENV', 'local'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__, static_folder=None, template_folder="src/templates/")
CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG
app.config.from_object('config.' + environ.get('DEFAULT_CONFIG_TYPE'))
app.config['CORS_HEADERS'] = 'Content-Type'
config.init_app(config=app.config)
# socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
jwt_redis_blocklist = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],
                                        db=app.config['REDIS_DB'], password=app.config['REDIS_PASSWORD'],
                                        decode_responses=True)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(f'blocked:{jti}')
    return token_in_redis is not None

@app.errorhandler(Exception)
def all_exception_handler(error):
    print(str(error))
    try:
        db.session.rollback()
        db.session.remove()
    except:
        pass

# jwt_handlers_config(jwt)
api = Api(app, prefix='/api')
response_handlers_config(app)
exception_handlers_config(app)
json_schema_handlers_config(app)
routes(api)
# injects_config(app)
# FlaskInjector(app=app)
db.init_app(app)
mail = Mail(app)
migrate = Migrate()
migrate.init_app(app, db)

#seeder = FlaskSeeder()
#seeder.init_app(app, db)


@app.cli.command("extension")
def extension():
    with db.engine.begin() as con:
        con.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        print('UUID extension create successfully')


app.app_context().push()
global_cache.init_app(app=app, config=app.config)
# worker.config_from_object(app.config)

if get_value("LOG_STATUS", app.config, "TERMINAL") == "FILE":
    logging.basicConfig(
        filename=get_value("LOG_FILE_PATH", app.config, "logs/transaction_{0}.log").format(
            datetime.datetime.today().date()),
        level=get_value("LOG_LEVEL", app.config, "DEBUG"),
        format=get_value("LOG_FORMAT", app.config),
        datefmt=get_value("LOG_FILE_PATH", app.config)
    )

if __name__ == "__main__":
    app.run(
        host=config.get("HOST"),
        port=config.get("PORT"),
        debug=config.get("DEBUG")
    )
