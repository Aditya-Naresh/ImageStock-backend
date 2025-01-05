import os
from celery import Celery
import logging
import ssl

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("mysite")

app.conf.update(
    broker_url="redis://red-ctstd68gph6c738ee8d0:6379",
    broker_transport_options={
        "ssl_cert_reqs": ssl.CERT_NONE,
        "socket_timeout": 30
    },
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logger.debug(f"Request: {self.request!r}")
