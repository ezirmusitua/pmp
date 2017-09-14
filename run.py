# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess

from crawler import CNProxySpider, PremProxySpider, ProxyDBSpider

process = CrawlerProcess()
process.crawl(CNProxySpider)
process.crawl(PremProxySpider)
process.crawl(ProxyDBSpider)
process.start()
