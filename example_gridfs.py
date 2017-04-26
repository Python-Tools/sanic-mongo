# @Author: Huang Sizhe <huangsizhe>
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: MIT


from sanic import Sanic
from sanic.response import json
from sanic_mongo import GridFS

app = Sanic(__name__)
mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='test',
    port=27017,
    host='localhost'
)

fs = GridFS(mongo_uri)
fs(app)
@app.get('/objects')
async def get(request):
    docs = await mongo.db.test_col.find().to_list(length=100)
    for doc in docs:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return json(docs)


@app.post('/objects')
async def new(request):
    doc = request.files
    async with await fs.fs.new_file() as gridin:
        await gridin.write(b'First part\n')
        await gridin.write(b'Second part')



    return json({'object_id': str(object_id)})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000,debug=True)
