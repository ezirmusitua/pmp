# -*- coding:utf-8 -*-
from proxy_model import ProxyModel
from database import Database


def run_validate():
    db = Database()
    for p in db.list():
        proxy = ProxyModel(p)
        proxy.validate()
    ProxyModel.flush_docs()


if __name__ == '__main__':
    run_validate()
