from abc import ABC, abstractmethod


class DB(ABC):
    @abstractmethod
    def create(self):
        """
        Create a key value mapping for data
        """
        raise NotImplementedError

    @abstractmethod
    def read(self):
        """
        Read data given the key
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        """
        Delete the key value mapping for data
        """
        raise NotImplementedError


class KeyError(Exception):
    pass


class ValueError(Exception):
    pass
