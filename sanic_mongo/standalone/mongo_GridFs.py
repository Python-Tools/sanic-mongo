from motor.motor_asyncio import AsyncIOMotorGridFSBucket


from sanic_mongo.standalone import mongo_connection

class GridFS(AsyncIOMotorGridFSBucket):

    def __init__(self, uri: str, ioloop=None,bucket_name="fs",chunk_size_bytes= 261120,write_concern=None,read_preference=None):
        mongo = mongo_connection(uri=uri,ioloop=ioloop)
        self.client = mongo.client
        super().__init__(mongo.db,bucket_name=bucket_name,
                         chunk_size_bytes= chunk_size_bytes,
                         write_concern=write_concern,
                         read_preference=read_preference)
