# -*- coding: utf-8 -*-
import functools
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimplestRequest(object):
    def __init__(self, command, path, headers, rfile):
        self.__command = command
        self.__path = path
        self.__headers = headers
        self.__rfile = rfile


class SimplestResponse(object):
    def __init__(self, request, make_response, wfile):
        self.__request = request
        self.__make_response = make_response
        self.__wfile = wfile


class SimplestHandler(BaseHTTPRequestHandler):
    __get_routes = dict()
    __post_routes = dict()

    def make_response(self, status, response_headers):
        # headers
        # status
        pass

    def create_req_res(self):
        req = SimplestRequest(self.command, self.path, self.headers, self.rfile)
        res = SimplestResponse(self.request, self.make_response, self.rfile)
        return req, res

    def route(self, method, path, handler):
        # decorator to wrap func as route handler
        # parse path, and set in get/post_routes
        if method == 'GET':
            SimplestHandler.__get_routes[path] = handler
        if method == 'POST':
            SimplestHandler.__post_routes[path] = handler

    def get(self, route_handler, path):
        @functools.wraps(route_handler)
        def wrapped():
            self.route('GET', path, route_handler)

        return wrapped

    def post(self, path, route_handler):
        @functools.wraps(route_handler)
        def wrapped():
            self.route('POST', path, route_handler)

        return wrapped

    def do_GET(self):
        req, res = self.create_req_res()
        self.__get_routes[self.path](req, res)

    def do_POST(self):
        req, res = self.create_req_res()
        self.__post_routes[self.path](req, res)


# 细细一想,事情并没有那么简单,,,
# 1. 看 HTTPServer 的源码,了解调用 Handler 过程
# 2. 外部实现,将 __routes 作为类变量,要保证单例

def run(server_class=HTTPServer, handler_class=SimplestHandler, port=81):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('\nStarting httpd...')
    httpd.serve_forever()


run()
