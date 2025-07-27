from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Profile

User = get_user_model() 

############################ SERIALIZAR OS USUÁRIOS ############################

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'nome_completo', 'perfil', 'unidade_saude', 'especialidade', 'data_criacao']



######################## SERIARIZAR OS FORMULÁRIOS PARA CADASTRO ############################

# Serializer para Cadastro
class UserRegistrationSerializer(serializers.Serializer):
    # Campos que vêm diretamente do modelo User
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirmacao = serializers.CharField(write_only=True, style={'input_type': 'password'})

    # Campos que vêm do modelo Profile
    nome_completo = serializers.CharField(max_length=100)
    perfil = serializers.ChoiceField(choices=Profile.PERFIL_CHOICES)
    unidade_saude = serializers.CharField(max_length=100, required=False, allow_blank=True)
    especialidade = serializers.CharField(max_length=100, required=False, allow_blank=True)

    # Etapa de Validação 
    def validate(self, data):
        # 1. Validação de senhas
        if data['password'] != data['password_confirmacao']:
            raise serializers.ValidationError({"password_confirmacao": "As senhas não coincidem."})
        
        # 2. Validação de unicidade de username (usando o modelo ativo)
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Este nome de usuário já está em uso."})
        
        # 3. Validação de unicidade de email (usando o modelo ativo)
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Este email já está cadastrado."})

        # 4. Validação de campos condicionais (unidade_saude e especialidade para 'profissional')
        if data['perfil'] == 'profissional':
            if not data.get('unidade_saude'):
                raise serializers.ValidationError({"unidade_saude": "Profissionais de saúde devem informar a unidade de saúde."})
            if not data.get('especialidade'):
                raise serializers.ValidationError({"especialidade": "Profissionais de saúde devem informar a especialidade."})
            
        elif data['perfil'] == 'gestor':
            # 4.1 Limpar ou garantir que são None para gestores se o modelo não permitir blank/null
            data['unidade_saude'] = "" 
            data['especialidade'] = "" 
            
        return data

    # Etapa de Criação do Usuário
    def create(self, validated_data):
        # Remove a confirmação de senha
        validated_data.pop('password_confirmacao') 
        
        # 1. Extrai os dados do Profile para usar APÓS a criação do User
        profile_data = {
            'nome_completo': validated_data.pop('nome_completo'),
            'perfil': validated_data.pop('perfil'),
            'unidade_saude': validated_data.pop('unidade_saude'),
            'especialidade': validated_data.pop('especialidade'),
        }
        
        # 2. Cria os dados validados de usuários
        user = User.objects.create_user(**validated_data) 

        # 2.1 Persiste os mesmos dados em Perfil também, com características a mais
        profile = user.profile
        profile.nome_completo = profile_data['nome_completo']
        profile.perfil = profile_data['perfil']
        profile.unidade_saude = profile_data['unidade_saude']
        profile.especialidade = profile_data['especialidade']
        profile.save()
        
        return user


# Serializer para Atualização de Usuário e Perfil em conjunto
class UserUpdateSerializer(serializers.Serializer):
    nome_completo = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    unidade_saude = serializers.CharField(max_length=100, required=False, allow_blank=True)
    especialidade = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_email(self, value):
        """
        Garante que o novo email não esteja em uso por OUTRO usuário.
        """
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Este email já está cadastrado em outra conta.")
        return value

    def validate(self, data):
        """
        Validação condicional para profissionais de saúde.
        """
        user = self.context['request'].user
        # Se o perfil for de profissional, os campos são obrigatórios.

        if user.profile.perfil == 'profissional': 
            # Verifica o valor que está chegando ou o valor que já existe
            if not (data.get('unidade_saude') or user.profile.unidade_saude):
                raise serializers.ValidationError({"unidade_saude": "Profissionais de saúde devem informar a unidade de saúde."})
            if not (data.get('especialidade') or user.profile.especialidade):
                raise serializers.ValidationError({"especialidade": "Profissionais de saúde devem informar a especialidade."})
        return data

    def update(self, instance, validated_data):
        profile_data = {
            'nome_completo': validated_data.get('nome_completo', instance.profile.nome_completo),
            'unidade_saude': validated_data.get('unidade_saude', instance.profile.unidade_saude),
            'especialidade': validated_data.get('especialidade', instance.profile.especialidade)
        }

        # Atualiza o campo de email no modelo User
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Atualiza os dados do Profile
        profile = instance.profile
        profile.nome_completo = profile_data['nome_completo']
        profile.unidade_saude = profile_data['unidade_saude']
        profile.especialidade = profile_data['especialidade']
        profile.save()

        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Valida que a nova senha e a confirmação são iguais e atende aos requisitos de segurança.
        """
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "As novas senhas não coincidem."})

        # Valida a complexidade da senha usando os validadores do Django
        # O self.context['request'].user garante que as regras específicas do usuário sejam aplicadas,
        # como não usar parte do username na senha, se configurado.
        try:
            validate_password(data['new_password'], self.context['request'].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)}) # `list(e.messages)` para formatar melhor
        
        return data
