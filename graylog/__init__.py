
import json
import arrow
from graylog.graylog import Graylog, GraylogQueryParser, GraylogExtractor
from graylog.auth import GraylogAuthenticator, GraylogBasicAuthenticator
from graylog.search import GraylogAbsoluteSearch, GraylogRelativeSearch

from .types import DotDict

class TimeRange:
    __fmt__ = 'YYYY-MM-DDTHH:mm:ss'
    def _range(self, start, end):
        return f"{start.format(self.__fmt__)}.000Z", f"{end.format(self.__fmt__)}.999Z"

    def ndays_before(self, days=-1):
        s, e = arrow.utcnow().shift(days=days).span('day')
        return self._range(s, e)


class Configuration(DotDict):
    def __init__(self, file: str):
        self._file = file
        super().__init__({})
        
    def parse(self):
        _data = {}
        with open(self._file) as fp:
            _data = json.load(fp)
        self.init(_data)
        return self
