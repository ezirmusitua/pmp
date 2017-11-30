# -*- coding: utf-8 -*-
from .chain import Task
from .models import Proxy, bind_models
from .validation import validation_chain


def run_validation():
    bind_models()
    print('validation start. ')
    for p in Proxy.list({}):
        proxy = Proxy(p)
        print('validating proxy: %s' % proxy)
        t = Task(proxy)
        validation_chain.start_handling(t)
        print('proxy: %s validated' % proxy)
    print('validation done. ')
