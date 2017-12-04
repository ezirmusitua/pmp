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
    from proxy_validator.chain import Task
    from proxy_validator.models import Proxy, ValidatorDatabase, bind_models
    from proxy_validator.validation import validation_chain
    bind_models()
    logging.info('validation start. ')
    for p in Proxy.list({}, sort=[('last_check_at', ValidatorDatabase.A_ORDER)], batch_size=10):
        proxy = Proxy(p)
        logging.info('validating proxy: %s' % proxy)
        t = Task(proxy)
        validation_chain.start_handling(t)
        logging.info('proxy: %s validated' % proxy)
    logging.info('validation done. ')
