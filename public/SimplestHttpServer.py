# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer


class Param(object):
    def __init__(self, path_parse_result, read_stream, headers):
        self._headers = headers
        self._parse_result = path_parse_result
        self._body = read_stream.read(headers.get('content-length', 0))
        self._query = Param.convert_query(self._parse_result.query)
        self._body = Param.convert_body(self._body, headers.get('content-type', 'text/html'))

    def __getattr__(self, attr_name):
        if type(self._body) is bytes:
            attr_in_body = None
        else:
            attr_in_body = self._body.get(attr_name, None)
        if attr_in_body:
            return attr_in_body
        attr_in_query = self._query.get(attr_name, None)
        if attr_in_query:
            return attr_in_query
        raise KeyError

    @staticmethod
    def convert_query(query_string):
        result = dict()
        if not query_string: return result
        tmp_list = map(lambda q: q.split('='), query_string.split('&'))
        for kv in tmp_list:
            result[kv[0]] = kv[1]
        return result

    @staticmethod
    def convert_body(raw_body, content_type):
        print('raw body', raw_body)
        lower_type = content_type.lower()
        if lower_type is 'application/x-www-form-urlencoded':
            return Param.convert_query(raw_body)
        if lower_type is 'application/json':
            from json import loads
            return loads(raw_body)
        # unknown type, plain or octet-stream just return the original one
        return raw_body


class SimplestRequest(object):
    def __init__(self, command, path, headers, read_stream):
        url_parse_result = urlparse(path)
        self.__command = command
        self.__path = path
        self.__url = url_parse_result.path
        self.__headers = headers
        self.__read_stream = read_stream
        self._params = Param(url_parse_result, read_stream, headers)

    @property
    def params(self):
        return self._params

    @property
    def url(self):
        return self.__url

    @property
    def method(self):
        return self.__command


class SimplestResponse(object):
    def __init__(self, request, status_setter, headers_setter, write_stream):
        self.__request = request
        self.__status_setter = status_setter
        self.__headers_setter = headers_setter
        self.__write_stream = write_stream
        self.response_content_to_send = ''

    def set_status(self, status=HTTPStatus.OK, message=''):
        self.__status_setter['set'](status, message)

    def set_headers(self, headers=None):
        if not headers: return
        for hkey, hval in headers.items():
            # convert all header key to lowercase
            self.__headers_setter['set'](hkey.lower(), hval)
        self.__headers_setter['end']()

    def send(self, content):
        self.response_content_to_send += content
        return self

    def end_send(self):
        print(self.__write_stream)
        self.__write_stream.write(self.response_content_to_send.encode())


class SimplestHttpServer(object):
    def __init__(self, server_address=('', 80)):
        self.server_address = server_address
        self.__get_routes = {}
        self.__post_routes = {}

    def route(self, method, path, handler):
        if method == 'GET':
            self.__get_routes[path] = handler
        if method == 'POST':
            self.__post_routes[path] = handler

    def generate_handler_cls(self):
        get_routes = self.__get_routes
        post_routes = self.__post_routes

        class SimplestHttpRequestHandler(BaseHTTPRequestHandler):
            @property
            def status_setter(self):
                return {'set': self.send_response}

            @property
            def headers_setter(self):
                return {'set': self.send_header, 'end': self.end_headers}

            def create_req_res(self):
                req = SimplestRequest(self.command, self.path, self.headers, self.rfile)
                res = SimplestResponse(self.request, self.status_setter, self.headers_setter, self.wfile)
                return req, res

            def do_GET(self):
                req, res = self.create_req_res()
                get_routes[req.url](req, res)

            def do_POST(self):
                req, res = self.create_req_res()
                post_routes[req.url](req, res)

        return SimplestHttpRequestHandler

    def run(self):
        httpd = HTTPServer(self.server_address, self.generate_handler_cls())
        print('\nStarting httpd...')
        httpd.serve_forever()


if __name__ == '__main__':
    server = SimplestHttpServer(('127.0.0.1', 81))


    def index(req, res):
        res.set_status(HTTPStatus.OK)
        res.set_headers({'Content-Type': 'text/html'})
        res.send('<html><body><p>Hello, %s</p></body></html>' % req.url).end_send()


    def display_query(req, res):
        res.set_status(HTTPStatus.OK)
        res.set_headers({'Content-Type': 'text/html'})
        res.send('<html><body><p>Hello, %s</p></body></html>' % req.params.name).end_send()


    server.route('GET', '/Jferroal', index)
    server.route('GET', '/query', display_query)

    server.run()
