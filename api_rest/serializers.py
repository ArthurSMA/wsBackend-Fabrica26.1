from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Piloto, ContaFinanceira

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    saldo = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'saldo']

    def get_saldo(self, obj):
        conta = getattr(obj, 'conta', None)
        return conta.saldo if conta else 0.00
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        ContaFinanceira.objects.create(usuario=user, saldo=100.00)
        return user

class PilotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piloto
        fields = '__all__'
