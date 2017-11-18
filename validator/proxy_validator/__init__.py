# -*- coding: utf-8 -*-
from proxy_validator.proxy import ProxyModel
from proxy_validator.database import Database
from proxy_validator.task import Task
from proxy_validator.validation import validation_chain


def run_validation():
    db = Database()
    for p in db.list({}):
        t = Task(ProxyModel(p))
        validation_chain.start_handling(t)
