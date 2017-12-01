# -*- coding: utf-8 -*-
class Config(object):
    def __init__(self, config_path):
        config_path = Config.validate_path(config_path)
        self.config_path = config_path
        self._config = Config.validate_format_and_parse(config_path)

    def __getitem__(self, key):
        return self._config.get(key)

    @staticmethod
    def validate_path(path):
        import os
        if os.path.splitext(path)[1] != '.json':
            raise Exception('Config file must be json format')
        is_exist = os.path.exists(path)
        if not is_exist:
            raise FileNotFoundError
        else:
            return path

    @staticmethod
    def validate_format_and_parse(path):
        import json
        import codecs
        with codecs.open(path, 'rb+', 'utf-8') as rcf:
            return json.load(rcf)


def concat_config_path(file_located, filename):
    import os
    return os.path.abspath(os.path.join(os.path.split(file_located)[0], os.pardir)) + '/' + filename
