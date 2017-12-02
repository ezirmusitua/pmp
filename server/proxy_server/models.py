# -*- coding: utf-8 -*-
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
            query['type'] = {'$in': _type}
        if connection and len(connection):
            query['connection'] = {'$in': connection}
        if anonymity and len(anonymity):
            query['anonymity'] = {'$in': anonymity}
        return list(map(lambda p: p.proxy_str(), Proxy.db_collection.list(query, limit=size)))


def bind_models():
    ServerDatabase(config['PROXY_MODEL_NAME']).bind_to_model(Proxy)
