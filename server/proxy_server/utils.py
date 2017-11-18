# -*- coding: utf-8 -*-
import math

from bottle import request, redirect


def generate_pagination(page_index, page_size, total_count):
    page_count = math.ceil(total_count / page_size)
    return {
        'page_count': page_count,
        'page_index': page_index,
        'next_page': page_index if page_index >= page_count else page_index + 1,
        'prev_page': 1 if page_index <= 1 else page_index - 1
    }


def login_required():
    sessions = request.environ.get('beaker.session')
    if not sessions.get('user'):
        return redirect('/login')