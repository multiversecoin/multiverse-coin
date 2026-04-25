# Agente 01 — Relatório Técnico Automatizado

Sistema corporativo para geração automatizada de relatórios técnicos de operações subaquáticas (inspeção, limpeza e reparo em cascos de navios, hélices, lemes, estruturas portuárias e plataformas).

## Arquitetura

```
┌─────────────┐     ┌──────────┐     ┌─────────────┐
│   FastAPI    │────▶│ PostgreSQL│     │    MinIO     │
│   (API)      │     │  (Dados)  │     │  (Storage)   │
└──────┬───────┘     └──────────┘     └──────┬───────┘
       │                                      │
       ▼                                      │
┌──────────────┐     ┌──────────┐             │
│    Celery     │────▶│  Redis    │             │
│  (Worker)     │     │ (Broker)  │             │
└──────┬────────┘     └──────────┘             │
       │                                       │
       ▼                                       │
┌──────────────┐                               │
│ python-docx  │──▶ DOCX ──▶ LibreOffice ──▶ PDF
│  + LLM API   │                               │
└──────────────┘                               │
       │                                       │
       └───── SHA256 + Assinatura Digital ─────┘
```

### Componentes

| Serviço | Tecnologia | Porta |
|---------|-----------|-------|
| API | FastAPI + Uvicorn | 8000 |
| Banco de Dados | PostgreSQL 16 | 5432 |
| Broker/Cache | Redis 7 | 6379 |
| Storage | MinIO | 9000 (API) / 9001 (Console) |
| Worker | Celery | - |

### Segurança

- **JWT Auth** com access + refresh tokens
- **RBAC** com 4 perfis: ADMIN, SUPERVISOR, OPERADOR, COMERCIAL
- **SHA-256** em todas as evidências e relatórios
- **Assinatura digital RSA** nos relatórios aprovados
- **Audit logs** imutáveis para todas as ações
- **LGPD compliance** com controle de retenção e expurgo
- **Zero Trust**: nenhuma rota pública (exceto `/health`)

## Início Rápido

### Pré-requisitos

- Docker e Docker Compose instalados
- (Opcional) Chave de API OpenAI ou Claude para geração de texto via LLM

### 1. Clonar e configurar

```bash
cd agente01
cp .env.example .env
# Edite o .env conforme necessário (LLM keys, JWT secret, etc.)
```

### 2. Subir a stack

```bash
docker-compose up --build -d
```

Isso inicia: PostgreSQL, Redis, MinIO, API FastAPI e Worker Celery.

### 3. Verificar saúde

```bash
curl http://localhost:8000/health
# {"status":"ok","env":"DEV"}
```

### 4. Acessar documentação da API

Abra no navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Console do MinIO

