import os
from datetime import timedelta
# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    NAME="development"
    DEBUG = True
    MONGO_URI = "mongodb+srv://kapil:k6K6EG47smjJuB0y@earnit-dev.ezmxz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    JWT_SECRET_KEY = 'dev'
    JWT_ACCESS_TOKEN_EXPIRES = False
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'contact@lemmebuy.in'
    MAIL_PASSWORD = 'sosabarapi'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class TestingConfig(Config):
    NAME="testing"
    DEBUG = True
    TESTING = True
    MONGO_URI = "mongodb+srv://kapil:g95oPBraubAmBECj@cluster0.inxon.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    JWT_SECRET_KEY = 'dev'


class ProductionConfig(Config):
    NAME="production"
    DEBUG = False
    MONGO_URI = "mongodb+srv://kapil:YUH5Y4GtauXx00R6@cluster0.iuipl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    JWT_SECRET_KEY = 'prddevsecret'
    JWT_ACCESS_TOKEN_EXPIRES = False
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'contact@lemmebuy.in'
    MAIL_PASSWORD = 'sosabarapi'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prd=ProductionConfig
)

key = Config.SECRET_KEY


