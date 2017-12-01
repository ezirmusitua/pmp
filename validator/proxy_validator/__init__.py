# -*- coding: utf-8 -*-
import logging
from public.config import Config, concat_config_path

config = Config(concat_config_path(__file__, 'config.json'))

logging.basicConfig(
    filename=config['LOG_FILE'],
    level=config['LOG_LEVEL'],
    format=config['LOG_FORMAT'],
)


def run_validation():
    from .chain import Task
    from .models import Proxy, bind_models
    from .validation import validation_chain
    bind_models()
    logging.info('validation start. ')
    for p in Proxy.list({}):
        proxy = Proxy(p)
        logging.info('validating proxy: %s' % proxy)
        t = Task(proxy)
        validation_chain.start_handling(t)
        logging.info('proxy: %s validated' % proxy)
    logging.info('validation done. ')
