# -*- coding: utf-8 -*-
import pymongo

# TODO: Use config
MONGO_URI = 'mongodb://localhost:27017'
DATABASE = 'proxy_crawler_demo'
COLLECTION = 'user'
ADMIN_USER = 'jferroal'
ADMIN_PWD = '123123'


def init_user():
    _db_collection = pymongo.MongoClient(MONGO_URI)[DATABASE][COLLECTION]
    user = _db_collection.find_one({'username': ADMIN_USER})
    print(user)
    if user is None:
        print(user)
        _db_collection.insert({'username': ADMIN_USER, 'password': ADMIN_PWD})


init_user()