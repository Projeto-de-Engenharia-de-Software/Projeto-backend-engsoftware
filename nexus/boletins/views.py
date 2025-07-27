from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import BoletimForm
from .models import Boletim

# Só permite gestores
def is_gestor(user):
    return user.groups.filter(name='Gestor').exists()

@login_required
@user_passes_test(is_gestor)
def gerar_boletim(request):
    if request.method == 'POST':
        form = BoletimForm(request.POST)
        if form.is_valid():
            boletim = form.save(commit=False)
            boletim.gestor = request.user
            boletim.save()
            messages.success(request, 'Boletim gerado com sucesso!')
            return redirect('listar_boletins')
        else:
            messages.error(request, 'Houve um erro ao gerar o boletim.')
    else:
        form = BoletimForm()
    
    return render(request, 'boletins/gerar_boletim.html', {'form': form})

@login_required
@user_passes_test(is_gestor)
def listar_boletins(request):
    boletins = Boletim.objects.filter(gestor=request.user).order_by('-data_criacao')
    return render(request, 'boletins/listar_boletins.html', {'boletins': boletins})

@login_required
@user_passes_test(is_gestor)
def visualizar_boletim(request, boletim_id):
    boletim = get_object_or_404(Boletim, id=boletim_id, gestor=request.user)
    return render(request, 'boletins/visualizar_boletim.html', {'boletim': boletim})

