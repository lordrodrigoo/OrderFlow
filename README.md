# OrderFlow

🇺🇸 English version first · 🇧🇷 Versão em Português logo abaixo

---

## 🇺🇸 English

REST API for order and user management, built with FastAPI and Clean Architecture. JWT authentication with role-based access control (OWNER/ADMIN/USER), full CI/CD pipeline with automatic rollback, 100% test coverage, and containerized deployment with multi-stage Docker.

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00?logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E)
![Pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=codecov&logoColor=white)

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Option A — Makefile (recommended)](#option-a--makefile-recommended)
  - [Option B — Manual commands](#option-b--manual-commands)
- [Running with Docker](#-running-with-docker)
  - [Docker via Makefile](#docker-via-makefile)
  - [Docker manual commands](#docker-manual-commands)
- [Migrations](#-migrations)
- [Tests & Coverage](#-tests--coverage)
- [Useful Debug Commands](#-useful-debug-commands)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [CI/CD & Deploy](#-cicd--deploy)
- [License](#-license)

---

## 🛠 Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0+
- Alembic
- Pytest + Coverage.py
- Docker & Docker Compose
- PostgreSQL 15+
- Pydantic v2
- Uvicorn (ASGI)
- pwdlib (Argon2id password hashing)
- python-jose (JWT)

---

## 📁 Project Structure

```
orderflow/
├── .github/workflows/     — CI/CD pipelines (GitHub Actions)
├── src/
│   ├── api/
│   │   ├── controllers/   — HTTP endpoints (FastAPI entrypoints)
│   │   └── dependencies.py
│   ├── config/            — Settings, security, OAuth2, rate limiter, logger
│   ├── domain/
│   │   ├── models/        — Domain entities
│   │   └── repositories/  — Repository interfaces (contracts)
│   ├── dto/
│   │   ├── request/       — Input schemas
│   │   └── response/      — Output schemas
│   ├── exceptions/        — Custom exceptions
│   ├── infra/
│   │   └── db/
│   │       ├── entities/      — ORM models (SQLAlchemy)
│   │       ├── repositories/  — Concrete implementations
│   │       └── settings/      — Database configuration
│   ├── middlewares/       — Correlation ID and structured logging
│   ├── usecases/          — Pure business logic
│   └── tests/             — Unit, integration and functional tests
├── alembic/               — Database migrations
├── docs/                  — Documentation and guides
├── Dockerfile             — Multi-stage build
├── docker-compose.yml     — Local environment
├── Makefile               — Ready-to-use commands
└── .env.example           — Required environment variables
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (if running with containers)
- PostgreSQL 15+ (if running locally without Docker)
- `make` (optional, for Makefile commands)
- `openssl` (for generating SECRET_KEY)

---

### Option A — Makefile (recommended)

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/orderflow.git
cd orderflow
```

#### 2. Copy the environment file

```bash
make init
```

#### 3. Create the virtualenv and install dependencies

```bash
make setup
```

#### 4. Generate a secure SECRET_KEY

```bash
make secret-key
```

Copy the output and paste it into your `.env` file:

```env
SECRET_KEY=your_generated_key_here
```

#### 5. Review your `.env` file

```bash
# Edit with your preferred editor
nano .env
# or
code .env
```

#### 6. Apply migrations

```bash
make migrate
```

#### 7. Start the application

```bash
make run
```

Access at: http://localhost:8000/docs

---

### Option B — Manual commands

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/orderflow.git
cd orderflow
```

#### 2. Copy and configure environment variables

```bash
cp .env.example .env
```

#### 3. Generate a secure SECRET_KEY

```bash
# Option 1 - openssl (recommended)
openssl rand -hex 64

# Option 2 - Python
python3 -c "import secrets; print(secrets.token_hex(64))"
```

Copy the output and paste it as the `SECRET_KEY` value in your `.env`.

#### 4. Create and activate a virtual environment

```bash
# Create virtualenv
python3 -m venv venv

# Activate — Linux/macOS
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

#### 5. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Apply migrations

```bash
alembic upgrade head
```

#### 7. Start the application

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Access at: http://localhost:8000/docs

---

## 🐳 Running with Docker

> **Note:** Make sure Docker and Docker Compose are installed and running before proceeding.

### Docker via Makefile

```bash
# Start all containers (app + database)
make up

# Start only the application container
make up-app

# Start only the database container
make up-database

# Stop all containers
make down

# Stop all containers and remove volumes (wipes database data)
make down-v

# Show status of all running containers
make ps

# Restart the app container
make restart

# Restart the database container
make restart-database
```

### Docker manual commands

```bash
# Build and start all containers
docker compose up -d --build

# Start without rebuilding
docker compose up -d

# Stop all containers
docker compose down

# Stop and remove volumes
docker compose down -v

# Show running containers
docker compose ps

# Restart only the app
docker compose restart app

# Restart only the database
docker compose restart database
```

#### Apply migrations inside Docker

```bash
# Via Makefile
make migrate-docker

# Manual
docker compose exec app alembic upgrade head
```

---

## 🔄 Migrations

```bash
# ── Makefile ──────────────────────────────────────────
# Apply all pending migrations
make migrate

# Revert last migration
make migrate-down

# Create a new migration (auto-generated from models)
make revision msg="your migration description"

# Apply migrations inside a running container
make migrate-docker

# ── Manual ────────────────────────────────────────────
# Apply all pending migrations
alembic upgrade head

# Revert last migration
alembic downgrade -1

# Create a new migration
alembic revision --autogenerate -m "your migration description"

# Check current migration state
alembic current

# Show full migration history
alembic history
```

---

## 🧪 Tests & Coverage

```bash
# ── Makefile ──────────────────────────────────────────
make test-unit           # Run unit tests only
make test-integration    # Run integration tests only
make test-functional     # Run functional tests only
make test-all            # Run all tests with full coverage report

# ── Manual ────────────────────────────────────────────
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest src/tests/unit_tests/test_example.py -v

# Run a specific test by name
pytest -k "test_login" -v

# Run with coverage report in terminal
pytest --cov=src --cov-report=term-missing

# Run with HTML coverage report (opens at htmlcov/index.html)
pytest --cov=src --cov-report=html
```

Current coverage: **100%** — unit, integration and functional.

---

## 🔍 Useful Debug Commands

These commands are helpful for inspecting logs, containers, and the database during development.

### Logs

```bash
# ── Makefile ──────────────────────────────────────────
make logs              # Stream app logs (Ctrl+C to exit)
make logs-database     # Stream database logs

# ── Manual ────────────────────────────────────────────
# Stream app logs in real time
docker compose logs -f app

# Stream database logs
docker compose logs -f database

# Show last 100 lines of app logs
docker compose logs --tail=100 app

# Show logs with timestamps
docker compose logs -f -t app

# Show logs for all services at once
docker compose logs -f
```

### Container shell access

```bash
# ── Makefile ──────────────────────────────────────────
make shell             # Open shell inside app container
make shell-database    # Open psql shell inside database container

# ── Manual ────────────────────────────────────────────
# Open a shell in the app container
docker compose exec app sh

# Open psql in the database container
docker compose exec database psql -U $DB_USER -d $DB_NAME

# Run a one-off command inside the app container
docker compose exec app python -c "print('hello')"
```

### Container & image management

```bash
# ── Makefile ──────────────────────────────────────────
make prune             # Remove stopped containers and unused images
make prune-all         # ⚠️  Remove everything (containers, volumes, images)
make remove-app        # Remove app container and its image
make remove-database   # ⚠️  Remove database container and its volume

# ── Manual ────────────────────────────────────────────
# Show all containers (including stopped)
docker ps -a

# Show all images
docker images

# Remove unused images
docker image prune -f

# Remove all stopped containers
docker container prune -f

# Full system cleanup (containers, images, networks — not volumes)
docker system prune -f

# Full cleanup including volumes ⚠️ (wipes all data)
docker system prune -af --volumes

# Inspect the app container
docker inspect orderflow_app

# Check resource usage
docker stats
```

### Quality

```bash
# ── Makefile ──────────────────────────────────────────
make lint              # Run pylint on the source code

# ── Manual ────────────────────────────────────────────
venv/bin/pylint src/
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in all required values:

```env
# ── Environment ───────────────────────────────────────
ENV=development               # development | production

# ── Database ──────────────────────────────────────────
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderflow_db

ALEMBIC_DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db

# ── JWT ───────────────────────────────────────────────
SECRET_KEY=           # Generate with: openssl rand -hex 64
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ── Trusted Hosts ─────────────────────────────────────
ALLOWED_HOSTS=localhost,127.0.0.1

# ── System Owner ──────────────────────────────────────
OWNER_USERNAME=owner
OWNER_PASSWORD=ChangeMe@2026
OWNER_EMAIL=owner@orderflow.com
OWNER_FIRST_NAME=System
OWNER_LAST_NAME=Owner

# ── API ───────────────────────────────────────────────
API_TITLE=OrderFlow API
API_VERSION=1.0.0
API_V1_PREFIX=/api/v1

# ── Logging ───────────────────────────────────────────
LOG_LEVEL=DEBUG        # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FORMAT=text        # text (development) | json (production)
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 📬 API Documentation

With the application running, access the interactive docs at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Full documentation with role-based examples at [docs/POSTMAN_GUIDE.md](docs/POSTMAN_GUIDE.md)

### Authentication roles

| Role    | Description                          |
|---------|--------------------------------------|
| `OWNER` | Full access to all resources         |
| `ADMIN` | Manage users and orders              |
| `USER`  | Access to own orders only            |

---

## 🚀 CI/CD & Deploy

Deploy is automated via GitHub Actions. On every push to the `main` branch:

1. Lint + tests run in parallel
2. Docker image is built and pushed to the registry
3. Deploy via SSH with automatic health check
4. On failure, automatic rollback to the previous version

See the full guide at [docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md)

---

## 📄 License

[MIT](LICENSE)

### Contact

rodrigog3wconcept@gmail.com

---
---

## 🇧🇷 Português

API REST para gestão de pedidos e usuários, construída com FastAPI e Clean Architecture. Autenticação JWT com sistema de roles (OWNER/ADMIN/USER), CI/CD completo com rollback automático, cobertura de testes de 100% e deploy containerizado com Docker multi-stage.

---

## 📋 Índice

- [Tecnologias](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Começar](#-como-começar)
  - [Opção A — Makefile (recomendado)](#opção-a--makefile-recomendado)
  - [Opção B — Comandos manuais](#opção-b--comandos-manuais)
- [Rodando com Docker](#-rodando-com-docker)
  - [Docker via Makefile](#docker-via-makefile-1)
  - [Docker comandos manuais](#docker-comandos-manuais)
- [Migrações](#-migrações)
- [Testes e Cobertura](#-testes-e-cobertura)
- [Comandos Úteis para Debug](#-comandos-úteis-para-debug)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Documentação da API](#-documentação-da-api)
- [CI/CD e Deploy](#-cicd-e-deploy)
- [Licença](#-licença)

---

## 🛠 Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0+
- Alembic
- Pytest + Coverage.py
- Docker & Docker Compose
- PostgreSQL 15+
- Pydantic v2
- Uvicorn (ASGI)
- pwdlib (hash de senhas com Argon2id)
- python-jose (JWT)

---

## 📁 Estrutura do Projeto

```
orderflow/
├── .github/workflows/     — Pipelines de CI/CD (GitHub Actions)
├── src/
│   ├── api/
│   │   ├── controllers/   — Endpoints HTTP (entrypoints FastAPI)
│   │   └── dependencies.py
│   ├── config/            — Settings, segurança, OAuth2, rate limiter, logger
│   ├── domain/
│   │   ├── models/        — Entidades de domínio
│   │   └── repositories/  — Interfaces dos repositórios (contratos)
│   ├── dto/
│   │   ├── request/       — Schemas de entrada
│   │   └── response/      — Schemas de saída
│   ├── exceptions/        — Exceções customizadas
│   ├── infra/
│   │   └── db/
│   │       ├── entities/      — Modelos ORM (SQLAlchemy)
│   │       ├── repositories/  — Implementações concretas
│   │       └── settings/      — Configuração do banco
│   ├── middlewares/       — Correlation ID e Logging estruturado
│   ├── usecases/          — Lógica de negócio pura
│   └── tests/             — Unitários, integração e funcionais
├── alembic/               — Migrações de banco de dados
├── docs/                  — Documentação e guias
├── Dockerfile             — Build multi-stage
├── docker-compose.yml     — Ambiente local
├── Makefile               — Comandos prontos
└── .env.example           — Variáveis de ambiente necessárias
```

---

## 🚀 Como Começar

### Pré-requisitos

- Python 3.11+
- Docker & Docker Compose (para rodar com containers)
- PostgreSQL 15+ (para rodar localmente sem Docker)
- `make` (opcional, para comandos via Makefile)
- `openssl` (para gerar a SECRET_KEY)

---

### Opção A — Makefile (recomendado)

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/orderflow.git
cd orderflow
```

#### 2. Copie o arquivo de ambiente

```bash
make init
```

#### 3. Crie o virtualenv e instale as dependências

```bash
make setup
```

#### 4. Gere uma SECRET_KEY segura

```bash
make secret-key
```

Copie o valor gerado e cole no seu arquivo `.env`:

```env
SECRET_KEY=seu_valor_gerado_aqui
```

#### 5. Revise seu arquivo `.env`

```bash
# Edite com seu editor preferido
nano .env
# ou
code .env
```

#### 6. Aplique as migrações

```bash
make migrate
```

#### 7. Inicie a aplicação

```bash
make run
```

Acesse em: http://localhost:8000/docs

---

### Opção B — Comandos manuais

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/orderflow.git
cd orderflow
```

#### 2. Copie e configure as variáveis de ambiente

```bash
cp .env.example .env
```

#### 3. Gere uma SECRET_KEY segura

```bash
# Opção 1 - openssl (recomendado)
openssl rand -hex 64

# Opção 2 - Python
python3 -c "import secrets; print(secrets.token_hex(64))"
```

Copie o valor gerado e cole como `SECRET_KEY` no seu `.env`.

#### 4. Crie e ative o ambiente virtual

```bash
# Criar virtualenv
python3 -m venv venv

# Ativar — Linux/macOS
source venv/bin/activate

# Ativar — Windows
venv\Scripts\activate
```

#### 5. Instale as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Aplique as migrações

```bash
alembic upgrade head
```

#### 7. Inicie a aplicação

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse em: http://localhost:8000/docs

---

## 🐳 Rodando com Docker

> **Atenção:** Certifique-se de que o Docker e o Docker Compose estão instalados e em execução.

### Docker via Makefile

```bash
# Iniciar todos os containers (app + banco de dados)
make up

# Iniciar apenas o container da aplicação
make up-app

# Iniciar apenas o container do banco de dados
make up-database

# Parar todos os containers
make down

# Parar todos e remover volumes (apaga dados do banco)
make down-v

# Ver status dos containers
make ps

# Reiniciar o container da aplicação
make restart

# Reiniciar o container do banco de dados
make restart-database
```

### Docker comandos manuais

```bash
# Construir e iniciar todos os containers
docker compose up -d --build

# Iniciar sem reconstruir
docker compose up -d

# Parar todos os containers
docker compose down

# Parar e remover volumes
docker compose down -v

# Ver containers em execução
docker compose ps

# Reiniciar apenas a aplicação
docker compose restart app

# Reiniciar apenas o banco de dados
docker compose restart database
```

#### Aplicar migrações dentro do Docker

```bash
# Via Makefile
make migrate-docker

# Manual
docker compose exec app alembic upgrade head
```

---

## 🔄 Migrações

```bash
# ── Makefile ──────────────────────────────────────────
# Aplicar todas as migrações pendentes
make migrate

# Reverter a última migração
make migrate-down

# Criar nova migração (gerada a partir dos models)
make revision msg="descrição da migração"

# Aplicar migrações dentro do container
make migrate-docker

# ── Manual ────────────────────────────────────────────
# Aplicar todas as migrações pendentes
alembic upgrade head

# Reverter a última migração
alembic downgrade -1

# Criar nova migração
alembic revision --autogenerate -m "descrição da migração"

# Ver estado atual das migrações
alembic current

# Ver histórico completo de migrações
alembic history
```

---

## 🧪 Testes e Cobertura

```bash
# ── Makefile ──────────────────────────────────────────
make test-unit           # Rodar apenas testes unitários
make test-integration    # Rodar apenas testes de integração
make test-functional     # Rodar apenas testes funcionais
make test-all            # Rodar todos com relatório de cobertura completo

# ── Manual ────────────────────────────────────────────
# Rodar todos os testes
pytest

# Rodar com saída detalhada
pytest -v

# Rodar um arquivo específico
pytest src/tests/unit_tests/test_exemplo.py -v

# Rodar um teste pelo nome
pytest -k "test_login" -v

# Rodar com relatório de cobertura no terminal
pytest --cov=src --cov-report=term-missing

# Rodar com relatório HTML (abre em htmlcov/index.html)
pytest --cov=src --cov-report=html
```

Cobertura atual: **100%** — unitários, integração e funcionais.

---

## 🔍 Comandos Úteis para Debug

Esses comandos são úteis para inspecionar logs, containers e o banco durante o desenvolvimento.

### Logs

```bash
# ── Makefile ──────────────────────────────────────────
make logs              # Acompanhar logs da aplicação em tempo real (Ctrl+C para sair)
make logs-database     # Acompanhar logs do banco de dados

# ── Manual ────────────────────────────────────────────
# Acompanhar logs da aplicação em tempo real
docker compose logs -f app

# Acompanhar logs do banco de dados
docker compose logs -f database

# Ver as últimas 100 linhas dos logs da aplicação
docker compose logs --tail=100 app

# Ver logs com timestamps
docker compose logs -f -t app

# Ver logs de todos os serviços ao mesmo tempo
docker compose logs -f
```

### Acesso ao shell dos containers

```bash
# ── Makefile ──────────────────────────────────────────
make shell             # Abrir shell dentro do container da aplicação
make shell-database    # Abrir shell psql dentro do container do banco

# ── Manual ────────────────────────────────────────────
# Abrir shell no container da aplicação
docker compose exec app sh

# Abrir psql no container do banco de dados
docker compose exec database psql -U $DB_USER -d $DB_NAME

# Executar um comando pontual dentro do container da aplicação
docker compose exec app python -c "print('hello')"
```

### Gerenciamento de containers e imagens

```bash
# ── Makefile ──────────────────────────────────────────
make prune             # Remover containers parados e imagens não utilizadas
make prune-all         # ⚠️  Remover tudo (containers, volumes, imagens)
make remove-app        # Remover container e imagem da aplicação
make remove-database   # ⚠️  Remover container e volume do banco de dados

# ── Manual ────────────────────────────────────────────
# Ver todos os containers (incluindo parados)
docker ps -a

# Ver todas as imagens
docker images

# Remover imagens não utilizadas
docker image prune -f

# Remover todos os containers parados
docker container prune -f

# Limpeza geral (containers, imagens, redes — sem volumes)
docker system prune -f

# Limpeza completa incluindo volumes ⚠️ (apaga todos os dados)
docker system prune -af --volumes

# Inspecionar o container da aplicação
docker inspect orderflow_app

# Ver uso de recursos dos containers
docker stats
```

### Qualidade de código

```bash
# ── Makefile ──────────────────────────────────────────
make lint              # Rodar pylint no código fonte

# ── Manual ────────────────────────────────────────────
venv/bin/pylint src/
```

---

## 🔐 Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha todos os valores necessários:

```env
# ── Environment ───────────────────────────────────────
ENV=development               # development | production

# ── Banco de Dados ────────────────────────────────────
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderflow_db

ALEMBIC_DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db

# ── JWT ───────────────────────────────────────────────
SECRET_KEY=           # Gere com: openssl rand -hex 64
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ── Trusted Hosts ─────────────────────────────────────
ALLOWED_HOSTS=localhost,127.0.0.1

# ── System Owner ──────────────────────────────────────
OWNER_USERNAME=owner
OWNER_PASSWORD=ChangeMe@2026
OWNER_EMAIL=owner@orderflow.com
OWNER_FIRST_NAME=System
OWNER_LAST_NAME=Owner

# ── API ───────────────────────────────────────────────
API_TITLE=OrderFlow API
API_VERSION=1.0.0
API_V1_PREFIX=/api/v1

# ── Logging ───────────────────────────────────────────
LOG_LEVEL=DEBUG        # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FORMAT=text        # text (desenvolvimento) | json (produção)
```

> ⚠️ Nunca faça commit do arquivo `.env`. Ele já está listado no `.gitignore`.

---

## 📬 Documentação da API

Com a aplicação rodando, acesse a documentação interativa em:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Documentação completa com exemplos por role em [docs/POSTMAN_GUIDE.md](docs/POSTMAN_GUIDE.md)

### Roles de autenticação

| Role    | Descrição                                    |
|---------|----------------------------------------------|
| `OWNER` | Acesso total a todos os recursos             |
| `ADMIN` | Gerencia usuários e pedidos                  |
| `USER`  | Acesso apenas aos próprios pedidos           |

---

## 🚀 CI/CD e Deploy

O deploy é automatizado via GitHub Actions. A cada push na branch `main`:

1. Lint + testes rodam em paralelo
2. Imagem Docker é buildada e enviada ao registry
3. Deploy via SSH com healthcheck automático
4. Em caso de falha, rollback automático para a versão anterior

Consulte o guia completo em [docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md)

---

## 📄 Licença

[MIT](LICENSE)

### Contato

rodrigog3wconcept@gmail.com