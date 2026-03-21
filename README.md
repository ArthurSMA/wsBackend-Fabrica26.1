# wsBackend-Fabrica26.1

### Rodar projeto

Em terminal bash

```bash
#1. Criar o ambiente virtual
py -m venv venv 
```
```bash
#2. Ativar o ambiente virtual
source .\venv\Scripts\activate
```
```bash
#3. Instalar dependências
pip install -r requirements.txt

#4. Rodar as migrações e o servidor
python manage.py migrate
python manage.py runserver
```

#### ENDPOINTS
Lista de usuários
- api/usuarios/
[Lista de Usuários]('http://127.0.0.1:8000/api/usuarios/')

Criar usuário
[Criar usuário]('http://127.0.0.1:8000/api/cadastro-usuario/')

Lista próximas 4 corridas
- /api/proximas-corridas/
[Proximas Corridas]('http://127.0.0.1:8000/api/proximas-corridas/?format=api')

Listar próximas 10 corridas
- /api/proximas-corridas/?limit=10
[Próximas 10 Corridas]('http://127.0.0.1:8000/api/proximas-corridas/?limit=10')