Abra: [http://localhost:9001](http://localhost:9001)
- Usuário: `minioadmin`
- Senha: `minioadmin`

## Usuário Admin Padrão

Ao iniciar, o sistema cria automaticamente um usuário administrador:

- **Email**: `admin@agente01.local`
- **Senha**: `admin123`
- **Role**: ADMIN

> ⚠️ **TROQUE A SENHA EM PRODUÇÃO!**

## Fluxo de Uso (Exemplos com curl)

### 1. Login

```bash
# Login como admin
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@agente01.local","password":"admin123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo $TOKEN
```

### 2. Criar Usuários

```bash
# Criar operador
curl -X POST http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "operador@empresa.com",
    "password": "operador123",
    "full_name": "João Silva",
    "role": "OPERADOR"
  }'

# Criar supervisor
curl -X POST http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "supervisor@empresa.com",
    "password": "supervisor123",
    "full_name": "Maria Santos",
    "role": "SUPERVISOR"
  }'
```

### 3. Criar Operação

```bash
curl -X POST http://localhost:8000/api/v1/operations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "Petrobras S.A.",
    "navio": "MV Atlantic Star",
    "imo": "9876543",
    "local": "Terminal Portuário de Santos",
    "porto": "Santos - SP",
    "data_operacao": "2025-01-15",
    "tipo_servico": "INSPECAO",
    "areas_inspecionadas": ["CASCO", "HELICE", "LEME"],
    "descricao_servico": "Inspeção subaquática completa do casco, hélice e leme para avaliação de bioincrustação e integridade estrutural.",
    "equipe": [
      {"nome": "Carlos Mergulhador", "funcao": "Mergulhador Líder", "certificacao": "IMCA D"},
      {"nome": "Ana Técnica", "funcao": "Operadora ROV", "certificacao": "ROV Pilot Level 2"}
    ],
    "equipamentos": ["ROV Observation Class", "Câmera HD Subaquática", "Medidor de Espessura"],
    "condicoes": {
      "visibilidade": "3-5 metros",
      "correnteza": "0.5 nós",
      "mare": "Preamar às 14:30",
      "observacoes": "Condições favoráveis para operação"
    },
    "observacoes_campo": "Bioincrustação moderada observada na região do bulbo de proa. Hélice com desgaste leve nas pontas das pás.",
    "recomendacoes_iniciais": "Recomenda-se limpeza do casco na próxima docagem. Monitorar desgaste da hélice."
  }'
```

### 4. Upload de Evidências

```bash
# Obtenha o ID da operação criada (OPERATION_ID)
OPERATION_ID="<uuid-da-operacao>"

# Upload de foto com tags
curl -X POST "http://localhost:8000/api/v1/operations/$OPERATION_ID/evidences/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@foto_casco_antes.jpg" \
  -F "tags=CASCO,ANTES" \
  -F "observacao_operador=Bioincrustação moderada na região do bulbo de proa"

curl -X POST "http://localhost:8000/api/v1/operations/$OPERATION_ID/evidences/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@foto_casco_depois.jpg" \
  -F "tags=CASCO,DEPOIS" \
  -F "observacao_operador=Área limpa após hidrojateamento"
```

### 5. Gerar Relatório

```bash
# Dispara geração assíncrona (Celery)
curl -X POST "http://localhost:8000/api/v1/operations/$OPERATION_ID/report/generate" \
  -H "Authorization: Bearer $TOKEN"

# Aguarde alguns segundos...

# Download DOCX
curl -o relatorio.docx \
  "http://localhost:8000/api/v1/operations/$OPERATION_ID/report/download?format=docx" \
  -H "Authorization: Bearer $TOKEN"

# Download PDF
curl -o relatorio.pdf \
  "http://localhost:8000/api/v1/operations/$OPERATION_ID/report/download?format=pdf" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Aprovar Relatório (Supervisor)

```bash
# Login como supervisor
SUP_TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"supervisor@empresa.com","password":"supervisor123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Aprovar e assinar
curl -X POST "http://localhost:8000/api/v1/operations/$OPERATION_ID/report/approve" \
  -H "Authorization: Bearer $SUP_TOKEN"
```

### 7. Verificar Assinatura

```bash
curl "http://localhost:8000/api/v1/operations/$OPERATION_ID/report/verify" \
  -H "Authorization: Bearer $TOKEN"
```

### 8. Ver Audit Logs (Admin)

```bash
curl "http://localhost:8000/api/v1/audit/logs?limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

### 9. Validar RBAC

```bash
# Operador NÃO acessa audit logs
OP_TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"operador@empresa.com","password":"operador123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl "http://localhost:8000/api/v1/audit/logs" \
  -H "Authorization: Bearer $OP_TOKEN"
# Deve retornar 403 Forbidden
```

## Endpoints da API

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh token |
| POST | `/api/v1/auth/logout` | Logout (registra log) |

### Users (Admin)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/users` | Criar usuário |
| GET | `/api/v1/users` | Listar usuários |
| PATCH | `/api/v1/users/{id}` | Atualizar usuário |
| DELETE | `/api/v1/users/{id}` | Desativar usuário |

### Operations
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/operations` | Criar operação |
| GET | `/api/v1/operations` | Listar operações |
| GET | `/api/v1/operations/{id}` | Detalhar operação |
| PATCH | `/api/v1/operations/{id}` | Atualizar operação |

### Evidences
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/operations/{id}/evidences/upload` | Upload evidência |
| GET | `/api/v1/operations/{id}/evidences` | Listar evidências |
| GET | `/api/v1/evidences/{id}/download` | Download evidência |

### Reports
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/operations/{id}/report/generate` | Gerar relatório |
| POST | `/api/v1/operations/{id}/report/approve` | Aprovar (Supervisor) |
| GET | `/api/v1/operations/{id}/report/download` | Download DOCX/PDF |
| GET | `/api/v1/operations/{id}/report/verify` | Verificar assinatura |

### Audit (Admin)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/audit/logs` | Listar audit logs |

### Compliance (LGPD)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/compliance/incident` | Registrar incidente |
| POST | `/api/v1/compliance/purge_operation/{id}` | Expurgar operação |

## Perfis RBAC

| Perfil | Permissões |
|--------|-----------|
| **ADMIN** | Acesso total: gerenciar usuários, audit logs, expurgo |
| **SUPERVISOR** | Criar operações, aprovar/assinar relatórios |
| **OPERADOR** | Criar operações, upload evidências, gerar relatórios |
| **COMERCIAL** | Leitura de operações e download de relatórios finalizados |

## Estrutura do Relatório DOCX/PDF

1. Capa (Cliente, Navio, IMO, Data, Local, Tipo)
2. Sumário
3. Introdução
4. Objetivo do Serviço
5. Escopo da Operação
6. Metodologia Executada
7. Equipe Técnica Envolvida
8. Equipamentos Utilizados
9. Condições Operacionais
10. Evidências Fotográficas (por área + antes/depois)
11. Diagnóstico / Achados Técnicos
12. Serviços Executados
13. Conclusão
14. Recomendações Técnicas
15. Anexos (tabela de integridade SHA-256)

## Configuração do LLM

O sistema suporta 3 provedores de LLM (configurável via `.env`):

| Provider | Variável | Nota |
|----------|----------|------|
| OpenAI | `OPENAI_API_KEY` | GPT-4o recomendado |
| Claude | `CLAUDE_API_KEY` | Claude Sonnet recomendado |
| Local | `LOCAL_LLM_URL` | Qualquer API compatível |
| Fallback | (padrão) | Texto template sem LLM |

Sem chave configurada, o sistema usa textos genéricos (fallback).

## Assinatura Digital

### Gerar chave RSA para assinatura:

```bash
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

Configure no `.env`:
```
SIGNING_PRIVATE_KEY_PATH=/path/to/private_key.pem
```

Ou via variável de ambiente (PEM inline):
```
SIGNING_PRIVATE_KEY_PEM="-----BEGIN PRIVATE KEY-----\n..."
```

> Em produção, use um Secrets Manager (AWS, Vault, etc.)

## Testes

```bash
# Instalar dependências de teste
pip install -e ".[dev]" aiosqlite

# Rodar testes
cd agente01
pytest tests/ -v
```

## Migrações

```bash
# Dentro do container da API
docker-compose exec api alembic upgrade head

# Gerar nova migration
docker-compose exec api alembic revision --autogenerate -m "descricao"
```

## Decisões Técnicas

1. **PostgreSQL** escolhido por suporte nativo a UUID, JSONB e ARRAY.
2. **MinIO** como S3-compatible para storage privado — fácil migração para AWS S3.
3. **Celery + Redis** para processamento assíncrono — relatórios pesados não bloqueiam a API.
4. **LibreOffice headless** para conversão DOCX→PDF — gratuito e confiável.
5. **python-docx** para geração DOCX — biblioteca madura e estável.
6. **SHA-256** para integridade de evidências — padrão industrial.
7. **RSA/PSS** para assinatura digital — seguro e amplamente aceito.
8. **Fallback LLM** garante que o sistema funciona sem chave de API.

## Evolução Futura (Preparado)

- [ ] Visão computacional para classificação automática de evidências
- [ ] RAG (Retrieval Augmented Generation) para consulta inteligente
- [ ] MFA (Multi-Factor Authentication)
- [ ] Anonimização de dados pessoais (LGPD)
- [ ] Integração com sistemas ERP/SAP
- [ ] Dashboard web para visualização de operações
- [ ] Notificações por email/WhatsApp
- [ ] Versionamento completo de relatórios

## Licença

Uso interno — propriedade da empresa.
