import time
from celery import Celery
from core import config
from core.twilio_manager import TwilioManager

celery = Celery()
celery.config_from_object('celeryconfig')

@celery.task
def add(x, y):
    return x + y

@celery.task
def send_message(to, body):
    time.sleep(30)
    return TwilioManager().send_sms(to, body)