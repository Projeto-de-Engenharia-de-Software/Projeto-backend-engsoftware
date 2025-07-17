from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Equipe
from .forms import EquipeForm, EditarEquipeForm


######################### TELAS DE EQUIPE ############################

## 1. Tela inicial - lista de equipes do usuário logado
@login_required
def equipes_home(request):
    user = request.user
    equipes = Equipe.objects.filter(profissionais=user) | Equipe.objects.filter(gestor=user)
    equipes = equipes.distinct()
    return render(request, 'equipes/home_equipes.html', {'equipes': equipes})


## 2. Cadastro de nova equipe
@login_required
def cria_equipes(request):
    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            equipe = form.save(commit=False) # Instancia equipe sem salvar ainda no banco
            equipe.gestor = request.user # Usuario atual como gestor da equipe
            equipe.save()
            messages.success(request, 'Equipe criada com sucesso!')
            return redirect('home_equipes')
    else:
        form = EquipeForm()
    return render(request, 'equipes/cria_equipes.html', {'form': form})


## 3. Adicionar usuario na equipe (somente gestor)
@login_required  
def adicionar_profissional(request, equipe_id):
    try:
        equipe = Equipe.objects.get(id=equipe_id)  # Busca a equipe pelo ID
    except Equipe.DoesNotExist:
        messages.error(request, "Equipe não encontrada.")  
        return redirect('home_equipes')  

    # Verifica se o usuário logado é o gestor da equipe
    if request.user != equipe.gestor:
        messages.error(request, "Apenas o gestor pode adicionar profissionais.")
        return redirect('home_equipes')  

    if request.method == 'POST':
        form = EditarEquipeForm(request.POST)  
        if form.is_valid():  
            username = form.cleaned_data['username']  # Pega o nome de usuário enviado

            try:
                profissional = User.objects.get(username=username)  # Busca o usuário
                equipe.profissionais.add(profissional)  
                messages.success(request, f'{username} adicionado com sucesso!')
            except User.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")

            return redirect('equipes_detalhe', equipe_id=equipe.id)  # Volta para os detalhes da equipe

    else:
        form = EditarEquipeForm()  

    return render(request, 'equipes/adicionar.html', {'form': form, 'equipe': equipe})

## 4. Remover usuario da equipe (somente gestor)
@login_required  
def remover_profissional(request, equipe_id):
    try:
        equipe = Equipe.objects.get(id=equipe_id)  
    except Equipe.DoesNotExist:
        messages.error(request, "Equipe não encontrada.")
        return redirect('home_equipes')  

    if request.user != equipe.gestor:
        messages.error(request, "Apenas o gestor pode remover profissionais.")
        return redirect('home_equipes') 

    
    if request.method == 'POST':
        form = EditarEquipeForm(request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data['username']  

            try:
                profissional = User.objects.get(username=username)  
                equipe.profissionais.remove(profissional)  
                messages.success(request, f'{username} removido com sucesso!')
            except User.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")

            return redirect('equipes_detalhe', equipe_id=equipe.id)  

    else:
        form = EditarEquipeForm()  

   
    return render(request, 'equipes/remover.html', {'form': form, 'equipe': equipe})

## 5. Detalhes da equipe (somente gestor ou membros)
@login_required
def equipes_detalhe(request, equipe_id):
    try:
        equipe = Equipe.objects.get(id=equipe_id)
    except Equipe.DoesNotExist:
        messages.error(request, "Equipe não encontrada.")
        return redirect('home_equipes')

    if request.user != equipe.gestor and request.user not in equipe.profissionais.all():
        messages.error(request, "Você não tem permissão para ver esta equipe.")
        return redirect('home_equipes')

    return render(request, 'equipes/detalhe.html', {'equipe': equipe})
