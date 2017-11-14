# -*- coding: utf-8 -*-
from scrapy.spiders import Spider

from proxy_crawler.helper import generate_proxydb_js_ip_port
from proxy_crawler.items import ProxyItemLoader, Proxy


class ProxyDBSpider(Spider):
    name = 'proxydb'
    allowed_domains = ['proxydb.net']
    start_urls = ['http://proxydb.net/?offset=%s' % offset for offset in range(0, 100, 20)]

    def parse(self, response):
        self.logger.critical('DebugNow')
        rows = response.css('.container > table > tbody > tr')
        proxies = []
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            ip_port_js_generator = row.css('td:nth-child(1) > script::text').extract()[0]
            address_port = generate_proxydb_js_ip_port(ip_port_js_generator)
            loader.add_value('ip_address', [address_port[0]])
            loader.add_value('port', [address_port[1]])
            loader.add_css('type', 'td:nth-child(2)::text')
            proxies.append(loader.load_item())
        return proxies
