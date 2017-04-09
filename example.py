# @Author: Huang Sizhe <huangsizhe>
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: MIT


from sanic import Sanic
from sanic.response import json
from sanic_mongo import Mongo

app = Sanic(__name__)
mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='test',
    port=27017,
    host='localhost'
)

mongo = Mongo(mongo_uri)
db = mongo(app)
@app.get('/objects')
async def get(request):
    docs = await db().test_col.find().to_list(length=100)
    for doc in docs:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return json(docs)


@app.post('/objects')
async def new(request):
    doc = request.json
    object_id = await db("test_col").save(doc)
    return json({'object_id': str(object_id)})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
