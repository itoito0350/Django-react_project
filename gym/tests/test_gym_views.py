from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from gym.models import GymClass, Schedule, Reservation

User = get_user_model()

class GymClassTests(APITestCase):
    def setUp(self):
        # Crear usuario para la autenticación
        self.user = User.objects.create_user(username='testuser', password='password')

        # Crear token de acceso para el usuario
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Crear un cliente de prueba para hacer las solicitudes
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_gym_class(self):
        # Datos de prueba para crear un GymClass
        data = {
            "title": "Yoga",
            "description": "Clase de yoga para todos los niveles",
            "trainer": "Juan Perez",
            "capacity": 20
        }

        # Realizar solicitud POST para crear una clase de gimnasio
        response = self.client.post('/api/gym/classes/', data=data, format='json')

        # Validar que la clase se crea correctamente (código 201)
        self.assertEqual(response.status_code, 201)

        # Verificar que el gym class se ha creado en la base de datos
        self.assertEqual(GymClass.objects.count(), 1)
        self.assertEqual(GymClass.objects.get().title, "Yoga")


class ScheduleTests(APITestCase):
    def setUp(self):
        # Crear usuario para la autenticación
        self.user = User.objects.create_user(username='testuser', password='password')

        # Crear token de acceso para el usuario
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Crear un cliente de prueba para hacer las solicitudes
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Crear una clase de gimnasio para usarla en el horario
        self.gym_class = GymClass.objects.create(
            title="Yoga",
            description="Clase de yoga para todos los niveles",
            trainer="Juan Perez",
            capacity=20
        )

    def test_create_schedule(self):
        # Datos de prueba para crear un Schedule
        data = {
            "gym_class": self.gym_class.id,
            "start_time": "2025-02-09T10:00:00Z",
            "end_time": "2025-02-09T11:00:00Z"
        }

        # Realizar solicitud POST para crear un horario
        response = self.client.post('/api/gym/schedules/', data=data, format='json')

        # Validar que el horario se crea correctamente (código 201)
        self.assertEqual(response.status_code, 201)

        # Verificar que el horario se ha creado en la base de datos
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Schedule.objects.get().gym_class.title, "Yoga")


class ReservationTests(APITestCase):
    def setUp(self):
        # Crear usuario para la autenticación
        self.user = User.objects.create_user(username='testuser', password='password')

        # Crear token de acceso para el usuario
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Crear un cliente de prueba para hacer las solicitudes
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Crear una clase de gimnasio y un horario para la reserva
        self.gym_class = GymClass.objects.create(
            title="Yoga",
            description="Clase de yoga para todos los niveles",
            trainer="Juan Perez",
            capacity=20
        )
        self.schedule = Schedule.objects.create(
            gym_class=self.gym_class,
            start_time="2025-02-09T10:00:00Z",
            end_time="2025-02-09T11:00:00Z"
        )

    def test_create_reservation(self):
        # Datos de prueba para crear una reserva
        data = {
            "schedule": self.schedule.id
        }

        # Realizar solicitud POST para crear una reserva
        response = self.client.post('/api/gym/reservations/', data=data, format='json')

        # Validar que la reserva se crea correctamente (código 201)
        self.assertEqual(response.status_code, 201)

        # Verificar que la reserva se ha creado en la base de datos
        self.assertEqual(Reservation.objects.count(), 1)

    def test_duplicate_reservation(self):
        # Hacer una primera reserva
        data = {
            "schedule": self.schedule.id
        }
        self.client.post('/api/gym/reservations/', data=data, format='json')

        # Intentar hacer una reserva duplicada
        response = self.client.post('/api/gym/reservations/', data=data, format='json')

        # Validar que la respuesta es un error (400)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Ya tienes una reserva para esta clase")


class ReservationCancelTests(APITestCase):
    def setUp(self):
        # Crear usuario para la autenticación
        self.user = User.objects.create_user(username='testuser', password='password')

        # Crear token de acceso para el usuario
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Crear un cliente de prueba para hacer las solicitudes
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Crear una clase de gimnasio y un horario para la reserva
        self.gym_class = GymClass.objects.create(
            title="Yoga",
            description="Clase de yoga para todos los niveles",
            trainer="Juan Perez",
            capacity=20
        )
        self.schedule = Schedule.objects.create(
            gym_class=self.gym_class,
            start_time="2025-02-09T10:00:00Z",
            end_time="2025-02-09T11:00:00Z"
        )
        self.reservation = Reservation.objects.create(
            schedule=self.schedule,
            user=self.user
        )

    def test_cancel_reservation(self):
        # Realizar solicitud POST para cancelar la reserva
        response = self.client.post(f'/api/gym/reservations/{self.reservation.id}/cancel/', format='json')

        # Validar que la reserva se cancela correctamente (código 204)
        self.assertEqual(response.status_code, 204)

        # Verificar que la reserva ha sido eliminada de la base de datos
        self.assertEqual(Reservation.objects.count(), 0)

    def test_cancel_reservation_not_found(self):
        # Intentar cancelar una reserva que no pertenece al usuario autenticado
        response = self.client.post('/api/gym/reservations/999/cancel/', format='json')

        # Validar que la respuesta es un error (404)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], "Reserva no encontrada")
