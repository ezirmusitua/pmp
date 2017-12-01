# -*- coding: utf-8 -*-
from unittest import TestCase, mock, main

from .models import ProxyModel
from .database import Database
from .decorators import singleton


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


class TestDatabase(TestCase):
    def setUp(self):
        self.database = Database('demo')
        self.database.collection = mock.MagicMock()
        self.mock_find_return = mock.MagicMock()
        self.mock_find_return.batch_size = mock.MagicMock(return_value=[0, 1, 2])
        self.database.collection.find = mock.MagicMock(return_value=self.mock_find_return)
        self.database.collection.insert = mock.MagicMock(return_value=None)
        self.database.collection.update = mock.MagicMock(return_value=None)
        self.database.collection.remove = mock.MagicMock(return_value=None)

    def test_bind_to_model(self):
        mock_database = mock.MagicMock()
        mock_database['demo'] = mock.MagicMock()
        Database.database = mock_database
        mock_model = mock.MagicMock()
        Database('demo').bind_to_model(mock_model)
        self.assertIsInstance(mock_model.db_collection, Database)

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
        self.database.collection.update.assert_called_with({}, {'ip': '127.0.0.1'}, upsert=False)

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
        self.database.collection.update.assert_called_with({'_id': '1'}, {'ip': '127.0.0.1'})

        self.database.collection.find_one = mock.MagicMock(return_value=None)
        self.database.find_one_and_update({'_id': '1'}, {'ip': '127.0.0.1'})
        self.database.collection.insert.assert_called_with({'ip': '127.0.0.1'})


class TestProxyModel(TestCase):
    def setUp(self):
        ProxyModel.db_collection = mock.MagicMock()
        self.proxy = ProxyModel({
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown',
            'connection': []
        })

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

    def test_getitem(self):
        self.assertEqual(self.proxy['port'], 8080)
        with self.assertRaises(KeyError):
            self.proxy['error_key']

    def test_setitem(self):
        proxy = ProxyModel({
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown',
            'connection': []
        })
        proxy['port'] = 80
        self.assertEqual(proxy.port, 80)
        with self.assertRaises(KeyError):
            proxy['error_key'] = -1


if __name__ == '__main__':
    main()
