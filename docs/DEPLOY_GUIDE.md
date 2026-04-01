# 🚀 Deploy Guide — OrderFlow

🇺🇸 English version first · 🇧🇷 Versão em Português logo abaixo

---

## 🇺🇸 English

### Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| Docker & Docker Compose | Latest |
| PostgreSQL | 15+ |
| Git | Any recent version |

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/orderflow.git
cd orderflow
```

---

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values. The defaults below work out of the box for local development:

#### Database
```dotenv
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderflow_db

ALEMBIC_DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db
```

> ⚠️ For production, replace `postgres/postgres` with strong credentials and point the host to your database server.

#### System Owner
Created automatically on first startup — no manual step needed.
```dotenv
OWNER_USERNAME=owner
OWNER_PASSWORD=ChangeMe@2026
OWNER_EMAIL=owner@orderflow.com
OWNER_FIRST_NAME=System
OWNER_LAST_NAME=Owner
```
> ⚠️ Change the default credentials before deploying to production.

#### JWT
```dotenv
SECRET_KEY=your_secret_key    # Generate with: openssl rand -hex 64
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> ⚠️ Never use a weak or default `SECRET_KEY` in production.

#### Environment & Trusted Hosts
```dotenv
ENV=development               # development | production
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### API
```dotenv
API_TITLE=OrderFlow API
API_VERSION=1.0.0
API_V1_PREFIX=/api/v1
```

#### Logging
```dotenv
LOG_LEVEL=DEBUG        # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FORMAT=text        # text (development) | json (production)
```

---

### 3. Run locally (without Docker)

> For a full walkthrough of local setup options (Makefile vs manual), see the [README](../README.md).

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the application
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Access: http://localhost:8000/docs

---

### 4. Run with Docker

```bash
docker compose up --build -d
```

The container will:
- Build using a **multi-stage Dockerfile** (builder → runtime)
- Run as a **non-root user** (`appuser`) for security
- Expose port `8000`
- Perform a **health check** every 30s at `/health`

Access: http://localhost:8000/docs

---

### 5. Run the test suite

> For the full list of test commands, see the [README](../README.md).

```bash
# Run all tests with coverage report
make test-all

# Or run each suite individually
make test-unit
make test-integration
make test-functional
```

---

### 6. CI/CD Pipeline (GitHub Actions)

The pipeline runs automatically on every push or pull request to `main`.

#### Pipeline stages

```
SOURCE                            BUILD                  DEPLOY
────────────────────────────      ───────────────────    ──────────────────────
[lint]            ─┐
[test-unit]        ├─→  [build-image]  →  [publish-image]  →  [deploy-vps]
[test-integration] ┤         │                  │                   │
[test-functional]  ─┘   (PR: validate     (main only:         (main only:
                           no push)         push to GHCR)       deploy to VPS)
