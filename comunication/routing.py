from django.urls import re_path
from .consumers import ChatConsumer

# Definición de las rutas de WebSocket
websocket_urlpatterns = [
    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),  # Sin room_name en la URL
]
