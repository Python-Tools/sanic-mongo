from abc import abstractmethod
from pymongo.uri_parser import parse_uri


class Base:

    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, value: str):
        if isinstance(value, str):
            parse_uri(value)
            self.__uri = value

    def __call__(self, app):
        if app:
            return self.init_app(app)
        else:
            raise AttributeError("need a sanic app to init the extension")

    def __init__(self, uri=None):
        self.__uri = uri

    @abstractmethod
    def init_app(self, app):
        print("init_app")
        pass
