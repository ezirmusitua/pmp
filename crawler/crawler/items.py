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


class TimeStrConverter(object):
    def __init__(self, format='%Y-%m-%d %H:%M:%S'):
        self.format = format

    def __call__(self, values):
        def strptime(ts):
            tt = datetime.datetime.strptime(ts, self.format).timetuple()
            if tt.tm_year < 2017:
                tmp = list(tt)
                tmp[0] = 2017
                tt = time.struct_time(tmp)
            return tt

        def to_timestamp(ts): return time.mktime(strptime(ts))

        return list(map(to_timestamp, values))


class StrToIntConverter(object):
    def __call__(self, values):
        return list(map(lambda x: int(x), values))


class Proxy(scrapy.Item):
    ip_address = scrapy.Field()
    port = scrapy.Field()
    type = scrapy.Field()


class CNProxyItemLoader(ItemLoader):
    default_input_processor = StrCleaner()
    default_output_processor = TakeFirst()
    port_in = StrToIntConverter()
    last_check_at_in = TimeStrConverter()


class PremProxyItemLoader(ItemLoader):
    default_input_processor = StrCleaner()
    default_output_processor = TakeFirst()
    port_in = StrToIntConverter()
    last_check_at_in = TimeStrConverter('%b-%d, %H:%M')


class ProxyDBItemLoader(ItemLoader):
    default_input_processor = StrCleaner()
    default_output_processor = TakeFirst()
    port_in = Identity()
    last_check_at_in = TimeStrConverter()
