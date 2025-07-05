from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    PERFIL_CHOICES = [
        ('gestor', 'Gestor'),
        ('profissional', 'Profissional'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='profissional')
    unidade_saude = models.CharField(max_length=100, blank=True, null=True) # Optional for gestor
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"nome=({self.nome_completo}), perfil=({self.perfil})"
    
# Signal to create/update user profile when User is created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



