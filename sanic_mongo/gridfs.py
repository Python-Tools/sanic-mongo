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

from sanic_mongo.standalone import GridFS
from sanic_mongo.base import Base


class Core(Base):
    FS = {}
    def __init__(self, uri=None,bucket_name="fs",chunk_size_bytes= 261120,write_concern=None,read_preference=None):
        super().__init__(uri)
        self.bucket_name=bucket_name
        self.chunk_size_bytes=chunk_size_bytes
        self.write_concern=write_concern
        self.read_preference=read_preference

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
            fs = GridFS(self.uri, ioloop=loop,self.bucket_name,self.chunk_size_bytes,self.write_concern,self.read_preference)
            Core.FS[self.uri+":"+self.bucket_name] = fs
            self.client = fs.client
            if hasattr(self,self.bucket_name):
                loop.close()
                raise AttributeError("bucket_name has used, choose a new one")
            setattr(self,self.bucket_name,fs)

        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            self.client.close
            log.info("{self.bucket_name} connection closed".format(self=self))

        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicGridFS'] = self
        return self
