from django.shortcuts import render
from django.http import HttpResponse

#1. Homepage do pds
def pds_home_view(request):
    return HttpResponse("<h1>Essa é a tela inicial de Profissional de Saúde, seja Bem-Vindo!</h1>")

#2. Configurações
def pds_config_view(request):
    return HttpResponse("<h1>Essa é a tela de configuração do *Profissional de Saúde*</h1>")

#3. Manuseio de Boletins
def pds_boletim_view(request):
    return HttpResponse("<h1>Essa é a tela de observações de boletins do *Profissional de Saúde*</h1>")

#4. Manuseio de Grupos por parte do pds
def pds_grupo_view(request):
    return HttpResponse("<h1>Essa é a tela de ánalise do grupo do *Profissional de Saúde*</h1>")

