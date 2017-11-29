# -*- coding: utf-8 -*-
from random import choice
from scrapy.utils.project import get_project_settings

from public.models import ProxyModel
from public.database import Database, bind_models, update_database_uri


class SpiderDatabase(Database):
    def __init__(self, *args, **kwargs):
        super(SpiderDatabase, self).__init__(*args, **kwargs)


settings = get_project_settings()
update_database_uri(SpiderDatabase, settings.get('MONGO_URI'), settings.get('MONGO_DATABASE'))


class Proxy(ProxyModel):
    def __init__(self, *args, **kwargs):
        super(Proxy, self).__init__(*args, **kwargs)

    @staticmethod
    def save(item):
        Proxy.db_collection.update({
            'ip_address': item['ip_address'], 'port': item['port']
        }, {'$set': dict(item)}, upsert=True)

    @staticmethod
    def get_random_usable_one_proxy(spider_name):
        usable_proxies = map(lambda p: Proxy(p), Proxy.db_collection.find(
            {'connection': spider_name, 'proxy_type': {'$in': ['http', 'https']}}).sort(
            [('last_check_at', SpiderDatabase.A_ORDER)]).limit(20))
        if not usable_proxies:
            return str(choice(usable_proxies))
        return ''


bind_models(SpiderDatabase, Proxy, 'proxy_list')
