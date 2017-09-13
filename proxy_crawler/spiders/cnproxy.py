# -*- coding: utf-8 -*-
import scrapy
from proxy_crawler.helper import get_list_item_safely
from proxy_crawler.items import Proxy, CNProxyItemLoader

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
        is_global = response.url.find('archives') > -1
        proxies = []
        rows = response.css('.sortable > tbody > tr')
        for row in rows:
            loader = CNProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            loader.add_value('type', 'HTTP')
            anonymity = '透明'
            if is_global:
                anonymity = get_list_item_safely(row.css('td:nth-child(3)::text').extract(), 0, '透明')
            loader.add_value('anonymity', CNPROXY_TYPE_TO_ANONYMITY.get(anonymity, 'unknown'))
            loader.add_css('location', 'td:nth-child(%s)::text' % (4 if is_global else 3))
            loader.add_css('last_check_at', 'td:nth-child(%s)::text' % (6 if is_global else 5))
            proxies.append(loader.load_item())
        return proxies
