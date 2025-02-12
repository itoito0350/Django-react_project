
from rest_framework.routers import DefaultRouter
from django.urls import path


class CustomRouter(DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        if hasattr(viewset, 'action') and hasattr(viewset.action, 'cancel'):
            routes.append(
                path('reservations/<int:pk>/cancel/', 
                     viewset.as_view({'post': 'cancel'}), 
                     name='reservation-cancel')
            )
        return routes

