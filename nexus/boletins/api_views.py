from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Boletim
from .serializers import BoletimSerializer, BoletimCreateSerializer, BoletimUpdateSerializer

# View para listar e visualizar boletins (apenas leitura)
class BoletimAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Boletim.objects.all()
    serializer_class = BoletimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Boletim.objects.filter(gestor=user)

# View para criar boletins
class BoletimCreateAPIView(generics.CreateAPIView):
    serializer_class = BoletimCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Boletim criado com sucesso!"}, status=status.HTTP_201_CREATED)

# View para atualizar boletins
class BoletimUpdateAPIView(generics.UpdateAPIView):
    serializer_class = BoletimUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Boletim.objects.all()

    def get_queryset(self):
        return Boletim.objects.filter(gestor=self.request.user)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Boletim atualizado com sucesso!"}, status=status.HTTP_200_OK)

# View para deletar boletins
class BoletimDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Boletim.objects.all()

    def get_queryset(self):
        return Boletim.objects.filter(gestor=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Boletim deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

