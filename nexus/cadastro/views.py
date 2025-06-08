from django.shortcuts import render
from django.http import HttpResponse

def cadastro_view(request):
    return HttpResponse("<h1>Essa é a tela de cadastro do usuário")

def cadastro_avanced_view(request):
    return HttpResponse("<h1>Essa é a tela de cadastro avançado do usuário")

