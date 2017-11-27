# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import json
from public import SimplestHttpServer, HTTPStatus
from proxy_validator.chain import Task
from proxy_validator.proxy import ProxyModel
from proxy_validator.database import Database
from proxy_validator.validation import validation_chain

global VALIDATION_TASK
VALIDATION_TASK = None


def get_stats(_req, res, _server):
    database = Database()
    database.connect()
    res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'application/json'}).end_headers()
    global VALIDATION_TASK
    result_json = {
        'is_validating': bool(VALIDATION_TASK and VALIDATION_TASK.is_alive()),
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


def _run_proxies_validation(_server):
    db = Database()
    db.connect()
    for p in db.list({}):
        t = Task(ProxyModel(p))
        validation_chain.start_handling(t)


def start_validation(_req, res, _server):
    from multiprocessing import Process
    res.set_status(HTTPStatus.OK).set_header('Content-Type', 'application/json').end_headers()
    global VALIDATION_TASK
    if not VALIDATION_TASK or not VALIDATION_TASK.is_alive():
        VALIDATION_TASK = Process(target=_run_proxies_validation, args=(_server,))
        VALIDATION_TASK.start()
        # do not add join, otherwise it will block
        res.send('{"status": "success"}').end_send()
    else:
        res.send('{"status": "failed"}').end_send()


def terminate_validation(_req, res, _server):
    res.set_status(HTTPStatus.OK).set_header('Content-Type', 'application/json').end_headers()
    global VALIDATION_TASK
    if not VALIDATION_TASK or not VALIDATION_TASK.is_alive():
        res.send('{"status": "failed"}').end_send()
    else:
        VALIDATION_TASK.terminate()
        res.send('{"status": "success"}').end_send()


server = SimplestHttpServer()
server.route('GET', '/', get_stats)
server.route('GET', '/proxies', query_proxies)
server.route('POST', '/validation_task', start_validation)
server.route('DELETE', '/validation_task', terminate_validation)
server.run()
