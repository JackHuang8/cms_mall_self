from time import sleep

from celery_tasks.main import celery_app


@celery_app.task(name='send_sms_code_to_mobile')
def send_sms_code(mobile, sms_code):
    sleep(10)
    print('send msg to %s:'% mobile, sms_code)
    return (mobile, sms_code)