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
