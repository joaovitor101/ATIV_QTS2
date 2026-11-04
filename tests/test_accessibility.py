import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import expect


@pytest.mark.accessibility
def test_wcag_compliance(page, live_server_url):
    """Deve passar na auditoria WCAG 2.1 AA sem violações de acessibilidade."""
    # Act
    page.goto(live_server_url)
    results = Axe().run(page)

    # Assert — zero violações WCAG
    violations = results.violations_count
    assert violations == 0, f"Erros de acessibilidade encontrados: {results.generate_report()}"


@pytest.mark.accessibility
def test_keyboard_navigation(page, live_server_url):
    """Deve permitir navegação sequencial por teclado (Tab) nos campos do formulário."""
    # Act & Assert — foco por teclado via TAB
    page.goto(live_server_url)

    page.keyboard.press("Tab")
    expect(page.get_by_label("Nome do Solicitante")).to_be_focused()

    page.keyboard.press("Tab")
    expect(page.get_by_label("Setor")).to_be_focused()
