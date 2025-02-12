
from django.urls import path
from payments import views

urlpatterns = [
    path('invoices/', views.create_invoice, name='create-invoice'),  # Solo admin puede acceder a esta URL
    path('user-invoices/', views.get_user_invoices, name='user-invoices'),  # Los usuarios pueden ver sus facturas
    path('invoices/<int:invoice_id>/pay/', views.pay_invoice, name='pay-invoice'),  # Los usuarios pueden pagar sus facturas
]

