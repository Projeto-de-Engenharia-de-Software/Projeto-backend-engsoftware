from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .models import Equipe
from .serializers import EquipeSerializer, CriarEquipeSerializer, EditarEquipeSerializer

User = get_user_model()

# ViewSet só para ler equipes (somente para usuários autenticados)
class EquipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def minhas(self, request):
        equipes = Equipe.objects.filter(profissionais=request.user) | Equipe.objects.filter(gestor=request.user)
        equipes = equipes.distinct()
        serializer = self.get_serializer(equipes, many=True)
        return Response(serializer.data)

# View para criação de equipe
class EquipeCreateAPIView(generics.CreateAPIView):
    serializer_class = CriarEquipeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Equipe criada com sucesso!"}, status=status.HTTP_201_CREATED)

