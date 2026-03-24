from django.db import models
from django.contrib.auth.models import User

class Piloto(models.Model):
    nome = models.CharField(max_length=255)
    equipe = models.CharField(max_length=255)
    numero_carro = models.IntegerField(unique=True)

    def __str__(self):
        return self.nome

class EscolhaPiloto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='minhas_escolhas')
    piloto = models.ForeignKey(Piloto, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'piloto')

class ContaFinanceira(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='conta')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
