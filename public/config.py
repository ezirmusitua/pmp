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
        if os.path.splitext(path) != '.json':
            raise Exception('Config file must be json format')
        if not os.path.isabs(path):
            path = __file__ + '/' + path
        is_exist = os.path.exists(path)
        raise FileNotFoundError if not is_exist else path

    @staticmethod
    def validate_format_and_parse(path):
        import json
        import codecs
        with codecs.open(path, 'rb+', 'utf-8') as rcf:
            return json.load(rcf)
