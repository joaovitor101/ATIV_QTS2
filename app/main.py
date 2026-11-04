from pathlib import Path
from typing import List
import uuid

from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.services import SlackNotificationGateway

app = FastAPI(title="Helpdesk TI")

_templates_dir = str(Path(__file__).parent / "templates")
templates = Jinja2Templates(directory=_templates_dir)
# Desabilita cache do Jinja2 — evita TypeError com Python 3.14+
templates.env.cache = None  # type: ignore[assignment]

db_chamados: list = []

SETORES = ["RH", "Financeiro", "Diretoria", "Comercial", "TI", "Jurídico", "Operações"]
PRIORIDADES = ["NORMAL", "ALTO", "CRITICO"]


class ChamadoCreate(BaseModel):
    solicitante: str = Field(..., min_length=3)
    setor: str = Field(..., min_length=2)
    descricao: str = Field(..., min_length=10)
    prioridade: str = Field(default="NORMAL")


class ChamadoResponse(ChamadoCreate):
    id: str
    status: str


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "chamados": db_chamados,
        "setores": SETORES,
        "prioridades": PRIORIDADES,
    })


@app.get("/api/v1/chamados", response_model=List[ChamadoResponse])
def list_chamados():
    return db_chamados


@app.post("/api/v1/chamados", response_model=ChamadoResponse, status_code=status.HTTP_201_CREATED)
def create_chamado(
    chamado: ChamadoCreate,
    gateway: SlackNotificationGateway = Depends(SlackNotificationGateway),
):
    new_chamado = {
        "id": str(uuid.uuid4()),
        "solicitante": chamado.solicitante,
        "setor": chamado.setor,
        "descricao": chamado.descricao,
        "prioridade": chamado.prioridade,
        "status": "ABERTO",
    }
    db_chamados.append(new_chamado)

    # Notifica o canal de TI automaticamente ao abrir o chamado (best-effort)
    try:
        gateway.notify_new_ticket(
            chamado.solicitante,
            chamado.setor,
            chamado.descricao,
            chamado.prioridade,
        )
    except Exception:
        pass  # Falha na notificação não impede a criação do chamado

    return new_chamado


@app.post("/api/v1/chamados/{chamado_id}/notify")
def notify_team(
    chamado_id: str,
    gateway: SlackNotificationGateway = Depends(SlackNotificationGateway),
):
    chamado = next((c for c in db_chamados if c["id"] == chamado_id), None)
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")

    success = gateway.notify_new_ticket(
        chamado["solicitante"],
        chamado["setor"],
        chamado["descricao"],
        chamado["prioridade"],
    )
    if not success:
        raise HTTPException(status_code=502, detail="Falha ao notificar equipe de TI")

    return {"status": "notificado", "chamado_id": chamado_id}
