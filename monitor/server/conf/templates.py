__author__ = 'alex'

from services import linux

class BaseTemplate(object):
    def __init__(self):
        self.name = 'your template name'
        self.hosts = []
        self.services = []

class LinuxGenericTemplate(BaseTemplate):
    def __init__(self):
        super(LinuxGenericTemplate,self).__init__()
        self.name = "LinuxCommonServices"
        self.services = [
            linux.CPU(),
            linux.Memory()
        ]

        self.services[0].interval= 90

class Linux2(BaseTemplate):
    def __init__(self):
        super(Linux2,self).__init__()
        self.name = 'linux 2'
        self.services = [
            linux.CPU(),
            linux.Network()
        ]

