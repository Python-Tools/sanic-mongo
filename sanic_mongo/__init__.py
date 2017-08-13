# @Author: Huang Sizhe
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: Apache License 2.0
__all__=["Mongo","GridFS"]

from sanic_mongo.mongo import Core as MongoCore
from sanic_mongo.gridfs import Core as GridFSCore
class Mongo(MongoCore):
    pass
class GridFS(GridFSCore):
    pass
