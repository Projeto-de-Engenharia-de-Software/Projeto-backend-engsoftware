from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipes_home, name='equipes_home'),
    path('cadastrar/', views.equipes_cadastrar, name='equipes_cadastrar'),
    path('<int:equipe_id>/', views.equipes_detalhe, name='equipes_detalhe'),
    path('<int:equipe_id>/editar/', views.equipes_editar, name='equipes_editar'),
]


