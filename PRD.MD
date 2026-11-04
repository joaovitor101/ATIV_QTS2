# Product Requirement Document (PRD) - Helpdesk TI — Gestão de Suporte de TI

## 1. Visão Geral
Aplicação web para abertura e controle de chamados técnicos de TI para escritórios. Permite que colaboradores de diferentes setores registrem problemas técnicos, com notificação automática para a equipe de TI via canal do Slack/Teams.

## 2. Modelo de Dados — Chamado

| Campo         | Tipo   | Restrições                              |
|---------------|--------|-----------------------------------------|
| `id`          | string | UUID gerado automaticamente             |
| `solicitante` | string | Mínimo 3 caracteres                     |
| `setor`       | string | Ex: RH, Financeiro, Diretoria, TI…     |
| `descricao`   | string | Mínimo 10 caracteres                    |
| `prioridade`  | string | `NORMAL` \| `ALTO` \| `CRITICO`         |
| `status`      | string | Valor inicial: `ABERTO`                 |

## 3. Rotas e Endpoints (API)

- `GET /` — Interface Web principal em HTML semântico com formulário de abertura de chamados e lista de pendências.
- `GET /api/v1/chamados` — Retorna a lista de chamados abertos.
- `POST /api/v1/chamados` — Abre um novo chamado e notifica a equipe de TI automaticamente (best-effort).
  - *Payload*: `{ "solicitante": string, "setor": string, "descricao": string, "prioridade": string }`
- `POST /api/v1/chamados/{id}/notify` — Renotifica a equipe via webhook Slack/Teams (Serviço Mockado nos testes).

## 4. Regras de Negócio

### RN-01 — Validação do Chamado
| Campo         | Regra                                                                        |
|---------------|------------------------------------------------------------------------------|
| `solicitante` | Obrigatório. Mínimo de **3 caracteres**.                                     |
| `setor`       | Obrigatório. Mínimo de **2 caracteres**.                                     |
| `descricao`   | Obrigatório. Mínimo de **10 caracteres**.                                    |
| `prioridade`  | Obrigatório. Valores aceitos: `NORMAL`, `ALTO`, `CRITICO`. Padrão: `NORMAL`. |

### RN-02 — Notificação Automática ao Abrir Chamado
Ao criar um novo chamado (`POST /api/v1/chamados`), o sistema deve tentar notificar automaticamente o canal de TI via Slack/Teams. A notificação é **best-effort**: uma falha no gateway externo **não** impede a criação do chamado.

### RN-03 — Destaque Visual para Chamados Críticos
Chamados com `prioridade = CRITICO` devem ser exibidos com destaque visual diferenciado na lista de pendências (fundo vermelho + badge `CRÍTICO`), para facilitar a triagem pela equipe de TI.

### RN-04 — Status Inicial
Todo chamado recém-criado deve ter `status = "ABERTO"` automaticamente.

## 5. Integração Externa (Mock)

Envio de notificação para o canal do Slack ou Microsoft Teams da equipe de TI ao abrir um chamado, via `SlackNotificationGateway`. Nos testes de integração, essa dependência é isolada com `pytest-mock`.

## 6. Requisitos Não Funcionais (ISO/IEC 25010)

- **Acessibilidade (Usabilidade)**: Conformidade com WCAG 2.1 Nível AA, navegação completa por teclado (auditoria via Axe-core).
- **Eficiência de Desempenho**: Tempo de resposta $p_{95} < 200\text{ms}$ e suporte a no mínimo 50 requisições simultâneas por segundo (RPS) via Locust.

## 7. Cenários de Teste

| Tipo           | Cenário                                                                   |
|----------------|---------------------------------------------------------------------------|
| Integração     | Abertura de chamado com retorno 201 e dados corretos                      |
| Integração     | Notificação Slack/Teams com mock — sucesso (200)                          |
| Integração     | Notificação Slack/Teams com mock — falha do gateway (502)                 |
| E2E            | Abrir chamado **CRÍTICO** via tela e verificar badge de destaque na lista |
| Acessibilidade | Auditoria WCAG 2.1 AA sem violações via Axe-core                          |
| Acessibilidade | Navegação por teclado (Tab) em todos os campos do formulário              |
