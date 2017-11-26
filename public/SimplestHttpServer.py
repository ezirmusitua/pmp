# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer


class Param(object):
    def __init__(self, path_parse_result, read_stream, headers):
        self._headers = headers
        self._parse_result = path_parse_result
        self._body = read_stream.read(int(headers.get('content-length', 0)))
        self._query = Param.convert_query(self._parse_result.query)
        self._body = Param.convert_body(self._body, headers.get('content-type', 'text/html'))

    def __getattr__(self, param_name):
        if self.is_param_in_body(param_name):
            return self._body.get(param_name, None)
        if self.is_param_in_query(param_name):
            return self._query.get(param_name, None)
        raise KeyError

    def has_param(self, param_name):
        return self.is_param_in_body(param_name) or self.is_param_in_query(param_name)

    def is_param_in_body(self, param_name):
        return type(self._body) is not bytes and not self._body.get(param_name, None)

    def is_param_in_query(self, param_name):
        return not self._query.get(param_name, None)

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
        lower_type = content_type.lower()
        if lower_type == 'application/x-www-form-urlencoded':
            # TODO: May be support this, but not now
            # return Param.convert_query(raw_body)
            return raw_body
        if lower_type == 'application/json':
            # I only need this
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
        return self

    def set_header(self, key, value):
        if not key or not value: return self
        self.__headers_setter['set'](key.lower(), value)
        return self

    def set_headers(self, headers=None):
        items = headers.items() if headers is not None else []
        if not headers: return
        for hkey, hval in items:
            # convert all header key to lowercase
            self.__headers_setter['set'](hkey.lower(), hval)
        return self

    def end_headers(self):
        self.__headers_setter['end']()
        return self

    def send(self, content):
        self.response_content_to_send += content
        return self

    def end_send(self):
        print(self.__write_stream)
        self.__write_stream.write(self.response_content_to_send.encode())


class SimplestHttpServer(object):
    def __init__(self, server_address=('', 3000)):
        self.server_address = server_address
        self.__get_routes = {}
        self.__post_routes = {}
        self.env = {'is_running': False}

    def route(self, method, path, handler):
        if method == 'GET':
            self.__get_routes[path] = handler
        if method == 'POST':
            self.__post_routes[path] = handler

    def generate_handler_cls(self):
        get_routes = self.__get_routes
        post_routes = self.__post_routes
        _server = self

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
                get_routes[req.url](req, res, _server)

            def do_POST(self):
                req, res = self.create_req_res()
                post_routes[req.url](req, res, _server)

        return SimplestHttpRequestHandler

    def run(self):
        httpd = HTTPServer(self.server_address, self.generate_handler_cls())
        print('\nStarting httpd...')
        httpd.serve_forever()


if __name__ == '__main__':
    server = SimplestHttpServer(('127.0.0.1', 3000))


    def index(req, res):
        # curl localhost:81/Jferroal
        res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'text/html'}).end_headers()
        res.send('<html><body><p>Hello, %s</p></body></html>' % req.url).end_send()


    def display_query(req, res):
        # curl localhost:81/query?name=jferroal
        res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'text/html'}).end_headers()
        res.send('<html><body><p>Hello, %s</p></body></html>' % req.params.name).end_send()


    def display_json_body(req, res):
        # curl -H "Content-Type: application/json" -X POST -d '{"name":"jferroal"}' localhost:81/json_body
        res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'text/html'}).end_headers()
        res.send('<html><body><p>Hello, %s</p></body></html>' % req.params.name).end_send()


    server.route('GET', '/Jferroal', index)
    server.route('GET', '/query', display_query)
    server.route('POST', '/json_body', display_json_body)

    server.run()
