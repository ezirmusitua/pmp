# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import json
from multiprocessing import Process
import schedule
from public import SimplestHttpServer, HTTPStatus
from proxy_validator.chain import Task
from proxy_validator.proxy import ProxyModel
from proxy_validator.database import Database
from proxy_validator.validation import validation_chain

global USER_VALIDATION_TASK
USER_VALIDATION_TASK = None
global SCHEDULER_VALIDATION_TASK
SCHEDULER_VALIDATION_TASK = None

server = SimplestHttpServer()


def is_validation_running():
    global USER_VALIDATION_TASK
    global SCHEDULER_VALIDATION_TASK
    is_user_running = bool(USER_VALIDATION_TASK and USER_VALIDATION_TASK.is_alive())
    is_scheduler_running = bool(SCHEDULER_VALIDATION_TASK and SCHEDULER_VALIDATION_TASK.is_alive())
    return is_user_running or is_scheduler_running


def run_validation_task(vname='user'):
    if is_validation_running():
        return False
    global USER_VALIDATION_TASK
    global SCHEDULER_VALIDATION_TASK
    if vname == 'user':
        USER_VALIDATION_TASK = Process(target=_do_proxies_validation)
        USER_VALIDATION_TASK.start()
    else:
        SCHEDULER_VALIDATION_TASK = Process(target=_do_proxies_validation)
        SCHEDULER_VALIDATION_TASK.start()
    return True


def schedule_validation_task():
    global SCHEDULER_VALIDATION_TASK

    def task():
        run_validation_task('scheduler')

    print('\n    Scheduler started. ')
    schedule.every(2).hours.do(task)
    schedule.run_pending()


scheduler = Process(target=schedule_validation_task)


def get_stats(_req, res, _server):
    database = Database()
    database.connect()
    res.set_status(HTTPStatus.OK).set_headers({'Content-Type': 'application/json'}).end_headers()
    result_json = {
        'is_validating': is_validation_running(),
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


def _do_proxies_validation():
    db = Database()
    db.connect()
    for p in db.list({}):
        t = Task(ProxyModel(p))
        validation_chain.start_handling(t)


def start_validation(_req, res, _server):
    res.set_status(HTTPStatus.OK).set_header('Content-Type', 'application/json').end_headers()
    is_running = run_validation_task()
    res.send('{"status": "%s"}' % 'success' if is_running else 'failed').end_send()


def terminate_validation(_req, res, _server):
    # can only terminate user validation task
    res.set_status(HTTPStatus.OK).set_header('Content-Type', 'application/json').end_headers()
    global USER_VALIDATION_TASK
    if not USER_VALIDATION_TASK or not USER_VALIDATION_TASK.is_alive():
        res.send('{"status": "failed"}').end_send()
    else:
        USER_VALIDATION_TASK.terminate()
        res.send('{"status": "success"}').end_send()


server.route('GET', '/', get_stats)
server.route('GET', '/proxies', query_proxies)
server.route('POST', '/validation_task', start_validation)
server.route('DELETE', '/validation_task', terminate_validation)
scheduler.start()
server.run()
