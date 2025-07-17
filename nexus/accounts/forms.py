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

    # Conferir a questão da senha, e também o gestor com seus campos opcionais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmacao = cleaned_data.get("password_confirmacao")

        if password and password_confirmacao and password != password_confirmacao:
            self.add_error('password_confirmacao', "As senhas não coincidem.")

        perfil = cleaned_data.get('perfil')
        # Referenciando o campo com o nome correto: unidade_saude
        unidade_saude = cleaned_data.get('unidade_saude') 
        especialidade = cleaned_data.get('especialidade')

        if perfil == 'profissional':
            if not unidade_saude: # Usa o nome correto
                self.add_error('unidade_saude', "Profissionais de saúde devem informar a unidade de saúde.")
            if not especialidade:
                self.add_error('especialidade', "Profissionais de saúde devem informar a especialidade.")
        elif perfil == 'gestor':
            # CORREÇÃO: Usar o nome correto do campo
            cleaned_data['unidade_saude'] = None 
            cleaned_data['especialidade'] = None
        return cleaned_data

    def save(self, commit=True):
        # 1. Cria a instância do User (o que é manipulado por Meta.model = User)
        user = super().save(commit=False)
        
        # 2. Define a senha no objeto User (essencial para hashing)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            # 3. Salva o User no DB. Esta linha (user.save()) DISPARA o sinal post_save,
            #    que automaticamente CRIA o Profile básico (com o user_id) para este User.
            user.save() 
            
            # 4. AGORA, ACESSE o objeto Profile que acabou de ser criado pelo sinal
            #    E PREENCHA seus campos com os dados do formulário.
            profile = user.profile # <-- ESSA É A LINHA CHAVE: Acessa o Profile EXISTENTE
            
            profile.nome_completo = self.cleaned_data['nome_completo']
            profile.perfil = self.cleaned_data['perfil']
            profile.unidade_saude = self.cleaned_data['unidade_saude']
            profile.especialidade = self.cleaned_data['especialidade']
            
            # 5. Salva o Profile, atualizando-o com os dados do formulário
            profile.save() 

        return user