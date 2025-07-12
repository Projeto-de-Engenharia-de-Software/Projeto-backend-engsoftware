from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import GestorCreationForm, ProfissionalSaudeCreationForm

def register_options_view(request):
    """
    View que mostra uma página com as duas opções de registo:
    "Sou um Gestor" e "Sou um Profissional de Saúde".
    """
    return render(request, 'accounts/register_options.html')

def register_gestor_view(request):
    """
    View para o formulário de registo de um Gestor.
    """
    if request.method == 'POST':
        form = GestorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Faz o login do utilizador automaticamente após o registo
            messages.success(request, 'Registo como Gestor realizado com sucesso!')
            return redirect('dashboard_gestor')  # Redireciona para o dashboard do gestor
    else:
        form = GestorCreationForm()
    
    context = {
        'form': form,
        'user_type': 'Gestor'
    }
    return render(request, 'accounts/register_form.html', context)

def register_profissional_view(request):
    """
    View para o formulário de registo de um Profissional de Saúde.
    """
    if request.method == 'POST':
        form = ProfissionalSaudeCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registo como Profissional de Saúde realizado com sucesso!')
            return redirect('dashboard_profissional')  # Redireciona para o dashboard do profissional
    else:
        form = ProfissionalSaudeCreationForm()
        
    context = {
        'form': form,
        'user_type': 'Profissional de Saúde'
    }
    return render(request, 'accounts/register_form.html', context)

def user_login_view(request):
    """
    View para o login de utilizadores. Aceita username ou email.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # O nosso backend personalizado trata de verificar por username ou email
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Verifica o tipo de utilizador e redireciona para a página correta
                if hasattr(user, 'gestor'):
                    messages.success(request, f'Bem-vindo, Gestor {user.nome_completo}!')
                    return redirect('dashboard_gestor')
                elif hasattr(user, 'profissionalsaude'):
                    messages.success(request, f'Bem-vindo, {user.nome_completo}!')
                    return redirect('dashboard_profissional')
                else:
                    # Para superutilizadores que não são nem gestores nem profissionais
                    messages.success(request, f'Bem-vindo, {user.username}!')
                    return redirect('admin:index')
            else:
                messages.error(request, 'Nome de utilizador/email ou senha inválidos.')
        else:
            messages.error(request, 'Nome de utilizador/email ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout_view(request):
    """
    View para fazer o logout do utilizador.
    """
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('login')
