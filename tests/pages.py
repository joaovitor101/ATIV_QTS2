from playwright.sync_api import Page


class ChamadoPage:
    """Page Object Model (POM) com seletores semânticos ARIA para o Helpdesk."""

    def __init__(self, page: Page):
        self.page = page
        self.input_solicitante = page.get_by_label("Nome do Solicitante")
        self.select_setor = page.get_by_label("Setor")
        self.textarea_descricao = page.get_by_label("Descrição do Problema")
        self.select_prioridade = page.get_by_label("Prioridade")
        self.btn_submit = page.get_by_role("button", name="Abrir Chamado")

    def navigate(self, base_url: str):
        self.page.goto(base_url)

    def fill_and_submit(self, solicitante: str, setor: str, descricao: str, prioridade: str = "NORMAL"):
        self.input_solicitante.fill(solicitante)
        self.select_setor.select_option(setor)
        self.textarea_descricao.fill(descricao)
        self.select_prioridade.select_option(prioridade)
        self.btn_submit.click()
