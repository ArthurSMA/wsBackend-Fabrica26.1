from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from .services import OpenF1Service
from .models import Usuario
from .serializers import UsuarioSerializer, PilotosSerializer

class PublicAPIView(APIView):
    permission_classes = [AllowAny]

class PrivateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(detail='Sem permissão de acesso', code='permission_denied')

class UsuarioCadastroView(PublicAPIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioLoginView(PublicAPIView):
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')
        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            #Gera o Token que da permissao de gerar novo JWT
            refresh = RefreshToken.for_user(usuario)
            serializer = UsuarioSerializer(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usuario':{
                    'nome': serializer.data['nome'],
                    'email': serializer.data['email']
                }
            }, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class ListarUsuariosView(PrivateAPIView):
    def get(self, request):
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListarPilotos(PrivateAPIView):
    def get(self, request):
        pilotos = OpenF1Service.listar_pilotos()
        serializer = PilotosSerializer(pilotos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProximasCorridasView(PrivateAPIView):
    def get(self, request):
        limit_param = request.query_params.get('limit', 4)
 
        try:
            limit = int(limit_param)
        except ValueError:
            limit = 4

        dados = OpenF1Service.get_proximas_corridas(limit=limit)

        return Response(dados, status=status.HTTP_200_OK)
