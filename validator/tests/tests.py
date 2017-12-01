# -*- coding: utf-8 -*-

import sys

sys.path.append('..')

from unittest import TestCase, mock, main
from proxy_validator.chain import RChain, Task, Handler
from proxy_validator.client import Client, Default_Timeout, Default_UA
from proxy_validator.models import Proxy


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
        self.proxy.last_check_at = -1

    def test_proxy_has_attribute_invalid(self):
        self.assertEqual(self.proxy.invalid, False)

    def test_proxy_get_and_set_item(self):
        self.assertEqual(self.proxy['invalid'], False)
        self.proxy['invalid'] = True
        self.assertEqual(self.proxy.invalid, True)


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


# TODO: How to mock import?
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
