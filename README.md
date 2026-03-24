# wsBackend-Fabrica26.1

## 🏎️ F1 World Championship - Backend Workshop
Este projeto é um sistema de acompanhamento do Campeonato Mundial de Fórmula 1 (Temporada 2026), integrando dados em tempo real da API OpenF1. O sistema permite que usuários se cadastrem, acompanhem a classificação, verifiquem resultados de corridas e votem em seus pilotos favoritos (mediante saldo virtual).

## 🚀 Tecnologias utilizadas

- Python 3.12
- Django 6.0 & Django REST Framework
- Pop!_OS Linux (Ambiente de Desenvolvimento)
- SQLite / SQL Server (Persistência de dados)
- OpenF1 API (Dados de telemetria e classificação)

---

## 🛠️ Como rodar
```bash
# 1. Clone o repositório e acesse a pasta
git clone <url-do-repositorio>
cd wsBackend-Fabrica26.1

# 2. Crie e ative o ambiente virtual
python -m venv venv
# No Linux (Pop!_OS):
source venv/bin/activate
# No Windows (caso precise):
# venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar o Banco de Dados
python manage.py migrate

# 5. Iniciar o servidor
python manage.py runserver
```
O servidor rodará em: http://127.0.0.1:8000/

---

## 🐳 Como rodar com Docker

Para rodar a aplicação em um ambiente isolado utilizando a imagem **Python 3.13-slim** configurada no projeto, siga os passos abaixo:

### 1. Construir a Imagem (Build)
Compila e instala as dependências dentro da imagem:
```bash
docker build -t f1-backend .
```
### 2. Iniciar o Container

```bash
docker run -d -p 8000:8000 --name f1-app f1-backend
```
### 3.Configurar o Banco de Dados (Migrations)
```bash
# Criar as tabelas (Usuários, Votos, Saldo)
docker exec -it f1-app python manage.py migrate

# Criar um Superusuário (Opcional - para acessar o /admin)
docker exec -it f1-app python manage.py createsuperuser
```
---
## Comandos de manutenção
|Ação                | Comando               |
| ---                | ---                   |
| Ver log            | docker logs -f f1-app |
| Parar servidor     | docker stop f1-app    |
| Reiniciar Servidor | docker start f1-app   |
| Remover Container  | docker rm -f f1-app   |
| Verificar Status   | docker ps             |
--- 

## 🛣️ Endpoints

### 🖥️ Interface Web (Navegador)
| Recurso | Rota | Nome da URL | Descrição |
| :--- | :--- | :--- | :--- |
| **Login** | `/login/` | `login` | Tela de acesso à conta. |
| **Cadastro** | `/cadastro/` | `cadastro-usuario` | Tela de criação de novos usuários. |
| **Dashboard** | `/pilotos/` | `pagina-campeonato` | Classificação em tempo real + Sistema de Votos. |
| **Resultados** | `/grid-resultado/` | `grid-resultado` | Grid final da última sessão de corrida. |
| **Sair** | `/logout/` | `logout` | Encerra a sessão (Logout). |

### ⚙️ API REST (Postman / Frontend)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/api/login/` | Autenticação (Retorna JWT/Session). |
| `POST` | `/api/cadastro/` | Criação de novo usuário via API. |
| `POST` | `/api/votar/` | Registra voto em piloto (Custo: R$ 10,00). |
| `GET` | `/api/usuarios/` | Listagem e gerenciamento de usuários (Privado). |

---

## 💡 Funcionalidades Implementadas
- [x] **Integração OpenF1:** Consumo de telemetria e pontuações em tempo real.
- [x] **Sistema de Favoritos:** Lógica para destacar e persistir o piloto escolhido no banco de dados.
- [x] **Regra de Negócio (Financeiro):** Cada voto debita automaticamente R$ 10,00 do saldo do usuário.
- [x] **Segurança CSRF:** Implementação de `csrf_exempt` para compatibilidade com Postman e `{% csrf_token %}` para segurança no navegador.
- [x] **Tratamento de Imagens:** Sistema de fallback para exibir a logo da F1 caso a foto do piloto falhe.

---

## 👨‍💻 Desenvolvedor
**Arthur Suassuna Maia Alves** *Ambiente: Pop!_OS Linux | Backend Developer*
