import socket
import threading
import time

import pytest
import uvicorn
from fastapi.testclient import TestClient
from app.main import app, db_chamados


@pytest.fixture
def api_client():
    """Setup e Teardown para o cliente de testes da API de Helpdesk."""
    # Setup
    db_chamados.clear()
    client = TestClient(app)
    yield client
    # Teardown
    db_chamados.clear()


@pytest.fixture(scope="session")
def live_server_url():
    """Sobe o servidor FastAPI em uma thread separada para testes E2E/acessibilidade."""
    host = "127.0.0.1"
    port = 8765
    config = uvicorn.Config(app=app, host=host, port=port, log_level="error")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Aguarda o servidor estar pronto
    for _ in range(50):
        try:
            with socket.create_connection((host, port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)

    yield f"http://{host}:{port}"

    server.should_exit = True
    thread.join(timeout=5)
