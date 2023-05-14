
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import news_creation.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_main.settings')

application = get_asgi_application()