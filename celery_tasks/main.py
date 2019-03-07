import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms_mall_self.settings')

celery_app = Celery('cms', broker='redis://127.0.0.1:6379/10', backend='redis://127.0.0.1:6379/9')

celery_app.autodiscover_tasks(['celery_tasks.sms'])