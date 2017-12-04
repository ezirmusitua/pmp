# -*- coding: utf-8 -*-
import time
import sys

sys.path.append('..')

from public.config import Config
from proxy_validator import run_validation

config = Config('config.json')

if __name__ == '__main__':
    while True:
        print('running ... ')
        run_validation()
