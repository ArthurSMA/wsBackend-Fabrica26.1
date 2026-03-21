from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from .services import OpenF1Service
from .models import Usuario
from .serializers import UsuarioSerializer, PilotosSerializer

# 1. CLASSES BASE
class PublicAPIView(APIView):
    permission_classes = [AllowAny]

class PrivateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(detail='Sem permissão de acesso', code='permission_denied')

# 2. TELAS DO NAVEGADOR
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

class CadastroView(View):
    def get(self, request):
        return render(request, 'auth/cadastro.html')

class CampeonatoView(View):
    def get(self, request):
        if 'usuario_id' not in request.session:
            return redirect('login')

        dados = OpenF1Service.listar_campeonato_detalhado()
        return render(request, 'campeonato.html', {'pilotos': dados})

class GridResultadoView(View):
    login_url = '/login/'

    def get(self, request):
        piloto_base = OpenF1Service.listar_pilotos_atuais()
        resultado = OpenF1Service.grid_resultado_corrida()

        grid_processado = []
        for res in resultado:
            detalhe  = next((p for p in piloto_base if p['driver_number'] == res['driver_number']), {})
            grid_processado.append({**res, **detalhe})

        return render(request, 'grid_resultado.html', {'grid': grid_processado})

# 3. ENDPOINTS API

class UsuarioCadastroView(PublicAPIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            if self._is_html(request):
                return redirect('pagina-campeonato')
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # --- TRATAMENTO DE ERRO WEB ---
        if self._is_html(request):
            return render(request, 'auth/cadastro.html', {
                'errors': serializer.errors,
                'dados_preenchidos': request.data # Para não apagar antigos registro
            })

        # Para retornar JSON na API
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _is_html(self, request):
        return (getattr(request, 'accepted_renderer', None) and 
                request.accepted_renderer.format == 'html') or \
               'text/html' in request.META.get('HTTP_ACCEPT', '')

class UsuarioLoginView(PublicAPIView):
    def get(self, request):
        if self._is_html(request):
            return render(request, 'auth/login.html')
        return Response({'detail': 'Método GET não permitido'}, status=405)

    def post(self, request):
        # Usamos .strip() para garantir que não haja espaços acidentais
        email = request.data.get('email', '').strip()
        senha = request.data.get('senha', '').strip()
        
        # Log para você ver no terminal exatamente o que está chegando
        print(f"Tentativa de login: {email} | Senha: {senha}")

        # Buscamos o usuário
        usuario = Usuario.objects.filter(email=email, senha=senha).first()

        if usuario:
            if self._is_html(request):
                request.session['usuario_id'] = usuario.id

                return redirect('pagina-campeonato')

            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usuario': {'nome': usuario.nome, 'email': usuario.email}
            }, status=status.HTTP_200_OK)
        
        # Se chegou aqui, as credenciais realmente não bateram
        if self._is_html(request):
            return render(request, 'auth/login.html', {'error': 'E-mail ou senha incorretos'})
        
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    def _is_html(self, request):
        return (getattr(request, 'accepted_renderer', None) and 
                request.accepted_renderer.format == 'html') or \
               'text/html' in request.META.get('HTTP_ACCEPT', '')

class ListarUsuariosView(PublicAPIView):
    def get(self, request):
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListarPilotos(PublicAPIView):
    def get(self, request):
        pilotos = OpenF1Service.listar_pilotos_atuais()
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

