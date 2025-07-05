from rest_framework import serializers
from .models import DadosMensaisRegiao, Regiao

############################ SERIALIZAR A REGIÃO ############################
class RegiaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Regiao
        fields = ['id', 'nome', 'total_anual_csv']

############################ SERIALIZAR OS DADOS MENSAIS DE CADA REGIÃO ############################

class DadosMensaisRegiaoSerializer(serializers.ModelSerializer):
    regiao = RegiaoSerializer(read_only=True)

    class Meta:
        model = DadosMensaisRegiao
        fields = ['id', 'regiao', 'ano', 'mes', 'valor']

    
