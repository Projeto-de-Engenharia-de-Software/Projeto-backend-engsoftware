from django.urls import path
from . import views

urlpatterns = [
    path('boletins/', views.listar_boletins, name='listar_boletins'),
    path('boletins/novo/', views.gerar_boletim, name='gerar_boletim'),
    path('boletins/<int:boletim_id>/', views.visualizar_boletim, name='visualizar_boletim'),
]

