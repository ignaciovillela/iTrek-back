from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class AuthViewSet(ViewSet):
    """
    ViewSet que maneja la autenticación de usuarios:

    - POST   /auth/login/       : Autenticar usuario y devolver token junto con los detalles del usuario.
    - POST   /auth/logout/      : Cerrar sesión eliminando el token del usuario autenticado.
    - GET    /auth/check-login/ : Verificar si el usuario está autenticado.
    """

    def get_permissions(self):
        if self.action in ['login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Autentica al usuario y devuelve un token junto con los detalles del usuario.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Debe proporcionar username y password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        Cierra la sesión eliminando el token del usuario autenticado.
        """
        request.user.auth_token.delete()
        return Response({'message': 'Ha cerrado sesión exitosamente.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='check-login')
    def check_login(self, request):
        """
        Verifica si el usuario está autenticado.
        """
        return Response({'message': 'User is authenticated', 'username': request.user.username}, status=status.HTTP_200_OK)
