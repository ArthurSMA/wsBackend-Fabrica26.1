from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class PilotosSerializer(serializers.Serializer):
    driver_number = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255)
    team_name = serializers.CharField(max_length=255)
