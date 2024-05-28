from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError

    @abstractmethod
    def increment(self, id, field):
        raise NotImplementedError
