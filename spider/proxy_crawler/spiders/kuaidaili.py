# -*- coding: utf-8 -*-
from scrapy import Spider

from ..items import ProxyItemLoader, Proxy


class KuaiDaiLiSpider(Spider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    start_urls = ['http://kuaidaili.com/free/inha/%d' % i for i in range(1, 11)] + \
                 ['http://kuaidaili.com/free/intr/%d' % i for i in range(1, 11)]

    def parse(self, response):
        proxies = []
        rows = response.css('div#list > table > tbody > tr')
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            proxy_type = row.css('td:nth-child(4)::text').extract()
            loader.add_value('proxy_type', proxy_type)
            proxies.append(loader.load_item())
        return proxies
