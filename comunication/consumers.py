import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        # Grupo común para todos los usuarios
        self.room_group_name = "chat_general"  

        if user.is_authenticated:
            # Unirse al grupo de canales (chat común)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                "message": f"Bienvenido, {user.username} al chat general!"
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Dejar el grupo cuando se desconecte
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recibe un mensaje del cliente y lo transmite a todos en el grupo.
        data = json.loads(text_data)
        message = data.get("message", "")
        username = data.get("username", "")

        # Enviar mensaje a todos los miembros del grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        # Recibe un mensaje del grupo y lo envía al WebSocket.
        message = event["message"]
        username = event["username"]

        # Enviar mensaje de vuelta al WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))
