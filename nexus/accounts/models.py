from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    """
    Classe que representa o usuário do sistema, estendendo a classe AbstractUser do Django, provavelmente nunca instanciada
    """
    nome_completo = models.CharField(max_length=80)

    def __str__(self):
        return self.username

###################### Classes de Especialização do Usuário ######################
class Gestor(CustomUser):
    """
    Classe que representa o gestor do sistema, estendendo a classe User como a especialização.
    """
    orgao = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Gestor'
        verbose_name_plural = 'Gestores'



class UnidadeSaude(models.Model):
    """
    Classe que representa a unidade de saúde do Profissional de Saúde.
    """
    nome = models.CharField(max_length=80, unique=True)
    # Pode adicionar outros campos como telefone, cidade, etc.

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Unidade de Saúde'
        verbose_name_plural = 'Unidades de Saúde'



class ProfissionalSaude(CustomUser):
    """
    Classe que representa o profissional de saúde do sistema, estendendo a classe User como a especialização.
    """
    unidade_saude = models.ManyToManyField(
        UnidadeSaude,
        related_name='profissionais_saude'
    )
    especialidade = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Profissional de Saúde'
        verbose_name_plural = 'Profissionais de Saúde'

@receiver(m2m_changed, sender=ProfissionalSaude.unidade_saude.through)
def limitar_unidade_saude(sender, instance, action, **kwargs):
    """
    Sinal para limitar a quantidade de unidades de saúde associadas a um profissional de saúde.
    """
    if action == 'post_add':
        if instance.unidade_saude.count() > 2:
            raise ValidationError("Um profissional de saúde não pode estar associado a mais de 3 unidades de saúde.")





