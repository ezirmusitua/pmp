# -*- coding: utf-8 -*-
from scrapy import Spider

from ..items import ProxyItemLoader, Proxy


class KXDaiLiSpider(Spider):
    name = 'kxdaili'
    allowed_domains = ['kxdaili.com']
    start_urls = ['http://www.kxdaili.com/ipList/%d.html' % i for i in range(1, 11)]

    def parse(self, response):
        rows = response.css('div.tab_c_box.buy_tab_box > table > tbody >tr')
        proxies = []
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            proxy_type = row.css('td:nth-child(4)::text').extract()[0]
            loader.add_value('proxy_type', proxy_type.split(','))
            proxies.append(loader.load_item())
        return proxies
