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

from sanic.log import log

from sanic_mongo.standalone import GridFSBucket
from sanic_mongo.base import Base


class Core(Base):
    FS = {}
    def __init__(self, uri=None,collection="fs",chunk_size_bytes= 261120,write_concern=None,read_preference=None):
        super().__init__(uri)
        self.collection=collection


    def init_app(self, app):
        """绑定app
        """
        if not self.uri:
            if app.config.MONGO_URI:
                self.uri = app.config.MONGO_URI
            else:
                raise AssertionError("need a db url")

        @app.listener("before_server_start")
        async def init_mongo_connection(app, loop):
            fs = GridFSBucket(self.uri, ioloop=loop,collection = self.collection).bucket
            Core.FS[self.uri+":"+self.collection] = fs
            self.client = fs.client
            if hasattr(self,self.collection):
                loop.close()
                raise AttributeError("bucket_name has used, choose a new one")
            setattr(self,self.collection,fs)

        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            self.client.close
            log.info("{self.collection} connection closed".format(self=self))

        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicGridFS'] = self
        return self
