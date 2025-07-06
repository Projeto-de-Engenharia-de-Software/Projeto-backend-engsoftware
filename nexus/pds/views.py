from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from equipes.models import Equipe

# #1. Homepage do pds
# def pds_home_view(request):
#     return HttpResponse("<h1>Essa é a tela inicial de Profissional de Saúde, seja Bem-Vindo!</h1>")

# #2. Configurações
# def pds_config_view(request):
#     return HttpResponse("<h1>Essa é a tela de configuração do *Profissional de Saúde*</h1>")

# #3. Manuseio de Boletins
# def pds_boletim_view(request):
#     return HttpResponse("<h1>Essa é a tela de observações de boletins do *Profissional de Saúde*</h1>")

# #4. Manuseio de Grupos por parte do pds
# def pds_grupo_view(request):
#     return HttpResponse("<h1>Essa é a tela de ánalise do grupo do *Profissional de Saúde*</h1>")


#1. Homepage do pds
@login_required
def pds_home_view(request):
    if request.user.profile.perfil != 'profissional':
        return HttpResponseForbidden()
    return JsonResponse({'mensagem': 'Bem-vindo(a) ao painel do Profissional de Saúde!'})

#2. Configurações
@login_required
def pds_config_view(request):
    if request.user.profile.perfil != 'profissional':
        return HttpResponseForbidden()
    return JsonResponse({'mensagem': 'Configurações do Profissional de Saúde.'})

#3. Manuseio de Boletins
@login_required
def pds_boletim_view(request):
    if request.user.profile.perfil != 'profissional':
        return HttpResponseForbidden()
    # Futuramente conectar com model Boletim
    return JsonResponse({'mensagem': 'Visualização dos boletins do profissional.'})

#4. Manuseio de Equipes por parte do pds
@login_required
def pds_equipe_view(request):
    if request.user.profile.perfil != 'profissional':
        return HttpResponseForbidden()

    equipes = Equipe.objects.filter(profissionais=request.user).values('id', 'nome', 'gestor__username')
    return JsonResponse({'equipes_participantes': list(equipes)})


