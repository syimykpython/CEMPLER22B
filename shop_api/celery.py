import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Пример настройки beat schedule (можно добавить сюда другие периодические задачи)
from celery.schedules import crontab

app.conf.beat_schedule = {
    'daily-cleanup-task': {
        'task': 'users.tasks.scheduled_cleanup',
        'schedule': crontab(hour=3, minute=30),  # каждый день в 3:30
    },
}