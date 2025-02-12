from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from .tasks import enviar_notificacion_factura

@login_required
def notifications_view(request):
    """Vista para mostrar y marcar como leídas las notificaciones."""
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notifications.update(is_read=True)

    # Enviar correos asincrónicamente
    for notification in notifications:
        context = {
            'user': request.user,
            'notification': notification,
        }
        # Llamamos a la tarea Celery para enviar el correo
        enviar_notificacion_factura.delay(request.user.email, "Nueva Notificación", context)

    return render(request, "comunication/notifications.html", {"notifications": notifications})


