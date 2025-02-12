import jwt
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware para autenticar usuarios en WebSockets usando JWT.
    """

    async def __call__(self, scope, receive, send):
        # Obtener el token de la URL del WebSocket
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]  # Extrae el token

        scope["user"] = AnonymousUser()  # Usuario por defecto

        if token:
            scope["user"] = await self.get_user_from_token(token)

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        """
        Decodifica el JWT y devuelve el usuario autenticado o AnonymousUser si falla.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return AnonymousUser()
