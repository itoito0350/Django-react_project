from django.urls import path
from .views import notifications_view

urlpatterns = [
    path("notificaciones/", notifications_view, name="notifications"),
]
