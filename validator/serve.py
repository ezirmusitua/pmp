# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import json
from public import SimplestHttpServer, HTTPStatus
from proxy_validator.proxy import ProxyModel
from proxy_validator.database import Database

server = SimplestHttpServer()


def get_stats(_req, res, _server):
    database = Database()
    database.connect()
    res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'application/json'}).end_headers()
    result_json = {
        'total_usable_count': database.count()
    }
    res.send(json.dumps(result_json)).end_send()


def query_proxies(req, res, _server):
    database = Database()
    database.connect()
    query = dict()
    if req.params.has_param('location'):
        query['location'] = req.params.location
    if req.params.has_param('proxy_type'):
        query['proxy_type'] = req.params.proxy_type
    if req.params.has_param('connection'):
        query['connection'] = req.params.connection
    if req.params.has_param('anonymity'):
        query['anonymity'] = req.params.anonymity
    # TODO: Extract database and model to public
    return_str = json.dumps(list(map(lambda p: ProxyModel(p).to_json(), database.list(query))))
    res.set_status().set_headers({'Content-Type': 'application/json'}).end_headers()
    res.send(return_str).end_send()


server.route('GET', '/', get_stats)
server.route('GET', '/proxies', query_proxies)
server.run()
