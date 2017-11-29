# -*- coding: utf-8 -*-
from public.models import ProxyModel
from public.database import Database, update_database_uri

MONGO_URI = 'localhost:27017'
MONGO_DATABASE = 'proxy_crawler_demo'


class ServerDatabase(Database):
    def __init__(self, *args, **kwargs):
        super(ServerDatabase, self).__init__(*args, **kwargs)


update_database_uri(ServerDatabase, MONGO_URI, MONGO_DATABASE)


class Proxy(ProxyModel):
    def __init__(self, proxy_doc):
        super(Proxy, self).__init__(proxy_doc)

    def to_csv(self, all_fields=False):
        short = self.ip_address + ':' + str(self.port)
        return short if not all_fields else short + ',(' + ','.join(
            self.proxy_type) + '),(' + ','.join(self.anonymity) + '),(' + self.location + '),(' + ','.join(
            self.connection) + ')'

    @staticmethod
    def list_all():
        res = Proxy.db_collection.find()
        return {'items': map(lambda p: Proxy(p), res)}

    @staticmethod
    def page(page_index=0, page_size=10, _filter=None, projection=None, _sort=None):
        sort = _sort if _sort is not None else [('_id', -1)]
        count = Proxy.db_collection.count(filter=_filter)
        return {
            'count': count,
            'items': map(
                lambda p: Proxy(p),
                Proxy.db_collection.find(filter=_filter, projection=projection).sort(sort).skip(
                    page_index * page_size).limit(page_size)
            )
        }


class User(object):
    db_collection = None

    def __init__(self, user_doc):
        self.id = user_doc['_id']
        self.username = user_doc.get('username', '')
        self.password = user_doc.get('password', '')

    @staticmethod
    def validate(username, password):
        user = User.db_collection.find_one({'username': username, 'password': password})
        return False if user is None else True


def bind_models():
    ServerDatabase('user').bind_to_model(User)
    ServerDatabase('proxy_list').bind_to_model(Proxy)
