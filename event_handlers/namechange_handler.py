from basehandler import BaseHandler

from tasks.namechange_task import change_name

class NamechangeEventHandler(BaseHandler):
    BUTL_EVENT_API_PATTERNS = ['namechange']

    def get(self):
        whom = self.get_argument("whom", default = None)
        count = int(self.get_argument("count", default = 1))
        if count < 1:
            count = 1

        if whom not in ['pope', 'rau', 'both']:
            self.write('who the fuck are you?')
            raise tornado.web.HTTPError(400, 'Do I know you?')

        if whom == 'both':
            doit1 = change_name.delay('pope')
            doit2 = change_name.delay('rau')
            self.write('tasks %s and %s added to the queue' % (doit1.id, doit2.id))
        else:    
            doit = change_name.delay(whom)
            self.write('task %s added to the queue' % doit.id)
