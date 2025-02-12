import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from comunication.routing import websocket_urlpatterns
from comunication.middleware import JWTAuthMiddleware

# Configurar Django antes de cualquier otro código
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")


# Definir la aplicación ASGI con WebSockets autenticados
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})

