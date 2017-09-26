# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawler import CNProxySpider, PremProxySpider, ProxyDBSpider

process = CrawlerProcess(get_project_settings())
process.crawl(CNProxySpider)
process.crawl(PremProxySpider)
process.crawl(ProxyDBSpider)
process.start()
