# -*- coding: utf-8 -*-
import re
import base64

PROXY_DB_VAR_1_PATTERN = re.compile(r"var .+? = '([\d.]+)'\.split\(''\)\.reverse\(\)\.join\(''\);")
PROXY_DB_VAR_2_PATTERN_1 = re.compile(r"var .+? = '([\d.]+)';")
PROXY_DB_VAR_2_PATTERN_2 = re.compile(r"var .+? = atob\('(.+?)'")
PROXY_DB_VAR_P_PATTERN = re.compile(r"var .+? = ([\-\d]+) \+ ([\-\d]+);")


def get_list_item_safely(list_in, idx, default=''):
    if list_in is not None and len(list_in) > idx:
        return list_in[idx]
    return default


def generate_proxydb_js_ip_port(code_segment):
    x = re.search(PROXY_DB_VAR_1_PATTERN, code_segment).groups()[0]
    x_tmp = list(x)
    x_tmp.reverse()
    try:
        y = re.search(PROXY_DB_VAR_2_PATTERN_1, code_segment).groups()[0]
    except AttributeError:
        # not match
        y_tmp = re.search(PROXY_DB_VAR_2_PATTERN_2, code_segment).groups()[0]
        base64_y = ''
        for hex_char_code in re.findall(r'\\x([0-9A-Fa-f]{2})', y_tmp):
            base64_y += chr(int(hex_char_code, 16))
        y = base64.decodebytes(base64_y.encode()).decode('utf-8')
    p = re.search(PROXY_DB_VAR_P_PATTERN, code_segment).groups()
    ip_address = ''.join(x_tmp) + y
    port = int(p[0]) + int(p[1])
    return ip_address, str(port)
