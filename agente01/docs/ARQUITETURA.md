# Arquitetura do Sistema — Agente 01

## Visão Geral

O Agente 01 é um sistema de geração automatizada de relatórios técnicos para operações subaquáticas. A arquitetura segue princípios de **Zero Trust**, **Least Privilege** e **Auditabilidade Total**.

## Diagrama de Fluxo

```
Usuário (API Client)
       │
       ▼
┌──────────────────┐
│   FastAPI (API)   │ ← JWT Auth + RBAC
│   Port 8000       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│Postgres│ │ MinIO  │ ← Storage privado (evidências + relatórios)
│  5432  │ │  9000  │
└────────┘ └────────┘
    │
    │  Celery Task
    ▼
┌─────────────────┐
│  Celery Worker   │
│                  │
│  1. Busca dados  │
│  2. Busca fotos  │
│  3. Gera textos  │ ← LLM (OpenAI/Claude/Local/Fallback)
│  4. Gera DOCX    │ ← python-docx
│  5. Converte PDF │ ← LibreOffice headless
│  6. SHA256       │
│  7. Assina       │ ← RSA/PSS
│  8. Salva        │
│  9. Audit log    │
└─────────────────┘
```

## Pipeline de Geração do Relatório

1. **Validação** — Verificar permissões RBAC do usuário
2. **Coleta** — Buscar dados da operação e evidências do banco
3. **Classificação** — Organizar evidências por área (CASCO, HELICE, etc.) e fase (ANTES/DEPOIS)
4. **Geração de Texto** — Usar LLM para gerar seções: introdução, metodologia, achados, conclusão, recomendações
5. **Montagem DOCX** — Usar python-docx com template padronizado
6. **Conversão PDF** — LibreOffice headless
7. **Integridade** — Calcular SHA-256 dos arquivos finais
8. **Armazenamento** — Upload para MinIO (bucket privado)
9. **Assinatura** — Assinatura digital RSA (se chave configurada)
10. **Registro** — Criar audit log no banco

## Pipeline de Aprovação

1. **Validação** — Verificar role SUPERVISOR ou ADMIN
2. **Verificação** — Recalcular hash e comparar com armazenado
3. **Assinatura** — Gerar assinatura digital com chave privada
4. **Registro** — Atualizar status, salvar assinatura, audit log

## Modelo de Dados

```
users ─────────────────────────────────────────┐
  id (UUID PK)                                  │
  email (unique)                                │
  password_hash (bcrypt)                        │
  role (ADMIN|SUPERVISOR|OPERADOR|COMERCIAL)    │
  is_active                                     │
                                                │
operations ─────────────────────────────────────┤
  id (UUID PK)                                  │
  cliente, navio, imo, local, porto             │
  tipo_servico, areas_inspecionadas             │
  equipe (JSONB), equipamentos (ARRAY)          │
  condicoes (JSONB)                             │
  created_by → users.id                         │
                                                │
evidences ──────────────────────────────────────┤
  id (UUID PK)                                  │
  operation_id → operations.id                  │
  storage_key, filename_original                │
  file_size, sha256, content_type               │
  tags (ARRAY), observacao_operador             │
  uploaded_by → users.id                        │
  previous_version_id → evidences.id (nullable) │
                                                │
reports ────────────────────────────────────────┤
  id (UUID PK)                                  │
  operation_id → operations.id                  │
  status (pending|generating|ready|approved|failed)
  docx_storage_key, pdf_storage_key             │
  docx_sha256, pdf_sha256                       │
  signature (base64), signed_by, signed_at      │
  created_by → users.id                         │
                                                │
audit_logs ─────────────────────────────────────┤
  id (UUID PK)                                  │
  user_id, action, target_type, target_id       │
  ip_address, user_agent, details_json          │
  timestamp                                     │
                                                │
compliance_events ──────────────────────────────┘
  id (UUID PK)
  type (INCIDENT|PURGE)
  description, created_by, created_at
```

## Segurança

### RBAC Matrix

| Ação | ADMIN | SUPERVISOR | OPERADOR | COMERCIAL |
|------|-------|-----------|----------|-----------|
| Criar operação | ✓ | ✓ | ✓ | ✗ |
| Upload evidência | ✓ | ✓ | ✓ | ✗ |
| Gerar relatório | ✓ | ✓ | ✓ | ✗ |
| Aprovar relatório | ✓ | ✓ | ✗ | ✗ |
| Download relatório | ✓ | ✓ | ✓ | ✓ |
| Audit logs | ✓ | ✗ | ✗ | ✗ |
| Gerenciar usuários | ✓ | ✗ | ✗ | ✗ |
| Expurgar dados | ✓ | ✗ | ✗ | ✗ |

### Integridade

- Toda evidência tem SHA-256 calculado no upload
- Duplicatas (mesmo SHA-256 na mesma operação) são rejeitadas
- Relatórios finais têm hash e assinatura digital
- Endpoint `/report/verify` para validação independente

### LGPD

- Minimização de dados: apenas campos necessários
- Controle de acesso: segregação por role
- Rastreabilidade: audit logs completos
- Retenção: configurável (padrão 5 anos)
- Expurgo: endpoint com log obrigatório
- Registro de incidentes: endpoint dedicado
