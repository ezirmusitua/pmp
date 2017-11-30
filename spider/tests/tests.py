# -*- coding: utf-8 -*
import sys

sys.path.append('..')

from unittest import TestCase, mock, main

from proxy_crawler import CNProxySpider, GouBanJiaSpider, Ip181Spider, KuaiDaiLiSpider, KXDaiLiSpider, PremProxySpider, \
    ProxyDBSpider, XiCiSpider
from proxy_crawler.models import Proxy
from proxy_crawler.items import StrCleaner
from proxy_crawler.helper import get_list_item_safely, generate_proxydb_js_ip_port

from mock import mock_spider_response


class TestSpiderParser(TestCase):
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


class TestProxyModel(TestCase):
    def setUp(self):
        self.proxy = Proxy({
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'connection': [],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown'
        })

    def test_get_random_usable_one_proxy(self):
        find_res = [{
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown',
            'connection': []
        }]
        Proxy.db_collection = mock.MagicMock()
        Proxy.db_collection.list = mock.MagicMock(return_value=find_res)
        proxy_str = Proxy.get_random_usable_one_proxy('demo')
        self.assertEqual(proxy_str, '127.0.0.1:8080')
        Proxy.db_collection.list.assert_called_with(
            query={'connection': 'demo', 'proxy_type': {'$in': ['http', 'https']}},
            sort=[('last_check_at', 1)],
            limit=20)


class TestItemProcessor(TestCase):
    def test_str_cleaner(self):
        cleaner = StrCleaner()
        self.assertEqual(['http'], cleaner(['\n   http   \n']))


class TestHelperFunctions(TestCase):
    def test_get_list_item_safely(self):
        self.assertEqual(get_list_item_safely(None, -1, 0), 0)
        self.assertEqual(get_list_item_safely([], 0, 0), 0)
        self.assertEqual(get_list_item_safely([1], 0, 0), 1)

    def test_generate_proxydb_js_ip_port(self):
        code_seg_v1 = r"""
        var s = '1.631.312'.split('').reverse().join('');
        var yy = '05.62';
        var pp = -17424 + 20552;
        document.write('<a href="/' + s + yy + '/' + pp + '#http" title="lsocit-213.136.105.62.aviso.ci">' + s + yy + String.fromCharCode(58) + pp + '</a>');
        proxies.push(s + yy + String.fromCharCode(58) + pp);
        """
        self.assertEqual(('213.136.105.62', '3128'), generate_proxydb_js_ip_port(code_seg_v1))
        code_seg_v2 = r"""
        var o = '1.791.831'.split('').reverse().join('');
        var yy = atob('\x4e\x54\x63\x75\x4e\x6a\x59\x3d'.replace(/\\x([0-9A-Fa-f]{2})/g, function () {
            return String.fromCharCode(parseInt(arguments[ 1 ], 16))
        }));
        var pp = -51279 + 54407;
        document.write('<a href="/' + o + yy + '/' + pp + '#http" title="">' + o + yy + String.fromCharCode(58) + pp + '</a>');
        proxies.push(o + yy + String.fromCharCode(58) + pp);
        """
        self.assertEqual(('138.197.157.66', '3128'), generate_proxydb_js_ip_port(code_seg_v2))


if __name__ == '__main__':
    main()
