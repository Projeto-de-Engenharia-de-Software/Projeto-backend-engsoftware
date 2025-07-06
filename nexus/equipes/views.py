from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import Equipe

# Listar equipes do usuário
@login_required
def equipes_home(request):
    user = request.user
    equipes = Equipe.objects.filter(profissionais=user) | Equipe.objects.filter(gestor=user)
    equipes = equipes.distinct().values('id', 'nome', 'gestor__username')
    return JsonResponse({'equipes': list(equipes)})

# Criar nova equipe (gestor)
@login_required
def equipes_cadastrar(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Use o método POST com campo "nome".'}, status=400)

    nome = request.POST.get('nome')
    if not nome:
        return JsonResponse({'erro': 'O nome da equipe é obrigatório'}, status=400)

    try:
        equipe = Equipe.criar_equipe(nome, request.user)
        return JsonResponse({'mensagem': 'Equipe criada com sucesso', 'equipe_id': equipe.id})
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)

# Adicionar/remover profissional (gestor)
@login_required
def equipes_editar(request, equipe_id):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Use método POST com "acao" e "username".'}, status=400)

    equipe = get_object_or_404(Equipe, id=equipe_id)

    if request.user != equipe.gestor:
        return HttpResponseForbidden("Apenas o gestor pode editar esta equipe.")

    acao = request.POST.get('acao')
    username = request.POST.get('username')

    if not username or not acao:
        return JsonResponse({'erro': 'Campos "username" e "acao" são obrigatórios'}, status=400)

    try:
        profissional = User.objects.get(username=username)

        if acao == 'adicionar':
            equipe.adicionar_profissional(profissional)
        elif acao == 'remover':
            equipe.remover_profissional(profissional)
        else:
            return JsonResponse({'erro': 'Ação inválida. Use "adicionar" ou "remover".'}, status=400)

        return JsonResponse({'mensagem': f'Profissional {acao} com sucesso'})

    except User.DoesNotExist:
        return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)

# Ver detalhes da equipe
@login_required
def equipes_detalhe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    
    if request.user != equipe.gestor and request.user not in equipe.profissionais.all():
        return HttpResponseForbidden("Você não pertence a esta equipe.")

    profissionais = equipe.profissionais.all().values('username', 'first_name', 'last_name')

    return JsonResponse({
        'equipe': {
            'id': equipe.id,
            'nome': equipe.nome,
            'gestor': equipe.gestor.username,
            'profissionais': list(profissionais)
        }
    })
