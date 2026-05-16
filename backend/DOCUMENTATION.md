# Documentação de Autenticação e Cadastro

Este documento explica o sistema de autenticação multi-tenant implementado.

## Visão Geral

O sistema implementa autenticação JWT com suporte a multi-tenancy, onde cada tenant (imobiliária/corretor) possui usuários próprios.

## Estrutura de Arquivos

### Core

| Arquivo | Descrição |
|---------|------------|
| `app/core/config.py` | Configurações do app (SECRET_KEY, ALGORITHM, etc.) |
| `app/core/security.py` | Funções de hash de senha e criação de JWT |
| `app/core/dependencies.py` | Injeção de dependências (get_db) |
| `app/core/database.py` | Configuração do SQLAlchemy |

### Módulos

| Módulo | Descrição |
|--------|------------|
| `app/modules/auth/` | Login e registro (tenant + admin) |
| `app/modules/users/` | Gerenciamento de usuários do tenant |
| `app/modules/tenants/` | Modelo e repositório de tenants |

---

## Fluxo de Uso

### 1. Registro de Novo Tenant + Admin

**Endpoint:** `POST /auth/register`

Cria um novo tenant (imobiliária) e um usuário administrador para ele.

**Requisição:**
```json
{
  "email": "admin@imobiliaria.com",
  "password": "senha123",
  "name": "João Silva",
  "phone": "(11) 99999-9999",
  "tenant_name": "Imobiliária ABC",
  "tenant_slug": "imobiliaria-abc"  // opcional
}
```

**Resposta:**
```json
{
  "user": {
    "id": "uuid",
    "email": "admin@imobiliaria.com",
    "name": "João Silva",
    "phone": "(11) 99999-9999",
    "is_active": true
  },
  "tenant": {
    "id": "uuid",
    "name": "Imobiliária ABC",
    "slug": "imobiliaria-abc",
    "plan": "free",
    "status": "active"
  },
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Comportamento:**
- Se `tenant_slug` não for fornecido, é gerado automaticamente a partir do `tenant_name`
- O tenant é criado com `plan: "free"` e `status: "active"`
- Retorna um JWT token para uso imediato

---

### 2. Login

**Endpoint:** `POST /auth/login`

Autentica usuário e retorna JWT token.

**Requisição:**
```json
{
  "email": "admin@imobiliaria.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Payload do Token:**
```json
{
  "sub": "user_id",
  "tenant_id": "tenant_id",
  "exp": 1234567890
}
```

---

### 3. Criar Usuário no Tenant

**Endpoint:** `POST /users/`

Cria um novo usuário vinculado ao tenant do usuário autenticado.

**Cabeçalho:**
```
Authorization: Bearer <token_jwt>
```

**Requisição:**
```json
{
  "email": "corretor@imobiliaria.com",
  "password": "senha123",
  "name": "Maria Santos",
  "phone": "(11) 88888-8888"
}
```

**Resposta:**
```json
{
  "id": "uuid",
  "email": "corretor@imobiliaria.com",
  "name": "Maria Santos",
  "phone": "(11) 88888-8888",
  "is_active": true,
  "tenant_id": "uuid_do_tenant"
}
```

**Requer autenticação** - o usuário deve estar logado.

---

## Detalhes de Implementação

### Configurações (`app/core/config.py`)

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str          # Chave para assinar JWT
    ALGORITHM: str = "HS256" # Algoritmo do JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: str
```

### Segurança (`app/core/security.py`)

- **Hash de senha:** Argon2 via passlib
- **JWT:** PyJWT com HS256

```python
get_password_hash(password: str) -> str
verify_password(plain_password: str, hashed_password: str) -> bool
create_access_token(data: dict, expires_delta: timedelta) -> str
```

### Autenticação (`app/modules/auth/dependencies.py`)

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_token_data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decodifica o JWT, busca o usuário no banco e retorna
    return User
```

### Repositórios

| Repositório | Métodos |
|-------------|---------|
| `TenantRepository` | `get_by_slug(slug)`, `create(data)` |
| `UserRepository` | `get_by_email(email)`, `get_by_id(id)`, `create(data)` |

---

## Modelos de Dados

### Tenant
| Campo | Tipo | Descrição |
|-------|------|------------|
| id | UUID | PK |
| name | str | Nome da imobiliária |
| slug | str | Identificador único (URL) |
| plan | str | Plano (free, basic, premium) |
| status | str | Status (active, inactive) |

### User
| Campo | Tipo | Descrição |
|-------|------|------------|
| id | UUID | PK |
| tenant_id | UUID | FK para Tenant |
| name | str | Nome do usuário |
| email | str | Email único |
| password_hash | str | Hash da senha |
| phone | str | Telefone |
| is_active | bool | Se está ativo |

---

## Rotas Resumo

| Método | Endpoint | Descrição | Autenticado |
|--------|----------|------------|-------------|
| POST | /auth/register | Cria tenant + admin | Não |
| POST | /auth/login | Login | Não |
| POST | /users/ | Cria usuário no tenant | Sim |

---

## Fluxo Multi-Tenant

1. **Novo tenant** → registra-se via `/auth/register` → cria tenant + admin
2. **Usuário do tenant** → faz login via `/auth/login` → recebe token com `tenant_id`
3. **Criar membros** → admin logado chama `/users/` → usuário criado com `tenant_id` do admin
4. **Todas as queries futuras** devem filtrar por `tenant_id` do usuário logado

Exemplo de query scoped por tenant:
```python
def get_properties(db: Session, current_user: User):
    return db.query(Property).filter(Property.tenant_id == current_user.tenant_id).all()
```

---

## Testando a API

Acesse a documentação interativa em: `http://localhost:8000/docs`

1. **Registrar tenant + admin:**
   - POST `/auth/register` com os dados do formulário

2. **Fazer login:**
   - POST `/auth/login` para obter o token

3. **Criar usuário:**
   - No endpoint `/users/`, clique em "Authorize"
   - Cole o token recebido do login
   - Faça a requisição para criar um novo usuário