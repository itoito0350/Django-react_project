import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

# Fixture para crear un usuario normal
@pytest.fixture
def user():
    return get_user_model().objects.create_user(username="testuser", password="testpassword")

# Fixture para crear un cliente API
@pytest.fixture
def client():
    return APIClient()

# Fixture para generar un token JWT para un usuario normal
@pytest.fixture
def user_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

# Test para el registro de un nuevo usuario
@pytest.mark.django_db
def test_register_user(client):
    url = "/api/auth/register/"
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword"
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.data
    assert "email" in response.data

# Test para login de un usuario con JWT
@pytest.mark.django_db
def test_login_user(client, user):
    url = "/api/auth/login/"
    data = {
        "username": user.username,
        "password": "testpassword"
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data  # Verifica que se reciba el token de acceso
    assert "refresh" in response.data  # Verifica que se reciba el token de refresco

# Test para el acceso al perfil de usuario (requiere autenticación)
@pytest.mark.django_db
def test_update_profile(client, user_token):
    url = "/api/auth/update-profile/"
    data = {
        "username": "updateduser",
        "email": "updateduser@example.com",
        "password": "newpassword"
    }
    response = client.put(
        url, 
        data, 
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
        format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "updateduser"
    assert response.data["email"] == "updateduser@example.com"

# Test para eliminar la cuenta de usuario (requiere autenticación)
@pytest.mark.django_db
def test_delete_user(client, user_token):
    url = "/api/auth/delete-account/"
    response = client.delete(
        url, 
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

