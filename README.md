# FastAPI JWT Authentication Template

Template completo de backend FastAPI com autenticação JWT, seguindo arquitetura limpa e boas práticas.

## 🚀 Funcionalidades

- ✅ Autenticação JWT completa (Access + Refresh tokens)
- ✅ Tokens em cookies HttpOnly (seguro para React)
- ✅ Sistema de permissões (Superuser/Admin/User)
- ✅ Criação de admin protegida (Basic Auth + Token)
- ✅ Criação de usuários por superuser autenticado
- ✅ Logout com blacklist de tokens
- ✅ Endpoint para obter dados do usuário logado
- ✅ Controle de transações com rollback automático
- ✅ Arquitetura limpa (Domain, Application, Infrastructure, Interface)
- ✅ SQLModel + MySQL (Async)
- ✅ Redis para cache e gerenciamento de tokens
- ✅ Docker + Docker Compose
- ✅ Configurações via variáveis de ambiente

## 📁 Estrutura do Projeto

```
app/
├── config.py                          # Configurações da aplicação
├── domain/                            # Camada de domínio
│   ├── entities/                      # Entidades de negócio
│   │   └── user.py                   # Entidade User
│   └── repositories/                  # Interfaces dos repositórios
│       └── user_repository.py        # Interface UserRepository
├── application/                       # Camada de aplicação
│   └── services/                     # Serviços de aplicação
│       └── auth_service.py           # Serviço de autenticação
├── infrastructure/                    # Camada de infraestrutura
│   ├── database/                     # Configuração do banco
│   │   ├── connection.py             # Conexão SQLModel
│   │   └── repositories/             # Implementações dos repositórios
│   │       └── user_repository.py    # Implementação SQLUserRepository
│   ├── cache/                        # Cache Redis
│   │   └── redis_service.py          # Serviço Redis
│   └── security/                     # Segurança
│       └── jwt_service.py            # Serviço JWT
└── interface/                         # Camada de interface
    ├── api/                          # API REST
    │   ├── main.py                   # Aplicação FastAPI
    │   ├── dependencies/             # Dependências FastAPI
    │   │   └── auth.py               # Dependências de autenticação
    │   └── routes/                   # Rotas da API
    │       └── auth.py               # Rotas de autenticação
    └── schemas/                      # Schemas Pydantic
        └── auth.py                   # Schemas de autenticação
```

## 🛠️ Configuração e Instalação

### Opção 1: Docker Compose (Produção)

1. Clone o repositório:
```bash
git clone <repository-url>
cd template-fastApi-backEnd-jwtAuth
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Execute com Docker Compose:
```bash
docker-compose up --build
```

### Opção 2: Desenvolvimento Local (Debug)

1. Inicie apenas MySQL e Redis:
```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
uvicorn app.interface.api.main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em: `http://localhost:8000`

## 📚 API Endpoints

### Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/api/v1/auth/create-admin` | Criar admin/superuser | 🔐 Basic Auth + Token |
| POST | `/api/v1/auth/create-user` | Criar usuário normal | 🍪 Cookie (Superuser) |
| POST | `/api/v1/auth/login` | Login do usuário | ❌ |
| POST | `/api/v1/auth/refresh` | Renovar tokens | 🍪 Cookie |
| POST | `/api/v1/auth/logout` | Logout do usuário | 🍪 Cookie |
| GET | `/api/v1/auth/me` | Obter dados do usuário logado | 🍪 Cookie |

