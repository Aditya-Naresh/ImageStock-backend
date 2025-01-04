from django.core.management import call_command

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

try:
    call_command("migrate")
except Exception as e:
    print(f"Error running migrations: {e}")

application = get_wsgi_application()
