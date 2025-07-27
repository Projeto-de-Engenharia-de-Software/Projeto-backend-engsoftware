from django.db import models
from django.contrib.auth.models import User  # Para associar ao gestor

class Boletim(models.Model):
    nome = models.CharField(max_length=100)
    anotacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    gestor = models.ForeignKey(User, on_delete=models.CASCADE)

    # Futuro: pode guardar filtro/dados do dashboard 
    dados_dashboard = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.nome
