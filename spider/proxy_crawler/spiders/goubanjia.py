# -*- coding: utf-8 -*-
from scrapy import Spider

from ..items import ProxyItemLoader, Proxy


class GouBanJiaSpider(Spider):
    name = 'goubanjia'
    allowed_domains = ['goubanjia.com']
    start_urls = ['http://www.goubanjia.com/index%d.shtml' % i for i in range(1, 11)]

    def parse(self, response):
        rows = response.css('div#list > table > tbody > tr')
        proxies = []
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            ip_port_texts = row.css('td:nth-child(1) > *:not([style*="display: none;"])::text').extract()
            loader.add_value('ip_address', ''.join(ip_port_texts[:-1]))
            loader.add_value('port', ip_port_texts[-1])
            proxy_type = row.css('td:nth-child(4)::text').extract()
            loader.add_value('proxy_type', proxy_type)
            proxies.append(loader.load_item())
        return proxies
