import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from payments.models import Invoice
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def user():
    # Fixture para crear un usuario normal.
    return get_user_model().objects.create_user(username="testuser", password="testpassword")

@pytest.fixture
def admin_user():
    # Fixture para crear un usuario administrador.
    return get_user_model().objects.create_user(username="adminuser", password="adminpassword", is_staff=True)

@pytest.fixture
def user_token(user):
    # Fixture para generar un token para un usuario normal.
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def admin_token(admin_user):
    # Fixture para generar un token para un administrador.
    refresh = RefreshToken.for_user(admin_user)
    return str(refresh.access_token)

@pytest.fixture
def client():
    #Fixture para crear un cliente API.
    return APIClient()

# Marcar las funciones de prueba con @pytest.mark.django_db
@pytest.mark.django_db
def test_create_invoice_as_admin(client, admin_token, user):
    url = "/api/payments/invoices/"
    data = {
        "user": user.id,
        "amount": 100.00,
        "status": "pending"
    }
    
    response = client.post(
        url,
        data,
        HTTP_AUTHORIZATION=f"Bearer {admin_token}",
        format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_invoice_as_non_admin(client, user_token, user):
    url = "/api/payments/invoices/"
    data = {
        "user": user.id,
        "amount": 100.00,
        "status": "pending"
    }

    response = client.post(
        url,
        data,
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
        format="json"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_get_user_invoices(client, user_token, user):
    invoice = Invoice.objects.create(user=user, amount=100.00, status="pending")
    url = "/api/payments/user-invoices/"

    response = client.get(
        url,
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
        format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Debería devolver 1 factura

@pytest.mark.django_db
def test_pay_invoice(client, user_token, user):
    invoice = Invoice.objects.create(user=user, amount=100.00, status="pending")
    url = f"/api/payments/invoices/{invoice.id}/pay/"

    response = client.patch(
        url,
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
        format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == "paid"
