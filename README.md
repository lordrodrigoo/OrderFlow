
# OrderFlow 

API REST para gestão de pedidos e usuários, construída com FastAPI e Clean Architecture. Autenticação JWT com sistema de roles (OWNER/ADMIN/USER), CI/CD completo com rollback automático, cobertura de testes de 100% e deploy containerizado com Docker multi-stage.

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00?logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E?logo=alembic&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?logo=gunicorn&logoColor=white)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=codecov&logoColor=white)


## Tecnologias Utilizadas
- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- Pytest
- Docker & Docker Compose
- PostgreSQL
- Pydantic
- Uvicorn
- Coverage.py

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
├── Makefile               — Comandos prontos (test, coverage, deploy)
└── .env.example           — Variáveis de ambiente necessárias
```

## ⚙️ Como Rodar Localmente

1. Clone o repositório
2. Copie o arquivo de exemplo e configure as variáveis:
```bash
   cp .env.example .env
```
3. Crie e ative um ambiente virtual, depois instale as dependências:
```bash
   pip install -r requirements.txt
```
4. Execute as migrações e inicie a aplicação:
```bash
   alembic upgrade head
   uvicorn src.main:app --reload
```

Acesse em http://localhost:8000/docs

---

## 🐳 Como Rodar com Docker
```bash
docker-compose up --build
```

Acesse em http://localhost:8000/docs

---

## 🧪 Testes
```bash
make test        # roda todos os testes
make coverage    # gera relatório de cobertura
```

Cobertura atual: **100%** — unitários, integração e funcionais.

---

## 🚀 Deploy

O deploy é automatizado via GitHub Actions. A cada push na branch principal:

1. Lint + testes rodam em paralelo
2. Imagem Docker é buildada e enviada ao registry
3. Deploy via SSH com healthcheck automático
4. Em caso de falha, rollback automático para a versão anterior

Consulte o guia completo em [docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md)

---

## 📬 API

Documentação completa com exemplos por role em [docs/POSTMAN_GUIDE.md](docs/POSTMAN_GUIDE.md)

Ou acesse `/docs` com a aplicação rodando para a documentação interativa do FastAPI.

---

## 📄 Licença

MIT

## Contato
rodrigo@g3wconcept@gmail.com
