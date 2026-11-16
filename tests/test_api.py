"""Testes automatizados da TaskFlow API."""

import pytest
from fastapi.testclient import TestClient

from app import main

cliente = TestClient(main.app)


@pytest.fixture(autouse=True)
def limpar_tarefas():
    """Garante que cada teste comece com a lista de tarefas vazia."""
    main.tarefas.clear()
    yield
    main.tarefas.clear()


def criar(titulo="Estudar DevOps"):
    return cliente.post("/tarefas", json={"titulo": titulo})


def test_health_retorna_ok():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_criar_tarefa():
    resposta = criar("Configurar pipeline")
    assert resposta.status_code == 201
    tarefa = resposta.json()
    assert tarefa["titulo"] == "Configurar pipeline"
    assert tarefa["concluida"] is False


def test_criar_tarefa_sem_titulo_retorna_400():
    resposta = criar("   ")
    assert resposta.status_code == 400


def test_listar_tarefas():
    criar("Tarefa 1")
    criar("Tarefa 2")
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_concluir_tarefa():
    tarefa_id = criar().json()["id"]
    resposta = cliente.put(f"/tarefas/{tarefa_id}/concluir")
    assert resposta.status_code == 200
    assert resposta.json()["concluida"] is True


def test_concluir_tarefa_inexistente_retorna_404():
    resposta = cliente.put("/tarefas/999/concluir")
    assert resposta.status_code == 404


def test_remover_tarefa():
    tarefa_id = criar().json()["id"]
    resposta = cliente.delete(f"/tarefas/{tarefa_id}")
    assert resposta.status_code == 204
    assert cliente.get("/tarefas").json() == []


def test_remover_tarefa_inexistente_retorna_404():
    resposta = cliente.delete("/tarefas/999")
    assert resposta.status_code == 404
