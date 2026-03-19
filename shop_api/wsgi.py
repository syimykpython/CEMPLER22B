"""
WSGI config for shop_api project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

# Загружаем переменные окружения из .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Создаем WSGI-приложение
application = get_wsgi_application()