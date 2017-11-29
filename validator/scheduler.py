# -*- coding: utf-8 -*-
import time

from proxy_validator import run_validation

if __name__ == '__main__':
    while True:
        run_validation()
        print('sleep for 100 seconds')
        time.sleep(100)
