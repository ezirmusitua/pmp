# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred

from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from proxy_crawler import KXDaiLiSpider, KuaiDaiLiSpider, Ip181Spider, GouBanJiaSpider, \
    XiCiSpider, CNProxySpider, PremProxySpider, ProxyDBSpider, bind_models

settings = get_project_settings()
configure_logging(settings, install_root_handler=True)
bind_models()
runner = CrawlerRunner(settings)


@inlineCallbacks
def start_kuaidaili_crawler():
    print('start scheduling kuaidaili')
    times = 1
    while True:
        spider_deferred = runner.crawl(KuaiDaiLiSpider)
        yield spider_deferred
        print('crawled kuaidaili', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + KuaiDaiLiSpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_xicidaili_crawler():
    print('start scheduling xicidaili')
    times = 1
    while True:
        spider_deferred = runner.crawl(XiCiSpider)
        yield spider_deferred
        print('crawled xicidaili: ', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + XiCiSpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_cnproxy_crawler():
    print('start scheduling cnproxy')
    times = 1
    while True:
        spider_deferred = runner.crawl(CNProxySpider)
        yield spider_deferred
        print('crawled cnproxy: ', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + CNProxySpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_premproxy_crawler():
    print('start scheduling premproxy')
    times = 1
    while True:
        spider_deferred = runner.crawl(PremProxySpider)
        yield spider_deferred
        print('crawled premproxy: ', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + PremProxySpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_proxydb_crawler():
    print('start scheduling proxydb')
    times = 1
    while True:
        spider_deferred = runner.crawl(ProxyDBSpider)
        yield spider_deferred
        print('crawled proxydb', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + ProxyDBSpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_goubanjia_crawler():
    print('start scheduling goubanjia')
    times = 1
    while True:
        spider_deferred = runner.crawl(GouBanJiaSpider)
        yield spider_deferred
        print('crawled goubanjia: ', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + GouBanJiaSpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_kxdaili_crawler():
    print('start scheduling kxdaili')
    times = 1
    while True:
        spider_deferred = runner.crawl(KXDaiLiSpider)
        yield spider_deferred
        print('crawled kxdaili: ', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + KXDaiLiSpider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


@inlineCallbacks
def start_ip_181_crawler():
    print('start scheduling ip181')
    times = 1
    while True:
        spider_deferred = runner.crawl(Ip181Spider)
        yield spider_deferred
        print('crawled ip181: ', times, ' times')
        wait_seconds = settings.get('SCHEDULE_' + Ip181Spider.name.upper())
        wait_deferred = Deferred()
        reactor.callLater(wait_seconds, wait_deferred.callback, 'Done')
        print('= = = = = wait for {} seconds = = = = ='.format(wait_seconds))
        yield wait_deferred
        times += 1


if __name__ == '__main__':
    start_ip_181_crawler()
    start_kxdaili_crawler()
    start_goubanjia_crawler()
    start_proxydb_crawler()
    start_premproxy_crawler()
    start_cnproxy_crawler()
    start_xicidaili_crawler()
    start_kuaidaili_crawler()
    reactor.run()
