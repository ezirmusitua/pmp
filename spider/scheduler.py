# -*- coding: utf-8 -*-
import logging
import pymongo
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from proxy_crawler import KXDaiLiSpider, KuaiDaiLiSpider, Ip181Spider, GouBanJiaSpider, \
    XiCiSpider, CNProxySpider, PremProxySpider, ProxyDBSpider

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'proxy_crawler_demo'
MONGO_COLLECTION = 'schedule_task'
client = pymongo.MongoClient(MONGO_URI)
database = client[MONGO_DATABASE]
collection = database[MONGO_COLLECTION]

logging.basicConfig(filename='logs/spiders.log')

TASKS = {
    # 8 hours
    'proxy.spider.cnproxy': 8 * 60 * 60,
    # 1 hour
    'proxy.spider.goubanjia': 1 * 60 * 60,
    # 10 minutes
    'proxy.spider.ip181': 10 * 60,
    # 8 hours
    'proxy.spider.kuaidaili': 8 * 60 * 60,
    # 30 minutes
    'proxy.spider.kxdaili': 30 * 60,
    # 4 hours
    'proxy.spider.premproxy': 4 * 60 * 60,
    # 2 hours
    'proxy.spider.proxydb': 2 * 60 * 60,
    # 8 hours
    'proxy.spider.xici': 8 * 60 * 60,
}


@inlineCallbacks
def start_kuaidaili_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling kuaidaili')
    times = 1
    while True:
        spider_deferred = runner.crawl(KuaiDaiLiSpider)
        yield spider_deferred
        print('crawled kuaidaili', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(6 * 60 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 6 hours = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_xicidaili_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling xicidaili')
    times = 1
    while True:
        spider_deferred = runner.crawl(XiCiSpider)
        yield spider_deferred
        print('crawled xicidaili: ', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(6 * 60 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 6 hours = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_cnproxy_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling cnproxy')
    times = 1
    while True:
        spider_deferred = runner.crawl(CNProxySpider)
        yield spider_deferred
        print('crawled cnproxy: ', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(6 * 60 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 6 hours = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_premproxy_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling premproxy')
    times = 1
    while True:
        spider_deferred = runner.crawl(PremProxySpider)
        yield spider_deferred
        print('crawled premproxy: ', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(4 * 60 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 4 hours = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_proxydb_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling proxydb')
    times = 1
    while True:
        spider_deferred = runner.crawl(ProxyDBSpider)
        yield spider_deferred
        print('crawled proxydb', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(2 * 60 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 2 hours = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_goubanjia_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling goubanjia')
    times = 1
    while True:
        spider_deferred = runner.crawl(GouBanJiaSpider)
        yield spider_deferred
        print('crawled goubanjia: ', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(1 * 60 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 1 hour = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_kxdaili_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling kxdaili')
    times = 1
    while True:
        spider_deferred = runner.crawl(KXDaiLiSpider)
        yield spider_deferred
        print('crawled kxdaili: ', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(30 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 30 minutes = = = = =')
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_ip_181_crawler():
    settings = get_project_settings()
    runner = CrawlerRunner(get_project_settings())
    configure_logging(settings, install_root_handler=False)
    print('start scheduling ip181')
    times = 1
    while True:
        spider_deferred = runner.crawl(Ip181Spider)
        yield spider_deferred
        print('crawled ip181: ', times, ' times')
        wait_deferred = Deferred()
        reactor.callLater(10 * 60, wait_deferred.callback, 'Done')
        print('= = = = = wait for 10 minutes = = = = =')
        yield wait_deferred
        times += 1


start_ip_181_crawler()
start_kxdaili_crawler()
start_goubanjia_crawler()
start_proxydb_crawler()
start_premproxy_crawler()
start_cnproxy_crawler()
start_xicidaili_crawler()
start_kuaidaili_crawler()

reactor.run()
