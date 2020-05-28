import logging

from flask import Flask
from flask.logging import default_handler

from app.api import api_bp
from app.error import handle_exception
from app.model import db
from app.util import multilog
from app.util.middleware import log_request_params, log_response
from config import config_map


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    register_extension(app)
    register_logger(app)
    register_middlewares(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_pysnooper_tracer(app)

    return app


def register_extension(app: Flask):
    db.init_app(app)


def register_blueprints(app: Flask):
    @app.route('/', endpoint='ping_pong')
    def ping_pong():
        return "I'm still alive.\n", 200

    app.register_blueprint(api_bp, url_prefix='/api')


def register_error_handlers(app: Flask):
    app.register_error_handler(Exception, handle_exception)


def register_middlewares(app: Flask):
    app.before_request(log_request_params)
    app.after_request(log_response)


def register_logger(app: Flask):
    # 写入日志文件
    app.logger.removeHandler(default_handler)
    handler = multilog.MyLoggerHandler('flask', 'data', encoding='UTF-8', when='D')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    # 写入控制台
    ch = logging.StreamHandler()
    ch.setFormatter(logging_format)
    ch.setLevel(logging.DEBUG)
    app.logger.addHandler(ch)
    app.logger.setLevel(logging.DEBUG)


def register_pysnooper_tracer(app: Flask):
    if app.config.get('PYSNOOPER_TRACE'):
        try:
            import pysnooper
            for func_name, func in app.view_functions.items():
                app.view_functions[func_name] = pysnooper.snoop(depth=2)(func)
        except ImportError:
            pass
