from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aviata.settings')

app = Celery('aviata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'task-every-day-midnight`': {
        'task': 'tz.tasks.get_cheap_tickets',
        # 'schedule': crontab(minute=0, hour=0),
        'schedule': 100000000.0,
    },
}

app.conf.timezone = 'UTC'

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))