from django.urls import path
from .api_views import BoletimAPIView, BoletimCreateAPIView, BoletimUpdateAPIView, BoletimDeleteAPIView

urlpatterns = [
    path('', BoletimAPIView.as_view({'get': 'list'}), name='boletim-list'),
    
    # Criar um novo boletim (POST /api/boletins/create/)
    path('create/', BoletimCreateAPIView.as_view(), name='boletim-create'),
    
    # Visualizar detalhes, Atualizar e Deletar um boletim específico
    # (GET, PUT/PATCH, DELETE /api/boletins/<int:pk>/)
    path('<int:pk>/', BoletimAPIView.as_view({'get': 'retrieve'}), name='boletim-detail'),
    path('<int:pk>/update/', BoletimUpdateAPIView.as_view(), name='boletim-update'),
    path('<int:pk>/delete/', BoletimDeleteAPIView.as_view(), name='boletim-delete'),
]

