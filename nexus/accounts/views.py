from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ProfileForm


######################## SERIARIZAR ############################

## 1. Tela de cadastro de usuário
def register(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login') # Redirect to login page
    else:
        form = ProfileForm()
    return render(request, 'accounts/register.html', {'form': form})


## 2. Tela de Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bem-vindo, {user.profile.nome_completo}!')
                if user.profile.perfil == 'gestor':
                    return redirect('home')
                elif user.profile.perfil == 'profisional':
                    return redirect('pds')  
            else:
                messages.error(request, 'Email ou senha inválidos.')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

######################## VIEWS ANTIGAS(Feitas mais pra debugar código msm :D) ############################

def cadastro_view(request):
    return HttpResponse("<h1>Essa é a tela de cadastro do usuário")

def cadastro_advanced_view(request):
    return HttpResponse("<h1>Essa é a tela de cadastro avançado do usuário")

def user_logout(request):
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('login')

## Recuperar Senha
def recuperar_senha_view(request):
    return HttpResponse("<h1>Essa é a tela de recuperar senha por meio de login do usuário</h1>")