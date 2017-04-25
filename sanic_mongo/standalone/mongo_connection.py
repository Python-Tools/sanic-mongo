from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.uri_parser import parse_uri
import asyncio
class MongoConnection:
    """每次都需要独立创建链接
    """
    def create_connection(self,collection:str=None):
        """返回连接的数据库或者集合
        """
        database = parse_uri(self.uri).get("database")
        client = AsyncIOMotorClient(self.uri,connect=False)
        if collection:
            return client[database][collection]
        else:
            return client[database]

    def create_client(self):
        """返回连接的数据库或者集合
        """
        #database = parse_uri(self.uri).get("database")
        if self.ioloop:
            client = AsyncIOMotorClient(self.uri,io_loop=self.ioloop)
        else:
            client = AsyncIOMotorClient(self.uri)
        return client


    def __init__(self,uri:str,ioloop=None):
        self.uri = uri
        self.ioloop=ioloop
        ###########
        self.client = self.create_client()
        self.database = parse_uri(self.uri).get("database")
        self.db = self.client[self.database]

    def __call__(self,collection:str=None):

        return self.create_connection(collection)
