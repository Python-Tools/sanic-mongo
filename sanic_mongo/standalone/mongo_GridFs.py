from motor.motor_asyncio import AsyncIOMotorGridFSBucket


from sanic_mongo.standalone import MongoConnection

#class GridFSBucket(AsyncIOMotorGridFSBucket):
class GridFSBucket:
    def __init__(self, uri: str, ioloop=None,collection="fs"):
        mongo = MongoConnection(uri=uri,ioloop=ioloop)
        fs = AsyncIOMotorGridFSBucket(mongo.db,collection=collection)
        #super().__init__(mongo.db,collection=collection)
        setattr(fs,"client",mongo.client)
        self.bucket = fs
