# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
sys.path.append('../..')

from public.models import ProxyModel
from public.database import Database
from public.decorators import singleton
from public.config import Config

config = Config('config.json')


class ValidatorDatabase(Database):
    def __init__(self, *args, **kwargs):
        super(ValidatorDatabase, self).__init__(*args, **kwargs)


ValidatorDatabase.uri = config['DB_URI']
ValidatorDatabase.db_name = config['DB_NAME']


class Proxy(ProxyModel):
    db_collection = None

    def __init__(self, doc):
        super(Proxy, self).__init__(doc)
        self.invalid = False

    @classmethod
    def list(cls, *args, **kwargs):
        return cls.db_collection.list(*args, **kwargs)

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
        if len(self.to_remove) >= config['BATCH_SIZE']:
            self.db_collection.remove({'_id': {'$in': list(map(lambda _p: _p.id, self.to_remove))}})
            self.to_remove = list()
        if len(self.to_update) >= config['BATCH_SIZE']:
            for p in self.to_update:
                self.db_collection.update({'_id': p.id}, p.to_json())
            self.to_update = list()

    def add_to_pool(self, proxy):
        if proxy.invalid:
            self.to_remove.append(proxy)
        else:
            self.to_update.append(proxy)

    def flush(self):
        self.db_collection.remove({'_id': {'$in': list(map(lambda _p: _p.id, self.to_remove))}})
        for p in self.to_update:
            self.db_collection.update({'_id': p.id}, p.to_json())


def bind_models():
    ValidatorDatabase(config['PROXY_MODEL_NAME']).bind_to_model(Proxy)
    ValidatorDatabase(config['PROXY_MODEL_NAME']).bind_to_model(ProxyToUpdatePool)
