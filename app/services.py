import httpx


class SlackNotificationGateway:
    """Serviço externo que simula envio de notificação para canal do Slack/Teams da equipe de TI."""

    def notify_new_ticket(self, solicitante: str, setor: str, descricao: str, prioridade: str) -> bool:
        # Simula integração com Incoming Webhook do Slack/Teams
        message = (
            f"🚨 Novo Chamado {'*CRÍTICO*' if prioridade == 'CRITICO' else ''} aberto!\n"
            f"Solicitante: {solicitante} | Setor: {setor}\n"
            f"Problema: {descricao}"
        )
        response = httpx.post(
            "https://hooks.slack.com/services/mock/webhook",
            json={"text": message},
            timeout=5.0,
        )
        return response.status_code == 200
