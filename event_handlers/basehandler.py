from tornado.web import RequestHandler
from traceback import format_exception
import logging

class BaseHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.logger = logging.getLogger(__name__)

        super(BaseHandler, self).__init__(application, request, **kwargs)


    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            etype, value, tb = kwargs['exc_info']
            trace = ''.join(format_exception(etype, value, tb, 10)) 
        else:
            trace = "None"
        self.logger.error('%s: %s' % (status_code, trace))
        self.write('you done fucked up: %s' % status_code)