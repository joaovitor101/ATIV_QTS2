from locust import HttpUser, task, between
from tests.factories import ChamadoFactory


class HelpdeskUserBehavior(HttpUser):
    """Simula comportamento de usuários acessando o Helpdesk de TI."""

    wait_time = between(1, 3)

    @task(3)
    def list_chamados(self):
        """Consulta a lista de chamados abertos (operação mais frequente)."""
        self.client.get("/api/v1/chamados")

    @task(1)
    def create_chamado(self):
        """Abre um novo chamado de suporte."""
        payload = ChamadoFactory.build_payload()
        self.client.post("/api/v1/chamados", json=payload)
