from django.urls import path
from .views import (
    ListarPilotos, 
    ProximasCorridasView, 
    ListarUsuariosView, 
    UsuarioCadastroView, 
    UsuarioLoginView,
    LoginView,
    CadastroView,
    CampeonatoView,
    GridResultadoView
)

urlpatterns = [
    path('api/usuarios/', ListarUsuariosView.as_view(), name='listar-usuarios'),
    path('api/login/', UsuarioLoginView.as_view(), name='login-usuario'),
    path('api/proximas-corridas/', ProximasCorridasView.as_view(), name='proximas-corridas'),
    path('api/pilotos-data/', ListarPilotos.as_view(), name='listar-pilotos'),
    path('api/cadastro-data/', UsuarioCadastroView.as_view(), name='api-cadastro'),

    path("login/", LoginView.as_view(), name="login"),
    path("cadastro/", CadastroView.as_view(), name="cadastro-usuario"),
    path('grid-resultado/', GridResultadoView.as_view(), name='pagina-grid-resultado'),
    path('pilotos/', CampeonatoView.as_view(), name='pagina-campeonato'),
]
