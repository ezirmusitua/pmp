# -*- coding: utf-8 -*-
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimplestRequest(object):
    def __init__(self, command, path, headers, rfile):
        self.__command = command
        self.__path = path
        self.__headers = headers
        self.__rfile = rfile

    @property
    def url(self):
        return self.__path

    @property
    def method(self):
        return self.__command


class SimplestResponse(object):
    def __init__(self, request, status_setter, headers_setter, wfile):
        self.__request = request
        self.__status_setter = status_setter
        self.__headers_setter = headers_setter
        self.__wfile = wfile
        self.response_content_to_send = ''

    def set_status(self, status=HTTPStatus.OK, message=''):
        self.__status_setter['set'](status, message)

    def set_headers(self, headers=None):
        if not headers: return
        for hkey, hval in headers.items():
            self.__headers_setter['set'](hkey, hval)
        self.__headers_setter['end']()

    def send(self, content):
        self.response_content_to_send += content
        return self

    def end_send(self):
        print(self.__wfile)
        self.__wfile.write(self.response_content_to_send.encode())


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
            def __init__(self, *args, **kwargs):
                self.__get_routes = {}
                self.__post_routes = {}
                super(BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

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
                get_routes[self.path](req, res)

            def do_POST(self):
                req, res = self.create_req_res()
                post_routes[self.path](req, res)

        return SimplestHttpRequestHandler

    def run(self):
        httpd = HTTPServer(self.server_address, self.generate_handler_cls())
        print('\nStarting httpd...')
        httpd.serve_forever()


if __name__ == '__main__':
    server = SimplestHttpServer(('127.0.0.1', 81))


    def index(req, res):
        res.set_status()
        res.set_headers({'Content-type': 'text/html'})
        res.send('<html><body><p>Hello, %s</p></body></html>' % req.url).end_send()


    server.route('GET', '/Jferroal', index)

    server.run()
