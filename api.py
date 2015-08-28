import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os, os.path
import uuid
import locale

import core.config as config
from core.strings import STRINGS

from tornado.options import define, options


class ButlertronAPI(tornado.web.Application):
    def __init__(self):
        # static handlers
        handlers = [
            #(r"/", MainHandler)
        ]
        # tornado app settings
        settings = dict(
            debug = True,
            cookie_secret = config.BUTL.API['cookie_secret'],
            # login_url="/auth/login",
            # template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=True,
            # autoescape="xhtml_escape",
        )
        # init app with settings and static handlers
        tornado.web.Application.__init__(self, handlers, **settings)

        # dynamically load nonstatic event handlers
        for handler_file in os.listdir('event_handlers'):
            if handler_file.endswith('_handler.py'):
                handler_module = handler_file.split('.py', 1)[0]
                handler_short_name = handler_file.split('_handler.py', 1)[0]
                handler_class_name = "%sEventHandler" % handler_short_name.capitalize()
                try:
                    mod = __import__('event_handlers.' + handler_module, fromlist=[handler_class_name])
                    klass = getattr(mod, handler_class_name)
                    # this would be a good place to do some kind of validation that this is a legit package
                    #  BUT I LIKE TO LIVE DANGEROUSLY
                    for pattern in klass.BUTL_EVENT_API_PATTERNS:
                        self.add_handlers(config.BUTL.API['host_pattern'], [(r"/event/" + pattern, klass)])
                except:
                    logger.error("Can't load " + handler_class_name)


class UnrecognizedEventError(Exception):
    def __init__(self, event_name = None):
        message = 'Unrecognized event: `%s`' % event_name
        logger.error(message)
        Exception.__init__(self, message)


def main():
    tornado.options.parse_command_line()
    app = ButlertronAPI()
    
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler())

    try:
        STRINGS = STRINGS[locale.getdefaultlocale()[0]]
    except:
        logger.warning('There was an error loading the locale, defaulted to en_US.')
        STRINGS = STRINGS["en_US"]

    # config object eventually
    define("port", default=config.BUTL.API['host_port'], help="run on the given port", type=int)

    main()