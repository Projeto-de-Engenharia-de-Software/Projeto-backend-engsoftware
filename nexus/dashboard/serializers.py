from rest_framework import serializers
from .models import RegistroViolencia

class GestorRegistroViolenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroViolencia
        fields = '__all__'


# Serializer para PROFISSIONAIS (mostra apenas os campos selecionados)
class ProfissionalRegistroViolenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroViolencia
        fields = [
            'id',             # ID do registro
            'NU_ANO',         # Ano da ocorrência
            'DT_NOTIFIC',     # Data da notificação
            'MUNICIPIO',      # Município da ocorrência
            'DT_OCOR',        # Data da ocorrência
            'CS_SEXO',        # Sexo da vítima
            'CS_RACA',        # Raça/Cor da vítima
            'LOCAL_OCOR',     # Local de ocorrência
            'SEX_ASSEDI',     # Se houve assédio sexual
            'SEX_ESTUPR',     # Se houve estupro
        ]



    
