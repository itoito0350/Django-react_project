from rest_framework import viewsets, status
from .models import GymClass, Schedule, Reservation
from .serializers import GymClassSerializer, ScheduleSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.all()
    serializer_class = GymClassSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Solo permite que los usuarios vean sus propias reservas, excepto admin."""
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        """Permite a un usuario reservar una clase si hay cupo disponible."""
        if not request.user or request.user.is_anonymous:
            return Response({"error": "Debes estar autenticado para hacer una reserva"}, status=status.HTTP_401_UNAUTHORIZED)

        schedule_id = request.data.get('schedule')
        user = request.user

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"error": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Contar las reservas existentes en este horario
        reservas_actuales = Reservation.objects.filter(schedule=schedule).count()
        capacidad_maxima = schedule.gym_class.capacity  # Corregido

        if reservas_actuales >= capacidad_maxima:
            return Response({"error": "Clase llena"}, status=status.HTTP_403_FORBIDDEN)

        # Verificar si el usuario ya tiene una reserva en este horario
        reservation, created = Reservation.objects.get_or_create(schedule=schedule, user=user)
        if not created:
            return Response({"error": "Ya tienes una reserva para esta clase"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        # Permite a un usuario cancelar su reserva.
        try:
            reservation = Reservation.objects.get(id=pk, user=request.user)
            reservation.delete()
            return Response({"message": "Reserva cancelada"}, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist:
            return Response({"error": "Reserva no encontrada"}, status=status.HTTP_404_NOT_FOUND)

