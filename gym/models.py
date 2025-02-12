from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GymClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    trainer = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name="schedules")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
      return f"{self.gym_class.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="reservations")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="reservations")
    reservation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =['user', 'schedule']
    
    def __str__(self):
        return f"{self.user.username} - {self.schedule.gym_class.title} ({self.schedule.start_time})"