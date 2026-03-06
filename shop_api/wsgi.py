"""
WSGI config for shop_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv  # <-- исправлено
from django.core.wsgi import get_wsgi_application

# Загружаем .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

application = get_wsgi_application()