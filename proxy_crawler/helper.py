# -*- coding: utf-8 -*-
import re

X_PATTERN = re.compile(r"var x = '([\d\.]+)'\.split\(''\)\.reverse\(\)\.join\(''\);")
Y_PATTERN = re.compile(r"var y = '([\d\.]+)';")
P_PATTERN = re.compile(r"var p = ([\-\d]+) \+ ([\-\d]+);")


def generate_proxydb_js_ip_port(code_segment):
    x = re.search(X_PATTERN, code_segment).groups()[0]
    x_tmp = list(x)
    x_tmp.reverse()
    y = re.search(Y_PATTERN, code_segment).groups()[0]
    p = re.search(P_PATTERN, code_segment).groups()
    ip_address = ''.join(x_tmp) + y
    port = int(p[0]) + int(p[1])
    return ip_address, port
