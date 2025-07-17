from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

############################## MODELO DE EQUIPE ##############################
class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    gestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipes_gerenciadas')
    profissionais = models.ManyToManyField(User, related_name='equipes_participantes', blank=True)

    def __str__(self):
        return self.nome 
    
    # Regras de Negócio
    @classmethod
    def criar_equipe(cls, nome, gestor):
        if gestor.profile.perfil != 'gestor': # Validação perfil gestor
            raise ValidationError("Apenas usuários com perfil 'gestor' podem criar equipes.")
        if cls.objects.filter(nome=nome, gestor=gestor).exists():
            raise ValidationError("Você já possui uma equipe com esse nome.") # Val nome dupl. 
        return cls.objects.create(nome=nome, gestor=gestor)

    def adicionar_profissional(self, user):
        if user.profile.perfil != 'profissional':
            raise ValidationError("Apenas profissionais de saúde podem ser adicionados à equipe.")
        self.profissionais.add(user)

    def remover_profissional(self, user):
        if user in self.profissionais.all():
            self.profissionais.remove(user)
        else:
            raise ValidationError("Usuário não faz parte da equipe.")


