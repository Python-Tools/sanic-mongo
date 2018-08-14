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

__all__ = ["Core"]

from sanic.log import logger as log

from sanic_mongo.standalone import MongoConnection


class Core:

    @staticmethod
    def SetConfig(app, **confs):
        app.config.MONGO_URIS = confs
        return app

    def __init__(self, app=None,):
        self.mongodbs = {}
        if app:
            self.init_app(app)
        else:
            pass

    def init_app(self, app):
        """绑定app
        """
        if app.config.MONGO_URIS and isinstance(app.config.MONGO_URIS, dict):
            self.MONGO_URIS = app.config.MONGO_URIS
            self.app = app

        else:
            raise ValueError(
                "nonstandard sanic config MONGO_URIS,MONGO_URIS must be a Dict[dbname,dburl]")


        @app.listener("before_server_start")
        async def init_mongo_connection(app, loop):
            for dbname, dburl in app.config.MONGO_URIS.items():
                if isinstance(dburl,str):
                    db = MongoConnection(dburl,ioloop=loop).db
                else:
                    db = MongoConnection(ioloop=loop,**dburl).db
                self.mongodbs[dbname] = db

        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            log.info("mongo connection {numbr}".format(numbr=len(self.mongodbs)))
            for dbname,db in self.mongodbs.items():
                db.client.close
                log.info("{dbname} connection closed".format(dbname=dbname))

        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicMongo'] = self

        app.mongo = self.mongodbs
        return self
