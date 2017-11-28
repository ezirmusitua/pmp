# -*- coding: utf-8 -*-
from scrapy import Spider

from ..items import ProxyItemLoader, Proxy


class XiCiSpider(Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/%d' % i for i in range(1, 6)] + \
                 ['http://www.xicidaili.com/nt/%d' % i for i in range(1, 6)] + \
                 ['http://www.xicidaili.com/wn/%d' % i for i in range(1, 6)] + \
                 ['http://www.xicidaili.com/wt/%d' % i for i in range(1, 6)]

    def parse(self, response):
        proxies = []
        rows = response.css('table#ip_list tr:not(:first-child)')
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(2)::text')
            loader.add_css('port', 'td:nth-child(3)::text')
            _type = row.css('td:nth-child(6)::text').extract()[0]
            loader.add_value('type', [_type])
            proxies.append(loader.load_item())
        return proxies
