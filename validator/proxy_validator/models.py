# -*- coding: utf-8 -*-
from public.models import ProxyModel
from public.database import Database
from public.decorators import singleton

from proxy_validator import config


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

    def save_or_remove(self):
        if self.invalid:
            self.db_collection.remove({'_id': self.id})
        else:
            print(self.to_json())
            self.db_collection.update({'_id': self.id}, self.to_json())

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


def bind_models():
    ValidatorDatabase(config['PROXY_MODEL_NAME']).bind_to_model(Proxy)
