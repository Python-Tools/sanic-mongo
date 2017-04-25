import datetime
from user_agents import parse
from sanic_mongo.standalone import MongoLogger
from sanic_mongo.base import Base
class Core(Base):
    def __init__(self,uri=None):
        super().__init__(uri)

    def init_app(self, app):
        """绑定app
        """
        if not self.__uri:
            if app.config.MONGO_URI:
                self.__uri = app.config.MONGO_URI
            else:
                raise AssertionError("need a db url")
        if app.config.MONGOLOGGER_INFO_CODEC_OPTIONS:
            info_codec_options = app.config.MONGOLOGGER_INFO_CODEC_OPTIONS
        else:
            info_codec_options = {'size':104857600,'capped':True }

        if app.config.MONGOLOGGER_WARMING_CODEC_OPTIONS:
            warming_codec_options = app.config.MONGOLOGGER_WARMING_CODEC_OPTIONS
        else:
            warming_codec_options = {'size':104857600,'capped':True }

        if app.config.MONGOLOGGER_ERROR_CODEC_OPTIONS:
            error_codec_options = app.config.MONGOLOGGER_ERROR_CODEC_OPTIONS
        else:
            error_codec_options = {'size':104857600,'capped':True }

        logger = MongoLogger(self.__uri,
                                 appname=app.name,
                                 info_codec_options=info_codec_options,
                                 warming_codec_options=warming_codec_options,
                                 error_codec_options=error_codec_options)
        if "extensions" not in app.__dir__():
            app.extensions = {}
        app.extensions['SanicMongoLogger'] = logger

        @app.middleware('request')
        async def add_session_to_request(request):
            # before each request initialize a session
            # using the client's request
            access_info = {}
            access_info["log_type"] = "access_log"
            access_info["access_time"] = datetime.datetime.now()
            access_info["access_ip"] = request.ip
            access_info["access_url"] = request.url
            access_info['access_method'] = request


            user-agent = request.headers.get("user-agent")
            device = parse(user-agent)
            if device.is_pc:
                access_info['access_device'] = {"type":"pc",
                                                "os":user_agent.os.family,
                                                "browser":user_agent.browser.family
                                                "is_touch_capable":user_agent.is_touch_capable
                                                }
            elif device.is_mobile:
                access_info['access_device'] = {"type":"mobile",
                                                "device":user_agent.device.family
                                                "os":user_agent.os.family,
                                                "browser":user_agent.browser.family
                                                "is_touch_capable":user_agent.is_touch_capable
                                                }

            elif device.is_tablet:
                access_info['access_device'] = {"type":"tablet",
                                                "device":user_agent.device.family
                                                "os":user_agent.os.family,
                                                "browser":user_agent.browser.family
                                                "is_touch_capable":user_agent.is_touch_capable
                                                }
            elif device.is_bot:
                access_info['access_device'] = {"type":"bot"}
            else:
                access_info['access_device'] = {"type":"unknown"}
            await logger.info(access_info)
            request["access_pass"] = {
                'access_uuid' = access_info['access_uuid'],
                "access_time" = access_info["access_time"]
            }



        @app.middleware('response')
        async def save_session(request, response):
            # after each request save the session,
            # pass the response to set client cookies
            info = {
                access_time
            }
            await logger.find_one_and_update({

            })


        return logger
