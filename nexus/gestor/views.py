from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from equipes.models import Equipe
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# #1. Homepage do Gestor
# def gestor_home_view(request):
#     return HttpResponse("<h1>Essa é a tela inicial de Gestor, seja Bem Vindo!</h1>")

# #2. Configurações
# def gestor_config_view(request):
#     return HttpResponse("<h1>Essa é a tela de configuração do *Gestor*</h1>")

# #3. Manuseio de Boletins
# def gestor_boletim_view(request):
#     return HttpResponse("<h1>Essa é a tela de observações de boletins do *Gestor*</h1>")

# #4. Manuseio de Grupos por parte do Gestor
# def gestor_grupo_view(request):
#     return HttpResponse("<h1>Essa é a tela de ánalise do grupo do *Gestor*</h1>")

# def gestor_add_grupo_view(request):
#     return HttpResponse("<h1>Essa é a tela de adicionar alguém no grupo do *Gestor*</h1>")

# def gestor_rmv_grupo_view(request):
#     return HttpResponse("<h1>Essa é a tela de remover alguém no grupo do *Gestor*</h1>")

# def gestor_att_grupo_view(request):
#     return HttpResponse("<h1>Essa é a tela de atualizar as permissões de alguém no grupo do *Gestor*</h1>")


#1. Homepage do Gestor
@login_required
def gestor_home_view(request):
    if request.user.profile.perfil != 'gestor':
        return HttpResponseForbidden("Apenas gestores podem acessar.")
    return JsonResponse({'mensagem': 'Bem-vindo(a) ao painel do Gestor!'})

#2. Configurações
@login_required
def gestor_config_view(request):
    if request.user.profile.perfil != 'gestor':
        return HttpResponseForbidden()
    return JsonResponse({'mensagem': 'Configurações do gestor.'})

#3. Manuseio de Boletins
@login_required
def gestor_boletim_view(request):
    if request.user.profile.perfil != 'gestor':
        return HttpResponseForbidden()
    # Futuramente conectar com model Boletim
    return JsonResponse({'mensagem': 'Visualização dos boletins.'})

#4. Manuseio de Equipes por parte do Gestor
@login_required
def gestor_equipe_view(request):
    if request.user.profile.perfil != 'gestor':
        return HttpResponseForbidden()

    equipes = Equipe.objects.filter(gestor=request.user).values('id', 'nome')
    return JsonResponse({'equipes_gerenciadas': list(equipes)})

@login_required
def gestor_add_equipe_view(request):
    if request.user.profile.perfil != 'gestor':
        return HttpResponseForbidden()

    if request.method != 'POST':
        return JsonResponse({'erro': 'Use método POST com equipe_id e username'}, status=400)

    equipe_id = request.POST.get('equipe_id')
    username = request.POST.get('username')

    try:
        equipe = Equipe.objects.get(id=equipe_id, gestor=request.user)
        profissional = User.objects.get(username=username)
        equipe.adicionar_profissional(profissional)
        return JsonResponse({'mensagem': f'Usuário {username} adicionado à equipe {equipe.nome}.'})
    except Equipe.DoesNotExist:
        return JsonResponse({'erro': 'Equipe não encontrada ou não pertence a você.'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)

@login_required
def gestor_rmv_equipe_view(request):
    if request.user.profile.perfil != 'gestor':
        return HttpResponseForbidden()

    if request.method != 'POST':
        return JsonResponse({'erro': 'Use método POST com equipe_id e username'}, status=400)


    equipe_id = request.POST.get('equipe_id')
    username = request.POST.get('username')

    try:
        equipe = Equipe.objects.get(id=equipe_id, gestor=request.user)
        profissional = User.objects.get(username=username)
        equipe.remover_profissional(profissional)
        return JsonResponse({'mensagem': f'Usuário {username} removido da equipe {equipe.nome}.'})
    except Equipe.DoesNotExist:
        return JsonResponse({'erro': 'Equipe não encontrada ou não pertence a você.'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)

