from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa_backend.settings")
app = Celery("qa_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(related_name="views")

@app.task(bind=True)
def debug_task(self):
    print("request: {0!r}".format(self.request))
