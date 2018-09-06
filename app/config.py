import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test'
    USERNAME = 'BITSLAB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False;
    SECRET_KEY = 'V\x827\\k,\xc1W\x91r\x1a\xcdw\x03\x83\xcd'
    PASSWORD = '123'

class ProductionConfig(Config):
    # PASSWORD = 'bitslabpersuasion'
    PASSWORD = 'bitslabpersuasion'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
