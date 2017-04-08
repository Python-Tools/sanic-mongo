# @Author: Huang Sizhe
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   Huang Sizhe
# @Last modified time: 08-Apr-2017
# @License: MIT

from pymongo.uri_parser import parse_uri
from motor.motor_asyncio import AsyncIOMotorClient
from itertools import repeat
class Core:
    @property
    def uri(self):
        return self.__uri
    def __call__(self,app):
        if app:
            return self.init_app(app)
        else:
            raise AttributeError("need a sanic app to init the extension")

    def __init__(self,uri=None):
        self.__uri = uri

    def init_app(self, app):
        """绑定app
        """
        if not self.uri:
            if app.config.MONGO_URI:
                self.__uri = app.config.MONGO_URI
            else:
                raise AssertionError("need a db url")

        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicMongo'] = self
        return self.get_db

    def get_db(self):
        def _get_db():
            database = parse_uri(self.uri).get("database")
            mongo_uri = "uri"
            client = AsyncIOMotorClient(mongo_uri)
            return client[database]
        a = repeat(_get_db)
        return next(a)
