# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
gridfs使用的模块,用于存储文件到mongodb,
需要设置app.config中的GRIDFS_URIS字段,格式为:

{
Bucket_name:(mongodbURI,collection),
...
}


"""

__all__ = ["Core"]

from sanic.log import log

from sanic_mongo.standalone import GridFSBucket


class Core:

    @staticmethod
    def SetConfig(app, **confs):
        app.config.GRIDFS_SETTINGS = confs
        return app

    def __init__(self, app):
        self.GridFSs = {}
        if app:
            self.init_app(app)
        else:
            pass

    def init_app(self, app):
        """绑定app
        """
        if app.config.GRIDFS_SETTINGS and isinstance(app.config.GRIDFS_SETTINGS, dict):
            self.GRIDFS_SETTINGS = app.config.GRIDFS_SETTINGS
            self.app = app

        else:
            raise ValueError(
                "nonstandard sanic config GRIDFS_URIS,GRIDFS_URIS must be a Dict[Bucket_name,Tuple[dburl,collection]]")

        @app.listener("before_server_start")
        async def init_mongo_connection(app, loop):
            for bucket_name, (dburl,collection) in app.config.GRIDFS_SETTINGS.items():
                bucket = GridFSBucket(dburl,ioloop=loop,collection = collection).bucket
                self.GridFSs[bucket_name] = bucket

        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            log.info("mongo connection {numbr}".format(numbr=len(self.GridFSs)))
            for bucket_name,bucket in self.GridFSs.items():
                bucket.client.close
                log.info("{bucket_name} connection closed".format(bucket_name=bucket_name))


        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicGridFS'] = self

        app.GridFS = self.GridFSs
        return self
