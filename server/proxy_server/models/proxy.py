# -*- coding:utf-8 -*-


class Proxy(object):
    db_collection = None

    def __init__(self, proxy_doc):
        self.id = proxy_doc.get('_id', '')
        self.ip_address = proxy_doc.get('ip_address', 'unknown')
        self.port = proxy_doc.get('port', 12345)
        self.proxy_type = proxy_doc.get('proxy_type', ['unknown'])
        self.anonymity = proxy_doc.get('anonymity', 'unknown')
        self.location = proxy_doc.get('location', 'unknown, unknown')
        self.connection = proxy_doc.get('connection', [])
        self.last_check_at = proxy_doc.get('last_check_at', 0)

    def to_csv(self, full=False):
        return self.ip_address + ':' + str(self.port) if full else self.ip_address + ':' + str(
            self.port) + '|'.join(
            self.proxy_type) + ',' + self.anonymity + ',' + self.location + ',' + '|'.join(self.connection) + str(
            self.last_check_at)

    @staticmethod
    def list_all():
        return {'items': map(Proxy, Proxy.db_collection.find())}

    @staticmethod
    def page(page_index=0, page_size=10, _filter=None, projection=None, _sort=None):
        sort = _sort if _sort is not None else [('_id', -1)]
        count = Proxy.db_collection.count(filter=_filter)
        return {
            'count': count,
            'items': map(Proxy,
                         Proxy.db_collection.find(filter=_filter, projection=projection)
                         .sort(sort)
                         .skip(page_index * page_size)
                         .limit(page_size))
        }