```

#### Stage details

| Stage | What it does |
|-------|-------------|
| **lint** | Runs `pylint` against `src/` |
| **test-unit** | Unit tests with SQLite in-memory |
| **test-integration** | Integration tests with SQLite in-memory |
| **test-functional** | Functional (end-to-end) tests with SQLite in-memory |
| **build-image** | Validates the Dockerfile builds correctly — runs on PRs too, so broken images are caught before merge |
| **publish-image** | Builds and pushes to GHCR tagged with the commit SHA (`sha-xxxxxxxx`) — full traceability |
| **deploy-vps** | Deploys to VPS via SSH with health check and automatic rollback |

#### Immutable image tagging

Every published image is tagged with the commit SHA:

```
ghcr.io/your-username/orderflow:sha-a1b2c3d4
ghcr.io/your-username/orderflow:latest
```

This guarantees that what was tested is exactly what gets deployed.

#### Deploy script — what happens on the VPS

```
1. Pull new image from GHCR
2. Save current image reference (for rollback)
3. Bring up new container (docker compose up -d)
4. Run database migrations (alembic upgrade head)
5. Health check — 5 attempts, 5s apart, hitting /health
6. If any step fails → trap ERR triggers automatic rollback to previous image
7. Prune unused images
8. Send failure email notification (if deploy fails)
```

---

### 7. Required GitHub Secrets

Configure these in your repository under **Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `VPS_HOST` | VPS IP address or hostname |
| `VPS_USER` | SSH username |
| `VPS_SSH_KEY` | Private SSH key for authentication |
| `VPS_DEPLOY_PATH` | Absolute path to the app directory on the VPS |
| `CONTAINER_REGISTRY_TOKEN` | GHCR Personal Access Token (read:packages) |
| `CONTAINER_REGISTRY_USERNAME` | GitHub username for GHCR login |
| `SMTP_USERNAME` | Email address for failure notifications |
| `SMTP_PASSWORD` | SMTP password or app password |

---

### 8. Docker — image details

The Dockerfile uses a **two-stage build**:

| Stage | Base image | Purpose |
|-------|-----------|---------|
| `builder` | `python:3.12-slim` | Installs dependencies into an isolated prefix |
| `runtime` | `python:3.12-slim` | Copies only what's needed — no build tools in production |

Security highlights:
- Runs as non-root user (`appuser`)
- No build dependencies in the final image
- Built-in health check at `/health`

---

### Troubleshooting

**Container not starting**
```bash
docker compose logs app
```

**Migration errors**
```bash
docker compose exec app alembic upgrade head
docker compose exec app alembic history
```

**Health check failing**
```bash
curl -v http://localhost:8000/health
docker inspect orderflow_app | grep -A 10 Health
```

**Port already in use**
```bash
lsof -i :8000
```

---
---

## 🇧🇷 Português

### Pré-requisitos

| Ferramenta | Versão |
|-----------|--------|
| Python | 3.12+ |
| Docker & Docker Compose | Mais recente |
| PostgreSQL | 15+ |
| Git | Qualquer versão recente |

---

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/orderflow.git
cd orderflow
```

---

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com seus valores. Os padrões abaixo já funcionam para desenvolvimento local:

#### Banco de dados
```dotenv
DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orderflow_db

ALEMBIC_DB_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orderflow_db
```

> ⚠️ Em produção, substitua `postgres/postgres` por credenciais fortes e aponte o host para o seu servidor de banco de dados.

#### Owner do sistema
Criado automaticamente na primeira inicialização — nenhum passo manual necessário.
```dotenv
OWNER_USERNAME=owner
OWNER_PASSWORD=ChangeMe@2026
OWNER_EMAIL=owner@orderflow.com
OWNER_FIRST_NAME=System
OWNER_LAST_NAME=Owner
```
> ⚠️ Altere as credenciais padrão antes de fazer deploy em produção.

#### JWT
```dotenv
SECRET_KEY=sua_chave_secreta    # Gere com: openssl rand -hex 64
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> ⚠️ Nunca use uma `SECRET_KEY` fraca ou padrão em produção.

#### Environment & Trusted Hosts
```dotenv
ENV=development               # development | production
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### API
```dotenv
API_TITLE=OrderFlow API
API_VERSION=1.0.0
API_V1_PREFIX=/api/v1
```

#### Logging
```dotenv
LOG_LEVEL=DEBUG        # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FORMAT=text        # text (desenvolvimento) | json (produção)
```

---

### 3. Rodar localmente (sem Docker)

> Para um passo a passo completo das opções de setup local (Makefile vs manual), consulte o [README](../README.md).

```bash
# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
alembic upgrade head

# Iniciar a aplicação
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse: http://localhost:8000/docs

---

### 4. Rodar com Docker

```bash
docker compose up --build -d
```

O container irá:
- Fazer build com **Dockerfile multi-stage** (builder → runtime)
- Rodar como **usuário não-root** (`appuser`) por segurança
- Expor a porta `8000`
- Executar **health check** a cada 30s no endpoint `/health`

Acesse: http://localhost:8000/docs

---

### 5. Executar os testes

> Para a lista completa de comandos de teste, consulte o [README](../README.md).

```bash
# Rodar todos os testes com relatório de cobertura
make test-all

