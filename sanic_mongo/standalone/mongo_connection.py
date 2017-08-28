from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.uri_parser import parse_uri
import asyncio


class MongoConnection:

    def create_client(self,only_db=False):
        """返回连接的客户端
        """
        #database = parse_uri(self.uri).get("database")

        if self.ioloop:
            if only_db == False:
                client = AsyncIOMotorClient("/".join(self.uri.split("/")[:-1]), io_loop=self.ioloop)
            else:
                client = AsyncIOMotorClient(self.uri, io_loop=self.ioloop)

        else:
            if only_db == False:
                client = AsyncIOMotorClient("/".join(self.uri.split("/")[:-1]))
            else:
                client = AsyncIOMotorClient(self.uri)
        return client

    def __init__(self, uri: str, ioloop=None, only_db=False):
  
        self.uri = uri
        self.ioloop = ioloop
        client = self.create_client(only_db = only_db)
        self.client = client
        self.database = parse_uri(self.uri).get("database")
        if not self.database:
            raise AttributeError("uri must have a database")
        self.db = self.client[self.database]
 
