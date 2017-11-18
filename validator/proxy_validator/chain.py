# -*- coding: utf-8 -*-


class Handler(object):
    def __init__(self, name, handle_func):
        self.name = name
        self.handle_func = handle_func

    def handle(self, task):
        task.run_handler(self.handle_func)


class RChain(object):
    def __init__(self):
        self.handlers = list()

    def start_handling(self, task):
        for handler in self.handlers:
            handler.handle(task)

    def append_handler(self, handler):
        self.handlers.append(handler)
        return self

    def pop_handler(self):
        self.handlers.pop()
        return self

    def insert_handler(self, pos, handler):
        self.handlers = self.handlers[:pos] + [handler] + self.handlers[pos + 1:]

    def remove_handler(self, pos):
        self.handlers.pop(pos)

    def size(self):
        return len(self.handlers)

    def __str__(self):
        return 'RChain: ' + ', '.join(list(map(lambda h: h.name, self.handlers)))

    def __unicode__(self):
        return self.__str__()