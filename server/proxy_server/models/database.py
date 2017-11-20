# -*- coding:utf-8 -*-
import pymongo

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'proxy_crawler_demo'


class Database(object):
    uri = MONGO_URI
    client = None
    db_name = MONGO_DATABASE
    database = None

    def __init__(self, collection_name):
        self.collection = None
        self.collection_name = collection_name

    def bind_to_model(self, model):
        if not Database.database:
            Database.connect()
        self.collection = Database.database[self.collection_name]
        model.db_collection = self

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

    @staticmethod
    def connect():
        Database.client = pymongo.MongoClient(Database.uri)
        Database.database = Database.client[Database.db_name]


def bind_models():
    from proxy_server.models.proxy import Proxy
    Database('proxy').bind_to_model(Proxy)
    from proxy_server.models.user import User
    Database('user').bind_to_model(User)
