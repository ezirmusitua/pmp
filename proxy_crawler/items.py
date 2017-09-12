# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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
