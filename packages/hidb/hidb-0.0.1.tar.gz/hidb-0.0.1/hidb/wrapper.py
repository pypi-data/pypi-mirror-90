from datetime import datetime


class fileWrapper(object):
    def __init__(self):
        self.data = {}
        self.keys = set()


class dataWrapper:
    def __init__(self, data, ttl):
        self.data = data
        self.timestamp = datetime.today().timestamp()
        self.ttl = ttl
