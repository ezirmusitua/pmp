# -*- coding:utf-8 -*-


class User(object):
    db_collection = None

    def __init__(self, user_doc):
        self.id = user_doc['_id']
        self.username = user_doc.get('username', '')
        self.password = user_doc.get('password', '')

    @staticmethod
    def validate(username, password):
        user = User.db_collection.find_one({'username': username, 'password': password})
        return False if user is None else True
