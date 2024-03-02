from celery import Celery
from celery.schedules import crontab
import os

app = Celery("prj")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prj.settings")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

"""
app.conf.beat_schedule = {
    "test_task": {
        "task": "app.tasks.test_task_function",
        "schedule": 300.0,
    },
}
"""