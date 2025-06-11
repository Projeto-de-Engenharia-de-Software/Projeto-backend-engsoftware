from django.shortcuts import render
from django.http import HttpResponse

## View para depuração de código :D
def dashboard_home_view(request):
    return HttpResponse("<h1>Essa é a tela inicial de Dashboard, seja Bem Vindo!</h1>")

