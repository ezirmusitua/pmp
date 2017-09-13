# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import time
import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class Proxy(scrapy.Item):
    ip_address = scrapy.Field()
    port = scrapy.Field()
    type = scrapy.Field()
    location = scrapy.Field()
    quality = scrapy.Field()
    # Up time in proxy db
    # Speed in cn proxy
    # NAI in premium proxy
    last_check_at = scrapy.Field()
    anonymity = scrapy.Field()
    pass


def strip(in_str):
    return in_str.strip()


def to_int(in_str):
    return int(in_str)


def default_http(in_str):
    return in_str.strip() if in_str is not None else 'HTTP'


def speed_to_quality(in_str):
    return in_str[:-1]


def time_str_to_stamp(in_str):
    # Example: 2017-09-12 14:26:59
    return time.mktime(datetime.datetime.strptime(in_str, "%Y-%m-%d %H:%M:%S").timetuple())


def default_anonymity(in_str):
    return in_str.strip() if in_str else 'unknown'


class CNProxyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    # ip_address_in = MapCompose(TakeFirst, strip)
    # port_in = MapCompose(TakeFirst, to_int)
    # type_in = MapCompose(TakeFirst,  default_http)
    # location_in = MapCompose(TakeFirst, strip)
    # quality_in = MapCompose(TakeFirst, speed_to_quality)
    # last_check_at = MapCompose(TakeFirst, time_str_to_stamp)
    # anonymity = MapCompose(TakeFirst, default_anonymity)


class PremProxyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ProxyDBItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
