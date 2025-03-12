import os

basedir = os.path.abspath(os.path.dirname(__file__))
sqliteDB = os.path.join(basedir, '../database')

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = None
    UPLOAD_FOLDER = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'drowssap'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(sqliteDB, 'bloglite.db')
    UPLOAD_FOLDER = './static/images'
