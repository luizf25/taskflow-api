# TaskFlow API

[![CI/CD](https://github.com/luizf25/taskflow-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/luizf25/taskflow-api/actions/workflows/ci-cd.yml)

API REST de lista de tarefas desenvolvida para o Projeto Final da disciplina **Integração DevOps**.

O objetivo do projeto não é a complexidade da aplicação, e sim demonstrar o ciclo DevOps completo: versionamento com Git, integração contínua, testes automatizados, geração de artefato, implantação, segurança e observabilidade.

## Integrantes

| Nome | GitHub |
|---|---|
| Luiz Felipe Formiga Soares | [@luizf25](https://github.com/luizf25) |
| Lucas Vinicius de Souza | [@lucasv-souza](https://github.com/lucasv-souza) |

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias e ferramentas](#tecnologias-e-ferramentas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Requisitos de infraestrutura](#requisitos-de-infraestrutura)
- [Como executar](#como-executar)
- [Como testar a API](#como-testar-a-api)
- [Testes automatizados](#testes-automatizados)
- [Versionamento e branches](#versionamento-e-branches)
- [Pipeline de CI/CD](#pipeline-de-cicd)
- [Artefato gerado](#artefato-gerado)
- [Segurança (DevSecOps)](#segurança-devsecops)
- [Evidências do pipeline](#evidências-do-pipeline)

## Funcionalidades

A API permite cadastrar, listar, concluir e remover tarefas. Os dados ficam em memória, então são perdidos quando a aplicação reinicia. Isso foi uma escolha consciente para manter o projeto simples, sem banco de dados.

| Método | Rota | Descrição | Respostas |
|---|---|---|---|
| GET | `/health` | Verificação de saúde (status e versão) | 200 |
| GET | `/tarefas` | Lista todas as tarefas | 200 |
| POST | `/tarefas` | Cria uma tarefa (`{"titulo": "..."}`) | 201, 400 |
| PUT | `/tarefas/{id}/concluir` | Marca a tarefa como concluída | 200, 404 |
| DELETE | `/tarefas/{id}` | Remove a tarefa | 204, 404 |

Regras de negócio:
- O título é obrigatório (vazio ou só com espaços retorna **400**)
- O título tem no máximo **100 caracteres** (acima disso retorna **400**)
- Concluir ou remover uma tarefa inexistente retorna **404**

## Tecnologias e ferramentas

| Ferramenta | Uso |
|---|---|
| Python 3.13 + FastAPI | API REST e documentação Swagger automática |
| Uvicorn | Servidor da aplicação |
| pytest | Testes automatizados |
| pip-audit | Análise de dependências vulneráveis |
| Docker | Imagem da aplicação (artefato) |
| Docker Compose | Implantação local reproduzível |
| GitHub Actions | Pipeline de CI/CD |
| GitHub Container Registry (GHCR) | Registro da imagem Docker |
| Git + GitHub | Versionamento, branches e Pull Requests |

## Estrutura do projeto

```
taskflow-api/
├── .github/workflows/ci-cd.yml   # Pipeline do GitHub Actions
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuração por variáveis de ambiente e logs
│   └── main.py                   # Endpoints da API
├── tests/
│   └── test_api.py               # Testes automatizados (pytest)
├── .dockerignore
├── .env.example                  # Modelo das variáveis de ambiente
├── .gitignore
├── docker-compose.yml            # Implantação com a imagem do GHCR
├── Dockerfile
├── requirements.txt              # Dependências da aplicação
└── requirements-dev.txt          # Dependências de teste e segurança
```

## Requisitos de infraestrutura

| Para | Requisito |
|---|---|
| Executar a aplicação (recomendado) | Docker 20+ e Docker Compose v2, acesso à internet para baixar a imagem do `ghcr.io` |
| Executar localmente sem Docker ou rodar os testes | Python 3.13 e pip |
| Rede | Porta definida em `APP_PORT` livre (padrão 8000) |
| Recursos | Mínimos: 1 CPU e 256 MB de memória são suficientes |

Variáveis de ambiente (modelo em [`.env.example`](.env.example)):

| Variável | Onde é usada | Padrão | Descrição |
|---|---|---|---|
| `IMAGE_TAG` | docker-compose | `latest` | Versão da imagem a ser implantada |
| `APP_PORT` | docker-compose | `8000` | Porta da máquina onde a API fica disponível |
| `LOG_LEVEL` | aplicação | `INFO` | Nível de log: DEBUG, INFO, WARNING ou ERROR |
| `APP_VERSION` | aplicação | `dev` | Versão exibida no `/health`. Gravada na imagem pelo pipeline, não precisa ser definida |

## Como executar

### Com Docker Compose (imagem publicada)

```bash
git clone https://github.com/luizf25/taskflow-api.git
cd taskflow-api
cp .env.example .env          # ajuste IMAGE_TAG, APP_PORT e LOG_LEVEL se quiser
docker compose up -d
```

A API fica disponível em http://localhost:8000.

### Localmente com Python

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Como testar a API

A forma mais simples é pelo **Swagger**, gerado automaticamente pelo FastAPI: http://localhost:8000/docs

Ou com `curl`:

```bash
# Verificar a saúde da aplicação
curl http://localhost:8000/health

# Criar uma tarefa
curl -X POST http://localhost:8000/tarefas -H "Content-Type: application/json" -d '{"titulo": "Estudar DevOps"}'

# Listar tarefas
curl http://localhost:8000/tarefas

# Concluir a tarefa 1
curl -X PUT http://localhost:8000/tarefas/1/concluir

# Remover a tarefa 1
curl -X DELETE http://localhost:8000/tarefas/1
```

## Testes automatizados

Os testes ficam em [`tests/test_api.py`](tests/test_api.py) e usam **pytest** com o `TestClient` do FastAPI. Cada teste começa com a lista de tarefas vazia.

| Teste | O que valida |
|---|---|
| `test_health_retorna_ok` | `/health` responde 200 com status ok |
| `test_criar_tarefa` | Criação retorna 201 e tarefa não concluída |
| `test_criar_tarefa_sem_titulo_retorna_400` | Regra de título obrigatório |
| `test_listar_tarefas` | Listagem retorna as tarefas criadas |
| `test_concluir_tarefa` | Tarefa é marcada como concluída |
| `test_concluir_tarefa_inexistente_retorna_404` | Erro para id inexistente |
| `test_remover_tarefa` | Tarefa é removida da lista |
| `test_remover_tarefa_inexistente_retorna_404` | Erro para id inexistente |
| `test_titulo_com_100_caracteres_e_aceito` | Limite de tamanho do título (fronteira) |
| `test_titulo_com_101_caracteres_e_rejeitado` | Limite de tamanho do título (acima) |

Para executar:

```bash
pip install -r requirements-dev.txt
python -m pytest -v
```

No pipeline, os testes rodam com `-v`, então o log do GitHub Actions mostra cada caso como `PASSED` ou `FAILED`. Se qualquer teste falhar, o job falha, e a imagem Docker **não** é gerada.

## Versionamento e branches

Adotamos o **GitHub Flow**, por ser a estratégia mais simples para uma equipe pequena com entregas contínuas:

- A branch `main` está sempre estável e pronta para gerar uma versão
- Toda alteração é feita em uma branch própria, criada a partir da `main`
- A alteração volta para a `main` **somente por Pull Request**, revisado e aprovado pelo outro integrante
- O pipeline roda em cada Pull Request, então problemas aparecem antes do merge
- Versões são marcadas com tags no padrão `vX.Y.Z` (versionamento semântico)

Prefixos de branch:

| Prefixo | Uso | Exemplo |
|---|---|---|
| `feature/` | Nova funcionalidade | `feature/api-tarefas` |
| `fix/` | Correção de erro | `fix/nome-do-erro` |
| `docs/` | Somente documentação | `docs/readme` |

Mensagens de commit seguem um prefixo que indica o tipo da alteração: `feat:`, `fix:`, `test:`, `build:`, `ci:`, `docs:` e `chore:`.

### Histórico de Pull Requests

| PR | Branch | Autor | Revisor |
|---|---|---|---|
| [#1](https://github.com/luizf25/taskflow-api/pull/1) | `feature/api-tarefas` | Luiz | Lucas |
| [#2](https://github.com/luizf25/taskflow-api/pull/2) | `feature/testes` | Lucas | Luiz |
| [#3](https://github.com/luizf25/taskflow-api/pull/3) | `feature/docker` | Luiz | Lucas |
| [#4](https://github.com/luizf25/taskflow-api/pull/4) | `feature/pipeline-ci` | Lucas | Luiz |
| [#5](https://github.com/luizf25/taskflow-api/pull/5) | `feature/limite-titulo` | Luiz (correção: Lucas) | Lucas |
| [#6](https://github.com/luizf25/taskflow-api/pull/6) | `docs/readme` | Luiz | Lucas |
| [#7](https://github.com/luizf25/taskflow-api/pull/7) | `docs/deploy-rollback` | Lucas | Luiz |

## Pipeline de CI/CD

Arquivo: [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)

**Quando executa:**

| Evento | O que acontece |
|---|---|
| Pull Request para a `main` | Valida, testa e constrói a imagem (sem publicar) |
| Push na `main` (merge de PR) | Valida, testa e publica a imagem com tag `sha-<commit>` |
| Tag `vX.Y.Z` | Valida, testa e publica a imagem com tags `X.Y.Z` e `latest` |

**Job 1: Validar e testar**

1. **Obter código-fonte (checkout)**: `actions/checkout`
2. **Preparar ambiente Python 3.13**: `actions/setup-python`, com cache do pip
3. **Instalar dependências**: `pip install -r requirements-dev.txt`
4. **Validar aplicação (compilação)**: `python -m compileall`, que detecta erros de sintaxe
5. **Verificação de segurança**: `pip-audit -r requirements.txt`
6. **Executar testes automatizados**: `python -m pytest -v`

**Job 2: Gerar artefato (imagem Docker)**, que só executa se o job 1 passar

1. Checkout do código
2. Definição das tags da imagem (`docker/metadata-action`)
3. Login no GHCR com `GITHUB_TOKEN` (fora de Pull Requests)
4. Build da imagem e publicação no GHCR (fora de Pull Requests)

## Artefato gerado

O artefato é uma **imagem Docker** publicada no GitHub Container Registry:

**`ghcr.io/luizf25/taskflow-api`**: [ver pacote no GitHub](https://github.com/luizf25/taskflow-api/pkgs/container/taskflow-api)

| Tag | Origem | Uso |
|---|---|---|
| `1.0.0`, `1.1.0`... | Tag git `v1.0.0`, `v1.1.0`... | Versões oficiais para implantação |
| `latest` | Última tag de versão | Atalho para a versão mais recente |
| `sha-<commit>` | Cada push na `main` | Rastrear exatamente qual commit gerou a imagem |

Rastreabilidade:
- A versão é gravada dentro da imagem (`APP_VERSION`) e aparece no `GET /health`
- A imagem recebe os labels OCI `org.opencontainers.image.revision` (commit) e `org.opencontainers.image.version`

Para usar a imagem diretamente:

```bash
docker pull ghcr.io/luizf25/taskflow-api:1.1.0
docker run -d -p 8000:8000 ghcr.io/luizf25/taskflow-api:1.1.0
curl http://localhost:8000/health
```

## Segurança (DevSecOps)

| Prática | Como contribui para a segurança |
|---|---|
| **pip-audit no pipeline** | Verifica as dependências contra bases públicas de vulnerabilidades. Se houver dependência vulnerável, o pipeline falha e nenhuma imagem é publicada |
| **Versões fixadas** (`==`) | Evita que uma versão nova e não verificada de uma dependência entre na imagem sem revisão |
| **`GITHUB_TOKEN` (GitHub Secrets)** | O login no GHCR usa um token temporário gerado pelo GitHub a cada execução. Nenhuma senha ou token fica no código |
| **Permissões mínimas no workflow** | O pipeline só tem leitura do código; a permissão de publicar pacotes existe apenas no job que gera a imagem |
| **Imagens não publicadas em PR** | Código ainda não revisado nunca vira imagem no registro |
| **Container sem root** | A aplicação roda com o usuário `appuser`. Se for comprometida, o atacante não tem privilégios de administrador no container |
| **Imagem enxuta** (`python:3.13-slim` + `.dockerignore`) | Menos pacotes significa menos vulnerabilidades. Testes, `.git` e `.env` não entram na imagem |
| **`.env` fora do Git** | Configurações locais ficam no `.env`, que está no `.gitignore`. Só o modelo `.env.example`, sem dados sensíveis, é versionado |

## Evidências do pipeline

Histórico completo: [GitHub Actions](https://github.com/luizf25/taskflow-api/actions/workflows/ci-cd.yml)

| Execução | Evento | Resultado |
|---|---|---|
| [43938037348](https://github.com/luizf25/taskflow-api/actions/runs/43938037348) | PR #4, primeira execução do pipeline | ✅ Sucesso |
| [43938332132](https://github.com/luizf25/taskflow-api/actions/runs/43938332132) | Tag `v1.0.0`, publicou a imagem `1.0.0` | ✅ Sucesso |
| [43938416223](https://github.com/luizf25/taskflow-api/actions/runs/43938416223) | PR #5, nova regra com erro | ❌ Falha |
| [43938609282](https://github.com/luizf25/taskflow-api/actions/runs/43938609282) | PR #5, após a correção | ✅ Sucesso |

### Falha controlada: o que aconteceu e como foi corrigida

**Contexto.** No [PR #5](https://github.com/luizf25/taskflow-api/pull/5), o Luiz adicionou a regra "o título tem no máximo 100 caracteres", junto com dois testes de fronteira (100 caracteres deve ser aceito, 101 deve ser rejeitado). A falha foi provocada de forma controlada: a validação foi escrita com o operador de comparação errado.

```python
if len(titulo) >= LIMITE_TITULO:   # errado: rejeita também o título com 100 caracteres
```

**Como foi identificada.** O pipeline executou automaticamente no Pull Request e o job **Validar e testar** falhou no passo *Executar testes automatizados*. Como o pytest roda com `-v`, o log mostra exatamente qual teste quebrou:

```
tests/test_api.py::test_titulo_com_100_caracteres_e_aceito FAILED
>       assert resposta.status_code == 201
E       assert 400 == 201
FAILED tests/test_api.py::test_titulo_com_100_caracteres_e_aceito - assert 400 == 201
========================= 1 failed, 9 passed =========================
```

Como o job de testes falhou, o job **Gerar artefato** nem foi executado. Nenhuma imagem com o erro foi gerada, e o PR ficou marcado com ❌, sinalizando para a dupla que ele não podia ser mergeado.

**Correção.** O Lucas, revisor do PR, analisou o log, registrou a causa na revisão e enviou o commit `fix: aceitar título com exatamente 100 caracteres` na mesma branch, trocando `>=` por `>`:

```python
if len(titulo) > LIMITE_TITULO:    # correto: só rejeita acima de 100
```

O pipeline executou de novo, os 10 testes passaram e o PR foi aprovado e mergeado. Depois disso, a tag `v1.1.0` publicou a imagem com a regra nova.
