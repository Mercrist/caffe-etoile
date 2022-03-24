import os
class Config(object):
    SECRET_KEY = os.urandom(16).hex()
    MONGO_DBNAME = 'mainframe'
    MONGO_URI = 'url'