import scrapy

from proxy_crawler.items import Proxy, CNProxyItemLoader


class CnproxySpider(scrapy.Spider):
    name = "cnproxy"
    start_urls = ['http://cn-proxy.com']

    def parse(self, response):
        proxies = []
        rows = response.css('.sortable > tbody > tr')
        for row in rows:
            loader = CNProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(1)::text')
            loader.add_value('type', 'HTTP')
            loader.add_css('port', 'td:nth-child(2)::text')
            loader.add_css('location', 'td:nth-child(3)::text')
            loader.add_value('anonymity', 'unknown')
            loader.add_css('last_check_at', 'td:nth-child(5)::text')
            proxies.append(loader.load_item())
        return proxies
