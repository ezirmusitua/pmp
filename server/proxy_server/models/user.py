# -*- coding:utf-8 -*-
import pymongo

# TODO: Use config
MONGO_URI = 'mongodb://localhost:27017'
DATABASE = 'proxy_crawler_demo'
COLLECTION = 'user'


class User(object):
    _db_collection = pymongo.MongoClient(MONGO_URI)[DATABASE][COLLECTION]

    def __init__(self, user_doc):
        self.id = user_doc.get('_id', '')
        self.username = user_doc.get('username', '')
        self.password = user_doc.get('password', '')

    @classmethod
    def validate(cls, username, password):
        user = cls._db_collection.find_one({'username': username, 'password': password})
        return False if user is None else True
