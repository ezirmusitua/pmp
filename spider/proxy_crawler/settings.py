# -*- coding: utf-8 -*-
BOT_NAME = 'proxy_crawler'
SPIDER_MODULES = ['proxy_crawler.spiders']
NEWSPIDER_MODULE = 'proxy_crawler.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/60.0.3112.113 Safari/537.36'
ROBOTSTXT_OBEY = False
SPIDER_MIDDLEWARES = {
    'proxy_crawler.middlewares.ProxyCrawlerSpiderMiddleware': 543
}
DOWNLOADER_MIDDLEWARES = {
    'proxy_crawler.middlewares.ProxyMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100,
}
ITEM_PIPELINES = {
    'proxy_crawler.pipelines.RemoveDuplicatedPipeline': 100,
    'proxy_crawler.pipelines.ExportToMongoPipeline': 200,
}
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 60
AUTOTHROTTLE_MAX_DELAY = 60
DOWNLOAD_TIMEOUT = 60
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_LEVEL = 'WARNING'
LOG_FILE = 'logs/spiders.log'
MONGO_URI = 'mongodb://pmpAdmin:pmpAdmin@mongo:27017/pmp'
MONGO_DATABASE = 'pmp'
PROXY_MODEL_NAME = 'proxy'
SCHEDULE_KUAIDAILI = 6 * 60 * 60
SCHEDULE_CNPROXY = 6 * 60 * 60
SCHEDULE_XICI = 4 * 60 * 60
SCHEDULE_PREMPROXY = 4 * 60 * 60
SCHEDULE_PROXYDB = 2 * 60 * 60
SCHEDULE_GOUBANJIA = 2 * 60 * 60
SCHEDULE_KXDAILI = 2 * 60 * 60
SCHEDULE_IP181 = 2 * 60 * 60
