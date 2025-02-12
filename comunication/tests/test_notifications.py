from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from comunication.models import Notification
from rest_framework.test import APIClient

User = get_user_model()

class NotificationModelTest(TestCase):
    def setUp(self):
        #Crea un usuario de prueba y una notificación
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.notification = Notification.objects.create(user=self.user, message="Prueba de notificación")

        # Crea un cliente de prueba para hacer peticiones a las vistas protegidas
        self.client = APIClient()

        # URL de la vista de notificaciones
        self.notifications_url = reverse('notifications')

    def test_notificacion_creada_correctamente(self):
        # Verifica que la notificación se crea correctamente
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, "Prueba de notificación")
        self.assertFalse(self.notification.is_read)  # Debe estar sin leer

    def test_marcar_notificacion_como_leida(self):
        # Verifica que una notificación puede marcarse como leída
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(Notification.objects.get(id=self.notification.id).is_read)

    def test_acceso_a_notificaciones_sin_login(self):
        # Verifica que un usuario no autenticado no puede acceder a la vista de notificaciones
        # Si estamos usando sesiones, deberíamos esperar un redirección (302)
        response = self.client.get(self.notifications_url)
        self.assertEqual(response.status_code, 302)

    def test_acceso_a_notificaciones_con_login(self):
        # Verifica que un usuario autenticado puede acceder a las notificaciones
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.notifications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalidar_token(self):
        # Verifica que después de hacer logout el token ya no es válido
        # Hacer login
        self.client.login(username="testuser", password="testpassword")
        
        # Hacer logout
        self.client.logout()
        
        # Intentar acceder a una vista protegida
        # En vez de 401, se espera una redirección (302)
        response = self.client.get(self.notifications_url)
        self.assertEqual(response.status_code, 302)
