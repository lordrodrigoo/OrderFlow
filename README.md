
# OrderFlow 📦

Sistema robusto para gestão de pedidos, usuários e operações de e-commerce, com API moderna, deploy facilitado e foco em escalabilidade.

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/fastapi-ready-green?logo=fastapi)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![PostgreSQL](https://img.shields.io/badge/postgresql-ready-blue?logo=postgresql)
![Alembic](https://img.shields.io/badge/alembic-migrations-yellowgreen)
![Pytest](https://img.shields.io/badge/pytest-tested-green?logo=pytest)
![Coverage](https://img.shields.io/badge/coverage-97%25-success)
![GitHub Actions](https://img.shields.io/badge/ci-github--actions-blue?logo=githubactions)
![Build](https://img.shields.io/badge/build-passing-brightgreen)


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

## Estrutura do Projeto
- `src/` — Código-fonte principal
- `alembic/` — Migrações de banco de dados
- `docs/` — Documentação e guias
- `tests/` — Testes automatizados
- `Dockerfile` & `docker-compose.yml` — Deploy e ambiente

## Como Rodar Localmente
1. Clone o repositório
2. Crie e ative um ambiente virtual
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente necessárias
5. Execute as migrações Alembic:
   ```bash
   alembic upgrade head
   ```
6. Inicie a aplicação:
   ```bash
   uvicorn src.main:app --reload
   ```

## Como Rodar com Docker
```bash
docker-compose up --build
```
Acesse em http://localhost:8000

## Como Rodar os Testes
```bash
pytest
```

## Deploy
Consulte o guia completo em [docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md)

## API
A documentação das rotas e exemplos de uso estão em [docs/POSTMAN_GUIDE.md](docs/POSTMAN_GUIDE.md)


## Licença
MIT

## Contato
rodrigo@email.com
