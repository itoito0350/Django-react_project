
from django.contrib import admin
from django.urls import path, include
from .views import home 

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/gym/', include('gym.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/auth/', include('authentication_back.urls')),
    path('api/comunication/', include('comunication.urls')),
]
