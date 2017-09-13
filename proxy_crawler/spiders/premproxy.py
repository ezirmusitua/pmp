# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from proxy_crawler.helper import get_list_item_safely
from proxy_crawler.items import PremProxyItemLoader, Proxy


class PremproxySpider(CrawlSpider):
    name = 'premproxy'
    allowed_domains = ['premproxy.com']
    start_urls = ['http://premproxy.com/list/']

    rules = (Rule(
        LinkExtractor(allow=('\d+.htm$',), deny=('ip-.*.htm', 'type-.*.htm', 'time-.*.htm')),
        callback='parse_item'
    ),)

    def parse_item(self, response):
        proxies = []
        rows = response.css('.container > table > tbody > tr')
        for row in rows:
            loader = PremProxyItemLoader(item=Proxy(), selector=row)
            ip_port = get_list_item_safely(row.css('td:nth-child(1)::text').extract(), 0).split(':')
            loader.add_value('ip_address', [get_list_item_safely(ip_port, 0, 'localhost')])
            loader.add_value('port', [get_list_item_safely(ip_port, 1, 80)])
            loader.add_value('type', 'HTTP')
            country = get_list_item_safely(row.css('td:nth-child(4)::text').extract(), 0)
            city = get_list_item_safely(row.css('td:nth-child(5)::text').extract(), 0)
            loader.add_value('location', [country + ', ' + city])
            loader.add_css('anonymity', 'td:nth-child(2)::text')
            loader.add_css('last_check_at', 'td:nth-child(3)::text')
            proxies.append(loader.load_item())
        return proxies
