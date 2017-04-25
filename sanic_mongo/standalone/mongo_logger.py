import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.uri_parser import parse_uri
from sanic_mongo.standalone import mongo_connection
from typing import Dict

class Namespace:
    def __call__(self,val:str)->str:
        return self.namespace+":"+val
    def __init__(self,namespace:str="default"):
        self.namespace = namespace


class MongoLogger:
    LEVELS = ["info","warming","error"]

    def __init__(self,uri:str,
                 appname:str,
                 info_codec_options={'size':104857600,'capped':True },
                 warming_codec_options={'size':104857600,'capped':True },
                 error_codec_options={'size':104857600,'capped':True }):
        self.uri = uri
        self.database = parse_uri(self.uri).get("database")
        self.appname = appname
        self.namespace = Namespace(appname+"-log:")
        self.info_codec_options = info_codec_options
        self.warming_codec_options = warming_codec_options
        self.error_codec_options = error_codec_options



    async def init(self):
        client = AsyncIOMotorClient(self.uri,connect=False)
        collection_names = await client[self.database].collection_names()
        try:
            if namespace("info") not in collection_names:
                await client[self.database].create_collection(
                    namespace("info"),
                    codec_options=self.info_codec_options)
            if namespace("warming") not in collection_names:
                await client[self.database].create_collection(
                    namespace("warming"),
                    codec_options=self.warming_codec_options)
            if namespace("error") not in collection_names:
                await client[self.database].create_collection(
                    namespace("error"),
                    codec_options=self.error_codec_options)
        except:
            raise
        else:
            return self




    async def write(self,source,level = "info"):
        database = parse_uri(self.uri).get("database")
        client = AsyncIOMotorClient(self.uri,connect=False)
        source["log-cutctime"] = datetime.datetime.utcnow()
        source["log-app"] = self.appname
        return await client[self.database][namespace(level)].save(source)
    async def find_one_and_update(self):
        pass


    async def info(self,source):
        return await self.write(source,"info")
    async def warn(self,source):
        return await self.write(source,"warming")
    async def error(self,source):
        return await self.write(source,"error")
