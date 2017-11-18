# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

from unittest import TestCase, mock, main

from proxy_validator.client import Client, Default_Timeout, Default_UA
from proxy_validator.database import Database


class TestClient(TestCase):
    def setUp(self):
        self.client = Client({}, {})
        self.client.session = mock.MagicMock()
        mock_response = mock.MagicMock()
        mock_response.status_code = 300
        self.client.session.get = mock.MagicMock(return_value=mock_response)

    def test_get(self):
        with self.assertRaises(Exception):
            self.client.get()
        self.client.get(url='http://httpbin.org')
        self.client.session.get.assert_called_with('http://httpbin.org', headers={'User-Agent': Default_UA}, proxies={},
                                                   timeout=1)

    def test_set_proxy(self):
        self.client.set_proxies('123.103.93.38:80')
        self.client.get(url='http://httpbin.org')
        self.client.session.get.assert_called_with('http://httpbin.org', headers={'User-Agent': Default_UA},
                                                   proxies={'http': 'http://123.103.93.38:80',
                                                            'https': 'https://123.103.93.38:80'},
                                                   timeout=Default_Timeout)
        self.client.set_proxies('123.103.93.38:80', 'http')
        self.client.get(url='http://httpbin.org')
        self.client.session.get.assert_called_with('http://httpbin.org', headers={'User-Agent': Default_UA},
                                                   proxies={'http': 'http://123.103.93.38:80',
                                                            'https': 'http://123.103.93.38:80'},
                                                   timeout=Default_Timeout)


class TestDatabase(TestCase):
    def setUp(self):
        self.database = Database()
        self.database.collection = mock.MagicMock()
        self.mock_find_return = mock.MagicMock()
        self.mock_find_return.batch_size = mock.MagicMock(return_value=[0, 1, 2])
        self.database.collection.find = mock.MagicMock(return_value=self.mock_find_return)
        self.database.collection.insert = mock.MagicMock(return_value=None)
        self.database.collection.update = mock.MagicMock(return_value=None)
        self.database.collection.remove = mock.MagicMock(return_value=None)

    def test_list(self):
        list(self.database.list({'ip': '127.0.0.1'}))
        self.database.collection.find.assert_called_with({'ip': '127.0.0.1'})
        self.mock_find_return.batch_size.assert_called_with(20)
        list(self.database.list())
        self.database.collection.find.assert_called_with({})

    def test_update(self):
        with self.assertRaises(Exception):
            self.database.update()
        self.database.update({}, {'ip': '127.0.0.1'})
        self.database.collection.update.assert_called_with({}, {'$set': {'ip': '127.0.0.1'}})

    def test_remove(self):
        with self.assertRaises(Exception):
            self.database.remove()
        self.database.remove({})
        self.database.collection.remove.assert_called_with({})

    def test_find_one_and_update(self):
        with self.assertRaises(Exception):
            self.database.find_one_and_update()

        self.database.collection.find_one = mock.MagicMock(return_value=True)
        self.database.find_one_and_update({'_id': '1'}, {'ip': '127.0.0.1'})
        self.database.collection.find_one.assert_called_with({'_id': '1'})
        self.database.collection.update.assert_called_with({'_id': '1'}, {'$set': {'ip': '127.0.0.1'}})

        self.database.collection.find_one = mock.MagicMock(return_value=None)
        self.database.find_one_and_update({'_id': '1'}, {'ip': '127.0.0.1'})
        self.database.collection.insert.assert_called_with({'ip': '127.0.0.1'})



if __name__ == '__main__':
    main()
