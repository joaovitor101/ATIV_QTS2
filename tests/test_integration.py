import pytest
from tests.factories import ChamadoFactory


@pytest.mark.integration
def test_create_chamado_success(api_client):
    """Deve criar um chamado e retornar status 201 com os dados corretos."""
    # Arrange
    payload = ChamadoFactory.build_payload()

    # Act
    response = api_client.post("/api/v1/chamados", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["solicitante"] == payload["solicitante"]
    assert data["setor"] == payload["setor"]
    assert data["status"] == "ABERTO"
    assert "id" in data


# ---------------------------------------------------------------------------
# Testes parametrizados de validação (RN-01) — padrão AAA
# ---------------------------------------------------------------------------

@pytest.mark.integration
@pytest.mark.parametrize(
    "solicitante, setor, descricao, status_esperado",
    [
        # Casos válidos
        ("Carlos Silva","TI","Computador não liga mais.",201),
        ("Ana","TI","Senha do sistema bloqueada.",201),
    ]
)
def test_validacao_chamado_parametrizado(api_client, solicitante, setor, descricao, status_esperado):
    """RN-01: Tabela de casos válidos e inválidos para criação de chamado."""
    # Arrange
    payload = {k: v for k, v in {
        "solicitante": solicitante,
        "setor":       setor,
        "descricao":   descricao,
        "prioridade":  "NORMAL",
    }.items() if v is not None}

    # Act
    response = api_client.post("/api/v1/chamados", json=payload)

    # Assert
    assert response.status_code == status_esperado


# ---------------------------------------------------------------------------
# Testes de caminho negativo (erros de negócio)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_notify_chamado_inexistente_retorna_404(api_client, mocker):
    """Deve retornar 404 ao tentar notificar um chamado que não existe."""
    # Arrange
    mocker.patch("app.services.SlackNotificationGateway.notify_new_ticket", return_value=True)

    # Act
    response = api_client.post("/api/v1/chamados/id-que-nao-existe/notify")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Chamado não encontrado"


# ---------------------------------------------------------------------------
# Testes de mock de integração externa
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_notify_team_success_with_mock(api_client, mocker):
    """Deve notificar a equipe de TI com sucesso ao acionar o endpoint de notify."""
    # Arrange
    payload = ChamadoFactory.build_payload(setor="Financeiro")
    created = api_client.post("/api/v1/chamados", json=payload).json()

    # Mock da dependência externa (Slack/Teams)
    mock_gateway = mocker.patch(
        "app.services.SlackNotificationGateway.notify_new_ticket", return_value=True
    )

    # Act
    response = api_client.post(f"/api/v1/chamados/{created['id']}/notify")

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "notificado"
    mock_gateway.assert_called_once_with(
        payload["solicitante"],
        payload["setor"],
        payload["descricao"],
        payload["prioridade"],
    )


@pytest.mark.integration
def test_notify_team_failure_with_mock(api_client, mocker):
    """Deve retornar 502 quando o webhook do Slack/Teams falhar."""
    # Arrange
    payload = ChamadoFactory.build_payload()
    created = api_client.post("/api/v1/chamados", json=payload).json()

    # Mock simulando falha do serviço externo
    mocker.patch(
        "app.services.SlackNotificationGateway.notify_new_ticket", return_value=False
    )

    # Act
    response = api_client.post(f"/api/v1/chamados/{created['id']}/notify")

    # Assert
    assert response.status_code == 502
    assert response.json()["detail"] == "Falha ao notificar equipe de TI"


