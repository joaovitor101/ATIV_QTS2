# Agent Context & Rules (.cursorrules / AGENTS.md)

## Diretrizes do Projeto
- **Linguagem**: Python 3.12+ utilizando `uv` como gerenciador de dependências.
- **Testes**: Padrão Arrange-Act-Assert (AAA), uso de Mocks isolando chamadas externas, fixtures com `yield` e seletores semânticos do Playwright.
- **Qualidade de Código**: Manter conformidade semântica para validação automatizada de acessibilidade via Axe-core.