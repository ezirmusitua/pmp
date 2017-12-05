# -*- coding: utf-8 -*-
import time
import pymongo


class Database(object):
    uri = None
    client = None
    db_name = None
    database = None
    A_ORDER = pymongo.ASCENDING
    D_ORDER = pymongo.DESCENDING

    def connect(self):
        retry_times = 0
        while True:
            Database.client = pymongo.MongoClient(self.uri)
            Database.database = Database.client[self.db_name]
            debug_collection = Database.database['demo']
            try:
                debug_collection.find({}).next()
            except StopIteration:
                break
            except Exception as e:
                print(e)
                if retry_times >= 10:
                    raise e
                else:
                    time.sleep(60)
                    retry_times += 1

    def __init__(self, collection_name):
        self.collection = None
        self.collection_name = collection_name

    def bind_to_model(self, model):
        if not self.database:
            self.connect()
        self.collection = self.database[self.collection_name]
        model.db_collection = self

    def count(self, query=None):
        return self.collection.count({} if query is None else query)

    def list(self, query=None, sort=None, skip=None, limit=None, batch_size=20):
        cursor = self.collection.find({} if query is None else query)
        if sort and type(sort) is 'list':
            cursor = cursor.sort(sort)
        if skip and type(skip) is 'int':
            cursor = cursor.skip(skip)
        if limit and type(limit) is 'int':
            cursor = cursor.limit(limit)
        for p in cursor.batch_size(batch_size):
            yield p

    def update(self, query=None, doc=None, upsert=False):
        if doc is None or query is None:
            raise Exception('Document is invalid. ')
        self.collection.update(query, doc, upsert=upsert)

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
            self.collection.update(query, doc)


if __name__ == '__main__':
    Database.uri = 'mongodb://abc:abc@dev.liaoyuan.io:27017/liaoyuan'
    Database.db_name = 'liaoyuan'
    print(1)
    db = Database('Profile')
    db.connect()
    db.collection = db.database['Profile']
    for i in db.list():
        print(i)
