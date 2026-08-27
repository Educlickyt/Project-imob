# SaaS para Gestão Imobiliária

Plataforma SaaS desenvolvida para centralizar a gestão operacional de corretores e imobiliárias. O MVP tem como foco a gestão de imóveis, clientes, proprietários, leads, usuários e a disponibilização de uma vitrine pública para divulgação dos imóveis cadastrados.

O projeto está sendo desenvolvido como um produto SaaS e como projeto de portfólio, com foco na aplicação de conceitos de desenvolvimento full stack, arquitetura de software, autenticação, autorização e arquitetura multi-tenant.

> **Status:** Em desenvolvimento — backend do ERP necessitando pequenas correções e frontend administrativo em desenvolvimento.

---

## Visão Geral

A plataforma permite que corretores e imobiliárias concentrem informações e processos relacionados à sua operação em um único sistema.

O MVP é dividido em duas áreas principais:

### Gestão administrativa

Ambiente destinado à administração da operação imobiliária, incluindo:

* Imóveis;
* Proprietários;
* Leads;
* Clientes;
* Usuários e equipe;
* Funções e permissões;
* Métricas e indicadores.

### Vitrine pública

Cada tenant pode disponibilizar seus imóveis por meio de uma vitrine pública, permitindo que visitantes consultem os imóveis disponíveis, visualizem seus detalhes e enviem solicitações de contato.

---

## Evoluções planejadas

Após a conclusão do MVP, o produto prevê novas funcionalidades e integrações, incluindo:

* API pública para consumo de dados por sistemas externos;
* Autenticação e gerenciamento de API Keys;
* Integração com sites externos;
* Suporte a domínios próprios;
* Configuração automatizada de DNS e SSL;
* Integração com portais imobiliários;
* Notificações por e-mail e Whatsapp.

---

## Tipos de Usuário

O sistema possui diferentes níveis e contextos de acesso:

| Tipo                           | Responsabilidade                                                        |
| ------------------------------ | ----------------------------------------------------------------------- |
| **Administrador / Superadmin** | Administração da plataforma, tenants e configurações globais            |
| **Tenant**                     | Corretor ou imobiliária responsável pela operação dentro da plataforma  |
| **Usuários do tenant**         | Membros da equipe com permissões definidas por função                   |
| **Visitantes / Leads**         | Usuários que acessam a vitrine pública e enviam solicitações de contato |

> Futuramente, a API pública permitirá a integração com sistemas e aplicações externas.

---

## Tecnologias

| Camada                               | Tecnologias                                       |
| ------------------------------------ | ------------------------------------------------- |
| **Backend**                          | Python, FastAPI, SQLAlchemy, Alembic, Pydantic v2 |
| **Autenticação e autorização**       | JWT, Refresh Tokens, RBAC, Argon2, Passlib        |
| **Frontend**                         | React 19, Vite 8, React Router 7, CSS Modules     |
| **Banco de dados**                   | PostgreSQL 16                                     |
| **Processamento assíncrono**         | Redis, ARQ                                        |
| **Armazenamento de arquivos**        | MinIO, compatível com Amazon S3                   |
| **Infraestrutura e desenvolvimento** | Docker, Docker Compose                            |

---

# Arquitetura

O backend foi estruturado como um **monólito modular**, buscando manter a separação entre os domínios de negócio sem introduzir a complexidade operacional de uma arquitetura baseada em microsserviços.

Cada domínio é organizado como um módulo independente, separando as responsabilidades relacionadas à camada de apresentação, regras de negócio, acesso a dados e validação.

```text
backend/app/
├── core/               # Configurações, banco de dados, segurança e dependências
├── modules/            # Módulos de domínio
│   ├── auth/
│   ├── users/
│   ├── roles/
│   ├── tenants/
│   ├── properties/
│   ├── property_owners/
│   ├── leads/
│   ├── clients/
│   └── ...
├── shared/             # Enums, utilitários e componentes compartilhados
└── main.py             # Inicialização da aplicação
```

Os módulos seguem uma organização baseada em responsabilidades:

```text
module/
├── router.py           # Endpoints da API
├── service.py          # Regras de negócio
├── repository.py       # Acesso e persistência de dados
├── models.py           # Modelos do banco de dados
└── schemas.py          # Schemas e validação de dados
```

