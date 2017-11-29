# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..helper import get_list_item_safely
from ..items import ProxyItemLoader, Proxy


class PremProxySpider(CrawlSpider):
    name = 'premproxy'
    allowed_domains = ['premproxy.com']
    start_urls = [
        'https://premproxy.com/list/',
        'https://premproxy.com/socks-list/'
    ]

    rules = (Rule(
        LinkExtractor(allow=('\d+.htm$',), deny=('ip-.*.htm', 'type-.*.htm', 'time-.*.htm')),
        callback='parse_item'
    ),)

    def parse_item(self, response):
        is_socks = response.url.find('socks') > -1
        proxies = []
        rows = response.css('#proxylist .container > table > tbody > tr')
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            ip_port = get_list_item_safely(row.css('td:nth-child(1)::text').extract(), 0).split(':')
            # ip address and port
            loader.add_value('ip_address', [get_list_item_safely(ip_port, 0, 'localhost')])
            loader.add_value('port', [get_list_item_safely(ip_port, 1, 80)])
            # for socks, here should use css selector to extract else use default HTTP
            proxy_type = ['HTTP']
            if is_socks:
                proxy_type = row.css('td:nth-child(2)::text').extract()
            loader.add_value('proxy_type', proxy_type)
            proxies.append(loader.load_item())
        return proxies
