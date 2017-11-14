# -*- coding: utf-8 -*
import sys
sys.path.append('..')

import unittest
from proxy_crawler import CNProxySpider, GouBanJiaSpider, Ip181Spider, KuaiDaiLiSpider, KXDaiLiSpider, PremProxySpider, \
    ProxyDBSpider, XiCiSpider
from mock import mock_spider_response


class SpiderParserTest(unittest.TestCase):
    def test_cnproxy_parse(self):
        spider = CNProxySpider()
        parse_res_cn = spider.parse(mock_spider_response('cn-proxy-china'))
        self.assertFalse(not parse_res_cn)
        parse_res_gb = spider.parse(mock_spider_response('cn-proxy-global'))
        self.assertFalse(not parse_res_gb)

    def test_goubanjia_parse(self):
        spider = GouBanJiaSpider()
        parse_res = spider.parse(mock_spider_response('goubanjia'))
        self.assertFalse(not parse_res)

    def test_ip181_parse(self):
        spider = Ip181Spider()
        parse_res = spider.parse(mock_spider_response('ip181'))
        self.assertFalse(not parse_res)

    def test_kuaidaili_parse(self):
        spider = KuaiDaiLiSpider()
        parse_res = spider.parse(mock_spider_response('kuaidaili'))
        self.assertFalse(not parse_res)

    def test_kxdaili_parse(self):
        spider = KXDaiLiSpider()
        parse_res = spider.parse(mock_spider_response('kxdaili'))
        self.assertFalse(not parse_res)

    def test_premproxy_parse(self):
        spider = PremProxySpider()
        parse_res = spider.parse(mock_spider_response('premproxy'))
        self.assertFalse(not parse_res)
        parse_res_socks = spider.parse(mock_spider_response('premproxy-socks'))
        self.assertFalse(not parse_res_socks)

    def test_proxydb_parse(self):
        spider = ProxyDBSpider()
        parse_res = spider.parse(mock_spider_response('proxydb'))
        self.assertFalse(not parse_res)

    def test_xici_parse(self):
        spider = XiCiSpider()
        parse_res = spider.parse(mock_spider_response('xici'))
        self.assertFalse(not parse_res)


if __name__ == '__main__':
    unittest.main()
