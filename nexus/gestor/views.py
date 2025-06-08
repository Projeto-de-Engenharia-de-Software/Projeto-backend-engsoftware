from django.shortcuts import render
from django.http import HttpResponse

#1. Homepage do Gestor
def gestor_home_view(request):
    return HttpResponse("<h1>Essa é a tela inicial de Gestor, seja Bem Vindo!</h1>")

#2. Configurações
def gestor_config_view(request):
    return HttpResponse("<h1>Essa é a tela de configuração do *Gestor*</h1>")

#3. Manuseio de Boletins
def gestor_boletim_view(request):
    return HttpResponse("<h1>Essa é a tela de observações de boletins do *Gestor*</h1>")

#4. Manuseio de Grupos por parte do Gestor
def gestor_grupo_view(request):
    return HttpResponse("<h1>Essa é a tela de ánalise do grupo do *Gestor*</h1>")

def gestor_add_grupo_view(request):
    return HttpResponse("<h1>Essa é a tela de adicionar alguém no grupo do *Gestor*</h1>")

def gestor_rmv_grupo_view(request):
    return HttpResponse("<h1>Essa é a tela de remover alguém no grupo do *Gestor*</h1>")

def gestor_att_grupo_view(request):
    return HttpResponse("<h1>Essa é a tela de atualizar as permissões de alguém no grupo do *Gestor*</h1>")