A camada de apresentação é implementada separadamente em React:

```text
frontend/src/
├── pages/              # Páginas e rotas do ERP
├── components/         # Componentes reutilizáveis
└── services/           # Comunicação com a API
```

---

# Funcionalidades do MVP

## Autenticação e autorização

* Autenticação baseada em JWT;
* Access tokens e refresh tokens;
* Controle de acesso baseado em funções e permissões;
* Gerenciamento de usuários;
* Gerenciamento de funções e permissões.

## Multi-tenancy

* Criação automática de tenants durante o processo de registro;
* Isolamento dos dados entre tenants;
* Suporte a múltiplos usuários por tenant.

## Gestão imobiliária

* Cadastro e gerenciamento de imóveis;
* Cadastro de proprietários;
* Upload e processamento de imagens;
* Armazenamento de arquivos compatível com S3.

## Gestão de relacionamento

* Captura e gerenciamento de leads;
* Atualização de status;
* Cadastro e gerenciamento de clientes.

## Dashboard

* Agregação de métricas relacionadas à operação;
* Indicadores administrativos do tenant.

## Vitrine pública

* Listagem pública de imóveis;
* Página de detalhes;
* Formulário de contato.

---

# Como Executar o Projeto

## Pré-requisitos

É necessário possuir:

* Docker;
* Docker Compose.

## Executando todos os serviços

```bash
docker compose up -d
```

O comando inicializa os serviços necessários para o ambiente de desenvolvimento, incluindo:

* Backend;
* Frontend;
* PostgreSQL;
* Redis;
* MinIO;
* Serviços auxiliares de desenvolvimento.

## Executando apenas o backend e o banco de dados

```bash
docker compose up -d backend database
```

---

## Serviços disponíveis

| Serviço              | Endereço                     |
| -------------------- | ---------------------------- |
| Frontend             | `http://localhost:5173`      |
| Backend              | `http://localhost:8000`      |
| Documentação da API  | `http://localhost:8000/docs` |
| Console do MinIO     | `http://localhost:9101`      |
| Interface do MailHog | `http://localhost:8025`      |

---

# Configuração de Ambiente

As variáveis de ambiente devem ser configuradas a partir do arquivo de exemplo:

```bash
cp backend/.env.example backend/.env
```

O arquivo `.env` contém as configurações necessárias para os serviços utilizados pela aplicação, incluindo:

* Banco de dados;
* Armazenamento de arquivos;
* Redis;
* SMTP;
* Chaves de segurança;
* Integrações externas.

> **Importante:** arquivos contendo credenciais ou informações sensíveis não devem ser versionados no repositório.

---

# Roadmap

## Implementado

* [x] Autenticação com JWT e refresh tokens;
* [x] Controle de acesso baseado em funções e permissões;
* [x] Gerenciamento de usuários, funções e permissões;
* [x] Arquitetura multi-tenant;
* [x] Cadastro e gerenciamento de imóveis;
* [x] Upload e processamento de imagens;
* [x] Gestão de proprietários;
* [x] Gestão de leads;
* [x] Gestão de clientes;
* [x] Dashboard com métricas;
* [x] Landing page;
* [x] Vitrine pública de imóveis;
* [x] Página de detalhes de imóveis;
* [x] Formulário de contato.

## Em desenvolvimento

* [ ] Interface administrativa completa;
* [ ] Gerenciamento de imóveis no frontend;
* [ ] Gerenciamento de leads no frontend;
* [ ] Gerenciamento de clientes no frontend;
* [ ] Gerenciamento de usuários e equipe;
* [ ] Refinamento da interface e integração das funcionalidades do ERP.

## Futuras adições

* [ ] API pública;
* [ ] Autenticação e gerenciamento de API Keys;
* [ ] Integração com sites externos;
* [ ] Suporte a domínios próprios;
* [ ] Configuração automatizada de DNS e SSL;
* [ ] Integração com portais imobiliários;
* [ ] Automação da publicação de anúncios;
* [ ] Notificações por e-mail.

---

# Estrutura do Repositório

```text
.
├── backend/              # API e regras de negócio
├── frontend/             # Aplicação web administrativa
├── docker-compose.yml    # Orquestração dos serviços
└── README.md
```

---

## Autor

Projeto desenvolvido por **Eduardo Cliquet**.
