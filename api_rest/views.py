from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import OpenF1Service
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioCadastroView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarUsuariosView(APIView):
    def get(self, request):
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProximasCorridasView(APIView):
    def get(self, request):
        limit_param = request.query_params.get('limit', 4)
 
        try:
            limit = int(limit_param)
        except ValueError:
            limit = 4

        dados = OpenF1Service.get_proximas_corridas(limit=limit)

        return Response(dados, status=status.HTTP_200_OK)
