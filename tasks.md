# MVP Imobiliário - Fluxo de Tasks
# Última atualização: 2026-07-24

---

## RESUMO DO MVP FINAL

### O que é o sistema?
Uma plataforma SaaS imobiliária que fornece:
1. **ERP completo** para gerenciar imóveis, leads, clientes, equipes
2. **Vitrine automática** — site de imóveis pronto para cada corretor/imobiliária
3. **API pública** — para corretores que já possuem site próprio consumirem os dados

### Quem são os usuários?
- **Admin/Superadmin** — gerencia o sistema, tenants, configurações
- **Corretor/Imobiliária (Tenant)** — usa o ERP e a vitrine para vender imóveis
- **Cliente/Lead** — visita a vitrine, preenche formulário de contato
- **Site de terceiros** — consome a API pública para exibir imóveis

### Fluxo de valor principal
```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUXO DO SISTEMA                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CADASTRO                                                   │
│     Admin cria tenant (corretor/imobiliária)                    │
│     Tenant configura: logo, cores, domínio, dados pessoais     │
│                                                                 │
│  2. IMÓVEIS                                                    │
│     Tenant cadastra imóveis (título, preço, fotos, local)      │
│     Sistema processa fotos automaticamente                      │
│     Dados ficam disponíveis na API pública                      │
│                                                                 │
│  3. VITRINE (3 modelos de consumo)                             │
│     a) Slug: imobapp.com/v/corretor-abc                        │
│     b) Domínio próprio: www.corretor-abc.com.br                │
│     c) API: site existente consome dados via API               │
│                                                                 │
│  4. LEADS                                                      │
│     Visitante preenche formulário de contato                    │
│     Lead é criado automaticamente no ERP                        │
│     Status: novo → atendido → descartado                       │
│                                                                 │
│  5. GESTÃO (ERP)                                               │
│     Tenant gerencia leads, clientes, imóveis, equipe           │
│     Dashboard mostra métricas do negócio                        │
│                                                                 │
│  6. INTEGRAÇÕES (futuro)                                       │
│     OLX, DreamCasa, portais de imóveis                         │
│     Webhooks, automações                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Funcionalidades do MVP

#### Backend (API REST)
| Módulo | Funcionalidade | Status |
|--------|---------------|--------|
| Auth | Login, register, JWT, refresh token | ✅ |
| Users | CRUD completo (5 endpoints) | ✅ |
| Roles | CRUD completo (6 endpoints + permissions) | ✅ |
| Tenants | Criação automática no register | ✅ |
| Properties | CRUD completo (10 endpoints + media upload) | ✅ |
| PropertyOwners | CRUD completo (5 endpoints) | ✅ |
| Leads | List, get, update status (3 endpoints) | ✅ |
| Clients | CRUD completo | ✅ Etapa 1 |
| Dashboard | Métricas agregadas | ✅ Etapa 1 |
| API Keys | CRUD para autenticação de API | ❌ Etapa 2 |
| TenantDomain | Domínios personalizados | ❌ Etapa 2 |
| API Pública | Endpoints para vitrine/terceiros | ❌ Etapa 2 |
| Email | Notificações automáticas | ❌ Post-MVP |
| Workers | Processamento assíncrono | ❌ Post-MVP |

#### Frontend (React + Vite)
| Módulo | Funcionalidade | Status |
|--------|---------------|--------|
| Auth | Login, register, logout | ✅ |
| Landing Page | Página pública do sistema | ✅
| Vitrine pública | Grid + detalhe + contato | ❌ Etapa 3A |
| ERP interno | Imóveis, leads, clientes, etc | ❌ Etapa 3B |
| Dashboard | Métricas e gráficos | ❌ Etapa 4 |

---

## ✅ CONCLUÍDO (não mexer)

### Phase 0 - Infraestrutura
- Redis + MailHog + Worker service em docker-compose
- .env atualizado (REDIS, SMTP, OLX, DREAMCASA URLs)
- app/core/config.py com todas as settings
- requirements.txt: arq, redis, aiosmtplib, httpx
- app/core/queue.py: job enqueueing helper (enqueue_job)
- app/workers/arq_settings.py: configuração ARQ
- app/shared/enums/: LeadStatus, PortalType, SyncStatus

### Phase 1 - Leads Module
- leads/models.py: Lead (com raw_data JSONB)
- leads/schemas.py: LeadResponse, LeadUpdate
- leads/repository.py: CRUD completo
- leads/service.py: lógica de negócio
- leads/router.py: 3 endpoints (list, get, update status)
- Migration criada: 55547a1d8e82 (adiciona permissions + raw_data)
- Registrado em main.py + modules/models.py

### Módulos Backend (existentes e funcionais)
- Users: CRUD completo (5 endpoints)
- Roles: CRUD completo (6 endpoints com permissions)
- Properties: CRUD completo (10 endpoints + media upload)
- PropertyOwners: CRUD completo (5 endpoints)
- Auth: Login, register, JWT, permissions
- Clients: CRUD completo (5 endpoints)
- Dashboard: GET /dashboard/summary funcional

---

# PLANO DO MVP (5 etapas)

---

## ETAPA 1: ERP CRUD Completo (Backend) ✅ CONCLUÍDA
Objetivo: Backend do ERP funcional, todos os módulos CRUD operacionais

### 1.1 Clients Module
- Arquivos: schemas.py, repository.py, service.py, router.py
- Padrão: identical ao UserRepository/UserService
- Fields: name, email, phone, document, notes, tenant_id, user_id, created_from_lead_id
- Endpoints: list, get, create, update, delete (soft delete)
- Esforço: 1-2h

### 1.2 Migration Clients
- Comando: alembic revision --autogenerate -m "create clients table"
- Esforço: 5 min

### 1.3 Register Clients
- Adicionar import em app/modules/models.py
- Registrar router em app/main.py
- Esforço: 5 min

### 1.4 Dashboard Backend
- Criar app/modules/dashboard/router.py
- Endpoint: GET /dashboard/summary
- Retorna: total imóveis, total leads, total clientes, leads por status
- Registrar em main.py
- Esforço: 1h

### 1.5 Testar Todos Endpoints
- Verificar: users, roles, properties, propertyOwners, leads, clients
- Testar via Swagger (http://localhost:8000/docs)
- Esforço: 30 min

**Entregável:** Backend completo, todos os módulos CRUD funcionando.

---

## ETAPA 2: Vitrine & API Pública (Backend)
Objetivo: Backend para vitrine pública, domínios personalizados e API para terceiros

### 3 Modelos de Consumo da Vitrine

#### Modelo 1: Slug no domínio do sistema
```
https://imobapp.com/v/joao-silva
https://imobapp.com/v/imobiliaria-abc
```
- Vitrine roda no domínio do sistema
- Tenant identificado pelo slug na URL
- Mais simples, sem configuração de DNS
- Ideal para: corretores que não têm site próprio

#### Modelo 2: Domínio próprio do corretor
```
https://www.joaosilva.com.br
https://imobabc.com.br
```
- Corretor aponta o domínio para o sistema (A record)
- Tenant identificado pelo Host header
- Precisa: configuração DNS + Let's Encrypt SSL
- Ideal para: corretores com marca pessoal

#### Modelo 3: API consumption (site existente)
```
GET https://api.imobapp.com/v1/joao-silva/properties
Headers: X-API-Key: sk_live_abc123...
```
- Site existente do corretor consome a API pública
- Precisa: API key + CORS headers
- Não precisa de frontend da vitrine
- Ideal para: imobiliárias com site próprio

### 2.1 TenantDomain Model
- Criar app/modules/domains/models.py
- Fields:
  - id: UUID (PK)
  - tenant_id: UUID (FK → tenants.id)
  - domain: String (unique) — ex: "www.joaosilva.com.br"
  - is_primary: Boolean — domínio principal do tenant
  - verified: Boolean — True quando DNS resolve corretamente
  - ssl_active: Boolean — True quando SSL emitido
  - verification_token: String — token para verificar posse do domínio
  - created_at: DateTime
  - updated_at: DateTime
- Esforço: 30 min

### 2.2 Migration TenantDomains
- Comando: alembic revision --autogenerate -m "create tenant_domains table"
- Esforço: 5 min

### 2.3 API Keys CRUD
- Arquivos: schemas.py, repository.py, service.py, router.py
- Model: ApiKey (já existe em app/modules/apiKeys/models.py)
- Fields:
  - id: UUID (PK)
  - tenant_id: UUID (FK)
  - name: String — nome descritivo (ex: "Site Pessoal")
  - key_hash: String — hash da API key (nunca expor a key original)
  - key_prefix: String — primeiros 8 caracteres (para identificação)
  - expires_at: DateTime (nullable) — data de expiração
  - is_active: Boolean
  - created_at: DateTime
- Endpoints:
  - GET /api-keys — lista todas as keys do tenant
  - GET /api-keys/{id} — detalhe de uma key
  - POST /api-keys — cria nova key (retorna key completa UMA VEZ)
  - PATCH /api-keys/{id} — ativa/desativa
  - DELETE /api-keys/{id} — remove
- Esforço: 1-2h

### 2.4 API Pública Endpoints
- Criar app/api/public/router.py
- Endpoints:
  - GET /v1/{slug}/properties — lista imóveis (paginação, filtros)
  - GET /v1/{slug}/properties/{id} — detalhe do imóvel
  - GET /v1/{slug}/info — informações do tenant (logo, nome, contato)
  - Registrar em main.py (rotas públicas, sem auth JWT)
- Esforço: 1-2h

### 2.5 Contact Endpoint
- POST /v1/{slug}/contact — cria lead (sem auth)
- Recebe: name, email, phone, message, property_id (opcional)
- Cria lead com:
  - source = "vitrine" (Modelo 1 e 2) ou "api" (Modelo 3)
  - status = "novo"
  - raw_data = { ip, user_agent, referrer }
- Validação: email obrigatório, phone opcional, message opcional
- Esforço: 30 min

### 2.6 Domain Middleware
- Criar app/api/public/deps.py
- Função: get_tenant_from_request(request, slug=None)
- Lógica:
  1. Se slug fornecido → busca tenant por slug (Modelo 1)
  2. Se não → extrai Host header → busca em tenant_domains (Modelo 2)
  3. Se não encontrado → 404
- Retorna: tenant_id
- Esforço: 1h

### 2.7 DNS Verification Service
- Criar app/services/dns_verification.py
- Função: verify_domain(domain, expected_ip)
- Lógica:
  1. Faz query DNS A record do domínio
  2. Compara com IP do servidor
  3. Se corresponder → domain.verified = True
- Endpoint: POST /domains/{id}/verify — dispara verificação
- Background task: verifica periodicamente (via ARQ)
- Esforço: 1h

### 2.8 SSL Automation (Let's Encrypt)
- Criar app/services/ssl_service.py
- Função: request_ssl_certificate(domain)
- Lógica:
  1. Usa python-requests ou acme client
  2. Cria CSR (Certificate Signing Request)
  3. Envia para Let's Encrypt
  4. Completa challenge HTTP-01
  5. Salva certificado
- Integração com nginx/caddy para auto-reload
- Nota: Para MVP, pode ser manual ou adiado
- Esforço: 2-3h (ou adiar)

### 2.9 CORS for API Keys
- Configurar CORS no FastAPI
- Lógica:
  1. Request com X-API-Key header → permite CORS para qualquer origem
  2. Request normal (vitrine) → não precisa CORS (mesmo domínio)
- Headers:
  - Access-Control-Allow-Origin: *
  - Access-Control-Allow-Headers: X-API-Key
  - Access-Control-Allow-Methods: GET, POST
- Esforço: 30 min

**Entregável:** API pública funcional, 3 modelos de consumo funcionando.

---

## ETAPA 3: Frontend Completo (Frontend)
Objetivo: UI completa — vitrine pública + ERP interno

### 3A. Vitrine Pública (sem auth)

#### 3A.1 Rota /v/[slug]
- Grid de imóveis com cards
- Filtros: preço (min/max), tipo, bairro, quartos
- Paginação infinita ou botão "carregar mais"
- Loading skeleton
- Esforço: 2-3h

#### 3A.2 Rota /v/[slug]/[id]
- Detalhe do imóvel
- Galeria de fotos (lightbox)
- Informações: preço, área, quartos, banheiros, vagas
- Mapa com localização (Google Maps ou OpenStreetMap)
- Botão "Tenho interesse" → abre modal de contato
- Esforço: 2-3h

#### 3A.3 Formulário de Contato
- Modal ou inline form
- Campos: nome, email, telefone, mensagem
- Opcional: selecionar imóvel de interesse
- Chama POST /v1/{slug}/contact
- Mensagem de sucesso/erro
- Validação client-side
- Esforço: 1h

#### 3A.4 Layout Personalizado
- Header: logo do tenant, nome, navegação
- Cores: tema personalizado via CSS variables
- Footer: dados de contato, links
- Botão WhatsApp: link direto para conversa
- Responsivo: mobile-first
- Esforço: 1-2h

#### 3A.5 SEO
- Meta tags dinâmicas: title, description, OG tags
- Usar react-helmet ou similar
- Schema.org markup (RealEstateListing)
- Sitemap dinâmico
- Esforço: 1h

### 3B. ERP Interno (com auth)

#### 3B.1 Layout Interno
- Sidebar: menu colapsável com ícones
- Header: info do user, notificações, logout
- Breadcrumb
- Responsivo: sidebar vira drawer no mobile
- Esforço: 1-2h

#### 3B.2 Página Imóveis
- Listagem: grid ou tabela, busca, filtros
- Criar imóvel: formulário multi-step
- Editar imóvel: mesmo formulário com dados preenchidos
- Deletar: confirmação
- Upload de fotos: drag & drop, preview, ordenação
- Status: rascunho, publicado, vendido
- Esforço: 2-3h

#### 3B.3 Página Leads
- Listagem: tabela, filtros (status, data, origem)
- Status visual: badge colorido (novo=azul, atendido=verde, descartado=cinza)
- Detalhe: informações do lead, imóvel de interesse, histórico
- Ações: marcar como atendido, descartar
- Esforço: 1-2h

#### 3B.4 Página Clientes
- Listagem: tabela, busca
- Criar cliente: formulário
- Editar cliente: formulário com dados preenchidos
- Deletar: confirmação
- Esforço: 1-2h

#### 3B.5 Página Usuários
- Listagem: tabela
- Criar usuário: formulário com seleção de roles
- Editar usuário: formulário
- Desativar: soft delete
- Esforço: 1h

#### 3B.6 Página Roles
- Listagem: tabela com permissions
- Criar role: formulário com checkboxes de permissions
- Editar role: formulário
- Deletar: confirmação
- Esforço: 1h

#### 3B.7 Página PropertyOwners
- Listagem: tabela, busca
- Criar proprietário: formulário
- Editar proprietário: formulário
- Deletar: confirmação
- Esforço: 1h

#### 3B.8 Página Domínios (Modelo 2)
- Listagem: domínios configurados
- Adicionar domínio: formulário
- Verificar DNS: botão "Verificar"
- Status: pendente, verificado, SSL ativo
- Instruções DNS: exibe como configurar o A record
- Esforço: 1-2h

#### 3B.9 Página API Keys (Modelo 3)
- Listagem: keys ativas
- Criar key: botão (mostra key completa UMA VEZ)
- Revoke: botão de confirmação
- Documentação: exemplos de uso da API
- Esforço: 1h

**Entregável:** Frontend completo, vitrine pública + ERP interno funcionais.

---

## ETAPA 4: Dashboard (Backend + Frontend)
Objetivo: Métricas e visão geral do negócio

### 4.1 Dashboard Backend
- Criar app/modules/dashboard/router.py
- Endpoints:
  - GET /dashboard/summary — métricas gerais
  - GET /dashboard/leads-by-status — leads agrupados por status
  - GET /dashboard/properties-by-type — imóveis por tipo
  - GET /dashboard/recent-activity — últimas ações
- Esforço: 1h

### 4.2 Dashboard Frontend
- pages/Dashboard.jsx
- Cards com KPIs:
  - Total de imóveis
  - Total de leads
  - Total de clientes
  - Leads novos (últimos 7 dias)
- Gráficos:
  - Leads por status (pie chart)
  - Imóveis por tipo (bar chart)
  - Leads ao longo do tempo (line chart)
- Atividade recente: últimas ações
- Esforço: 2-3h

**Entregável:** Dashboard com métricas de imóveis, leads, clientes.

---

## ETAPA 5: Finalizações do MVP
Objetivo: Polish, testes, deploy

### 5.1 Testes Manuais
- Testar todos os fluxos:
  - CRUD completo (users, roles, properties, clients, leads)
  - Vitrine pública (Modelo 1)
  - Domínio próprio (Modelo 2)
  - API consumption (Modelo 3)
  - Formulário de contato
- Esforço: 2h

### 5.2 Bug Fixes
- Corrigir bugs encontrados nos testes
- Esforço: 1-2h

### 5.3 Deploy
- Configurar produção:
  - VPS (DigitalOcean, Hetzner, etc)
  - Docker + Docker Compose
  - Nginx/Caddy como reverse proxy
  - Let's Encrypt SSL
  - DNS para domínio principal
  - Backup automático
- Esforço: 2-3h

### 5.4 Documentação
- README com instruções de setup
- API docs (Swagger automático)
- Guia do usuário (básico)
- Esforço: 1h

**Entregável:** MVP pronto para uso.

---

## ORDEM DE EXECUÇÃO

```
Etapa 1 (Backend ERP) → Etapa 2 (API Pública) → Etapa 3 (Frontend) → Etapa 4 (Dashboard) → Etapa 5 (Finalizações)
```

---

# OBSERVAÇÕES

1. **Leads só entram pela vitrine** — não há criação manual no ERP
2. **Email service adiado** — sem OLX, leads aparecem no ERP, notificação é nice-to-have
3. **API pública usa API key** — não JWT, para consumo de terceiros
4. **Vitrine não precisa de CORS** — roda no mesmo domínio
5. **API consumption precisa de CORS** — requests cross-origin
6. **SSL para domínios próprios** — pode ser manual no MVP, automático depois
7. **Testar cada módulo ao implementar** — não esperar a Etapa 5

---

## REFERÊNCIAS

- Backend: /backend/
- Frontend: /frontend/
- API Docs: http://localhost:8000/docs (quando backend rodando)
- Env: /backend/.env
- Docker: docker-compose.yml
- Tasks: /tasks.md (este arquivo)
