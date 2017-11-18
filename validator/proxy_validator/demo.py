# -*- coding: utf-8 -*-


class RequestToHandle(object):
    def __init__(self, _next):
        self.value = 3
        self._next = _next

    def update_next(self):
        if self.value is 6:
            self._next = 'div'
        elif self.value == 3.0:
            self._next = 'add'
        else:
            self._next = None

    def is_end(self):
        return self._next is None

    def should_handle(self, handler):
        return self._next is handler.name

    def __mul__(self, other):
        self.value = self.value * other
        return self

    def __truediv__(self, other):
        self.value = self.value / other
        return self

    def __add__(self, other):
        self.value = self.value + other
        return self


class ChainHandler(object):
    def __init__(self, handler, name):
        self.handler = handler
        self._name = name

    def handle(self, request):
        self.handler(request)
        request.update_next()
        return request

    @property
    def name(self):
        return self._name


class RChain(object):
    def __init__(self, chain_handlers=None):
        self.chain_handlers = list() if chain_handlers is None else chain_handlers

    def handle(self, request):
        h_index = 0
        while True:
            handler = self.chain_handlers[h_index]
            if request.is_end():
                break
            if not request.should_handle(handler):
                h_index += 1
                continue
            request = handler.handle(request)
            h_index += 1
            if h_index >= len(self.chain_handlers):
                h_index = 0
        return request

    def add_handler(self, handler):
        self.chain_handlers.append(handler)


if __name__ == '__main__':
    chain = RChain()


    def mul2(val):
        return val * 2


    ch1 = ChainHandler(mul2, 'mul')
    chain.add_handler(ch1)


    def add2(val):
        return val + 2


    ch2 = ChainHandler(add2, 'add')
    chain.add_handler(ch2)


    def div2(val):
        return val / 2


    ch3 = ChainHandler(div2, 'div')
    chain.add_handler(ch3)

    req = RequestToHandle('mul')
    res = chain.handle(req)
    print(res.value)
