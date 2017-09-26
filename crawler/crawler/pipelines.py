# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import pymongo
import requests
from scrapy.exceptions import DropItem


class RemoveDuplicatedPipeline(object):
    def __init__(self):
        self.ip_port_seen = set()

    def process_item(self, item, spider):
        ip_port = item['ip_address'] + ':' + str(item['port'])
        ip_port_hash = hashlib.md5(ip_port.encode()).hexdigest()
        if ip_port_hash in self.ip_port_seen:
            raise DropItem('Duplicated item found: %s' % item)
        else:
            self.ip_port_seen.add(ip_port_hash)
        return item


class ValidatePipeline(object):
    def __init__(self, ua):
        self.ua = ua

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ua=crawler.settings.get('User_Agent'))

    def process_item(self, item, spider):
        proxy_str = item['type'].lower() + '://' + item['ip_address'] + ':' + str(item['port'])
        proxies = {
            'http': proxy_str,
            'https': proxy_str
        }
        should_drop = False
        try:
            requests.get('https://httpbin.org', timeout=1, proxies=proxies, headers={'User-Agent': self.ua})
        except Exception as e:
            should_drop = True
        if should_drop:
            raise DropItem('proxy %s not usable' % proxy_str)
        else:
            return item


class ExportToMongoPipeline(object):
    collection_name = 'proxy_list'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'demo')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({
            'ip_address': item['ip_address'],
            'port': item['port']
        }, {'$set': dict(item)}, upsert=True)
        return item
