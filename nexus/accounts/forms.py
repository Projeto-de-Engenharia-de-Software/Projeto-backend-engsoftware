from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    nome_completo = forms.CharField(label='Nome Completo', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirmacao = forms.CharField(label='Digite novamente a mesma senha', widget=forms.PasswordInput)
    perfil = forms.ChoiceField(label='Escolha qual seu perfil', choices=Profile.PERFIL_CHOICES)
    unidade_saude = forms.CharField(label='Unidade de Trabalho', max_length=100, required=False)
    especialidade = forms.CharField(label='Especialidade', max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Conferir se o username já existe
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.") # Mensagem mais precisa
        return username

    # Conferir se o email já existe
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email

    # Conferir se as senhas coincidem e validar campos condicionais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmacao = cleaned_data.get("password_confirmacao")

        if password and password_confirmacao and password != password_confirmacao:
            self.add_error('password_confirmacao', "As senhas não coincidem.")

        perfil = cleaned_data.get('perfil')

        unidade_saude = cleaned_data.get('unidade_saude') 
        especialidade = cleaned_data.get('especialidade')

        # Validação condicional para profissionais de saúde
        if perfil == 'profissional':
            if not unidade_saude: 
                self.add_error('unidade_saude', "Profissionais de saúde devem informar a unidade de saúde.")
            if not especialidade:
                self.add_error('especialidade', "Profissionais de saúde devem informar a especialidade.")
        elif perfil == 'gestor':
            # Gestores não precisam desses campos, então podemos limpar
            cleaned_data['unidade_saude'] = None 
            cleaned_data['especialidade'] = None
        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)
        

        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save() 
            
            profile = user.profile
            
            profile.nome_completo = self.cleaned_data['nome_completo']
            profile.perfil = self.cleaned_data['perfil']
            profile.unidade_saude = self.cleaned_data['unidade_saude']
            profile.especialidade = self.cleaned_data['especialidade']
            
            profile.save() 

        return user

class ProfileUpdateForm(forms.ModelForm):
    # Campos que o usuário poderá editar
    nome_completo = forms.CharField(label='Nome Completo', max_length=100)
    email = forms.EmailField(label='Email')
    
    # Campos condicionais, não são obrigatórios para todos
    unidade_saude = forms.CharField(label='Unidade de Trabalho', max_length=100, required=False)
    especialidade = forms.CharField(label='Especialidade', max_length=100, required=False)

    # Campos de senha opcionais
    password = forms.CharField(label='Nova Senha', widget=forms.PasswordInput, required=False)
    password_confirmacao = forms.CharField(label='Confirme a Nova Senha', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['email'] # Apenas o email vem diretamente do modelo no Meta

    def __init__(self, *args, **kwargs):
        # O 'instance' é o objeto do usuário que estamos editando
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Preenche o formulário com os dados atuais do usuário e do perfil
        if self.instance:
            self.fields['email'].initial = self.instance.email
            self.fields['nome_completo'].initial = self.instance.profile.nome_completo
            self.fields['unidade_saude'].initial = self.instance.profile.unidade_saude
            self.fields['especialidade'].initial = self.instance.profile.especialidade
    
    def clean_email(self):
        # Validação para garantir que o novo email não esteja em uso por OUTRO usuário
        email = self.cleaned_data.get('email')
        # Exclui o próprio usuário da busca para permitir que ele mantenha seu email
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email já está cadastrado em outra conta.")
        return email

    def clean(self):
        # Validação para as senhas
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmacao = cleaned_data.get("password_confirmacao")

        # Só valida a confirmação se uma nova senha foi digitada
        if password and password != password_confirmacao:
            self.add_error('password_confirmacao', "As senhas não coincidem.")
        
        # Validação condicional para profissionais de saúde (igual à do registro)
        if self.instance.profile.perfil == 'profissional':
            if not cleaned_data.get('unidade_saude'):
                self.add_error('unidade_saude', "Profissionais de saúde devem informar a unidade de saúde.")
            if not cleaned_data.get('especialidade'):
                self.add_error('especialidade', "Profissionais de saúde devem informar a especialidade.")
                
        return cleaned_data

    def save(self, commit=True):
        user = self.instance
        profile = user.profile
        
        # Atualiza os dados
        user.email = self.cleaned_data['email']
        profile.nome_completo = self.cleaned_data['nome_completo']
        profile.unidade_saude = self.cleaned_data.get('unidade_saude')
        profile.especialidade = self.cleaned_data.get('especialidade')

        # Se uma nova senha foi fornecida, atualiza
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            profile.save()
            
        return user