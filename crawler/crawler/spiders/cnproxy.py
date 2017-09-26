# -*- coding: utf-8 -*-
import scrapy
from crawler.helper import get_list_item_safely
from crawler.items import Proxy, CNProxyItemLoader

CNPROXY_TYPE_TO_ANONYMITY = {
    '透明': 'bad1',
    '普通匿名': 'elite',
    '高度匿名': 'anonymous'
}


class CNProxySpider(scrapy.Spider):
    name = "cnproxy"
    start_urls = [
        'http://cn-proxy.com',
        'http://cn-proxy.com/archives/218',
    ]

    def parse(self, response):
        proxies = []
        rows = response.css('.sortable > tbody > tr')
        for row in rows:
            loader = CNProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            loader.add_value('type', 'HTTP')
            proxies.append(loader.load_item())
        return proxies
