# -*- coding: utf-8 -*-
import codecs
import json
import yaml


def read_json_config(path):
    with codecs.open(path, 'rb+', 'utf-8') as rf:
        return json.load(rf)


def save_json_config(config, path):
    with codecs.open(path, 'wb+', 'utf-8') as wf:
        json.dump(config, wf)


def read_validator_config(path='./configs/validator-config.template.json'):
    return read_json_config(path)


def save_validator_config(config, path='./configs/validator-config.prod.json'):
    save_json_config(config, path)


def read_server_config(path='./configs/server-config.template.json'):
    return read_json_config(path)


def save_server_config(config, path='./configs/server-config.prod.json'):
    save_json_config(config, path)


def read_spider_config(path='./configs/spider-config.template.json'):
    return read_json_config(path)


def convert_val(val):
    if isinstance(val, str):
        return '\'' + val + '\''
    else:
        return str(val)


def save_spider_config(config, path='./configs/spider-config.prod.py'):
    result = ''
    for key, val in config.items():
        result += key + ' = '
        if isinstance(val, list):
            result += '[\n'
            for subVal in val:
                result += '    ' + convert_val(subVal) + ',\n'
            result += ']\n'
        elif isinstance(val, dict):
            result += '{\n'
            for subKey, subVal in val.items():
                result += '    \'' + subKey + '\': ' + convert_val(subVal) + ',\n'
            result += '}\n'
        else:
            result += convert_val(val) + '\n'
    with codecs.open(path, 'wb+', 'utf-8') as wf:
        wf.write(result)


def read_docker_compose_yml(path='./configs/docker-compose.template.yml'):
    with codecs.open(path, 'rb+', 'utf-8') as rf:
        return yaml.load(rf)


def save_docker_compose_yml(config, path='./configs/docker-compose.prod.yml'):
    with codecs.open(path, 'wb+', 'utf-8') as wf:
        ordered_config = {
            'version': config['version'],
            'services': config['services'],
            'volumes': config['volumes']
        }
        wf.write(yaml.dump(ordered_config, default_flow_style=False)[:-6])


def ask_config_questions():
    custom_config = dict()
    custom_config['mongo_port'] = input('What is the mongo port: ')
    custom_config['mongo_admin_username'] = input('What is the mongo admin username: ')
    custom_config['mongo_admin_password'] = input('What is the mongo admin password: ')
    custom_config['mongo_db_admin_username'] = input('What is the mongo database admin username: ')
    custom_config['mongo_db_admin_password'] = input('What is the mongo database admin password: ')
    custom_config['server_host'] = input('What is the server host: ')
    custom_config['server_port'] = input('What is the server port: ')
    custom_config['server_admin_username'] = input('What is the server admin username: ')
    custom_config['server_admin_password'] = input('What is the server admin password: ')
    custom_config['validator_check_interval'] = int(input('What is the validator check interval: '))
    custom_config['kuaidaili_spider_interval'] = int(input('What is the interval of kuaidaili spider: '))
    custom_config['cnproxy_spider_interval'] = int(input('What is the interval of cnproxy spider: '))
    custom_config['xici_spider_interval'] = int(input('What is the interval of xicidaili spider: '))
    custom_config['premproxy_spider_interval'] = int(input('What is the interval of premproxy spider: '))
    custom_config['proxydb_spider_interval'] = int(input('What is the interval of proxydb spider: '))
    custom_config['goubanjia_spider_interval'] = int(input('What is the interval of goubanjia spider: '))
    custom_config['kxdaili_spider_interval'] = int(input('What is the interval of kxdaili spider: '))
    custom_config['ip181_spider_interval'] = int(input('What is the interval of ip181 spider: '))
    return custom_config


def generate_docker_compose(tmpl, custom):
    tmpl['services']['mongo']['ports'] = [custom['mongo_port'] + ':27017']
    tmpl['services']['mongo']['environment'] = [
        'AUTH=yes',
        'MONGODB_APPLICATION_DATABASE=pmp',
        'MONGODB_ADMIN_USER=' + custom['mongo_admin_username'],
        'MONGODB_ADMIN_PASS=' + custom['mongo_admin_password'],
        'MONGODB_APPLICATION_USER=' + custom['mongo_db_admin_username'],
        'MONGODB_APPLICATION_PASS=' + custom['mongo_db_admin_password'],
    ]
    return tmpl


def generate_server_config(tmpl, custom):
    tmpl['DB_URI'] = 'mongodb://' + custom['mongo_db_admin_username'] + ':' + custom[
        'mongo_db_admin_username'] + '@mongo:27017/pmp'
    tmpl['HOST'] = custom['server_host']
    tmpl['PORT'] = custom['server_port']
    tmpl['ADMIN']['USERNAME'] = custom['server_admin_username']
    tmpl['ADMIN']['PASSWORD'] = custom['server_admin_password']
    return tmpl


def generate_validator_config(tmpl, custom):
    tmpl['DB_URI'] = 'mongodb://' + custom['mongo_db_admin_username'] + ':' + custom[
        'mongo_db_admin_username'] + '@mongo:27017/pmp'
    tmpl['SCHEDULER'] = custom['validator_check_interval']
    return tmpl


def generate_spider_config(tmpl, custom):
    tmpl['MONGO_URI'] = tmpl['DB_URI'] = 'mongodb://' + custom['mongo_db_admin_username'] + ':' + custom[
        'mongo_db_admin_username'] + '@mongo:27017/pmp'
    tmpl['SCHEDULE_KUAIDAILI'] = custom['kuaidaili_spider_interval']
    tmpl['SCHEDULE_CNPROXY'] = custom['cnproxy_spider_interval']
    tmpl['SCHEDULE_XICI'] = custom['xici_spider_interval']
    tmpl['SCHEDULE_PREMPROXY'] = custom['premproxy_spider_interval']
    tmpl['SCHEDULE_PROXYDB'] = custom['proxydb_spider_interval']
    tmpl['SCHEDULE_GOUBANJIA'] = custom['goubanjia_spider_interval']
    tmpl['SCHEDULE_KXDAILI'] = custom['kxdaili_spider_interval']
    tmpl['SCHEDULE_IP181'] = custom['ip181_spider_interval']
    return tmpl


if __name__ == '__main__':
    custom_config = ask_config_questions()
    save_docker_compose_yml(generate_docker_compose(read_docker_compose_yml(), custom_config))
    save_server_config(generate_server_config(read_server_config(), custom_config))
    save_validator_config(generate_validator_config(read_validator_config(), custom_config))
    save_spider_config(generate_spider_config(read_spider_config(), custom_config))
