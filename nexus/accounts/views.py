from django.shortcuts import render
from django.http import HttpResponse

## 1. Tela de cadastro de usuário
# Cadastro 1
def cadastro_view(request):
    return HttpResponse("<h1>Essa é a tela de cadastro do usuário")

# Castro Com as telas mais avançadas
def cadastro_advanced_view(request):
    return HttpResponse("<h1>Essa é a tela de cadastro avançado do usuário")

## 2. Tela de Login
# Tela de Login
def login_view(request):
    return HttpResponse("<h1>Essa é a tela de login do usuário</h1>")

# Recuperar Senha
def recuperar_senha_view(request):
    return HttpResponse("<h1>Essa é a tela de recuperar senha por meio de login do usuário</h1>")