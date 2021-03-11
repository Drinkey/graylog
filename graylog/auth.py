
import requests

from .abstracts import AbstractAuthenticator

class GraylogAuthenticator(AbstractAuthenticator):
    def __init__(self, username: str, password: str):
        self._auth = None
        self.username = username
        self.password = password


class GraylogBasicAuthenticator(GraylogAuthenticator):
    def __init__(self, username: str, password: str):
        super().__init__(username=username, password=password)

    def authenticate(self):
        if self._auth is None:
            self._auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        return self._auth
