
from typing import Dict

from .abstracts import AbstractSearchParameters, AbstractSearcher, AbstractServer

DEFAULT_STREAM_FILTER = "streams:000000000000000000000001"

class SearchParameterError(ValueError): pass


class GraylogSearchParameters(AbstractSearchParameters):
    def __init__(self, default_filter):
        self._default_filter = default_filter
        self._default_params = {"filter": self._default_filter}
        self._params = self._default_params
        self.method = "relative"
        self.query = ""
        self.limit = 0
        self.start = ""
        self.end = ""
        self.time_range = 0
        self.sort = ""

    def _add_params(self, p: dict):
        self._params.update(p)


class _GraylogRelativeSearchParameters(GraylogSearchParameters):
    def __init__(self, default_filter):
        super().__init__(default_filter)
        self.method = "relative"

    def params(self) -> dict:
        if self.start != "" or self.end != "" or self.time_range == 0:
            raise SearchParameterError(
                    "Relative search must have a valid time_range other than 0,"
                    " or should not have start or end properties configured")
        self._add_params({"range": self.time_range, "sort": self.sort})
        return self._params


class _GraylogAbsoluteSearchParameters(GraylogSearchParameters):
    def __init__(self, default_filter):
        super().__init__(default_filter)
        self.method = "absolute"

    def params(self) -> dict:
        if self.start == "" or self.end == "" or self.time_range != 0:
            raise SearchParameterError("Absolute search must have a valid start/end,"
                                        " or should not have time_range properties configured")
        self._add_params({"from": self.start, "to": self.end, "sort": self.sort})
        return self._params


class GraylogSearch(AbstractSearcher):
    def __init__(self, server: AbstractServer, default_filter: str=DEFAULT_STREAM_FILTER):
        self.server = server
        self._default_filter = default_filter


class GraylogRelativeSearch(GraylogSearch):
    def __init__(self, server: AbstractServer, default_filter: str=DEFAULT_STREAM_FILTER):
        super().__init__(server=server, default_filter=default_filter)
        self._search = _GraylogRelativeSearchParameters(self._default_filter)

    def search(self, q, time_range: int=3600, start: str="", end: str = "",
                limit: int=10, sort: str="timestamp:desc") -> Dict:
        self._search.query = q
        self._search.limit = limit
        self._search.time_range = time_range
        self._search.sort = sort
        return self.server.query(self._search)


class GraylogAbsoluteSearch(GraylogSearch):
    def __init__(self, server: AbstractServer, default_filter: str=DEFAULT_STREAM_FILTER):
        super().__init__(server=server, default_filter=default_filter)
        self._search = _GraylogAbsoluteSearchParameters(self._default_filter)

    def search(self, q, time_range: int=3600, start: str="", end: str = "",
                limit: int=10, sort: str="timestamp:desc") -> Dict:
        self._search.query = q
        self._search.limit = limit
        self._search.start = start
        self._search.end = end
        self._search.sort = sort
        return self.server.query(self._search)
