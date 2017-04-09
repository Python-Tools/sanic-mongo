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

required = ['aiofiles>=0.3.1',
            'aiomysql>=0.0.9',
            'aiopg>=0.13.0',
            'httptools>=0.0.9',
            'peewee>=2.9.1',
            'peewee-async>=0.5.7',
            'psycopg2>=2.7.1',
            'PyMySQL>=0.7.10',
            'sanic>=0.4.1',
            'ujson>=1.35']


long_description = '''# sanic-peewee

    sanic-peewee is a async_peewee orm extension for sanic,
    I hope users can deal with the database simplely and efectively when using sanic.


    ## Features

    + a peewee API similar to peewee's standard, blocking API.
    + support for async/await (PEP 492) constructs
    + use database url (peewee's playhose)
    + support pool and pg's ext (peewee-async)
    + sync api for creating and delecting tables,async api for GRUD data.


    ## Requirements

    1. aiomysql>=0.0.9
    + aiopg>=0.13.0
    + peewee>=2.9.1
    + peewee-async>=0.5.7
    + psycopg2>=2.7.1
    + PyMySQL>=0.7.10
    + sanic>=0.4.1

    ## Installation

        pip install sanic-peewee



    ## Example

    ```python
    from sanic import Sanic
    from sanic.response import text,json
    from sanic_peewee import Peewee,select
    from peewee import CharField, TextField

    app = Sanic(__name__)
    dburl = "mysql://{user}:{password}@{host}:{port}/{database}".format(
        database='test1',
        port=3306,
        host='127.0.0.1',
        user='root',
        password='hsz881224'
    )
    peewee = Peewee(dburl)
    db = peewee(app)


    class KeyValue(db.AsyncModel):
        key = CharField(max_length=40, unique=True)
        text = TextField(default='')



    db.create_tables([KeyValue])



    @app.route('/post/<key>/<value>')
    async def post(request, key, value):
        """
        Save get parameters to database
        """
        obj = await KeyValue.aio.create(key=key, text=value)# use the model's async object to manage the query
        return json({'object_id': obj.id})


    @app.route('/get')
    async def get(request):
        """
        Load all objects from database
        """
        # use the sanic_peewee object's async api
        all_objects = await db.aio.select(db.SelectQuery(KeyValue))

        serialized_obj = []
        for obj in all_objects:
            serialized_obj.append({
                'id': obj.id,
                'key': obj.key,
                'value': obj.text}
            )

        return json({'objects': serialized_obj})


    @app.route("/")
    async def test(request):
        return text('Hello world!')

    app.run(host="0.0.0.0", port=8000, debug=True)
    ```
    '''
setup(
    name='sanic-peewee',
    version='1.0.0',
    author='Huang Sizhe',
    author_email='hsz1273327@gmail.com',
    packages=['sanic_peewee'],
    license='BSD',
    description='a simple sanic extension for using async-peewee',
    long_description=long_description,
    install_requires=required,
    url="https://github.com/Sanic-Extensions/sanic-peewee"
)
