from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    PERFIL_CHOICES = [
        ('gestor', 'Gestor'),
        ('profissional', 'Profissional'),
    ]

    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES)
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    unidade_saude = models.CharField(max_length=100, blank=True, null=True)  # Só para profissionais
    especialidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.perfil})"
