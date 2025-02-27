from django.db import models
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario personalizado 
User = get_user_model()

# Definición del modelo Notification
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.message}"

