sanic-mongo
====================

sanic的mongodb异步工具,灵感来源自 `官方例子 <https://github.com/channelcat/sanic/blob/master/examples/sanic_motor.py).是[motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html>`_ 的封装,
目的只是为了简化操作.

更新
-----------------------

* v1.6.1 修正了mongo连接权限可能引发的问题,现在可以配置每个连接是否是只能连database,默认为False.{"uri":xxxx,"only_db":True}
* v1.6.0 修正了验证无法通过的问题
* v1.5.0 将接口调整至和sanic-aioorm一致.



特点 Features
-------------------------

* `motor <https://motor.readthedocs.io/en/stable/tutorial-asyncio.html>`_ 支持的操作都支持
* 支持3.5版本以上的
* 支持多数据库
* 支持mongodb和gridfs



依赖 Requirements
-----------------------------
1. motor>=1.1
2. pymongo>=3.4.0
3. sanic>=0.4.1


 安装 Installation
--------------------------

- ``pip install sanic-mongo``


用法
----------------------------

mongo需要给`app.config`设置关键字`MONGO_URIS`,它是一个由mongodb名字和url组成的字典.
同时也可以使用`Mongo.SetConfig(app,**kws)`来注册kws的内容到`MONGO_URIS`.
而使用的时候可以访问`app.mongo[mongodb名字]`访问对应的db

gridfs与之类似,只是关键字是`GRIDFS_SETTINGS`,而访问需要使用`app.GridFS[GridFS名字]`


例子 Example
-----------------------------------

1. mongodb

.. code:: python
    from sanic import Sanic
    from sanic.response import json
    from sanic_mongo import Mongo

    app = Sanic(__name__)
    mongo_uri = "mongodb://{host}:{port}/{database}".format(
        database='test',
        port=27017,
        host='localhost'
    )

    Mongo.SetConfig(app,test=mongo_uri)
    Mongo(app)

    @app.get('/objects')
    async def get(request):
        docs = await app.mongo['test'].test_col.find().to_list(length=100)
        for doc in docs:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        return json(docs)


    @app.post('/objects')
    async def new(request):
        doc = request.json
        print(type(app.mongo['test']))
        object_id = await app.mongo['test']["test_col"].save(doc)
        return json({'object_id': str(object_id)})


    if __name__ == "__main__":
        app.run(host='127.0.0.1', port=8000,debug=True)




2. gridfs

.. code:: python

    from sanic import Sanic
    from sanic.response import json,text
    from sanic_mongo import GridFS

    app = Sanic(__name__)
    mongo_uri = "mongodb://{host}:{port}/{database}".format(
        database='test',
        port=27017,
        host='localhost'
    )

    GridFS.SetConfig(app,test_fs=(mongo_uri,"fs"))
    GridFS(app)

    @app.get('/pics')
    async def get(request):
        cursor = app.GridFS["test_fs"].find()
        result = [{i._id:i.name} async for i in cursor]
        return json({"result":result})


    @app.post('/pics')
    async def new(request):
        doc = request.files.get('file')

        async with app.GridFS["test_fs"].open_upload_stream(filename=doc.name,
            metadata={"contentType": doc.type}) as gridin:

            object_id = gridin._id
            await gridin.write(doc.body)

        return json({'object_id': str(object_id)})


    if __name__ == "__main__":
        app.run(host='127.0.0.1', port=8000,debug=True)
    
