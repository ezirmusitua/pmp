# -*- coding: utf-8 -*-
import re
import time

import datetime
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import ProxyItemLoader, Proxy


class KuaiDaiLiSpider(CrawlSpider):
    name = 'kuaidaili'
    allowed_domains = ['kuaidaili.com']
    # this crawler should run per 4 hour
    start_at = time.time()
    end_at = start_at + 4 * 60 * 60
    url_pattern = re.compile(r'^http://www.kuaidaili.com/free/(in(ha|tr))/?\d*/$')
    target_all_crawled = {'inhr': False, 'inha': False}
    start_urls = ['http://kuaidaili.com/free/inha/1', 'http://kuaidaili.com/free/intr/1']

    rules = (
        Rule(LinkExtractor(allow=r'/free/in(ha|tr)/\d{1,2}'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if KuaiDaiLiSpider.should_close_spider():
            raise CloseSpider
        target = KuaiDaiLiSpider.get_url_info(response.url)
        if KuaiDaiLiSpider.target_all_crawled[target]:
            return []
        proxies = []
        rows = response.css('table#ip_list tr:not(:first-child)')
        last_check_at = 0
        for row in rows:
            loader = ProxyItemLoader(item=Proxy(), selector=row)
            loader.add_css('ip_address', 'td:nth-child(2)::text')
            loader.add_css('port', 'td:nth-child(3)::text')
            _type = row.css('td:nth-child(6)::text').extract()[0]
            loader.add_value('type', [_type])
            proxies.append(loader.load_item())
            last_check_at_time_str = row.css('td:last-child::text').extract()[0]
            last_check_at = time.mktime(
                datetime.datetime.strptime(last_check_at_time_str, "%Y-%m-%d %H:%S:%f").timetuple())
            self.logger.critical('last check at: %s' % last_check_at)
        KuaiDaiLiSpider.target_all_crawled[target] = KuaiDaiLiSpider.should_continue(last_check_at)
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
        return len(list(filter(lambda t: cls.target_all_crawled[t], cls.target_all_crawled))) == 2
