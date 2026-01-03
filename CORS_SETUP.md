# Configuração CORS - Desenvolvimento e Produção

Guia para configurar CORS corretamente para desenvolvimento local e deploy em produção.

## 🔧 Desenvolvimento Local

### Backend (FastAPI)

O backend já está configurado para desenvolvimento local:

```python
# Configuração automática baseada no ambiente
cors_origins = [
    "http://localhost:3000",    # React dev server
    "http://127.0.0.1:3000",   # React dev server alternativo
]
```

### Frontend (React)

Configure o Axios para incluir cookies:

```javascript
// src/services/api.js
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,  // CRÍTICO: Permite cookies cross-origin
});
```

### Testando Localmente

1. **Backend**: `http://localhost:8000`
2. **Frontend**: `http://localhost:3000`
3. **Cookies**: Funcionam automaticamente entre diferentes portas

## 🚀 Produção

### 1. Configurar Domínios

```bash
# .env (produção)
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Configuração de Cookies

Em produção, os cookies são automaticamente configurados como:

```python
# Configuração automática em produção
httponly=True    # Não acessível via JavaScript
secure=True      # Apenas HTTPS
samesite="none"  # Permite cross-origin (se necessário)
```

### 3. Opções de Deploy

#### Opção A: Mesmo Domínio (Recomendado)
```
Frontend: https://yourdomain.com
Backend:  https://yourdomain.com/api
```

**Vantagens:**
- Sem problemas de CORS
- Cookies funcionam nativamente
- Melhor performance

**Configuração:**
```python
# Não precisa de CORS origins específicos
cors_origins = ["https://yourdomain.com"]
```

#### Opção B: Subdomínios
```
Frontend: https://app.yourdomain.com
Backend:  https://api.yourdomain.com
```

**Configuração:**
```python
cors_origins = [
    "https://app.yourdomain.com",
    "https://yourdomain.com"
]
```

#### Opção C: Domínios Diferentes
```
Frontend: https://myapp.com
Backend:  https://api.mybackend.com
```

**Configuração:**
```python
cors_origins = ["https://myapp.com"]
# samesite="none" é necessário
```

## 🛠️ Configuração Dinâmica

### Backend Inteligente

```python
# app/config.py
class Settings(BaseSettings):
    environment: str = "development"
    cors_origins: list = ["http://localhost:3000"]
    
    @property
    def cookie_samesite(self) -> str:
        return "none" if self.environment == "production" else "lax"
```

### Frontend Adaptável

```javascript
// src/config/api.js
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://api.yourdomain.com/api/v1'
  : 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});
```

## 🚨 Problemas Comuns e Soluções

### 1. Cookies não funcionam

**Problema:** Cookies não são enviados nas requisições

**Solução:**
```javascript
// ✅ Correto
axios.defaults.withCredentials = true;

// ❌ Incorreto
// Esquecer withCredentials
```

### 2. CORS Error em Produção

**Problema:** `Access-Control-Allow-Origin` error

**Solução:**
```python
# ✅ Correto - Origins específicos
allow_origins=["https://yourdomain.com"]

# ❌ Incorreto - Wildcard com credentials
allow_origins=["*"]  # Não funciona com cookies
```

### 3. SameSite Issues

**Problema:** Cookies bloqueados por SameSite

**Solução:**
```python
# Desenvolvimento
samesite="lax"

# Produção (cross-origin)
samesite="none"
secure=True  # Obrigatório com samesite="none"
```

### 4. HTTPS Obrigatório

**Problema:** Cookies secure não funcionam em HTTP

**Solução:**
```python
# Desenvolvimento
secure=False

# Produção
secure=True  # Apenas HTTPS
```

## 📋 Checklist de Deploy

### Backend
- [ ] `ENVIRONMENT=production`
- [ ] CORS origins corretos
- [ ] HTTPS configurado
- [ ] Cookies secure=True

### Frontend
- [ ] `withCredentials: true`
- [ ] URL de produção configurada
- [ ] Build otimizado
- [ ] HTTPS configurado

### Infraestrutura
- [ ] SSL/TLS certificado
- [ ] Proxy reverso (Nginx/Cloudflare)
- [ ] Firewall configurado
- [ ] Monitoramento ativo

## 🎯 Configurações Recomendadas

### Desenvolvimento
```python
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Produção
```python
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com
```

Esta configuração garante que cookies funcionem perfeitamente tanto em desenvolvimento quanto em produção!