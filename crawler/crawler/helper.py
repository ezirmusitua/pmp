# -*- coding: utf-8 -*-
import re

PROXY_DB_VAR_1_PATTERN = re.compile(r"var .+? = '([\d.]+)'\.split\(''\)\.reverse\(\)\.join\(''\);")
PROXY_DB_VAR_2_PATTERN = re.compile(r"var .+? = '([\d.]+)';")
PROXY_DB_VAR_P_PATTERN = re.compile(r"var .+? = ([\-\d]+) \+ ([\-\d]+);")


def get_list_item_safely(list_in, idx, default=''):
    if list_in is not None and len(list_in) > idx:
        return list_in[idx]
    return default


def generate_proxydb_js_ip_port(code_segment):
    x = re.search(PROXY_DB_VAR_1_PATTERN, code_segment).groups()[0]
    x_tmp = list(x)
    x_tmp.reverse()
    y = re.search(PROXY_DB_VAR_2_PATTERN, code_segment).groups()[0]
    p = re.search(PROXY_DB_VAR_P_PATTERN, code_segment).groups()
    ip_address = ''.join(x_tmp) + y
    port = int(p[0]) + int(p[1])
    return ip_address, port
