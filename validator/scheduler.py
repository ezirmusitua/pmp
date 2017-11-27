# -*- coding: utf-8 -*-
import sys

sys.path.append('..')
import schedule
from proxy_validator.chain import Task
from proxy_validator.proxy import ProxyModel
from proxy_validator.database import Database
from proxy_validator.validation import validation_chain


def _do_proxies_validation():
    print('\n    Validation start.')
    db = Database()
    db.connect()
    for p in db.list({}):
        t = Task(ProxyModel(p))
        validation_chain.start_handling(t)
    print('\n    Validation done.')


while True:
    schedule.every(5).seconds.do(_do_proxies_validation)
    schedule.run_all()
