import abc
from typing import Dict


class AbstractSearchParameters(abc.ABC):
    def __init__(self, default_filter: str):
        pass
    @abc.abstractmethod
    def params(self) -> Dict:
        raise NotImplementedError


class AbstractAuthenticator(abc.ABC):
    @abc.abstractmethod
    def authenticate(self):
        pass


class AbstractServer(abc.ABC):
    @abc.abstractmethod
    def query(self, search_params: AbstractSearchParameters) -> Dict:
        pass


class AbstractSearcher(abc.ABC):
    def __init__(self, server: AbstractServer, default_filter: str):
        pass
    @abc.abstractmethod
    def search(self, q, time_range: int=3600, start: str="", end: str = "",
                limit: int=10, sort: str="timestamp:desc") -> Dict:
        """Interface definition of subclasses"""
        raise NotImplementedError
