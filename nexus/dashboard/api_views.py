from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Regiao, DadosMensaisRegiao
from .serializers import RegiaoSerializer, DadosMensaisRegiaoSerializer

# Requisição de API focada para a análise da Região
class RegiaoView(viewsets.ReadOnlyModelViewSet):
    queryset = Regiao.objects.all()
    serializer_class = RegiaoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Requisição de API focada para a análise dos dados Mensais de Cada Região
class DadosMensaisRegiaoView(viewsets.ReadOnlyModelViewSet):
    queryset = DadosMensaisRegiao.objects.all()
    serializer_class = DadosMensaisRegiaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 1. Relação de Filtragem
    def get_queryset(self):
        queryset = super().get_queryset()
        # 1.1 Filtros de Região
        regiao_id = self.request.query_params.get('regiao_id')
        if regiao_id:
            queryset = queryset.filter(regiao_id=regiao_id)
        # 1.2 Filtros de Ano
        ano = self.request.query_params.get('ano')
        if ano:
            queryset = queryset.filter(ano=ano)
        # 1.3 Filtros de Mês
        mes = self.request.query_params.get('mes')
        if mes:
            queryset = queryset.filter(mes=mes)

        return queryset.order_by('regiao__nome', 'ano', 'mes')