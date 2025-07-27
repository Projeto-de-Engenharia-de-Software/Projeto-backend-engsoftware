from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Equipe
from .serializers import EquipeSerializer, MembroEquipeSerializer

class IsGestorDaEquipe(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas o gestor da equipe
    possa realizar ações de escrita (edição, adição/remoção de membros).
    Isso substitui a verificação 'if request.user != equipe.gestor:'.
    """
    def has_object_permission(self, request, view, obj):
        # Permite acesso de leitura para todos os membros da equipe.
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.gestor or request.user in obj.profissionais.all()
        # Permite acesso de escrita apenas para o gestor.
        return request.user == obj.gestor


class EquipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet que gerencia todas as operações de API para Equipes.
    """
    serializer_class = EquipeSerializer
    permission_classes = [permissions.IsAuthenticated, IsGestorDaEquipe]



    def get_queryset(self):
        """
        Esta função substitui a view 'equipes_home'.
        Ela filtra a lista de equipes para mostrar apenas aquelas
        às quais o usuário logado pertence (seja como gestor ou profissional).
        """
        user = self.request.user
        queryset = Equipe.objects.filter(profissionais=user) | Equipe.objects.filter(gestor=user)
        return queryset.distinct()



    def perform_create(self, serializer):
        """
        Esta função substitui a view 'equipes_cadastrar'.
        Ela chama o método do modelo para criar a equipe,
        automaticamente definindo o usuário logado como o gestor.
        """
        try:
            # Reutiliza a lógica de validação do seu modelo
            Equipe.criar_equipe(nome=serializer.validated_data.get('nome'), gestor=self.request.user)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    
    
    def destroy(self, request, *args, **kwargs):
        """
        Função que remove uma equipe.
        Ela chama o método do modelo para remover a equipe, garantindo que somente o gestor possa removê-la.
        """
        equipe = self.get_object()

        try:
            # com as validações do modelo, removendo a equipe
            Equipe.remover_equipe(nome=equipe.nome, gestor=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            # Caso o método do modelo tenha alguma outra validação que falhe
            return Response({'erro': str(e)}, status=status.HTTP_400_BAD_REQUEST)




    @action(detail=True, methods=['post'], url_path='adicionar-profissional')
    def adicionar_profissional(self, request, pk=None):
        """
        Ação customizada que substitui a parte 'adicionar' da view 'equipes_editar'.
        """
        equipe = self.get_object() # Busca a equipe pelo ID na URL
        serializer = MembroEquipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profissional = User.objects.get(username=serializer.validated_data['username'])
        
        try:
            equipe.adicionar_profissional(profissional)
            return Response({'status': 'Profissional adicionado com sucesso'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'erro': str(e)}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=['post'], url_path='remover-profissional')
    def remover_profissional(self, request, pk=None):
        """
        Ação customizada que substitui a parte 'remover' da view 'equipes_editar'.
        """
        equipe = self.get_object()
        serializer = MembroEquipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profissional = User.objects.get(username=serializer.validated_data['username'])

        equipe.remover_profissional(profissional)
        return Response({'status': 'Profissional removido com sucesso'}, status=status.HTTP_200_OK)