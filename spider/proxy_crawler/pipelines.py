# -*- coding: utf-8 -*-

import hashlib

from scrapy.exceptions import DropItem


class RemoveDuplicatedPipeline(object):
    def __init__(self):
        self.ip_port_seen = set()

    def process_item(self, item, spider):
        ip_port = item['ip_address'] + ':' + str(item['port'])
        ip_port_hash = hashlib.md5(ip_port.encode()).hexdigest()
        if ip_port_hash in self.ip_port_seen:
            raise DropItem('Duplicated item found: %s' % ip_port)
        else:
            self.ip_port_seen.add(ip_port_hash)
        return item


class ExportToMongoPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        from .models import Proxy
        Proxy.save(item)
        return item
