# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
@Author: Huang Sizhe
@Date:   06-Apr-2017
@Email:  hsz1273327@gmail.com
# @Last modified by:   Huang Sizhe
# @Last modified time: 08-Apr-2017
@License: MIT
@Description:
"""


from distutils.core import setup

required = ["motor>=1.1",
            "pymongo>=3.4.0",
            "sanic>=0.4.1",
            "user_agents>=1.1.0"]


long_description = '''# sanic-mongo

sanic的mongodb异步工具,灵感来源自[官方例子](https://github.com/channelcat/sanic/blob/master/examples/sanic_motor.py).是[motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)的封装,目的只是为了简化操作.



## 特点 Features

+ [motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html) 支持的操作都支持
+ 支持3.5版本以上的


## 依赖 Requirements

1. motor>=1.1
2. pymongo>=3.4.0
3. sanic>=0.4.1


## 安装 Installation

    pip install sanic-mongo

## 文档 Document


## 例子 Example

```python
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

```

    '''
setup(
    name='sanic-mongo',
    version='1.5.5',
    author='Huang Sizhe',
    author_email='hsz1273327@gmail.com',
    packages=['sanic_mongo'],
    license='Apache License 2.0',
    description='a simple sanic extension for using motor',
    long_description=long_description,
    install_requires=required,
    url="https://sanic-extensions.github.io/sanic-mongo/"
)
