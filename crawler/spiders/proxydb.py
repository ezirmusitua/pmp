# -*- coding: utf-8 -*-
from scrapy.spiders import Spider

from crawler.helper import generate_proxydb_js_ip_port
from crawler.items import ProxyDBItemLoader, Proxy


class ProxyDBSpider(Spider):
    name = 'proxydb'
    allowed_domains = ['proxydb.net']
    start_urls = ['http://proxydb.net/?offset=%s' % offset for offset in range(0, 6140, 20)]

    def parse(self, response):
        rows = response.css('.container > table > tbody > tr')
        proxies = []
        for row in rows:
            loader = ProxyDBItemLoader(item=Proxy(), selector=row)
            ip_port_js_generator = row.css('td:nth-child(1) > script::text').extract()[0]
            address_port = generate_proxydb_js_ip_port(ip_port_js_generator)
            loader.add_value('ip_address', [address_port[0]])
            loader.add_value('port', [address_port[1]])
            loader.add_css('type', 'td:nth-child(2)::text')
            loader.add_css('location', 'td:nth-child(3) > abbr::attr(title)')
            loader.add_css('anonymity', 'td:nth-child(4) span::text')
            loader.add_css('last_check_at', 'td:nth-child(8) > abbr::attr(title)')
            proxies.append(loader.load_item())
        return proxies
