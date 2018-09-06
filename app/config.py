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
    SQLALCHEMY_DATABASE_URI = 'postgres://egdwpxluzvtmbi:b8b7e7d969d088edadeea313de23ba35f24251463b3f6f968d6d623a93f352ba@ec2-54-227-244-12.compute-1.amazonaws.com:5432/dagcpfn26ejbh4'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
