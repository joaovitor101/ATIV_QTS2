from faker import Faker
import random

fake = Faker("pt_BR")

SETORES = ["RH", "Financeiro", "Diretoria", "Comercial", "TI", "Jurídico", "Operações"]
PRIORIDADES = ["NORMAL", "ALTO", "CRITICO"]


class ChamadoFactory:
    """Gerador de dados sintéticos de chamados de Helpdesk no padrão Factory."""

    @staticmethod
    def build_payload(
        solicitante: str = None,
        setor: str = None,
        descricao: str = None,
        prioridade: str = None,
    ) -> dict:
        return {
            "solicitante": solicitante or fake.name(),
            "setor": setor or random.choice(SETORES),
            "descricao": descricao or fake.sentence(nb_words=8),
            "prioridade": prioridade or "NORMAL",
        }

    @staticmethod
    def build_critico_payload(**kwargs) -> dict:
        """Gera payload de chamado com prioridade CRÍTICA."""
        return ChamadoFactory.build_payload(prioridade="CRITICO", **kwargs)