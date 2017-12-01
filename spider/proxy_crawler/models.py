# -*- coding: utf-8 -*-
from random import choice
from scrapy.utils.project import get_project_settings

from public.models import ProxyModel
from public.database import Database


class SpiderDatabase(Database):
    def __init__(self, *args, **kwargs):
        super(SpiderDatabase, self).__init__(*args, **kwargs)


settings = get_project_settings()
SpiderDatabase.uri = settings.get('MONGO_URI')
SpiderDatabase.db_name = settings.get('MONGO_DATABASE')


class Proxy(ProxyModel):
    db_collection = None

    def __init__(self, *args, **kwargs):
        super(Proxy, self).__init__(*args, **kwargs)

    @staticmethod
    def save(item):
        Proxy.db_collection.update({
            'ip_address': item['ip_address'], 'port': item['port']
        }, dict(item), upsert=True)

    @staticmethod
    def get_random_usable_one_proxy(spider_name):
        usable_proxies = list(map(lambda p: Proxy(p), Proxy.db_collection.list(
            query={'connection': spider_name, 'proxy_type': {'$in': ['http', 'https']}},
            sort=[('last_check_at', SpiderDatabase.A_ORDER)],
            limit=20)))
        if not usable_proxies:
            return None
        return str(choice(usable_proxies))


def bind_models():
    SpiderDatabase(settings.get('PROXY_MODEL_NAME')).bind_to_model(Proxy)
