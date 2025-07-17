from django import forms
from django.contrib.auth.models import User
from .models import Equipe


class EquipeForm(forms.ModelForm):
    nome = forms.CharField(label='Nome da Equipe', max_length=100)

    class Meta:
        model = Equipe
        fields = ['nome']

# Validação: não permitir nomes de equipe duplicados para o mesmo gestor
def clean_nome(self):
    nome = self.cleaned_data.get('nome')
    gestor = self.initial.get('gestor') or self.gestor_externo

    if Equipe.objects.filter(nome=nome, gestor=gestor).exists():
        raise forms.ValidationError("Você já possui uma equipe com esse nome.")
    return nome


def save(self, commit=True):
    equipe = super().save(commit=False)

    # Garante que o gestor foi definido via self.gestor_externo
    if not hasattr(self, 'gestor_externo'):
        raise ValueError("É necessário definir o gestor com `form.set_gestor(user)` antes de salvar.")

    equipe.gestor = self.gestor_externo

    if commit:
        equipe.save()

    return equipe


# Método extra para definir o gestor 
def set_gestor(self, user):
    self.gestor_externo = user


class adicionar_profissionalForm(forms.Form):
    username = forms.CharField(label='Usuário')

    def __init__(self, *args, equipe=None, **kwargs):
        self.equipe = equipe
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Usuário não encontrado.")

        if self.equipe and self.equipe.profissionais.filter(username=username).exists():
            raise forms.ValidationError("Este usuário já faz parte da equipe.")
        return username

    def save(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        self.equipe.profissionais.add(user)


class remover_profissionalForm(forms.Form):
    username = forms.CharField(label='Usuário')

    def __init__(self, *args, equipe=None, **kwargs):
        self.equipe = equipe
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Usuário não encontrado.")

        if self.equipe and not self.equipe.profissionais.filter(username=username).exists():
            raise forms.ValidationError("Este usuário não está na equipe.")
        return username

    def save(self):
        user = User.objects.get(username=self.cleaned_data['username'])
        self.equipe.profissionais.remove(user)
