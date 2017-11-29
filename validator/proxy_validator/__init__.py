# -*- coding: utf-8 -*-
from .chain import Task
from .models import Proxy
from .validation import validation_chain

from public.database import Database


def run_validation():
    print('validation start. ')
    for p in Proxy.list({}):
        proxy = Proxy(p)
        print('validating proxy: %s' % proxy)
        t = Task(proxy)
        validation_chain.start_handling(t)
        print('proxy: %s validated' % proxy)
    print('validation done. ')
