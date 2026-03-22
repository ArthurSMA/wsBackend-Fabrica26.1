from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied

from .services import OpenF1Service
from .models import Piloto, EscolhaPiloto, ContaFinanceira
from .serializers import UsuarioSerializer, PilotoSerializer

#1. CLASSES BASE
class PublicAPIView(APIView):
    permission_classes = [AllowAny]

class PrivateAPIView(APIView):
    permission_classes = [IsAuthenticated]

#2. TELAS WEB
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

class CadastroView(View):
    def get(self, request):
        return render(request, 'auth/cadastro.html')

class PilotosDataAPIView(PrivateAPIView):
    def get(self, request):
        dados = OpenF1Service.listar_campeonato_detalhado()

        return Response(dados, status=status.HTTP_200_OK)

class CampeonatoView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        dados = OpenF1Service.listar_campeonato_detalhado()
        return render(request, 'campeonato.html', {'pilotos': dados})

#3. Lógica de voto
class VotarPilotoView(PrivateAPIView):
    def post(self, request):
        piloto_id = request.data.get('piloto_id')
        piloto = get_object_or_404(Piloto, id=piloto_id)

        voto, created = EscolhaPiloto.objects.get_or_create(
            usuario=request.user,
            piloto=piloto
        )

        if self._is_html(request):
            return redirect('pagina-campeonato')
        
        return Response({"status": "voto registrado"}, status=status.HTTP_201_CREATED)
    
    def _is_html(self, request):
        return 'text/html' in request.META.get('HTTP_ACCEPT', '')

class GridResultadoView(PrivateAPIView):
    login_url = '/login/'

    def get(self, request):
        piloto_base = OpenF1Service.listar_pilotos_atuais()
        resultado = OpenF1Service.grid_resultado_corrida()

        grid_processado = []
        for res in resultado:
            detalhe  = next((p for p in piloto_base if p['driver_number'] == res['driver_number']), {})
            grid_processado.append({**res, **detalhe})

        return render(request, 'grid_resultado.html', {'grid': grid_processado})

class UsuarioCadastroView(PublicAPIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if self._is_html(request):
                return redirect('login')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if self._is_html(request):
            return render(request, 'auth/cadastro.html', {'erros': serializer.errors})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ESTA FUNÇÃO PRECISA ESTAR AQUI DENTRO (IDENTADA)
    def _is_html(self, request):
        return 'text/html' in request.META.get('HTTP_ACCEPT', '')

class UsuarioLoginView(PublicAPIView):
    def post(self, request):
        email = request.data.get('email', '').strip()
        senha = request.data.get('password') or request.data.get('senha')
        senha = senha.strip() if senha else ''

        # 1. Tenta achar o usuário pelo e-mail
        user_obj = User.objects.filter(email=email).first()
        username = user_obj.username if user_obj else None

        # 2. O authenticate do Django exige o username (que pegamos acima)
        usuario = authenticate(request, username=username, password=senha)

        if usuario:
            login(request, usuario)
            if self._is_html(request):
                return redirect('pagina-campeonato')
            
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token) # Corrigido: access
            }, status=status.HTTP_200_OK)

        # 3. SE CHEGOU AQUI, O LOGIN FALHOU
        if self._is_html(request):
            return render(request, 'auth/login.html', {'error': 'Invalido'})
        
        # Resposta em JSON para o Postman não receber HTML de erro
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    def _is_html(self, request):
        return 'text/html' in request.META.get('HTTP_ACCEPT', '')
    