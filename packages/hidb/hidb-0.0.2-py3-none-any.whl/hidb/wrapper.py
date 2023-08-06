from datetime import datetime


class fileWrapper(object):
    def __init__(self):
        self.data = {}
        self.keys = set()
        # JSON data size 16KB in Bytes
        self.max_data_size = 16384
        # Max database size 1GB in Bytes
        self.max_database_size = 1073741824
        self.current_database_size = 0


class dataWrapper:
    def __init__(self, data, ttl):
        self.data = data
        self.timestamp = datetime.today().timestamp()
        self.ttl = ttl
