# wsBackend-Fabrica26.1

## Como Rodar o Projeto
Siga os passos a baixo:
(Bash)
```bash
#1. Crie um ambiente virtual
python -m venv venv

#2. Ativar o modo ambiente virtual
source venv/Scripts/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar as migrações e o servidor
python manage.py migrate
python manage.py runserver
```

## ENDPOINTs da Aplicação

| Recurso              | Rota              | Nome da URL          |
|----------------------|-------------------|----------------------|
| Login                | /login/           | login                |
| Cadastro             | /cadastro/        | cadastro-usuario     |
| Grid de Resultados   | /grid-resultado/  | pagina-grid-resultado|
| Página de Pilotos    | /pilotos/         | pagina-campeonato    |

#### ENDPOINTS LINK
Login
- /login/
[Login](http://127.0.0.1:8000/login/)

Cadastro
- /cadastro/
[Cadastro](http://127.0.0.1:8000/cadastro/)

Lista de usuários
- api/usuarios/
[Lista de Usuários]('/api/usuarios/')

Criar usuário
[Criar usuário]('http://127.0.0.1:8000/api/cadastro-usuario/')

Lista próximas 4 corridas
- /api/proximas-corridas/
[Proximas Corridas]('http://127.0.0.1:8000/api/proximas-corridas/?format=api')

Listar próximas 10 corridas
- /api/proximas-corridas/?limit=10
[Próximas 10 Corridas]('http://127.0.0.1:8000/api/proximas-corridas/?limit=10')
