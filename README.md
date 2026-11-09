# AT2 - Helpdesk TI — Testes de Integração, E2E e Qualidade Não-Funcional

Sistema de abertura e controle de chamados técnicos de TI para escritórios, construído com FastAPI + Playwright.

## Execução Local do Projeto (`uv`)

```bash
# 1. Instalar dependências e browsers do Playwright
uv sync

# 2. Executar suíte completa de testes
uv run pytest -v

# 3. Subir o servidor da aplicação
uv run uvicorn app.main:app --reload

# 4. Executar testes de carga com Locust
uv run python -m locust -f locustfile.py
```
