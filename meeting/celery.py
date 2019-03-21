import os, sys
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meeting.settings')

#sys.path.append('/opt/celery')

app = Celery('scheduler')
app.config_from_object('django.conf:settings')
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
