# -*- coding: utf-8 -*
"""
Reference: https://stackoverflow.com/questions/6456304/scrapy-unit-testing
"""

import os
import codecs

from scrapy.http import TextResponse

SPIDER_MOCK_INFO_NAME_MAP = {
    'cn-proxy-china': {'url': 'http://cn-proxy.com', 'response_file': 'mock/spider_response/cn-proxy-china.html'},
    'cn-proxy-global': {'url': 'http://cn-proxy.com', 'response_file': 'mock/spider_response/cn-proxy-global.html'},
    'goubanjia': {'url': 'http://www.goubanjia.com', 'response_file': 'mock/spider_response/goubanjia.html'},
    'ip181': {'url': 'http://www.ip181.com', 'response_file': 'mock/spider_response/ip181.html'},
    'kuaidaili': {'url': 'http://www.kuaidaili.com', 'response_file': 'mock/spider_response/kuaidaili.html'},
    'kxdaili': {'url': 'http://www.kxdaili.com', 'response_file': 'mock/spider_response/kxdaili.html'},
    'premproxy': {'url': 'http://www.premproxy.com/list/', 'response_file': 'mock/spider_response/premproxy.html'},
    'premproxy-socks': {'url': 'http://www.premproxy.com/socks-list/',
                        'response_file': 'mock/spider_response/premproxy-socks.html'},
    'proxydb': {'url': 'http://proxydb.net', 'response_file': 'mock/spider_response/proxydb.html'},
    'xici': {'url': 'http://www.xicidaili.com', 'response_file': 'mock/spider_response/xici.html'},
}


def mock_spider_response(spider_name):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param spider_name: The spider name of scrapy
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    mock_info = SPIDER_MOCK_INFO_NAME_MAP[spider_name]
    url = mock_info['url']
    with codecs.open(mock_info['response_file'], 'rb', 'utf-8') as rf:
        response = TextResponse(url=url, body=rf.read().encode(), status=200, headers={})
        return response
