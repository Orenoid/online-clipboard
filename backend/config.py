import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = '0.0.0.0'
    PORT = '5000'


class ProductionConfig(Config):
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DB_URL') \
                              or "sqlite:///" + os.path.join(basedir, 'data', 'prod.sqlite')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URL') or 'sqlite:///' + os.path.join(basedir, 'data', 'dev.sqlite')


config_map = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}
