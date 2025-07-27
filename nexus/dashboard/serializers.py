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
        fields = '__all__'



    
