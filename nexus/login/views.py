from django.shortcuts import render
from django.http import HttpResponse


# Tela de Login
def login_view(request):
    return HttpResponse("<h1>Essa é a tela de login do usuário</h1>")

# Recuperar Senha
def recuperar_senha_view(request):
    return HttpResponse("<h1>Essa é a tela de recuperar senha por meio de login do usuário</h1>")

# Create your views here.
