# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@Author: Huang Sizhe <huangsizhe>
@Date:   08-Apr-2017
@Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
@License: Apache License 2.0
@Description:
"""

__all__=["Core"]

from sanic.log import log

from sanic_mongo.standalone import MongoConnection
from sanic_mongo.base import Base
class Core(Base):
    DBS = {}
    def __init__(self,uri=None):
        super().__init__(uri)
        self.db = None

    def init_app(self, app):
        """绑定app
        """
        if not self.uri:
            if app.config.MONGO_URI:
                self.__uri = app.config.MONGO_URI
            else:
                raise AssertionError("need a db url")

        @app.listener("before_server_start")
        async def init_mongo_connection(app, loop):
            mongo = MongoConnection(self.uri,ioloop=loop)
            Core.DBS[self.uri]=mongo.db
            setattr(self,"db",mongo.db)

        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            log.info("mongo connection {numbr}".format(numbr=len(Core.DBS)))
            self.db.close
            log.info("mongo connection closed")


        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicMongo'] = self
        return self
