from django.db import models

class RegistroViolencia(models.Model):
    ## Prévias da Adições de Registro, nós do back, precisamos adicionar todos os campos.
    ano = models.IntegerField()
    uf = models.CharField(max_length=2)
    tipo_crime = models.CharField(max_length=255)
    ocorrencias = models.IntegerField()

    def __str__(self):
        return f"{self.tipo_crime} em {self.uf} ({self.ano}) - {self.ocorrencias} casos"

    class Meta:
        verbose_name = "Registro de Violência"
        verbose_name_plural = "Registros de Violência"
