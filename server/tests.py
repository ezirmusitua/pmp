# -*- coding: utf-8 -*-
from unittest import TestCase, mock, main

from proxy_server.models import Proxy


class TestModel(TestCase):
    def setUp(self):
        Proxy.db_collection = mock.MagicMock()
        self.proxy = Proxy({
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown',
            'connection': []
        })

    def test_search(self):
        self.assertTrue(False)


if __name__ == '__main__':
    main()
