# @Author: Huang Sizhe
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: Apache License 2.0
__all__=["Mongo"]

from sanic_mongo.core import Core

class Mongo(Core):
    def __init__(self, uri=None):
        super().__init__(uri)
