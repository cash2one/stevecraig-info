from basehandler import BaseHandler

class NamechangeEventHandler(BaseHandler):
    BUTL_EVENT_API_PATTERNS = ['namechange']

    def post(self):
        test = self.get_argument("test", default = None)
        print test
        self.write('sup')
