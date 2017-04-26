# @Author: Huang Sizhe <huangsizhe>
# @Date:   08-Apr-2017
# @Email:  hsz1273327@gmail.com
# @Last modified by:   huangsizhe
# @Last modified time: 08-Apr-2017
# @License: MIT


from sanic import Sanic
from sanic.response import json,text
from sanic_mongo import GridFS

app = Sanic(__name__)
mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='test',
    port=27017,
    host='localhost'
)

fs = GridFS(mongo_uri)
fs(app)
@app.get('/pics')
async def get(request):
    cursor = fs.fs.find()
    result = [{i._id:i.name} async for i in cursor]
    return json({"result":result})


@app.post('/pics')
async def new(request):
    doc = request.files.get('file')

    async with fs.fs.open_upload_stream(filename=doc.name,
        metadata={"contentType": doc.type}) as gridin:

        object_id = gridin._id
        await gridin.write(doc.body)

    return json({'object_id': str(object_id)})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000,debug=True)
