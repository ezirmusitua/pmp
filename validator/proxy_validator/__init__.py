# -*- coding: utf-8 -*-
from .chain import Task
from .proxy import ProxyModel
from .database import Database
from .validation import validation_chain


def run_validation():
    db = Database()
    db.connect()
    for p in db.list({}):
        t = Task(ProxyModel(p))
        validation_chain.start_handling(t)
