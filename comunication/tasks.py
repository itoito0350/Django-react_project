
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User

@shared_task
def enviar_notificacion_factura():
    """Tarea para enviar una notificación de factura a todos los usuarios el primer día de cada mes."""
    # Obtener todos los usuarios activos
    usuarios = User.objects.all()

    # Preparar el asunto y el contexto para el correo
    subject = "Recordatorio de Factura del Mes"
    context = {
        'message': "Recuerda que tu factura de este mes ya está disponible.",
    }

    # Enviar el correo a todos los usuarios
    for usuario in usuarios:
        # Renderizar el contenido del correo usando la plantilla HTML
        message = render_to_string('comunication/notification_email.html', context)

        # Enviar el correo
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Configura tu correo de envío
            [usuario.email],  # Dirección de correo del usuario
            html_message=message  # Contenido en HTML
        )

