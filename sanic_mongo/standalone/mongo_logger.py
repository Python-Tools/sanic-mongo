import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.uri_parser import parse_uri
from bson.codec_options import CodecOptions
from sanic_mongo.standalone import mongo_connection
from typing import Dict


class Namespace:

    def __call__(self, val: str) -> str:
        return self.namespace + ":" + val

    def __init__(self, namespace: str="default"):
        self.namespace = namespace


class MongoLogger:
    LEVELS = ["info", "warming", "error"]

    def create_client(self):
        """返回连接的客户端
        """
        #database = parse_uri(self.uri).get("database")
        if self.ioloop:
            client = AsyncIOMotorClient(self.uri, io_loop=self.ioloop)
        else:
            client = AsyncIOMotorClient(self.uri)
        return client

    def __init__(self, uri: str,
                 appname: str,
                 ioloop=None,
                 info_options={'size': 104857600, 'capped': False},
                 warming_options={'size': 104857600, 'capped': False},
                 error_options={'size': 104857600, 'capped': False}):
        self.uri = uri
        self.database = parse_uri(self.uri).get("database")
        if not self.database:
            raise AttributeError("uri must have a database")
        self.appname = appname
        self.ioloop = ioloop
        self.namespace = Namespace(appname + "-log:")
        self.info_options = info_options
        self.warming_options = warming_options
        self.error_options = error_options
        client = self.create_client()
        self.client = client



    async def init(self):
        collection_names = await self.client[self.database].collection_names()
        try:
            if self.namespace("info") not in collection_names:
                await self.client[self.database].create_collection(
                    self.namespace("info"),
                    **self.info_options)
            if self.namespace("warming") not in collection_names:
                await self.client[self.database].create_collection(
                    self.namespace("warming"),
                    **self.warming_options)
            if self.namespace("error") not in collection_names:
                await self.client[self.database].create_collection(
                    self.namespace("error"),
                    **self.error_options)
        except:
            raise
        else:
            return self

    async def write(self, source, level="info"):
        client = self.client
        source["log-cutctime"] = datetime.datetime.utcnow()
        source["log-app"] = self.appname
        return await client[self.database][self.namespace(level)].insert_one(source)

    async def find_one_and_update(self, filter, update, level='info', projection=None,
                                  sort=None, upsert=False, return_document=False, **kwargs):
        return await self.client[self.database][self.namespace(level)].find_one_and_update(
            filter=filter, update=update, projection=projection,
            sort=sort, upsert=upsert, return_document=return_document, **kwargs
        )


    async def info(self, source):
        return await self.write(source, "info")
    async def warn(self, source):
        return await self.write(source, "warming")
    async def error(self, source):
        return await self.write(source, "error")
