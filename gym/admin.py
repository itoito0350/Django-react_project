from django.contrib import admin
from .models import GymClass, Schedule, Reservation
# Register your models here.
admin.site.register(GymClass)
admin.site.register(Schedule)
admin.site.register(Reservation)