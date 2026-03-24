from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    CadastroView,
    CampeonatoView,
    UsuarioLoginView,
    UsuarioCadastroView,
    VotarPilotoView,
    GridResultadoView,
    UsuarioGerenciamentoView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("cadastro/", CadastroView.as_view(), name="cadastro-usuario"),
    path('pilotos/', CampeonatoView.as_view(), name='pagina-campeonato'),
    path('grid-resultado/', GridResultadoView.as_view(), name='grid-resultado'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('api/login/', UsuarioLoginView.as_view(), name='api-login'),
    path('api/cadastro/', UsuarioCadastroView.as_view(), name='api-cadastro'),
    path("api/votar/", VotarPilotoView.as_view(), name="votar-piloto"),
    path('api/usuarios/', UsuarioGerenciamentoView.as_view(), name='api-gerenciamento-usuario')
]
