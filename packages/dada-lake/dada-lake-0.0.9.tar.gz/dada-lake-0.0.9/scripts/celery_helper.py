#!/usr/bin/env python
import os
from dada.queue.core import celery
from dada.factory import create_app

app = create_app(celery=celery)
app.app_context().push()
