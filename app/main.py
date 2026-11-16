"""TaskFlow API: API REST de lista de tarefas."""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import APP_NAME, APP_VERSION

logger = logging.getLogger("taskflow")

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API REST de lista de tarefas - Projeto Final de Integração DevOps.",
)

# Tamanho máximo permitido para o título de uma tarefa
LIMITE_TITULO = 100

# Armazenamento em memória: os dados são perdidos ao reiniciar a aplicação.
tarefas: dict[int, dict] = {}
proximo_id = 1


class NovaTarefa(BaseModel):
    titulo: str


def buscar_tarefa(tarefa_id: int) -> dict:
    """Retorna a tarefa ou responde 404 se ela não existir."""
    if tarefa_id not in tarefas:
        logger.warning("Tarefa %s não encontrada", tarefa_id)
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefas[tarefa_id]


@app.get("/health")
def health():
    """Verificação de saúde da aplicação."""
    return {"status": "ok", "versao": APP_VERSION}


@app.get("/tarefas")
def listar_tarefas():
    return list(tarefas.values())


@app.post("/tarefas", status_code=201)
def criar_tarefa(dados: NovaTarefa):
    global proximo_id

    titulo = dados.titulo.strip()
    if not titulo:
        logger.warning("Tentativa de criar tarefa sem título")
        raise HTTPException(status_code=400, detail="O título da tarefa é obrigatório")

    if len(titulo) >= LIMITE_TITULO:
        logger.warning("Título com %s caracteres excede o limite", len(titulo))
        raise HTTPException(
            status_code=400,
            detail=f"O título deve ter no máximo {LIMITE_TITULO} caracteres",
        )

    tarefa ={"id": proximo_id, "titulo": titulo, "concluida": False}
    tarefas[proximo_id] = tarefa
    proximo_id += 1
    logger.info("Tarefa %s criada", tarefa["id"])
    return tarefa


@app.put("/tarefas/{tarefa_id}/concluir")
def concluir_tarefa(tarefa_id: int):
    tarefa = buscar_tarefa(tarefa_id)
    tarefa["concluida"] = True
    logger.info("Tarefa %s concluída", tarefa_id)
    return tarefa


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def remover_tarefa(tarefa_id: int):
    buscar_tarefa(tarefa_id)
    del tarefas[tarefa_id]
    logger.info("Tarefa %s removida", tarefa_id)
