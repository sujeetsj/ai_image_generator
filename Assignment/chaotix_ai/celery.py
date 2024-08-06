import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaotix_ai.settings')

app = Celery('chaotix_ai')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Explicitly set the task serializer and result serializer
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')