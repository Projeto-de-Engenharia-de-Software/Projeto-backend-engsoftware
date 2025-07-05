from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import ProfileSerializer, UserRegistrationSerializer

# Obtém o modelo de usuário ativo (User padrão)
User = get_user_model() 

# Requisição de API focada para o Perfil criado
class UserProfileView(viewsets.ReadOnlyModelViewSet): 
    queryset = Profile.objects.all() # Retorna todos os perfis
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # Somente usuários autenticados podem ver

    # Definir o ponto me! para autenticar o usuário que já afirma seu Token no login
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user.profile) # Acessa o perfil do usuário logado
        return Response(serializer.data)

# View específica para Cadastro de Perfis/Usuários
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    #Função de coleta de e persistência dos dados no banco de dados via API
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({"message": "Usuário cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)


    
