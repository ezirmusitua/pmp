# -*- coding: utf-8 -*-
import pprint
import pymongo

from utils import singleton

MONGO_URI = 'localhost:27017'
MONGO_DATABASE = 'proxy_crawler_demo'
MONGO_COLLECTION = 'proxy_list'


@singleton
class Database(object):
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://' + MONGO_URI)
        self.database = self.client[MONGO_DATABASE]
        self.collection = self.database[MONGO_COLLECTION]

    def list(self, query=None, batch_size=20):
        for p in self.collection.find({} if query is None else query).batch_size(batch_size):
            yield p

    def update(self, query=None, doc=None):
        if doc is None or query is None:
            raise Exception('Document is invalid. ')
        self.collection.update(query, {'$set': doc})

    def remove(self, query=None):
        if query is None:
            raise Exception('query not found. ')
        self.collection.remove(query)

    def find_one_and_update(self, query=None, doc=None):
        if query is None or doc is None:
            raise Exception('Parameters missed. ')
        origin = self.collection.find_one(query)
        if origin is None:
            self.collection.insert(doc)
        else:
            self.collection.update(query, {'$set': doc})


if __name__ == '__main__':
    db = Database()
    for proxy in db.list():
        pprint.pprint(proxy)
