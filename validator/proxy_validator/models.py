# -*- coding: utf-8 -*-

from public.models import ProxyModel
from public.database import Database
from public.decorators import singleton

MONGO_URI = 'localhost:27017'
MONGO_DATABASE = 'proxy_crawler_demo'


class ValidatorDatabase(Database):
    def __init__(self, *args, **kwargs):
        super(ValidatorDatabase, self).__init__(*args, **kwargs)


ValidatorDatabase.uri = MONGO_URI
ValidatorDatabase.db_name = MONGO_DATABASE


class Proxy(ProxyModel):
    def __init__(self, doc):
        super(Proxy, self).__init__(doc)
        self.invalid = False

    def __getitem__(self, key):
        try:
            result = super().__getitem__(key)
        except KeyError:
            if key == 'invalid':
                return self.invalid
            raise KeyError
        else:
            return result

    def __setitem__(self, key, value):
        try:
            super().__setitem__(key, value)
        except KeyError:
            if key == 'invalid':
                self.invalid = value
            else:
                raise KeyError


@singleton
class ProxyToUpdatePool(object):
    db_collection = None

    def __init__(self):
        self.to_remove = list()
        self.to_update = list()

    def handle_pool(self):
        # FIXME: update size with configuration
        if len(self.to_remove) >= 1:
            self.db_collection.remove({'_id': {'$in': list(map(lambda _p: _p.id, self.to_remove))}})
            self.to_remove = list()
        # FIXME: update size with configuration
        if len(self.to_update) >= 1:
            for p in self.to_update:
                self.db_collection.update({'_id': p.id}, p.to_json())
            self.to_update = list()

    def add_to_pool(self, proxy):
        if proxy.invalid:
            self.to_remove.append(proxy)
        else:
            self.to_update.append(proxy)


def bind_models():
    ValidatorDatabase('proxy_list').bind_to_model(Proxy)
    ValidatorDatabase('proxy_list').bind_to_model(ProxyToUpdatePool)
