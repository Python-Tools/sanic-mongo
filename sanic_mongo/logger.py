import datetime
from user_agents import parse
from sanic.log import log
from sanic_mongo.standalone import MongoLogger
from sanic_mongo.base import Base
from bson.objectid import ObjectId
class Core(Base):
    def __init__(self,uri=None,session_in_cockie='session',
            info_options={'size': 104857600, 'capped': False},
            warming_options={'size': 104857600, 'capped': False},
            error_options={'size': 104857600, 'capped': False}):
        super().__init__(uri)
        self.session_in_cockie = session_in_cockie
        self.info_options = info_options
        self.warming_options = warming_options
        self.error_options = error_options
        self.logger = None

    async def info(self, source):
        return await self.logger.write(source, "info")
    async def warn(self, source):
        return await self.logger.write(source, "warming")
    async def error(self, source):
        return await self.logger.write(source, "error")

    def init_app(self, app):
        """绑定app
        """
        if not self.uri:
            if app.config.MONGO_URI:
                self.uri = app.config.MONGO_URI
            else:
                raise AssertionError("need a db url")

        @app.listener("before_server_start")
        async def init_mongo_connection(app, loop):
            mongo = MongoLogger(self.uri,appname=app.name, ioloop=loop,
                    info_options=self.info_options,
                    warming_options=self.warming_options,
                    error_options=self.error_options
                    )
            await mongo.init()
            self.logger = mongo


        @app.listener("before_server_stop")
        async def sub_close(app, loop):
            self.logger.client.close
            log.info("mongologger connection closed")


        @app.middleware('request')
        async def add_session_to_request(request):
            # before each request initialize a session
            # using the client's request
            access_info = {}
            access_info["log_type"] = "access_log"
            access_info["access_time"] = datetime.datetime.now()
            access_info["access_ip"] = request.ip[0]
            access_info["access_port"] = request.ip[1]
            access_info["access_scheme"] = request.scheme
            access_info["access_url"] = request.url
            access_info['access_method'] = request.method
            access_session = request.cookies.get(self.session_in_cockie)
            user_agent = parse(request.headers.get("user-agent"))
            if user_agent.is_pc:
                access_info['access_device'] = {"type":"pc",
                                                "os":user_agent.os.family,
                                                "browser":user_agent.browser.family,
                                                "is_touch_capable":user_agent.is_touch_capable
                                                }
            elif user_agent.is_mobile:
                access_info['access_device'] = {"type":"mobile",
                                                "device":user_agent.device.family,
                                                "os":user_agent.os.family,
                                                "browser":user_agent.browser.family,
                                                "is_touch_capable":user_agent.is_touch_capable
                                                }

            elif user_agent.is_tablet:
                access_info['access_device'] = {"type":"tablet",
                                                "device":user_agent.device.family,
                                                "os":user_agent.os.family,
                                                "browser":user_agent.browser.family,
                                                "is_touch_capable":user_agent.is_touch_capable
                                                }
            elif user_agent.is_bot:
                access_info['access_device'] = {"type":"bot"}
            else:
                access_info['access_device'] = {"type":"unknown"}

            _id = await self.logger.info(access_info)
            request["access_pass"] = {
                'access_id':_id.inserted_id,
                "access_time":access_info["access_time"]
            }

        @app.middleware('response')
        async def save_session(request, response):
            # after each request save the session,
            # pass the response to set client cookies
            leave_info = {}
            leave_info["leave_time"] = datetime.datetime.now()
            leave_info["cost_time"] = (leave_info["leave_time"]-request["access_pass"]["access_time"]).total_seconds()
            leave_info["status_code"] = response.status
            leave_info['content_type'] = response.content_type

            r = await self.logger.find_one_and_update(
                        {"_id":request["access_pass"]['access_id']},
                        {"$set":leave_info}
                    )

        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicMongoLogger'] = self
        return self
