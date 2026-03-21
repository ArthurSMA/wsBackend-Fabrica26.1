from django.urls import path
from .views import (
    ListarPilotos, 
    ProximasCorridasView, 
    ListarUsuariosView, 
    UsuarioCadastroView, 
    UsuarioLoginView
)

urlpatterns = [
    path('usuarios/', ListarUsuariosView.as_view(), name='listar-usuarios'),
    path('login/', UsuarioLoginView.as_view(), name='login-usuario'),
    path('cadastro-usuario/', UsuarioCadastroView.as_view(), name='cadastro-usuario'),
    path('proximas-corridas/', ProximasCorridasView.as_view(), name='proximas-corridas'),
    path('pilotos/', ListarPilotos.as_view(), name='listar-pilotos'),
]
