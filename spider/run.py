# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from proxy_crawler import CNProxySpider, GouBanJiaSpider, Ip181Spider, KuaiDaiLiSpider, KXDaiLiSpider, PremProxySpider, \
    ProxyDBSpider, XiCiSpider

process = CrawlerProcess(get_project_settings())
process.crawl(CNProxySpider)
process.crawl(GouBanJiaSpider)
process.crawl(Ip181Spider)
process.crawl(KuaiDaiLiSpider)
process.crawl(KXDaiLiSpider)
process.crawl(PremProxySpider)
process.crawl(ProxyDBSpider)
process.crawl(XiCiSpider)
process.start()
