from django.urls import path, include
from .routers import CustomRouter  
from .views import GymClassViewSet, ScheduleViewSet, ReservationViewSet

# Usar el CustomRouter para registrar las rutas
router = CustomRouter()

# Registra los viewsets con el router personalizado
router.register(r'classes', GymClassViewSet, basename='gym-class')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'reservations', ReservationViewSet, basename='reservation')

# Incluye las URLs generadas por el router
urlpatterns = [
    path('', include(router.urls)),  
]
