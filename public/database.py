# -*- coding: utf-8 -*-
import pymongo


class Database(object):
    uri = None
    client = None
    db_name = None
    database = None
    A_ORDER = pymongo.ASCENDING
    D_ORDER = pymongo.DESCENDING

    def connect(self):
        Database.client = pymongo.MongoClient(self.uri, connect=False)
        Database.database = Database.client[self.db_name]

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
