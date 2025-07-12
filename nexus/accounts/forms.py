from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Gestor, ProfissionalSaude, UnidadeSaude

class GestorCreationForm(UserCreationForm):
    """
    Formulário para criar um novo Gestor.
    Herda do formulário de criação de utilizador padrão e adiciona os campos de Gestor.
    """
    class Meta(UserCreationForm.Meta):
        model = Gestor
        # Adiciona os campos de Gestor aos campos padrão de utilizador
        fields = UserCreationForm.Meta.fields + ('nome_completo', 'email', 'orgao')

class GestorChangeForm(UserChangeForm):
    """
    Formulário para editar um Gestor existente.
    """
    class Meta(UserChangeForm.Meta):
        model = Gestor
        fields = UserChangeForm.Meta.fields

class ProfissionalSaudeCreationForm(UserCreationForm):
    """
    Formulário para criar um novo Profissional de Saúde.
    """
    # Usamos um ModelMultipleChoiceField para permitir a seleção de múltiplas unidades
    unidades_saude = forms.ModelMultipleChoiceField(
        queryset=UnidadeSaude.objects.all(),
        widget=forms.CheckboxSelectMultiple, # Apresenta como checkboxes
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = ProfissionalSaude
        fields = UserCreationForm.Meta.fields + ('nome_completo', 'email', 'especialidade', 'unidades_saude')

    def clean_unidades_saude(self):
        """
        Validação personalizada para garantir que não mais de 2 unidades são selecionadas.
        """
        unidades = self.cleaned_data.get('unidades_saude')
        if unidades and len(unidades) > 2:
            raise forms.ValidationError("Você não pode selecionar mais de 2 unidades de saúde.")
        return unidades

class ProfissionalSaudeChangeForm(UserChangeForm):
    """
    Formulário para editar um Profissional de Saúde existente.
    """
    unidades_saude = forms.ModelMultipleChoiceField(
        queryset=UnidadeSaude.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta(UserChangeForm.Meta):
        model = ProfissionalSaude
        fields = UserChangeForm.Meta.fields
