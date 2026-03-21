from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=120)

    def __str__(self):
        return self.nome

class Aposta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.IntegerField()
    piloto_id = models.IntegerField()
    valor_aposta = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aposta de {self.usuario.username}"

class ContaFinanceira(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)