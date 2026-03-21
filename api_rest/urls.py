from django.urls import path
from .views import ProximasCorridasView, ListarUsuariosView, UsuarioCadastroView

urlpatterns = [
    path('usuarios/', ListarUsuariosView.as_view(), name='listar-usuarios'),
    path('cadastro-usuario/', UsuarioCadastroView.as_view(), name='cadastro-usuario'),
    path('proximas-corridas/', ProximasCorridasView.as_view(), name='proximas-corridas'),
]
