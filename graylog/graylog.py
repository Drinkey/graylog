
from typing import Dict
import requests

from .types import DotDict
from .abstracts import AbstractAuthenticator, AbstractSearchParameters, AbstractSearcher, AbstractServer

class Graylog(AbstractServer):
    def __init__(self, api_server: str, auth: AbstractAuthenticator):
        self._api_server = api_server
        self._auth = auth.authenticate()
        self._api_url = "api/search/universal/{}"
        self._headers = {
            "Accept": "application/json",
        }

    def _get_url(self, t: str, params: dict):
        _url = self._api_url.format(t)
        _p = "&".join(["=".join([str(k), str(v)]) for k,v in params.items()])
        return f"{self._api_server}{_url}?{_p}"

    def _request_params(self, search_params: AbstractSearchParameters):
        url = self._get_url(search_params.method, search_params.params())
        return url, {'query': search_params.query, 'limit': search_params.limit}

    def query(self, search_params: AbstractSearchParameters) -> Dict:
        url, params = self._request_params(search_params)
        r = requests.get(url=url, params=params, auth=self._auth, headers=self._headers)
        r.raise_for_status()
        return r.json()


class GraylogQueryParser(DotDict):
    def __init__(self, data: dict):
        self.data = data

    def get_messages(self):
        """return "message" field dict of "messages" in response

        :yield: message dict
        :rtype: generator[dict]
        """
        for msg in self.messages:
            yield msg['message']


class AbstractGraylogExtractor:
    def __init__(self, searcher: AbstractSearcher, time_range: int = 0,
                start: str = "", end: str = "", sort: str = "timestamp:desc"):
        pass
    def extract(self) -> Dict:
        raise NotImplementedError


class GraylogExtractor(AbstractGraylogExtractor):
    def __init__(self, searcher: AbstractSearcher, time_range: int = 0,
                start: str = "", end: str = "", sort: str = "timestamp:desc"):
        self.searcher = searcher
        self.time_range = time_range
        self.start = start
        self.end = end
        self.sort = sort

    def do_search(self, q, limit, raw: bool = False):
        result = self.searcher.search(
                                    q=q,
                                    time_range=self.time_range,
                                    start=self.start,
                                    end=self.end,
                                    limit=limit,
                                    sort=self.sort)
        # return raw JSON from requests or return parsed result
        return result if raw else GraylogQueryParser(result)
