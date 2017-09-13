import scrapy


class CnproxySpider(scrapy.Spider):
    name = "cnproxy"
    start_urls = ['http://cn-proxy.com']

    def parse(self, response):
        with open('cnproxy.html', 'wb') as f:
            f.write(response.body)
