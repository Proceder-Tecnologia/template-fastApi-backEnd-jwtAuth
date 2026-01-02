# FastAPI JWT Authentication Template

Template completo de backend FastAPI com autenticação JWT, seguindo arquitetura limpa e boas práticas.

## 🚀 Funcionalidades

- ✅ Autenticação JWT completa (Access + Refresh tokens)
- ✅ Registro e login de usuários
- ✅ Logout com blacklist de tokens
- ✅ Endpoint para obter dados do usuário logado
- ✅ Arquitetura limpa (Domain, Application, Infrastructure, Interface)
- ✅ SQLModel + MySQL
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
| POST | `/api/v1/auth/register` | Registrar novo usuário | ❌ |
| POST | `/api/v1/auth/login` | Login do usuário | ❌ |
| POST | `/api/v1/auth/refresh` | Renovar access token | ❌ |
| POST | `/api/v1/auth/logout` | Logout do usuário | ✅ |
| GET | `/api/v1/auth/me` | Obter dados do usuário logado | ✅ |

### Outros

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/health` | Health check |
| GET | `/docs` | Documentação Swagger |

## 🔐 Exemplos de Uso

### 1. Registrar Usuário

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "firstname": "John",
    "lastname": "Doe",
    "password": "strongpassword123"
  }'
```

**Resposta:**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "username": "johndoe",
  "firstname": "John",
  "lastname": "Doe",
  "is_active": true,
  "last_login": null,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "strongpassword123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Obter Dados do Usuário Logado

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Resposta:**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "username": "johndoe",
  "firstname": "John",
  "lastname": "Doe",
  "is_active": true,
  "last_login": "2024-01-01T10:05:00",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:05:00"
}
```

### 4. Renovar Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### 5. Logout

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔧 Configurações

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | URL de conexão MySQL | `mysql+aiomysql://root:password@localhost:3306/authdb` |
| `REDIS_URL` | URL de conexão Redis | `redis://localhost:6379/0` |
| `SECRET_KEY` | Chave secreta para JWT | `your-super-secret-key-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do access token (minutos) | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Expiração do refresh token (dias) | `7` |

## 🏗️ Arquitetura

Este projeto segue os princípios da **Arquitetura Limpa**:

- **Domain**: Entidades de negócio e interfaces de repositórios
- **Application**: Casos de uso e serviços de aplicação
- **Infrastructure**: Implementações concretas (banco, cache, segurança)
- **Interface**: Controllers, rotas e schemas da API

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- JWT com access e refresh tokens
- Blacklist de tokens no logout
- Validação de tokens em todas as rotas protegidas
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