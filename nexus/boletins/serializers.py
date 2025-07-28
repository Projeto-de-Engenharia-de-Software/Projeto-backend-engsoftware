from rest_framework import serializers
from .models import Boletim

class BoletimSerializer(serializers.ModelSerializer):
    gestor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Boletim
        fields = ['id', 'nome', 'anotacoes', 'data_criacao', 'gestor', 'dados_dashboard']


class BoletimCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=100)
    anotacoes = serializers.CharField(required=False, allow_blank=True)
    dados_dashboard = serializers.JSONField(required=False)

    def validate_nome(self, value):
        user = self.context['request'].user
        if Boletim.objects.filter(nome=value, gestor=user).exists():
            raise serializers.ValidationError("Já existe um boletim com esse nome para esse gestor.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return Boletim.objects.create(
            nome=validated_data['nome'],
            anotacoes=validated_data.get('anotacoes', ''),
            dados_dashboard=validated_data.get('dados_dashboard', {}),
            gestor=user
        )


