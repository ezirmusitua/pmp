# -*- coding: utf-8 -*-
import pymongo
from proxy_validator.utils import singleton

MONGO_URI = 'localhost:27017'
MONGO_DATABASE = 'proxy_crawler_demo'
MONGO_COLLECTION = 'proxy_list'


@singleton
class Database(object):
    def __init__(self, uri=MONGO_URI, database=MONGO_DATABASE, collection=MONGO_COLLECTION):
        self._uri = uri
        self.database_name = database
        self.collection_name = collection
        self.client = self.database = self.collection = None

    def connect(self, uri=None, database_name=None, collection_name=None):
        if uri:
            self._uri = uri if uri.startswith('mongodb://') else 'mongodb://' + uri
        self.client = pymongo.MongoClient(self._uri)
        self.database_name = database_name if database_name else self.database_name
        self.database = self.client[self.database_name]
        self.collection_name = collection_name if collection_name else self.collection_name
        self.collection = self.database[self.collection_name]

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
