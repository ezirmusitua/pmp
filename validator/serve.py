# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import json
from public import SimplestHttpServer, HTTPStatus
from proxy_validator.chain import Task
from proxy_validator.proxy import ProxyModel
from proxy_validator.database import Database
from proxy_validator.validation import validation_chain


def get_stats(_req, res, _server):
    database = Database()
    database.connect()
    res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'application/json'}).end_headers()
    total_count = database.count()
    res.send('{"total_usable_count": %s}' % str(total_count)).end_send()


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


def _run_proxies_validation(_server):
    db = Database()
    db.connect()
    for p in db.list({}):
        print('validating %s' % p)
        t = Task(ProxyModel(p))
        validation_chain.start_handling(t)


def start_validation(_req, res, _server):
    print(_server.env)
    from multiprocessing import Process
    p = Process(target=_run_proxies_validation, args=(_server,))
    p.start()
    # do not add join, otherwise it will block
    res.set_status(HTTPStatus.OK).set_header('Content-Type', 'text/html').end_headers()
    res.send('<html><body><p>Start validation task</p></body></html>').end_send()


if __name__ == '__main__':
    global_stats = {'is_running': False}
    server = SimplestHttpServer()
    server.route('GET', '/', get_stats)
    server.route('GET', '/proxies', query_proxies)
    server.route('POST', '/validation_task', start_validation)
    server.run()
