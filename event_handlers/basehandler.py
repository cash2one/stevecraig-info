from tornado.web import RequestHandler
import logging

class BaseHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

        super(BaseHandler, self).__init__(application, request, **kwargs)