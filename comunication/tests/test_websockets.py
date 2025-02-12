
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from backend.asgi import application
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import IntegrityError
from asgiref.sync import sync_to_async

class WebSocketTests(TestCase):
    async def test_websocket_connection(self):

        # Crear un usuario de prueba y generar un token JWT (usando sync_to_async)
        user = await self.create_user("testuser", "testpassword")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Conectar al WebSocket, pasando el token JWT en la URL
        communicator = WebsocketCommunicator(application, f"/ws/chat/?token={access_token}")
        connected, _ = await communicator.connect()

        # Asegurar que la conexión fue exitosa
        self.assertTrue(connected)

        # Recibir el mensaje de bienvenida
        response = await communicator.receive_json_from()
        self.assertEqual(response["message"], "Bienvenido, testuser al chat general!")

        # Enviar un mensaje de prueba
        message = {"username": "testuser", "message": "Hola mundo!"}
        await communicator.send_json_to(message)

        # Recibir la respuesta del servidor
        response = await communicator.receive_json_from()

        # Asegurar que la respuesta sea la esperada (el mensaje que enviamos)
        self.assertEqual(response["message"], "Hola mundo!")
        self.assertEqual(response["username"], "testuser")

        # Cerrar la conexión del WebSocket
        await communicator.disconnect()

    @sync_to_async
    def create_user(self, username, password):
        # Crea un usuario de prueba de manera sincrónica para evitar problemas de contexto asíncrono.
        try:
            return User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return User.objects.get(username=username)
