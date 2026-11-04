import pytest
from playwright.sync_api import expect
from tests.pages import ChamadoPage
from tests.factories import ChamadoFactory


@pytest.mark.e2e
def test_open_critical_ticket_appears_highlighted(page, live_server_url):
    """
    Cenário E2E: Abrir um chamado CRÍTICO via tela e verificar se ele
    aparece com destaque (classe 'critico') na lista de pendências.
    """
    # Arrange
    chamado_page = ChamadoPage(page)
    payload = ChamadoFactory.build_critico_payload(
        solicitante="Carlos Souza",
        setor="Diretoria",
        descricao="Servidor de e-mail fora do ar, impactando toda a empresa.",
    )

    # Act
    chamado_page.navigate(live_server_url)
    chamado_page.fill_and_submit(
        payload["solicitante"],
        payload["setor"],
        payload["descricao"],
        payload["prioridade"],
    )

    # Assert — chamado aparece na lista de pendências
    lista = page.get_by_role("list", name="Lista de Chamados Pendentes")
    expect(lista).to_contain_text(payload["solicitante"])

    # Assert — chamado crítico tem destaque visual (badge CRÍTICO)
    badge = page.get_by_text("CRÍTICO")
    expect(badge).to_be_visible()
