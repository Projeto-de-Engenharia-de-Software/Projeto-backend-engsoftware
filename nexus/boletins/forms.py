from django import forms
from .models import Boletim

class BoletimForm(forms.ModelForm):
    class Meta:
        model = Boletim
        fields = ['nome', 'anotacoes', 'dados_dashboard']
        widgets = {
            'anotacoes': forms.Textarea(attrs={'rows': 4}),
        }
