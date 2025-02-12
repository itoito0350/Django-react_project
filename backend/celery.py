
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo predeterminado para 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Usar configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas de todos los módulos de la app Django
app.autodiscover_tasks()