# Ou rodar cada suite individualmente
make test-unit
make test-integration
make test-functional
```

---

### 6. Pipeline CI/CD (GitHub Actions)

O pipeline executa automaticamente a cada push ou pull request para a branch `main`.

#### Estágios do pipeline

```
SOURCE                            BUILD                  DEPLOY
────────────────────────────      ───────────────────    ──────────────────────
[lint]            ─┐
[test-unit]        ├─→  [build-image]  →  [publish-image]  →  [deploy-vps]
[test-integration] ┤         │                  │                   │
[test-functional]  ─┘   (PR: valida       (só na main:        (só na main:
                           sem push)        push pro GHCR)      deploy no VPS)
```

#### Detalhes por estágio

| Estágio | O que faz |
|---------|----------|
| **lint** | Executa `pylint` no diretório `src/` |
| **test-unit** | Testes unitários com SQLite em memória |
| **test-integration** | Testes de integração com SQLite em memória |
| **test-functional** | Testes funcionais (ponta a ponta) com SQLite em memória |
| **build-image** | Valida que o Dockerfile compila corretamente — roda em PRs também, para pegar imagens quebradas antes do merge |
| **publish-image** | Builda e envia para o GHCR com tag do commit SHA (`sha-xxxxxxxx`) — rastreabilidade total |
| **deploy-vps** | Deploy no VPS via SSH com health check e rollback automático |

#### Tags imutáveis de imagem

Cada imagem publicada recebe a tag do commit SHA:

```
ghcr.io/seu-usuario/orderflow:sha-a1b2c3d4
ghcr.io/seu-usuario/orderflow:latest
```

Isso garante que o que foi testado é exatamente o que vai para produção.

#### Script de deploy — o que acontece no VPS

```
1. Pull da nova imagem do GHCR
2. Salva referência da imagem atual (para rollback)
3. Sobe novo container (docker compose up -d)
4. Executa migrações (alembic upgrade head)
5. Health check — 5 tentativas, intervalo de 5s, no endpoint /health
6. Se qualquer etapa falhar → trap ERR dispara rollback automático para a imagem anterior
7. Remove imagens não utilizadas
8. Envia notificação por email em caso de falha
```

---

### 7. Secrets necessários no GitHub

Configure em **Settings → Secrets and variables → Actions**:

| Secret | Descrição |
|--------|----------|
| `VPS_HOST` | IP ou hostname do VPS |
| `VPS_USER` | Usuário SSH |
| `VPS_SSH_KEY` | Chave SSH privada para autenticação |
| `VPS_DEPLOY_PATH` | Caminho absoluto do diretório da aplicação no VPS |
| `CONTAINER_REGISTRY_TOKEN` | Personal Access Token do GHCR (read:packages) |
| `CONTAINER_REGISTRY_USERNAME` | Usuário GitHub para login no GHCR |
| `SMTP_USERNAME` | Email para notificações de falha |
| `SMTP_PASSWORD` | Senha SMTP ou app password |

---

### 8. Docker — detalhes da imagem

O Dockerfile usa **build em dois estágios**:

| Estágio | Imagem base | Finalidade |
|---------|------------|-----------|
| `builder` | `python:3.12-slim` | Instala dependências em um prefixo isolado |
| `runtime` | `python:3.12-slim` | Copia apenas o necessário — sem ferramentas de build em produção |

Destaques de segurança:
- Roda como usuário não-root (`appuser`)
- Sem dependências de build na imagem final
- Health check nativo no endpoint `/health`

---

### Troubleshooting

**Container não sobe**
```bash
docker compose logs app
```

**Erros de migração**
```bash
docker compose exec app alembic upgrade head
docker compose exec app alembic history
```

**Health check falhando**
```bash
curl -v http://localhost:8000/health
docker inspect orderflow_app | grep -A 10 Health
```

**Porta já em uso**
```bash
lsof -i :8000
```
