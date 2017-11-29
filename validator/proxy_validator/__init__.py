# -*- coding: utf-8 -*-
from .chain import Task
from .proxy import ProxyModel
from .database import Database
from .validation import validation_chain


def run_validation():
    db = Database()
    db.connect()
    print('validation start. ')
    for p in db.list({}):
        proxy = ProxyModel(p)
        print('validating proxy: %s' % proxy)
        t = Task(proxy)
        validation_chain.start_handling(t)
        print('proxy: %s validated' % proxy)
    print('validation done. ')
