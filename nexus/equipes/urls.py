from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipes_home, name='home_equipes'),
    path('cria_equipes/', views.cria_equipes, name='cria_equipes'),
    path('<int:equipe_id>/', views.equipes_detalhe, name='equipes_detalhe'),
    
    # Novas URLs para adicionar e remover profissional
    path('<int:equipe_id>/add_profissional/', views.adicionar_profissional, name='equipe_adicionar_profissional'),
    path('<int:equipe_id>/rm_profissional/', views.remover_profissional, name='equipe_remover_profissional'),
]



