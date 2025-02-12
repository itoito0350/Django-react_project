from .models import Notification

def crear_notificacion(user, mensaje):
    """Crea una notificación para un usuario."""
    return Notification.objects.create(user=user, message=mensaje)
