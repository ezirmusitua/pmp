# -*- coding: utf-8 -*-
import re
import time
import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor

from crawler.items import XiCiProxyItemLoader, Proxy


class XiCiSpider(CrawlSpider):
    name = 'xici'
    start_at = time.time()
    # this crawler should run per 4 hour
    end_at = start_at + 4 * 60 * 60
    url_pattern = re.compile('^http://www.xicidaili.com/([ntw]{2})/?\d?')
    allowed_domains = ['xicidaili.com']
    target_all_crawled = {'nn': False, 'nt': False, 'wn': False, 'wt': False}
    start_urls = ['http://www.xicidaili.com']

    rules = (Rule(
        LinkExtractor(allow='\/[ntw]{2}\/\d?$'),
        callback='parse_item',
        follow=True
    ),)

    def parse_item(self, response):
        if XiCiSpider.should_close_spider():
            raise CloseSpider
        target = XiCiSpider.get_url_info(response.url)
        if XiCiSpider.target_all_crawled[target]:
            return []
        proxies = []
        rows = response.css('table#ip_list tr:not(:first-child)')
        last_check_at = 0
        for row in rows:
            loader = XiCiProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(2)::text')
            loader.add_css('port', 'td:nth-child(3)::text')
            _type = row.css('td:nth-child(6)::text').extract()[0]
            loader.add_value('type', [_type])
            proxies.append(loader.load_item())
            last_check_at_time_str = row.css('td:last-child::text').extract()[0]
            last_check_at = time.mktime(
                datetime.datetime.strptime(last_check_at_time_str, "%y-%m-%d %H:%S").timetuple())
        XiCiSpider.target_all_crawled[target] = XiCiSpider.should_continue(last_check_at)
        return proxies

    @classmethod
    def get_url_info(cls, url):
        groups = cls.url_pattern.search(url).groups()
        return groups[0]

    @classmethod
    def should_continue(cls, last):
        return last >= cls.end_at

    @classmethod
    def should_close_spider(cls):
        return len(list(filter(lambda t: cls.target_all_crawled[t], cls.target_all_crawled))) == 4
