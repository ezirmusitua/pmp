# -*- coding: utf-8 -*-
from unittest import TestCase, mock, main

from proxy_server.models import Proxy, Token
from proxy_server.route import check_user


class TestModel(TestCase):
    def setUp(self):
        Proxy.db_collection = mock.MagicMock()
        Token.db_collection = mock.MagicMock()
        self.test_token_dict = {
            '_id': 'd1',
            'salt': '123',
            'token': '263fec58861449aacc1c328a4af' +
                     'f64aff4c62df4a2d50b3f207fa8' +
                     '9b6e242c9aa778e7a8baeffef85' +
                     'b6ca6d2e7dc16ff0a760d59c13c' +
                     '238f6bcdc32f8ce9cc62',
            'create_at': 0
        }

    def test_proxy_search_with_no_search_params(self):
        # input search params is None, use empty query
        Proxy.db_collection.list = mock.MagicMock(return_value=list())
        res = Proxy.search(None, None, None, 10)
        self.assertEqual(res, list())
        Proxy.db_collection.list.assert_called_with({}, limit=10)

    def test_proxy_search_with_no_size(self):
        Proxy.db_collection.list = mock.MagicMock(return_value=list())
        # input size is None, use 20 as default
        res = Proxy.search(['http'], ['baidu'], ['elite'])
        self.assertEqual(res, list())
        Proxy.db_collection.list.assert_called_with({
            'proxy_type': {'$in': ['http']},
            'connection': {'$in': ['baidu']},
            'anonymity': {'$in': ['elite']}
        }, limit=20)

    def test_proxy_search_return(self):
        # return value should be proxy string list
        Proxy.db_collection.list = mock.MagicMock(return_value=[
            Proxy({
                '_id': '0',
                'ip_address': '127.0.0.1',
                'port': 8080,
                'proxy_type': ['unknown'],
                'anonymity': ['unknown'],
                'location': 'unknown, unknown',
                'connection': []
            })
        ])
        print(Proxy.db_collection.list())
        res = Proxy.search(None, None, None)
        self.assertEqual(res, ['127.0.0.1:8080'])

    def test_token_hash(self):
        import hashlib
        self.assertTrue(hashlib.sha512('123123'.encode()), Token.hash('123', '123'))

    def test_token_find(self):
        token = Token(self.test_token_dict)
        Token.db_collection.list = mock.MagicMock(return_value=[self.test_token_dict])
        result = Token.find('123')
        self.assertIsInstance(result, Token)
        self.assertEqual(result.token, token.token)
        self.assertIsNone(Token.find('12345'))

    def test_token_validate(self):
        Token.db_collection.list = mock.MagicMock(return_value=[self.test_token_dict])
        self.assertTrue(Token.find('123'))
        self.assertFalse(Token.find('12345'))


class TestHelper(TestCase):
    def test_check_user(self):
        self.assertTrue(check_user('admin', '123123'))
        self.assertFalse(check_user('admin', '123456'))
        self.assertFalse(check_user('admin1', '123123'))


if __name__ == '__main__':
    main()
