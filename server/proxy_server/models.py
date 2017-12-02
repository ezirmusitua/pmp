# -*- coding: utf-8 -*-
import hashlib
import uuid
import time
from public.models import ProxyModel
from public.database import Database
from proxy_server import config


class ServerDatabase(Database):
    def __init__(self, *args, **kwargs):
        super(ServerDatabase, self).__init__(*args, **kwargs)


ServerDatabase.uri = config['DB_URI']
ServerDatabase.db_name = config['DB_NAME']


class Proxy(ProxyModel):
    db_collection = None

    def __init__(self, proxy_doc):
        super(Proxy, self).__init__(proxy_doc)

    @staticmethod
    def search(_type=None, connection=None, anonymity=None, size=20):
        query = dict()
        if _type and len(_type):
            query['proxy_type'] = {'$in': _type}
        if connection and len(connection):
            query['connection'] = {'$in': connection}
        if anonymity and len(anonymity):
            query['anonymity'] = {'$in': anonymity}
        return list(map(lambda p: p.proxy_str(), Proxy.db_collection.list(query, limit=size)))


class Token(object):
    db_collection = None

    def __init__(self, token_doc):
        self.id = token_doc['_id']
        self.salt = token_doc['salt']
        self.token = token_doc['token']
        self.create_at = token_doc['create_at']

    @staticmethod
    def hash(key, salt):
        return hashlib.sha512((key + salt).encode()).hexdigest()

    @staticmethod
    def find(key):
        token = None
        for t in Token.db_collection.list({}):
            if t['token'] == Token.hash(key, t['salt']):
                token = Token(t)
        return token

    @staticmethod
    def validate(key):
        if Token.find(key):
            return True
        return False

    @staticmethod
    def generate(key):
        salt = uuid.uuid4().hex
        create_at = time.time()
        token = Token.hash(key, salt)
        Token.db_collection.insert({
            'salt': salt,
            'token': token,
            'create_at': create_at
        })

    @staticmethod
    def delete(key):
        token = Token.find(key)
        Token.db_collection.remove({'_id': token.id})


def bind_models():
    ServerDatabase(config['PROXY_MODEL_NAME']).bind_to_model(Proxy)
    ServerDatabase(config['TOKEN_MODEL_NAME']).bind_to_model(Token)
