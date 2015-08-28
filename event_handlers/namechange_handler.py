from basehandler import BaseHandler

class NamechangeEventHandler(BaseHandler):
    BUTL_EVENT_API_PATTERNS = ['namechange']

    def write_error(self, status_code, **kwargs):
        self.logger.error('butts')
        self.write('you done fucked up')

    def post(self):
        test = self.get_argument("test", default = None)
        print test
        self.write('sup')
