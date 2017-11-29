# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

from unittest import TestCase, mock, main
from proxy_validator.chain import RChain, Task, Handler
from proxy_validator.client import Client, Default_Timeout, Default_UA
from proxy_validator.proxy import ProxyModel, ProxyToUpdatePool
from proxy_validator.database import Database
from proxy_validator.utils import singleton


class TestUtils(TestCase):
    def test_singleton(self):
        class DemoClass1(object):
            def __init__(self):
                pass

        self.assertNotEqual(DemoClass1(), DemoClass1())

        @singleton
        class DemoClass2(object):
            def __init__(self):
                pass

        self.assertEqual(DemoClass2(), DemoClass2())


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
                                                            'https': 'http://123.103.93.38:80'},
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


class TestProxyModel(TestCase):
    def setUp(self):
        self.proxy = ProxyModel({
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'connection': [],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown'
        })
        self.proxy.last_check_at = -1
        self.proxy_pool = ProxyToUpdatePool()

    def test_proxy_str(self):
        self.assertEqual(self.proxy.proxy_str(), '127.0.0.1:8080')

    def test_proxy_to_json(self):
        self.assertEqual(self.proxy.to_json(), {
            'anonymity': ['unknown'],
            'ip_address': '127.0.0.1',
            'port': 8080,
            'last_check_at': -1,
            'location': 'unknown, unknown',
            'connection': [],
            'proxy_type': ['unknown']
        })

    def test_update_proxy_pool(self):
        self.proxy_pool.db = mock.MagicMock()
        self.proxy_pool.db.remove = mock.MagicMock()
        self.proxy_pool.db.update = mock.MagicMock()
        self.proxy_pool.to_update = self.proxy_pool.to_remove = [
            ProxyModel({'_id': str(i), 'ip_address': '127.0.0.1', 'port': i}) for i in
            range(0, 20)]
        self.assertEqual(len(self.proxy_pool.to_remove), 20)
        self.assertEqual(len(self.proxy_pool.to_update), 20)
        self.proxy_pool.handle_pool()
        self.assertEqual(len(self.proxy_pool.to_remove), 0)
        self.assertEqual(len(self.proxy_pool.to_update), 0)

    def test_add_to_proxy_pool(self):
        self.proxy_pool.to_remove = list()
        self.proxy_pool.to_update = list()
        invalid_p = ProxyModel({'_id': '1', 'ip_address': '127.0.1.1', 'port': 80})
        invalid_p.invalid = True
        valid_p = ProxyModel({'_id': '2', 'ip_address': '127.0.2.1', 'port': 80})
        self.proxy_pool.add_to_pool(invalid_p)
        self.assertEqual(len(self.proxy_pool.to_remove), 1)
        self.proxy_pool.add_to_pool(valid_p)
        self.assertEqual(len(self.proxy_pool.to_update), 1)


class TestChain(TestCase):
    def test_task(self):
        task = Task({'name': 'demo'})
        handler = Handler('name', lambda p: 'omed')
        task.run_handler(handler)
        self.assertEqual(task.target['name'], 'omed')

    def test_chain(self):
        chain = RChain()
        self.assertEqual(chain.size(), len(chain.handlers))
        chain.append_handler(Handler('name', lambda p: 'demo-1'))
        self.assertEqual(len(chain.handlers), 1)
        chain.append_handler(Handler('name', lambda p: 'demo1'))
        insert_handler = Handler('name', lambda p: 'demo0.5')
        chain.insert_handler(1, insert_handler)
        self.assertEqual(len(chain.handlers), 3)
        self.assertEqual(chain.handlers[1], insert_handler)
        chain.remove_handler(1)
        self.assertEqual(len(chain.handlers), 2)
        chain.pop_handler()
        self.assertEqual(len(chain.handlers), 1)
        res_task = chain.start_handling(Task({'name': 'demo'}))
        self.assertEqual(res_task.target['name'], 'demo-1')


"""
How to mock import?
"""


class TestValidation(TestCase):
    def setUp(self):
        pass

    def test_connection(self):
        pass

    def test_proxy_type(self):
        pass

    def test_anonymity(self):
        pass

    def test_location(self):
        pass

    def test_db(self):
        pass


if __name__ == '__main__':
    main()
