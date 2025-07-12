from rest_framework import serializers
from .models import Gestor, ProfissionalSaude, UnidadeSaude

class UnidadeSaudeSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo UnidadeSaude.
    """
    class Meta:
        model = UnidadeSaude
        fields = ['id', 'nome', 'endereco']

class GestorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Gestor.
    """
    # O campo 'password' é write-only para não ser exposto em GET requests.
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # Sobrescreve o método create para lidar com a password corretamente.
        user = Gestor.objects.create_user(**validated_data)
        return user

    class Meta:
        model = Gestor
        # Lista de campos a serem incluídos na API
        fields = ['id', 'username', 'email', 'nome_completo', 'orgao', 'password']
        # Define campos que não devem ser expostos ao ler dados
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProfissionalSaudeSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Profissional de Saúde.
    """
    password = serializers.CharField(write_only=True)
    # Inclui o serializer de UnidadeSaude para mostrar os detalhes das unidades
    unidades_saude = UnidadeSaudeSerializer(many=True, read_only=True)
    # Campo para receber os IDs das unidades ao criar/atualizar
    unidades_saude_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=UnidadeSaude.objects.all(), 
        source='unidades_saude'
    )

    def create(self, validated_data):
        user = ProfissionalSaude.objects.create_user(**validated_data)
        return user

    def validate_unidades_saude_ids(self, value):
        """
        Validação para o limite de 2 unidades de saúde na API.
        """
        if len(value) > 2:
            raise serializers.ValidationError("Um profissional de saúde não pode estar associado a mais de 2 unidades de saúde.")
        return value

    class Meta:
        model = ProfissionalSaude
        fields = [
            'id', 'username', 'email', 'nome_completo', 'especialidade', 
            'unidades_saude', 'unidades_saude_ids', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
