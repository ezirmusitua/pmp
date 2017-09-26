# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from pymongo import MongoClient
from scrapy import signals


class ProxyCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    collection_name = 'proxy_list'

    def __init__(self, mongo_uri, mongo_db):
        self.collection = MongoClient(mongo_uri)[mongo_db][ProxyMiddleware.collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_db=crawler.settings.get('MONGO_DATABASE'), mongo_uri=crawler.settings.get('MONGO_URI'))

    def process_request(self, request, spider):
        query = {'available_sites': '', 'type': {'$in': ['http', 'https']}}
        if spider.name == 'cnproxy':
            query['available_sites'] = 'http://cn-proxy.com'
        if spider.name == 'proxydb':
            query['available_sites'] = 'http://proxy-db.net'
        proxy = self.collection.find_one(query)
        if proxy is not None:
            request.meta['proxy'] = proxy['type'] + '://' + proxy['ip_address'] + ':' + str(proxy['port'])
