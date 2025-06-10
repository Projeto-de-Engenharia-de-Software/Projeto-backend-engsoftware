from django.db import models

class Regiao(models.Model):
    # A coluna 'Regiao' do CSV (ex: "VALE DO S.FRANCISCO E ARARIPE")
    nome = models.CharField(max_length=200, unique=True)
    # A coluna 'Total' do CSV
    total_anual_csv = models.FloatField(null=True, blank=True, help_text="Total anual somado a partir do CSV")

    class Meta:
        verbose_name = "Região"
        verbose_name_plural = "Regiões"

    def __str__(self):
        return self.nome

class DadosMensaisRegiao(models.Model):
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE, help_text="Região a que o dado se refere")
    ano = models.IntegerField(help_text="Ano do registro (ex: 2024)")
    mes = models.IntegerField(help_text="Mês do registro (1 para Janeiro, 12 para Dezembro)") # 1 a 12
    valor = models.FloatField(help_text="Valor numérico para o mês/ano")

    class Meta:
        unique_together = ('regiao', 'ano', 'mes') # Garante que não haja duplicatas para o mesmo mês/ano/região
        ordering = ['regiao', 'ano', 'mes'] # Ordena os dados para consulta
        verbose_name = "Dado Mensal da Região"
        verbose_name_plural = "Dados Mensais das Regiões"

    def __str__(self):
        # Formatando o mês com dois dígitos (ex: 01, 02)
        return f"{self.regiao.nome} - {self.mes:02d}/{self.ano}: {self.valor}"
