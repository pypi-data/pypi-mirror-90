import os
import pickle
from typing import Dict, Any
from datetime import datetime

from .db import DB
from .wrapper import fileWrapper, dataWrapper


class fileStoreDB(DB):
    def __init__(self, location="./"):
        super().__init__()
        self.filestore = fileWrapper()
        self.location = location

    def addNewData(self, key: str, value: Dict[str, Any], ttl: int):
        self.filestore.current_database_size += value.__sizeof__()
        self.filestore.keys.add(key)
        self.filestore.data[key] = dataWrapper(value, ttl)

    def showData(self, key: str):
        if self.filestore.data[key].ttl:
            currtime = datetime.today().timestamp()
            datatime = self.filestore.data[key].timestamp
            print(currtime, datatime)
            if currtime - datatime >= self.filestore.data[key].ttl:
                self.delete(key)
                raise KeyError(f"{key} does not exist")

        return self.filestore.data[key].data

    def saveData(self, filename):
        self.filepath = os.path.join(self.location + filename)
        with open(filename, "wb") as outputfile:
            pickle.dump(self.filestore, outputfile, pickle.HIGHEST_PROTOCOL)

    def loadData(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found {os.path.join(self.location, filename)}")
        with open(filename, "rb") as readfile:
            self.filestore = pickle.load(readfile)

    def create(self, key: str, value: Dict[str, Any], ttl: int = None):
        if len(key) > 32:
            raise KeyError(f"Length of key: {len(key)} exceeds limits should be: 32")
        if key in self.filestore.keys:
            raise KeyError(f"{key} does not exist")
        if value.__sizeof__() > self.filestore.max_data_size:
            raise MemoryError(f"The size of json object is {value.__sizeof__()} bytes should be {self.filestore.max_data_size} bytes")
        if self.filestore.current_database_size + value.__sizeof__() >= self.filestore.max_database_size:
            raise MemoryError(f"Cannot create key: {key}, database size exceeds the limit {self.filestore.max_database_size}")
        self.addNewData(key, value, ttl)

    def read(self, key: str):
        if len(key) > 32:
            raise KeyError(f"Length of key: {len(key)} exceeds limits should be: 32")
        if key not in self.filestore.keys:
            raise KeyError(f"{key} does not exist")

        return self.showData(key)

    def delete(self, key: str):
        if len(key) > 32:
            raise KeyError(f"Length of key: {len(key)} exceeds limits should be: 32")
        if key not in self.filestore.keys:
            raise KeyError(f"{key} does not exist")
        self.filestore.current_database_size -= self.filestore.data[key].__sizeof__()
        self.filestore.keys.remove(key)
        del self.filestore.data[key]
