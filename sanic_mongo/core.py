# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@Author: Huang Sizhe <huangsizhe>
@Date:   08-Apr-2017
@Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
@License: MIT
@Description:
"""

__all__=["Core"]

from pymongo.uri_parser import parse_uri
from motor.motor_asyncio import AsyncIOMotorClient
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
        return self.__get_db(self.uri)

    class __get_db:
        """利用生成器的next方法每次调用都会创建一个新的连接
        """
        def __init__(self,uri):
            def _get_db(collection=None):
                """返回连接的数据库或者集合
                """
                database = parse_uri(uri).get("database")
                mongo_uri = uri
                client = AsyncIOMotorClient(mongo_uri,connect=False)
                if collection:
                    return client[database][collection]
                else:
                    return client[database]
            self.a = _get_db

        def __call__(self,collection=None):
            b = self.a
            return b(collection)
