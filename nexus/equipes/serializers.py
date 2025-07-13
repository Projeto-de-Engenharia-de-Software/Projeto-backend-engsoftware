from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Equipe

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer simples para exibir informações básicas do usuário (gestor e profissionais).
    """
    class Meta:
        model = User 
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Profile, que inclui informações adicionais do usuário.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'nome_completo', 'unidade_saude', 'especialidade']

class EquipeSerializer(serializers.ModelSerializer):
    """
    Serializer principal para o modelo Equipe.
    Ele exibe os detalhes do gestor e a lista de profissionais de forma aninhada.
    Isso substitui a construção manual do dicionário na sua view 'equipes_detalhe'.
    """
    gestor = UserSerializer(read_only=True)
    profissionais = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Equipe
        # Inclui os campos que queremos exibir na API
        fields = ['id', 'nome', 'gestor', 'profissionais']

class MembroEquipeSerializer(serializers.Serializer):
    """
    Serializer auxiliar usado pelas ações de adicionar/remover.
    Ele valida o campo 'username' enviado na requisição,
    substituindo a busca manual e o bloco try/except na view 'equipes_editar'.
    """
    username = serializers.CharField()

    def validate_username(self, value):
        # Garante que o usuário com o username fornecido exista
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Usuário não encontrado.")
        return value