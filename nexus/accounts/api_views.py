from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Gestor, ProfissionalSaude, UnidadeSaude, CustomUser
from .serializers import *

class UnidadeSaudeViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API que permite que as Unidades de Saúde sejam visualizadas ou editadas.
    """
    queryset = UnidadeSaude.objects.all()
    serializer_class = UnidadeSaudeSerializer
    permission_classes = [permissions.IsAdminUser]

class GestorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar e editar os Gestores.
    """
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfissionalSaudeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar e editar os Profissionais de Saúde.
    """
    queryset = ProfissionalSaude.objects.all()
    serializer_class = ProfissionalSaudeSerializer
    permission_classes = [permissions.IsAdminUser]

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Um ViewSet que fornece um endpoint `me` para obter os dados do utilizador autenticado.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Determina qual serializer usar com base no tipo de utilizador.
        """
        if hasattr(self.request.user, 'gestor'):
            return GestorSerializer
        elif hasattr(self.request.user, 'profissionalsaude'):
            return ProfissionalSaudeSerializer
        return CustomUserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        """
        Retorna os dados do perfil do utilizador atualmente autenticado.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RegistrationAPIView(generics.GenericAPIView):
    """
    Endpoint da API para o registo de novos utilizadores.
    """
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        perfil = self.request.data.get('perfil')
        if perfil == 'gestor':
            return GestorSerializer
        elif perfil == 'profissional':
            return ProfissionalSaudeSerializer
        return None

    def post(self, request, *args, **kwargs):
        perfil = request.data.get('perfil')
        if not perfil:
            return Response(
                {"error": "O campo 'perfil' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer_class = self.get_serializer_class()
        if serializer_class is None:
            return Response(
                {"error": "O valor do 'perfil' deve ser 'gestor' ou 'profissional'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
