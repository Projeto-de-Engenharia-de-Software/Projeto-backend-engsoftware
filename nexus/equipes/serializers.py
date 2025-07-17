from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Equipe

User = get_user_model()

############################ SERIALIZAR USUÁRIOS E EQUIPES ############################

class UsuarioSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class EquipeSerializer(serializers.ModelSerializer):
    gestor = UsuarioSimplesSerializer(read_only=True)
    profissionais = UsuarioSimplesSerializer(many=True, read_only=True)

    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'gestor', 'profissionais']


##################### SERIALIZER PARA CADASTRO E EDIÇÃO DE EQUIPE #########################

class CriarEquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = ['nome']  # gestor será atribuído via view com `request.user`

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None     

    # 1. Verifica se o usuário é gestor
        if user.profile.perfil != 'gestor':
            raise serializers.ValidationError("Apenas usuários com perfil 'gestor' podem criar equipes.")

    # 2. Verifica se o nome da equipe já foi usado por esse gestor
        if Equipe.objects.filter(nome=data['nome'], gestor=user).exists():
            raise serializers.ValidationError("Você já criou uma equipe com esse nome.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['gestor'] = request.user
        return super().create(validated_data)


class AdicionarProfissionalSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")
        return value
    
class RemoverProfissionalSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")
        return value
