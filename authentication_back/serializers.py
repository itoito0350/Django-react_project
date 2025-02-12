from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Serializador para crear usuarios (registro)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Encriptar contraseña
        return super().create(validated_data)

# Serializador para actualizar los datos del usuario
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def update(self, instance, validated_data):
        # Si se quiere modificar la contraseña, se encripta antes de guardarla
        password = validated_data.get('password', None)
        if password:
            validated_data['password'] = make_password(password)

        return super().update(instance, validated_data)
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)