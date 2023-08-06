import os
import importlib

from celery import Celery

import dada_settings


def get_celery_tasks_from_module(module_name):
    """
    Discover a list of task modules to pass to `include`
    """
    modules = []
    mod = importlib.import_module(module_name)
    package_name = mod.__name__
    package_path = mod.__path__[0]
    for fp in os.listdir(package_path):
        if not fp.endswith(".pyc") and "__init__" not in fp and "templates" not in fp:
            name = fp.replace(".py", "")
            modules.append(f"{package_name}.{name}")
    return modules


def make_celery(app_name):
    """
    Make a celery app
    """
    return Celery(
        app_name,
        backend=dada_settings.CELERY_RESULT_BACKEND,
        broker=dada_settings.CELERY_BROKER_URL,
        include=get_celery_tasks_from_module("dada.queue"),
    )


def init_celery(celery, app):
    """
    Init the celery task (for use in factory)
    """
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


# make celery

celery = make_celery(__name__)
