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
            'ano',
            'id_municip',
            'dt_ocor',
            'dt_nasc',
            'cs_sexo',
            'cs_raca',
            'id_munic_resi',
            'id_mn_ocor',
            'local_ocor',
            'local_espec',
            'out_vezes'
        ]



    
