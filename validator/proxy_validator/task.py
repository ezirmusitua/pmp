# -*- coding: utf-8 -*-


class Task(object):
    def __init__(self, target):
        self.target = target

    def run_handler(self, handler):
        self.target.set_result(handler.name, handler.handle(self.target))
