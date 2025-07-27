from rest_framework import viewsets, permissions
from .models import RegistroViolencia
from .serializers import GestorRegistroViolenciaSerializer, ProfissionalRegistroViolenciaSerializer

############################ PERMISSÃO DE VISUALIZAR DADOS ############################

# Permissão personalizada para permitir acesso apenas a usuários com perfil 'gestor'.
class IsGestor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.profile.perfil == 'gestor'

# Permissão personalizada para permitir acesso apenas a usuários com perfil 'profissional'.
class IsProfissional(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.profile.perfil == 'profissional'


class RegistroViolenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite visualizar os registros de violência.
    - Gestores: podem ver todos os dados.
    - Profissionais: podem ver apenas dados específicos.
    """
    permission_classes = [IsGestor | IsProfissional]

    def get_queryset(self):
        user = self.request.user

        if user.profile.perfil == 'gestor' or user.profile.perfil == 'profissional':
            return RegistroViolencia.objects.all().order_by('-NU_ANO')

        return RegistroViolencia.objects.none()
    

    def get_serializer_class(self):
        user = self.request.user

        if user.profile.perfil == 'gestor':
            return GestorRegistroViolenciaSerializer
        
        elif user.profile.perfil == 'profissional':
            # Para profissionais, usa o serializer com campos limitados
            return ProfissionalRegistroViolenciaSerializer
        
        return super().get_serializer_class()
