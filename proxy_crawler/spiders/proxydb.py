# -*- coding: utf-8 -*-
import scrapy

from proxy_crawler.helper import generate_proxydb_js_ip_port
from proxy_crawler.items import ProxyDBItemLoader, Proxy


class ProxydbSpider(scrapy.Spider):
    name = 'proxydb'
    allowed_domains = ['proxydb.net']
    start_urls = ['http://proxydb.net/?offset=0']

    def parse(self, response):
        if len(response.css('.alert-warning')) is 0:
            offset = int(response.url.split('=')[1]) + 20
            yield scrapy.Request('http://proxydb.net/?offset=%s' % offset)
        return self.parse_item(response)

    def parse_item(self, response):
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
            loader.add_value('quality', 'unknown')
            loader.add_css('last_check_at', 'td:nth-child(8) > abbr::attr(title)')
            proxies.append(loader.load_item())
            self.logger.info('aaaaaa', proxies)
        return proxies
