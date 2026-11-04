# AT2 - Helpdesk TI — Testes de Integração, E2E e Qualidade Não-Funcional

Sistema de abertura e controle de chamados técnicos de TI para escritórios, construído com FastAPI + Playwright.

## Execução Local do Projeto (`uv`)

```bash
# 1. Instalar dependências e browsers do Playwright
uv sync
uv run playwright install chromium

# 2. Executar suíte completa de testes
uv run pytest -v

# 3. Subir o servidor da aplicação
uv run uvicorn app.main:app --reload

# 4. Executar testes de carga com Locust
uv run locust -f locustfile.py --headless -u 50 -r 10 --run-time 30s --host http://localhost:8000
```

## Estrutura do Projeto

```
at2-qts-app/
├── app/
│   ├── main.py          # Aplicação FastAPI (rotas, modelos)
│   ├── services.py      # SlackNotificationGateway (integração externa)
│   └── templates/
│       └── index.html   # Interface Web do Helpdesk
├── tests/
│   ├── conftest.py      # Fixtures: api_client, live_server_url
│   ├── factories.py     # ChamadoFactory com Faker
│   ├── pages.py         # Page Object Model (POM) com seletores ARIA
│   ├── test_integration.py  # Testes de integração com mocks
│   ├── test_e2e.py          # Testes E2E com Playwright
│   └── test_accessibility.py # Auditoria WCAG via Axe-core
├── locustfile.py        # Testes de carga
└── PRD.MD               # Requisitos do produto
```

## Endpoints da API

| Método | Rota                             | Descrição                                   |
|--------|----------------------------------|---------------------------------------------|
| GET    | `/`                              | Interface Web com formulário e lista        |
| GET    | `/api/v1/chamados`               | Lista todos os chamados abertos             |
| POST   | `/api/v1/chamados`               | Abre novo chamado + notifica equipe de TI   |
| POST   | `/api/v1/chamados/{id}/notify`   | Renotifica equipe via Slack/Teams           |

```

## Estrutura do Projeto

```
at2-qts-app/
├── app/
│   ├── main.py          # Aplicação FastAPI (rotas, modelos)
│   ├── services.py      # SlackNotificationGateway (integração externa)
│   └── templates/
│       └── index.html   # Interface Web do Helpdesk
├── tests/
│   ├── conftest.py      # Fixtures: api_client, live_server_url
│   ├── factories.py     # ChamadoFactory com Faker
│   ├── pages.py         # Page Object Model (POM) com seletores ARIA
│   ├── test_integration.py  # Testes de integração com mocks
│   ├── test_e2e.py          # Testes E2E com Playwright
│   └── test_accessibility.py # Auditoria WCAG via Axe-core
├── locustfile.py        # Testes de carga
└── PRD.MD               # Requisitos do produto
```

## Endpoints da API

| Método | Rota                             | Descrição                                   |
|--------|----------------------------------|---------------------------------------------|
| GET    | `/`                              | Interface Web com formulário e lista        |
| GET    | `/api/v1/chamados`               | Lista todos os chamados abertos             |
| POST   | `/api/v1/chamados`               | Abre novo chamado + notifica equipe de TI   |
| POST   | `/api/v1/chamados/{id}/notify`   | Renotifica equipe via Slack/Teams           |