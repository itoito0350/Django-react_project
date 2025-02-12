from django.urls import path
from .views import RegisterView, LoginView, UpdateProfileView, DeleteUserView,  LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Rutas para el registro y manejo de tokens (ya existentes)
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas para login, actualización de perfil y eliminación de cuenta
    path('login/', LoginView.as_view(), name='login'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
    path('logout/', LogoutView.as_view(), name='logout'), 
]
