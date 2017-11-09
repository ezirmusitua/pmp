# -*- coding: utf-8 -*-
import math


def generate_pagination(page_index, page_size, total_count):
    page_count = math.ceil(total_count / page_size)
    return {
        'page_count': page_count,
        'page_index': page_index,
        'next_page': page_index if page_index >= page_count else page_index + 1,
        'prev_page': 1 if page_index <= 1 else page_index - 1
    }


def validate_is_login(request, redirect, target):
    sessions = request.environ.get('beaker.session')
    redirect(target) if sessions.get('user') else None


def validate_not_login(request, redirect):
    sessions = request.environ.get('beaker.session')
    redirect('/login') if not sessions.get('user') else None
