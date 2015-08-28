from basehandler import BaseHandler
import uuid

class SmsEventHandler(BaseHandler):
    BUTL_EVENT_API_PATTERNS = ['sms']

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    def write_error(status_code, **kwargs):
        pass

    def post(self):
        conversation_id = self.get_secure_cookie('butl_conversation_id')
        if conversation_id is not None:
            print "hello again, " + conversation_id
        else:
            conversation_id = uuid.uuid4().hex
            print "nice to meet you, this is conversation " + conversation_id
            self.set_secure_cookie('butl_conversation_id', conversation_id)
        event_id = self.get_argument("event_id", default = None)
