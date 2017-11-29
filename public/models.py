# -*- coding: utf8 -*-
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
        self.last_check_at = doc.get('last_check_at', -1)
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

    def __getitem__(self, key):
        if key == 'anonymity':
            return self.anonymity
        if key == 'ip_address':
            return self.ip_address
        if key == 'port':
            return self.port
        if key == 'last_check_at':
            return self.last_check_at
        if key == 'location':
            return self.location
        if key == 'connection':
            return self.connection
        if key == 'proxy_type':
            return self.proxy_type
        raise KeyError

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
        raise KeyError

    def __unicode__(self):
        return self.proxy_str()

    def __str__(self):
        return self.proxy_str()

    def __repr__(self):
        return self.proxy_str()
