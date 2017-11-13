# -*- coding: utf-8 -*
import os
import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('..')

import unittest 
from crawler.spiders import cnproxy, goubanjia, ip181, kuaidaili, kxdaili, premproxy, proxydb, xici     
from mock import mock_spider_response


class SpiderParserTest(unittest.TestCase):
    def test_cnproxy_parse(self):
        self.assertTrue(False)


    def test_goubanjia_parse(self):
        self.assertTrue(False)

    def test_ip181_parse(self):
        self.assertTrue(False)

    def test_kuaidaili_parse(self):
        self.assertTrue(False)

    def test_kxdaili_parse(self):
        self.assertTrue(False)

    def test_premproxy_parse(self):
        self.assertTrue(False)

    def test_proxydb_parse(self):
        self.assertTrue(False)

    def test_xici_parse(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