### Outros

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/health` | Health check |
| GET | `/docs` | Documentação Swagger |

## 🔐 Sistema de Permissões

### Tipos de Usuário

- **Superuser** (`is_superuser: true`): Acesso total ao sistema, pode criar novos usuários
- **User** (`is_superuser: false`): Acesso padrão limitado

### Criação de Admins

O endpoint `/api/v1/auth/create-admin` é protegido por **Basic Authentication + Token fixo** para máxima segurança.

**Credenciais necessárias:**
- Basic Auth: `admin:admin123` (configurável via .env)
- Token fixo: `create-admin-secure-token-2024` (configurável via .env)

### Criação de Usuários

O endpoint `/api/v1/auth/create-user` requer autenticação via **cookie de superuser**.

**IMPORTANTE:** Altere as credenciais padrão em produção!

## 🍪 Sistema de Cookies

### Autenticação Transparente

- **Tokens em cookies**: Access e refresh tokens são automaticamente salvos em cookies
- **HttpOnly em produção**: Cookies seguros apenas em ambiente de produção
- **Autenticação automática**: Rotas protegidas usam cookies automaticamente
- **Perfeito para React**: Não precisa gerenciar tokens manualmente

### Configuração por Ambiente

- **Development**: `httponly=false, secure=false` (facilita debug)
- **Production**: `httponly=true, secure=true` (máxima segurança)

## 🔐 Exemplos de Uso

### 1. Criar Admin (Requer Basic Auth + Token)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/create-admin" \
  -u "admin:admin123" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "firstname": "Admin",
    "lastname": "User",
    "password": "strongpassword123",
    "admin_token": "create-admin-secure-token-2024"
  }'
```

### 2. Login (Define Cookies Automaticamente)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "admin@example.com",
    "password": "strongpassword123"
  }'
```

**Resposta:**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-here",
    "email": "admin@example.com",
    "username": "admin",
    "firstname": "Admin",
    "lastname": "User",
    "is_active": true,
    "is_superuser": true,
    "last_login": "2024-01-01T10:05:00",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:05:00"
  }
}
```

### 3. Criar Usuário (Requer Cookie de Superuser)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/create-user" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "firstname": "John",
    "lastname": "Doe",
    "password": "strongpassword123"
  }'
```

### 4. Obter Dados do Usuário Logado (Usa Cookies)

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -b cookies.txt
```

### 5. Renovar Tokens (Usa Cookies)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -b cookies.txt -c cookies.txt
```

### 6. Logout (Remove Cookies)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -b cookies.txt
```

## 🔧 Configurações

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | URL de conexão MySQL | `mysql+aiomysql://root:password@localhost:3306/authdb` |
| `REDIS_URL` | URL de conexão Redis | `redis://localhost:6379/0` |
| `SECRET_KEY` | Chave secreta para JWT | `your-super-secret-key-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do access token (minutos) | `30` |
| `SUPERUSER_USERNAME` | Username para criação de admin | `admin` |
| `SUPERUSER_PASSWORD` | Password para criação de admin | `admin123` |
| `ADMIN_CREATION_TOKEN` | Token fixo para criação de admin | `create-admin-secure-token-2024` |
| `ENVIRONMENT` | Ambiente da aplicação (development/production) | `development` |

## 🏗️ Arquitetura

Este projeto segue os princípios da **Arquitetura Limpa**:

- **Domain**: Entidades de negócio e interfaces de repositórios
- **Application**: Casos de uso e serviços de aplicação
- **Infrastructure**: Implementações concretas (banco, cache, segurança)
- **Interface**: Controllers, rotas e schemas da API

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- JWT com access e refresh tokens em cookies HttpOnly
- Criação de admin protegida por Basic Auth + Token fixo
- Sistema de permissões com superuser/user
- Controle de transações com rollback automático
- Blacklist de tokens no logout
- Validação de tokens em todas as rotas protegidas
- Cookies seguros por ambiente (HttpOnly em produção)
- CORS configurado

## 🚀 Desenvolvimento

### Ambiente de Desenvolvimento Local

1. **Iniciar serviços de infraestrutura:**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. **Executar aplicação localmente:**
```bash
pip install -r requirements.txt
uvicorn app.interface.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Ambiente Completo com Docker

```bash
docker-compose up --build
```

### Arquivos de Configuração

- `docker-compose.yml` - Ambiente completo (app + MySQL + Redis)
- `docker-compose.dev.yml` - Apenas MySQL e Redis para desenvolvimento

### Testes

Para adicionar testes, crie arquivos na pasta `tests/` seguindo a estrutura das camadas.

## 📝 Próximos Passos

- [ ] Adicionar testes unitários e de integração
- [ ] Implementar rate limiting
- [ ] Adicionar logs estruturados
- [ ] Implementar recuperação de senha
- [ ] Adicionar roles e permissões
- [ ] Implementar 2FA

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.