from __future__ import absolute_import
from django.conf import settings
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    os.getenv(
        'DJANGO_SETTINGS_MODULE',
        'n1sp.settings'
    ))

app = Celery('NinetyOneSpringboard', broker=settings.BROKER_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("\n\n CELERY WORKS \n\n")
    print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
    app.start()
