from django.urls import path
from .views import (
    LoginView,
    CadastroView,
    CampeonatoView,
    UsuarioLoginView,
    UsuarioCadastroView,
    VotarPilotoView,
    GridResultadoView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("cadastro/", CadastroView.as_view(), name="cadastro-usuario"),
    path('pilotos/', CampeonatoView.as_view(), name='pagina-campeonato'),
    path('grid-resultado/', GridResultadoView.as_view(), name='grid-resultado'),

    path('api/login/', UsuarioLoginView.as_view(), name='api-login'),
    path('api/cadastro/', UsuarioCadastroView.as_view(), name='api-cadastro'),
    path("api/votar/", VotarPilotoView.as_view(), name="votar-piloto")
]

