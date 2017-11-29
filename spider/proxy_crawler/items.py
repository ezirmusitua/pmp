# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import time
import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


class StrCleaner(object):
    def __call__(self, values):
        return list(map(lambda x: str.strip(x), values))


class Proxy(scrapy.Item):
    ip_address = scrapy.Field()
    port = scrapy.Field()
    proxy_type = scrapy.Field()


class ProxyItemLoader(ItemLoader):
    default_input_processor = StrCleaner()
    default_output_processor = TakeFirst()
    proxy_type_in = StrCleaner()
    proxy_type_out = Identity()
