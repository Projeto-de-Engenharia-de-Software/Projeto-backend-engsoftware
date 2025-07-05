from django.urls import path, include
from . import views


urlpatterns = [
    # Tela de cadastro de usuário - Cadastro avançado - Login - Recuperar Senha
    path('', views.register, name='register'),
    path('2/', views.cadastro_advanced_view, name='home'),
    path('login/', views.user_login, name='login'),
    path('rec-senha/', views.recuperar_senha_view, name='password_reset'),
]