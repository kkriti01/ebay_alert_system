import os

from django.apps import apps, AppConfig
from django.conf import settings
from celery.schedules import crontab

from celery import Celery

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shore.settings')


app = Celery('shore')


class CeleryConfig(AppConfig):
    name = 'taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings')
        installed_apps = [app_config.name for app_config in
                          apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(),  # every minute
        debug_task.s(),
    )


@app.task()
def debug_task():
    print('Hello, world!')

