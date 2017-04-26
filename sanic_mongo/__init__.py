# @Author: Huang Sizhe
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: Apache License 2.0
__all__=["Mongo","MongoLogger","GridFS"]

from sanic_mongo.mongo import Core as MongoCore
from sanic_mongo.logger import Core as MongoLoggerCore
from sanic_mongo.gridfs import Core as GridFSCore
class Mongo(MongoCore):
    def __init__(self, uri=None):
        super().__init__(uri)

class GridFS(GridFSCore):
    def __init__(self,uri=None,collection="fs"):
        super().__init__(uri,collection)

class MongoLogger(MongoLoggerCore):
    def __init__(self, uri=None,session_in_cockie='session',
            info_options={'size': 104857600, 'capped': False},
            warming_options={'size': 104857600, 'capped': False},
            error_options={'size': 104857600, 'capped': False}):
        super().__init__(uri=uri,
                session_in_cockie=session_in_cockie,
                info_options=info_options,
                warming_options=warming_options,
                error_options=error_options)
