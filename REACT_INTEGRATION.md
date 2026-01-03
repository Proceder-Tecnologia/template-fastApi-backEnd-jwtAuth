# Integração React - FastAPI JWT Auth

Guia completo para integrar sua aplicação React com o backend FastAPI JWT Auth usando cookies HttpOnly.

## 🚀 Configuração Inicial

### 1. Configurar Axios

```bash
npm install axios
```

```javascript
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true, // IMPORTANTE: Permite envio de cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

### 2. Context de Autenticação

```javascript
// src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Verificar se usuário está logado ao carregar a aplicação
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.data);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      
      setUser(response.data.user);
      return { success: true, user: response.data.user };
    } catch (error) {
      const message = error.response?.data?.detail || 'Erro no login';
      return { success: false, error: message };
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Erro no logout:', error);
    } finally {
      setUser(null);
    }
  };

  const value = {
    user,
    login,
    logout,
    loading,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

## 🔐 Componentes de Autenticação

### 1. Formulário de Login

```javascript
// src/components/LoginForm.js
import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(email, password);
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <h2>Login</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <div className="form-group">
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="password">Senha:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
};

export default LoginForm;
```

### 2. Componente de Logout

```javascript
// src/components/LogoutButton.js
import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const LogoutButton = () => {
  const { logout, user } = useAuth();

  const handleLogout = async () => {
    if (window.confirm('Deseja realmente sair?')) {
      await logout();
    }
  };

  return (
    <div className="user-menu">
      <span>Olá, {user?.firstname}!</span>
      <button onClick={handleLogout} className="logout-btn">
        Sair
      </button>
    </div>
  );
};

export default LogoutButton;
```

## 🛡️ Proteção de Rotas

### 1. Componente PrivateRoute

```javascript
// src/components/PrivateRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Carregando...</div>;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
```

### 2. Configuração de Rotas

```javascript
// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import LoginForm from './components/LoginForm';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route 
              path="/dashboard" 
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } 
            />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
```

## 🔄 Interceptador para Refresh Token

```javascript
// src/services/api.js (versão completa)
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptador para refresh automático
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        await api.post('/auth/refresh');
        return api(originalRequest);
      } catch (refreshError) {
        // Redirect para login se refresh falhar
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

## 📱 Exemplo de Dashboard

```javascript
// src/pages/Dashboard.js
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import LogoutButton from '../components/LogoutButton';
import api from '../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Exemplo de requisição autenticada
      const response = await api.get('/some-protected-endpoint');
      setData(response.data);
    } catch (error) {
      console.error('Erro ao buscar dados:', error);
    }
  };

  return (
    <div className="dashboard">
      <header>
        <h1>Dashboard</h1>
        <LogoutButton />
      </header>
      
      <main>
        <div className="user-info">
          <h2>Bem-vindo, {user?.firstname} {user?.lastname}!</h2>
          <p>Email: {user?.email}</p>
          <p>Tipo: {user?.is_superuser ? 'Administrador' : 'Usuário'}</p>
        </div>
        
        {data && (
          <div className="content">
            {/* Seu conteúdo aqui */}
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
```

## ⚙️ Configurações Importantes

### 1. CORS no Backend

O backend já está configurado para aceitar cookies. Certifique-se de que o CORS está permitindo credenciais:

```python
# Já configurado no backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do React
    allow_credentials=True,  # IMPORTANTE
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Variáveis de Ambiente React

```bash
# .env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🎯 Fluxo de Autenticação

1. **Login**: Usuário faz login → Backend define cookies HttpOnly
2. **Requisições**: Todas as requisições incluem cookies automaticamente
3. **Refresh**: Token renovado automaticamente quando expira
4. **Logout**: Cookies removidos do navegador

## ✅ Vantagens desta Implementação

- **Segurança**: Tokens em cookies HttpOnly (não acessíveis via JavaScript)
- **Simplicidade**: Não precisa gerenciar tokens manualmente
- **Automático**: Refresh de tokens transparente
- **Compatibilidade**: Funciona perfeitamente com SSR/Next.js

## 🚨 Pontos Importantes

- Sempre use `withCredentials: true` no Axios
- Configure CORS corretamente no backend
- Cookies funcionam apenas com HTTPS em produção
- Teste o refresh automático de tokens

Este setup garante uma autenticação robusta e segura para sua aplicação React!