# -*- coding: utf-8 -*
"""
Reference: https://stackoverflow.com/questions/6456304/scrapy-unit-testing
"""

import os

from scrapy.http import Response, Request

SPIDER_MOCK_INFO_NAME_MAP = {
    'cn-proxy-china': {'url': 'http://cn-proxy.com', 'response_file': 'spider_response/cn-proxy-china.html'},
    'cn-proxy-global': {'url': 'http://cn-proxy.com', 'response_file': 'spider_response/cn-proxy-global.html'},
    'goubanjia': {'url': 'http://www.goubanjia.com', 'response_file': 'spider_response/goubanjia.html'},
    'ip181': {'url': 'http://www.ip181.com', 'response_file': 'spider_response/ip181.html'},
    'kuaidaili': {'url': 'http://www.kuaidaili.com', 'response_file': 'spider_response/kkuaidaili.html'},
    'kxdaili': {'url': 'http://www.kxdaili.com', 'response_file': 'spider_response/kxdaili.html'},
    'premproxy': {'url': 'http://www.premproxy.com', 'response_file': 'spider_response/premproxy.html'},
    'proxydb': {'url': 'http://proxydb.net', 'response_file': 'spider_response/proxydb.html'},
    'xici': {'url': 'http://www.xicidaili.com', 'response_file': 'spider_response/xici.html'},
}

def mock_spider_response(spider_name):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param spider_name: The spider name of scrapy
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    mock_info = SPIDER_MOCK_INFO_NAME_MAP[spider_name]
    url=mock_info['url']
    with codecs.open(mock_info[spider_name], 'rb+', 'utf-8') as rf:
        request = Request(url=url)
        response = Response(url=url, request=request, body=file_content)
        response.encoding = 'utf-8'
        return response
