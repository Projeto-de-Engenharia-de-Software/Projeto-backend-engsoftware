from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Equipe(models.Model):
    """
    Modelo que representa uma equipe de profissionais de saúde.
    Cada equipe tem um gestor (um usuário) e uma lista de profissionais (outros usuários).
    """
    nome = models.CharField(max_length=100)
    gestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipes_gerenciadas')
    profissionais = models.ManyToManyField(User, related_name='equipes_participantes')

    def __str__(self):
        return self.nome

    @classmethod
    # Adiciona uma nova equipe, onde somente um gestor pode criar equipes.
    def criar_equipe(cls, nome, gestor):
        if gestor.profile.perfil != 'gestor':
            raise ValidationError("Apenas usuários com perfil 'gestor' podem criar equipes.")

        if cls.objects.filter(nome=nome, gestor=gestor).exists():
            raise ValidationError("Você já possui uma equipe com esse nome.")

        return cls.objects.create(nome=nome, gestor=gestor)
    
    # Remover uma equipe, onde somente o gestor da equipe pode removê-la.
    @classmethod
    def remover_equipe(cls,nome, gestor):
        if gestor.profile.perfil != 'gestor':
            raise ValidationError("Apenas usuários com perfil 'gestor' podem remover equipes.")
        
        if not cls.objects.filter(nome=nome, gestor=gestor).exists():
            raise ValidationError("Equipe não encontrada ou você não é o gestor desta equipe.")
        
        equipe = cls.objects.get(nome=nome, gestor=gestor)
        equipe.delete()


    # CRUD de profissionais na equipe, onde somente o gestor pode adicionar ou remover profissionais.
    def adicionar_profissional(self, user):
        if user.profile.perfil != 'profissional':
            raise ValidationError("Apenas profissionais de saúde podem ser adicionados.")
        
        if user.username in self.profissionais.values_list('username', flat=True):
            raise ValidationError("Este profissional já está na equipe.")
        self.profissionais.add(user)

    def remover_profissional(self, user):
        if user.profile.perfil != 'profissional':
            raise ValidationError("Apenas profissionais de saúde podem ser removidos.")
        
        if user not in self.profissionais.all():
            raise ValidationError("Este profissional não está na equipe.")
        self.profissionais.remove(user)
