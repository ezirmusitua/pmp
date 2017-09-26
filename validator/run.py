# -*- coding:utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
from proxy_model import ProxyModel
from database import Database


def validate_proxy(proxy):
    ProxyModel(proxy).validate()


if __name__ == '__main__':
    db = Database()
    proxies = db.list()
    pool = ThreadPool(4)
    pool.map(validate_proxy, proxies)
    pool.close()
    pool.join()
