import os
from celery import Celery
import logging
import ssl

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("mysite")

app.conf.update(
    broker_user_ssl=True,
    broker_transport_options={
        'ssl_cert_reqs': ssl.CERT_NONE
    }
)
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logger.debug(f"Request: {self.request!r}")
