from basehandler import BaseHandler

from tasks.namechange_task import change_name

class NamechangeEventHandler(BaseHandler):
    BUTL_EVENT_API_PATTERNS = ['namechange']

    def get(self):
        whom = self.get_argument("whom", default = None)
        count = int(self.get_argument("count", default = 1))
        if count < 1:
            count = 1

        doit = change_name.delay(whom)
        self.write('i did the thing')
