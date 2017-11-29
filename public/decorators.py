# -*- coding:utf-8 -*-
import functools


def singleton(class_):
    instances = {}

    @functools.wraps(class_)
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
