import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DISK_TOKEN = os.getenv('DISK_TOKEN', None)
    YADISK_API_HOST = 'https://cloud-api.yandex.net/'
    YADISK_API_VERSION = 'v1'
    MAX_LEN_AUTO = int(os.getenv('MAX_LEN_AUTO', 6))
