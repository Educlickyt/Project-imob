# ImobConnect — SaaS Imobiliário (ERP + Vitrine + API)

Uma plataforma SaaS para o mercado imobiliário que reúne **ERP completo**, **vitrine automática** e **API pública** em um único produto. Projetada para corretoras e corretores autônomos que querem ferramentas de nível enterprise a um custo acessível.

> Status: **MVP em andamento** — backend funcional (CRUD completo), frontend do ERP em desenvolvimento.

---

## ✨ O que o produto faz

1. **ERP completo** — gerencie imóveis, leads, clientes, proprietários e equipe em um só lugar, com painel de métricas (dashboard).
2. **Vitrine automática** — cada corretor/imobiliária ganha um site de imóveis pronto, em 3 modelos:
   - **Slug** no domínio da plataforma (`imobapp.com/v/meu-nome`)
   - **Domínio próprio** do corretor (`www.minhamarca.com.br`)
   - **API pública** — sites existentes do corretor consomem os dados via API com chave
3. **API pública** — para corretores que já possuem site consumirem os imóveis.

### Quem são os usuários
- **Admin/Superadmin** — gerencia o sistema, tenants e configurações
- **Corretor/Imobiliária (Tenant)** — opera o ERP e a vitrine
- **Cliente/Lead** — visita a vitrine e envia formulário de contato
- **Integradores** — consomem a API pública

---

## 🛠️ Stack

| Camada | Tecnologia |
|--------|------------|
| Backend | Python, FastAPI, SQLAlchemy, Alembic, Pydantic v2 |
| Autenticação | JWT (access + refresh), RBAC com permissões, Argon2/passlib |
| Frontend | React 19, Vite 8, React Router 7, CSS Modules |
| Banco de dados | PostgreSQL 16 |
| Cache / filas | Redis + ARQ (workers assíncronos) |
| Armazenamento | MinIO (S3-compatível) para fotos de imóveis |
| Email | MailHog (dev), aiosmtplib |
| Infra | Docker Compose |

---

## 🏗️ Arquitetura

**Monólito modular** no backend — cada domínio é um módulo com `router.py`, `service.py`, `repository.py`, `models.py` e `schemas.py`:

```
backend/app/
├── core/           # configuração, banco, segurança, deps, storage
├── modules/        # domínios (auth, users, roles, properties, leads, clients ...)
├── api/public/     # API pública da vitrine (/v1/{slug}/...)
├── shared/         # enums, utilitários
├── workers/        # processamento assíncrono (ARQ)
└── main.py         # app FastAPI

frontend/src/
├── pages/          # rotas do ERP (Dashboard, Properties, Leads, Clients ...)
├── components/     # componentes reutilizáveis
└── services/       # clientes HTTP (API interna + API pública)
```

### Módulos do backend (MVP)
- **Auth** — login, registro, JWT, refresh token, RBAC
- **Users / Roles** — CRUD completo com permissões
- **Tenants** — criação automática no registro (multi-tenant com isolamento de dados)
- **Properties** — CRUD com upload e processamento automático de fotos
- **PropertyOwners** — proprietários de imóveis
- **Leads** — captura e gestão de status (novo → atendido → descartado)
- **Clients** — clientes do ERP
- **Dashboard** — métricas agregadas do negócio
- **API Keys / Domains** — suporte à vitrine por domínio próprio e API
- **Showcase Configs** — personalização (logo, cores, domínio) por tenant

---

## 🚀 Como rodar

Pré-requisitos: **Docker** e **Docker Compose**.

```bash
# sobe todos os serviços (database, backend, frontend, minio, redis, worker)
docker compose up -d

# apenas backend + banco
docker compose up -d backend database
```

| Serviço | URL |
|---------|-----|
| Frontend (React) | http://localhost:5173 |
| Backend (FastAPI) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| MinIO Console | http://localhost:9101 |
| MailHog UI | http://localhost:8025 |

### Variáveis de ambiente
Copie `backend/.env.example` para `backend/.env` e preencha as credenciais locais (banco, S3/MinIO, Redis, SMTP, integrações).

> Padrões de desenvolvimento: `postgres/postgres` · MinIO: `minioadmin/minioadmin` (ver `docker-compose.yml`).

---

## 🧪 Testes

```bash
cd backend
pytest          # testes unit, integração e e2e
```

---

## 🗺️ Roadmap

**Feito (MVP):**
- [x] Autenticação JWT + refresh tokens + RBAC
- [x] CRUD de usuários, roles, permissões
- [x] Multi-tenant com criação automática
- [x] CRUD de imóveis com upload/processamento de fotos
- [x] Gestão de leads, clientes, proprietários
- [x] Dashboard com métricas
- [x] Landing page + vitrine pública (grid/detalhe/contato)
- [x] API pública (vitrine por slug, info e contato)

**Próximos passos:**
- [ ] ERP completo no frontend (imóveis, leads, clientes, equipe)
- [ ] Domínios próprios + DNS/SSL automático
- [ ] Notificações por email
- [ ] Integração com portais (OLX, DreamCasa)
- [ ] Workers assíncronos em produção
- [ ] Documentação completa da API pública

---

## 🗂️ Estrutura do repositório

```
├── backend/          # API FastAPI (monólito modular)
├── frontend/         # Aplicação React + Vite
└── docker-compose.yml# Orquestração dos serviços
```

---

## 👤 Autor

Projeto desenvolvido como portfólio. Contato e mais informações disponíveis no [perfil do GitHub](https://github.com/Educlickyt).
