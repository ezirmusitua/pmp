# -*- coding: utf8 -*-
import time

from proxy_validator.utils import singleton
from proxy_validator.database import Database


class ProxyModel(object):
    def __init__(self, doc_from_db=None):
        doc = doc_from_db if doc_from_db is not None else {}
        self.id = doc['_id']
        self.port = doc['port']
        self.ip_address = doc['ip_address']
        self.proxy_type = doc.get('proxy_type', ['unknown'])
        self.connection = doc.get('connection', list())
        self.anonymity = doc.get('anonymity', ['unknown'])
        self.location = doc.get('location', 'unknown, unknown')
        self.last_check_at = time.time() * 1000  # convert to ms
        self.invalid = False

    def proxy_str(self):
        return self.ip_address + ':' + str(self.port)

    def to_json(self):
        return {
            'anonymity': self.anonymity,
            'ip_address': self.ip_address,
            'port': self.port,
            'last_check_at': self.last_check_at,
            'location': self.location,
            'connection': self.connection,
            'proxy_type': self.proxy_type
        }

    def __setitem__(self, key, value):
        if key == 'anonymity':
            self.anonymity = value
        if key == 'ip_address':
            self.ip_address = value
        if key == 'port':
            self.port = value
        if key == 'last_check_at':
            self.last_check_at = value
        if key == 'location':
            self.location = value
        if key == 'connection':
            self.connection = value
        if key == 'proxy_type':
            self.proxy_type = value

    def __unicode__(self):
        return self.proxy_str()

    def __str__(self):
        return self.proxy_str()

    def __repr__(self):
        return self.proxy_str()


@singleton
class ProxyToUpdatePool(object):
    def __init__(self):
        self.db = Database()
        self.to_remove = list()
        self.to_update = list()

    def handle_pool(self):
        if len(self.to_remove) >= 10:
            self.db.remove({'_id': {'$in': list(map(lambda _p: _p.id, self.to_remove))}})
            self.to_remove = list()
        if len(self.to_update) >= 10:
            for p in self.to_update:
                self.db.update({'_id': p.id}, p)
            self.to_update = list()

    def add_to_pool(self, proxy):
        if proxy.invalid:
            self.to_remove.append(proxy)
        else:
            self.to_update.append(proxy)
