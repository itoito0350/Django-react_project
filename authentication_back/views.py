# views.py

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UpdateProfileSerializer, LoginSerializer

# Vista para el registro de usuarios
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Vista para la autenticación de usuarios (Login con JWT)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Asegúrate de añadir el serializador
    permission_classes = [AllowAny]

    def post(self, request):
        # Usar el serializador para validar los datos de la solicitud
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            else:
                return Response({'detail': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para actualizar el perfil del usuario
class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Vista para eliminar la cuenta del usuario
class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # En este caso no estamos realmente "cerrando" sesión
        # Solo debemos eliminar el token en el lado del cliente
        return Response({"detail": "Has cerrado sesión correctamente."}, status=200)