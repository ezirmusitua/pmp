# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import json
from public import SimplestHttpServer, HTTPStatus
from proxy_validator.database import Database
from proxy_validator.proxy import ProxyModel

database = Database()
database.connect()


def stats(req, res):
    res.set_status(HTTPStatus.OK)
    res.set_headers({'Content-Type': 'application/json'})
    res.send('{"running": true, ') \
        .send('"total_usable_count": 100}').end_send()


def query_proxies(req, res):
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
    res.set_status()
    res.set_headers({'Content-Type': 'application/json'})
    res.send(return_str).end_send()


if __name__ == '__main__':
    server = SimplestHttpServer()
    server.route('GET', '/', stats)
    server.route('GET', '/proxies', query_proxies)
    server.run()
