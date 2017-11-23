# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimplestResponse(object):
    def __init__(self, command, path, headers, wfile):
        self.__command = command
        self.__path = path
        self.__headers = headers
        self.__wfile = wfile


class SimplestRequest(object):
    def __init__(self, request, make_response, rfile):
        self.__request = request
        self.__make_response = make_response
        self.__rfile = rfile


class SimplestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__get_routes = list()
        self.__post_routes = list()

    def make_response(self, status, response_headers):
        # headers
        # status
        pass

    def create_req_res(self):
        req = SimplestRequest(self.command, self.path, self.headers, self.rfile)
        res = SimplestResponse(self.request, self.make_response, self.rfile)
        return req, res

    def route(self, method, path):
        # decorator to wrap func as route handler
        # parse path, and set in get/post_routes
        pass

    def do_GET(self):
        req, res = self.create_req_res()
        # dispatch to get_routes
        pass

    def do_POST(self):
        req, res = self.create_req_res()
        # dispatch to get_routes
        pass


def run(server_class=HTTPServer, handler_class=SimplestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('\nStarting httpd...')
    httpd.serve_forever()
