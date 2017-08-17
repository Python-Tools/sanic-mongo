from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.uri_parser import parse_uri
import asyncio


class MongoConnection:

    def create_client(self):
        """返回连接的客户端
        """
        #database = parse_uri(self.uri).get("database")
        if self.ioloop:
            client = AsyncIOMotorClient("/".join(self.uri.split("/")[:-1]), io_loop=self.ioloop)
        else:
            client = AsyncIOMotorClient("/".join(self.uri.split("/")[:-1]))
        return client

    def __init__(self, uri: str, ioloop=None):
        self.uri = uri
        self.ioloop = ioloop
        client = self.create_client()
        self.client = client
        self.database = parse_uri(self.uri).get("database")
        if not self.database:
            raise AttributeError("uri must have a database")
        self.db = self.client[self.database]
