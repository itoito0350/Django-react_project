from rest_framework import serializers
from .models import GymClass, Schedule, Reservation

class GymClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymClass
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    gym_class = serializers.PrimaryKeyRelatedField(queryset=GymClass.objects.all())  # Solo ID en lugar de objeto

    class Meta:
        model = Schedule
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__' 
