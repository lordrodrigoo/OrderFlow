# Guia de Deploy — OrderFlow

Este guia cobre o processo de deploy do OrderFlow em diferentes ambientes.

## Pré-requisitos
- Python 3.11+
- Docker e Docker Compose
- PostgreSQL
- Variáveis de ambiente configuradas

## Setup do Ambiente
1. Clone o repositório
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Migrações Alembic
```bash
alembic upgrade head
```

## Deploy Local
- Execute:
  ```bash
  uvicorn src.main:app --host 0.0.0.0 --port 8000
  ```
- Acesse: http://localhost:8000

## Deploy com Docker
```bash
docker-compose up --build -d
```
- Acesse: http://localhost:8000

## Variáveis de Ambiente
- `DATABASE_URL`: string de conexão do banco
- `SECRET_KEY`: chave secreta para autenticação
- Outras variáveis podem ser necessárias conforme o ambiente

## Troubleshooting
- Verifique logs do Docker com `docker-compose logs`
- Certifique-se de que as portas não estão em uso
- Confira as variáveis de ambiente

## Checklist Pós-Deploy
- [ ] Aplicação rodando
- [ ] Banco migrado
- [ ] Variáveis de ambiente corretas
- [ ] Testes executados

Dúvidas? Consulte o README principal ou entre em contato.
