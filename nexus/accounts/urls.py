from django.urls import path, include
from . import views


urlpatterns = [
    # Tela de cadastro de usuário - Cadastro avançado - Login - Recuperar Senha
    path('', views.cadastro_view),
    path('2/', views.cadastro_advanced_view),
    path('login/', views.login_view),
    path('rec-senha/', views.recuperar_senha_view),
]