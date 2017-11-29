# -*- coding: utf-8 -*-


from unittest import TestCase, mock, main

from .models.user import User
from .models.proxy import Proxy
from .models.database import Database


class TestDatabase(TestCase):
    def test_bind_to_model(self):
        mock_database = mock.MagicMock()
        mock_database['demo'] = mock.MagicMock()
        Database.database = mock_database
        mock_model = mock.MagicMock()
        Database('demo').bind_to_model(mock_model)
        self.assertIsInstance(mock_model.db_collection, Database)


class TestModel(TestCase):
    def setUp(self):
        User.db_collection = mock.MagicMock()
        Proxy.db_collection = mock.MagicMock()
        self.user = User({'_id': 'user-1', 'username': 'jferroal', 'password': '123123'})
        self.proxy = Proxy({
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown',
            'connection': []
        })

    def test_proxy_to_csv(self):
        self.assertEqual(self.proxy.to_csv(), '127.0.0.1:8080')
        self.assertEqual(self.proxy.to_csv(all_fields=True), '127.0.0.1:8080,(unknown),(unknown),(unknown, unknown),()')

    def test_proxy_list_all(self):
        find_res = [{
            '_id': '0',
            'ip_address': '127.0.0.1',
            'port': 8080,
            'proxy_type': ['unknown'],
            'anonymity': ['unknown'],
            'location': 'unknown, unknown',
            'connection': []
        }]
        Proxy.db_collection.find = mock.MagicMock(return_value=find_res)
        all_proxies = list(Proxy.list_all()['items'])
        self.assertIsNotNone(all_proxies)
        self.assertIsInstance(all_proxies[0], Proxy)

    def test_proxy_page(self):
        mock_limit = mock.MagicMock()
        mock_skip = mock.MagicMock(return_value=mock_limit)
        mock_sort = mock.MagicMock(return_value=mock_skip)
        Proxy.db_collection.find = mock.MagicMock(return_value=mock_sort)
        Proxy.db_collection.count = mock.MagicMock(return_value=10)
        Proxy.page(1, 10, {}, {}, [])
        Proxy.db_collection.find.assert_called_with(filter={}, projection={})
        Proxy.db_collection.count.assert_called_with(filter={})
        # FIXME: Fix following test
        # mock_sort.assert_called_with([('_id', -1)])
        # mock_skip.assert_called_with(10)
        # mock_limit.assert_called_with(10)

    def test_user_validate(self):
        User.db_collection.find_one = mock.MagicMock(return_value={'username': 'jferroal', 'password': '123123'})
        validation = User.validate(self.user.username, self.user.password)
        User.db_collection.find_one.assert_called_with({'username': 'jferroal', 'password': '123123'})
        self.assertTrue(validation)
        User.db_collection.find_one = mock.MagicMock(return_value=None)
        validation = User.validate(self.user.username, self.user.password)
        self.assertFalse(validation)


if __name__ == '__main__':
    main()
