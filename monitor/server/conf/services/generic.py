__author__ = 'alex'


class BaseService(object):
    def __init__(self):
        self.name = 'BaseService'
        self.interval = 300
        self.plugin_name = 'your_plugin_name'
        self.triggers = {}
