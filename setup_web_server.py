#!/usr/bin/env python3
"""
Setup para Servidor Web do Sistema FONTES
Transforma o sistema desktop em aplicação web
"""
import os
import sys
import subprocess
from pathlib import Path

class WebServerBuilder:
    """Construtor de servidor web para o Sistema FONTES"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.web_dir = self.project_dir / "web_server"
        
    def check_dependencies(self):
        """Verificar e instalar dependências web"""
        print("🔍 Verificando dependências web...")
        
        required_packages = [
            "flask",
            "flask-socketio",
            "gunicorn",
            "waitress"
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package} - OK")
            except ImportError:
                print(f"📦 Instalando {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} - Instalado")
    
    def create_web_app(self):
        """Criar aplicação Flask"""
        self.web_dir.mkdir(exist_ok=True)
        
        app_content = '''#!/usr/bin/env python3
"""
Sistema FONTES - Aplicação Web
Servidor Flask para acesso via navegador
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import os
import sys
import json
import sqlite3
from datetime import datetime
import secrets

# Configurar path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurar banco de dados
DATABASE = 'fontes_web.db'

def init_db():
    """Inicializar banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserir usuário admin padrão
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, full_name, email, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin123', 'Administrador do Sistema', 'admin@fontes.inss.gov.br', 'admin'))
    
    # Tabela de sessões
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Autenticar usuário"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, full_name, email, role 
        FROM users 
        WHERE username = ? AND password = ?
    ''', (username, password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'full_name': user[2],
            'email': user[3],
            'role': user[4]
        }
    return None

@app.route('/')
def index():
    """Página inicial"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            
            return jsonify({
                'success': True,
                'message': f'Bem-vindo, {user["full_name"]}!',
                'user': user
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas'
            }), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/user-info')
def user_info():
    """Informações do usuário logado"""
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    return jsonify({
        'user_id': session['user_id'],
        'username': session['username'],
        'full_name': session['full_name'],
        'role': session['role']
    })

@app.route('/api/services')
def services():
    """Listar serviços disponíveis"""
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    services_list = [
        {
            'id': 'aposentadoria',
            'title': 'Aposentadoria',
            'icon': '👨‍🦳',
            'description': 'Solicitações de aposentadoria',
            'color': '#1976D2'
        },
        {
            'id': 'maternidade',
            'title': 'Maternidade',
            'icon': '🤱',
            'description': 'Benefícios de maternidade',
            'color': '#E91E63'
        },
        {
            'id': 'arquivos',
            'title': 'Arquivos',
            'icon': '📁',
            'description': 'Gestão de documentos',
            'color': '#FF9800'
        },
        {
            'id': 'meu_inss',
            'title': 'Meu INSS',
            'icon': '🏢',
            'description': 'Portal do INSS',
            'color': '#4CAF50'
        },
        {
            'id': 'suporte',
            'title': 'Suporte',  
            'icon': '🛠️',
            'description': 'Atendimento técnico',
            'color': '#607D8B'
        },
        {
            'id': 'servicos',
            'title': 'Solicitar Serviço',
            'icon': '📋',
            'description': 'Novas solicitações',
            'color': '#3F51B5'
        }
    ]
    
    return jsonify(services_list)

@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    print(f'Cliente conectado: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    print(f'Cliente desconectado: {request.sid}')

if __name__ == '__main__':
    init_db()
    print("🌐 Sistema FONTES - Servidor Web")
    print("=" * 40)
    print("🚀 Iniciando servidor...")
    print("📱 Acesso local: http://localhost:5000")
    print("🌍 Acesso rede: http://[SEU_IP]:5000")
    print("👤 Login: admin / admin123")
    print("=" * 40)
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
'''
        
        with open(self.web_dir / "app.py", "w", encoding="utf-8") as f:
            f.write(app_content)
        
        print("✅ Aplicação Flask criada")
    
    def create_templates(self):
        """Criar templates HTML"""
        templates_dir = self.web_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Template base
        base_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema FONTES{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body class="bg-dark text-light">
    {% block content %}{% endblock %}
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
        
        with open(templates_dir / "base.html", "w", encoding="utf-8") as f:
            f.write(base_template)
        
        # Template de login
        login_template = '''{% extends "base.html" %}

{% block title %}Login - Sistema FONTES{% endblock %}

{% block content %}
<div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
    <div class="card bg-secondary" style="width: 400px;">
        <div class="card-body">
            <div class="text-center mb-4">
                <h1 class="display-4">🏛️</h1>
                <h2 class="text-primary">FONTES</h2>
                <p class="text-muted">Sistema INSS v3.0</p>
            </div>
            
            <form id="loginForm">
                <div class="mb-3">
                    <label class="form-label">👤 Usuário:</label>
                    <input type="text" class="form-control" id="username" required>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">🔒 Senha:</label>
                    <div class="input-group">
                        <input type="password" class="form-control" id="password" required>
                        <button class="btn btn-outline-secondary" type="button" id="togglePassword">👁️</button>
                    </div>
                </div>
                
                <div class="mb-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="remember">
                        <label class="form-check-label" for="remember">
                            Manter conectado
                        </label>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-primary w-100">
                    🔓 ENTRAR NO SISTEMA
                </button>
            </form>
            
            <div class="text-center mt-3">
                <small class="text-muted">
                    💬 Problemas? Contate o suporte<br>
                    📞 (11) 99999-9999
                </small>
            </div>
        </div>
    </div>
</div>

<div class="position-fixed bottom-0 end-0 p-3">
    <div id="toast" class="toast" role="alert">
        <div class="toast-body"></div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => window.location.href = '/', 1000);
        } else {
            showToast(data.message, 'error');
        }
    } catch (error) {
        showToast('Erro de conexão', 'error');
    }
});

document.getElementById('togglePassword').addEventListener('click', () => {
    const password = document.getElementById('password');
    const toggle = document.getElementById('togglePassword');
    
    if (password.type === 'password') {
        password.type = 'text';
        toggle.textContent = '🙈';
    } else {
        password.type = 'password';
        toggle.textContent = '👁️';
    }
});

function showToast(message, type) {
    const toast = document.getElementById('toast');
    const toastBody = toast.querySelector('.toast-body');
    
    toastBody.textContent = message;
    toast.className = `toast ${type === 'success' ? 'bg-success' : 'bg-danger'} text-white`;
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}
</script>
{% endblock %}'''
        
        with open(templates_dir / "login.html", "w", encoding="utf-8") as f:
            f.write(login_template)
        
        # Template do dashboard
        dashboard_template = '''{% extends "base.html" %}

{% block title %}Dashboard - Sistema FONTES{% endblock %}

{% block content %}
<!-- Header -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">
            <h3>🏛️ FONTES</h3>
        </a>
        
        <div class="navbar-nav ms-auto">
            <div class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                    👤 <span id="userName">Usuário</span>
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" onclick="openProfile()">⚙️ Perfil</a></li>
                    <li><a class="dropdown-item" href="#" onclick="openSupport()">🆘 Suporte</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/logout">🚪 Sair</a></li>
                </ul>
            </div>
        </div>
    </div>
</nav>

<!-- Main Content -->
<div class="container-fluid py-4">
    <div class="row mb-4">
        <div class="col">
            <h2 class="text-center text-primary">📋 SELECIONE UMA CATEGORIA DE SERVIÇOS</h2>
        </div>
    </div>
    
    <div id="servicesGrid" class="row g-4">
        <!-- Services will be loaded here -->
    </div>
</div>

<!-- Modal for Service Details -->
<div class="modal fade" id="serviceModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content bg-secondary">
            <div class="modal-header">
                <h5 class="modal-title" id="modalTitle"></h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Content will be loaded here -->
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
let socket = io();

// Load user info
fetch('/api/user-info')
    .then(response => response.json())
    .then(data => {
        document.getElementById('userName').textContent = data.full_name;
    });

// Load services
fetch('/api/services')
    .then(response => response.json())
    .then(services => {
        const grid = document.getElementById('servicesGrid');
        grid.innerHTML = '';
        
        services.forEach(service => {
            const card = createServiceCard(service);
            grid.appendChild(card);
        });
    });

function createServiceCard(service) {
    const col = document.createElement('div');
    col.className = 'col-md-4';
    
    col.innerHTML = `
        <div class="card bg-secondary h-100 service-card" onclick="openService('${service.id}')" style="cursor: pointer;">
            <div class="card-body text-center">
                <div class="display-1 mb-3">${service.icon}</div>
                <h5 class="card-title text-primary">${service.title}</h5>
                <p class="card-text">${service.description}</p>
            </div>
        </div>
    `;
    
    return col;
}

function openService(serviceId) {
    const modal = new bootstrap.Modal(document.getElementById('serviceModal'));
    document.getElementById('modalTitle').textContent = 'Serviço em Desenvolvimento';
    document.getElementById('modalBody').innerHTML = `
        <div class="text-center">
            <div class="display-1 mb-3">🚧</div>
            <h4>Funcionalidade em Desenvolvimento</h4>
            <p>Este serviço será implementado em breve.</p>
            <p>ID do serviço: <code>${serviceId}</code></p>
        </div>
    `;
    modal.show();
}

function openProfile() {
    alert('🔧 Configurações de perfil em desenvolvimento');
}

function openSupport() {
    alert('🆘 Central de suporte:\\n📞 (11) 99999-9999\\n📧 suporte@fontes.inss.gov.br');
}

// Socket events
socket.on('connect', () => {
    console.log('Conectado ao servidor');
});
</script>
{% endblock %}'''
        
        with open(templates_dir / "dashboard.html", "w", encoding="utf-8") as f:
            f.write(dashboard_template)
        
        print("✅ Templates HTML criados")
    
    def create_static_files(self):
        """Criar arquivos estáticos (CSS, JS)"""
        static_dir = self.web_dir / "static"
        static_dir.mkdir(exist_ok=True)
        
        # CSS
        css_dir = static_dir / "css"
        css_dir.mkdir(exist_ok=True)
        
        css_content = '''/* Sistema FONTES - Estilos */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    min-height: 100vh;
}

.service-card:hover {
    transform: translateY(-5px);
    transition: transform 0.3s ease;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

.card {
    border: none;
    border-radius: 15px;
}

.btn-primary {
    background: linear-gradient(45deg, #2196F3, #1976D2);
    border: none;
}

.btn-primary:hover {
    background: linear-gradient(45deg, #1976D2, #0D47A1);
}

.navbar-brand h3 {
    margin: 0;
    font-weight: bold;
}

.toast {
    border-radius: 10px;
}

.form-control {
    border-radius: 10px;
    background-color: #495057;
    border: 1px solid #6c757d;
    color: white;
}

.form-control:focus {
    background-color: #495057;
    border-color: #2196F3;
    color: white;
    box-shadow: 0 0 0 0.2rem rgba(33, 150, 243, 0.25);
}

.display-1 {
    font-size: 4rem;
}

@media (max-width: 768px) {
    .display-1 {
        font-size: 2.5rem;
    }
}'''
        
        with open(css_dir / "style.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        
        # JavaScript
        js_dir = static_dir / "js"
        js_dir.mkdir(exist_ok=True)
        
        js_content = '''// Sistema FONTES - JavaScript

// Configurações globais
const FONTES = {
    version: '3.0',
    apiUrl: '/api',
    socketConnected: false
};

// Utilitários
function showNotification(message, type = 'info') {
    // Implementar sistema de notificações
    console.log(`[${type.toUpperCase()}] ${message}`);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(amount);
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema FONTES v3.0 carregado');
});'''
        
        with open(js_dir / "app.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        
        print("✅ Arquivos estáticos criados")
    
    def create_startup_scripts(self):
        """Criar scripts de inicialização"""
        
        # Script Windows
        windows_script = '''@echo off
title Sistema FONTES - Servidor Web
echo ========================================
echo  Sistema FONTES v3.0 - Servidor Web
echo ========================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo 📥 Baixe Python em: https://python.org
    pause
    exit /b 1
)

echo 📦 Verificando dependências...
cd /d "%~dp0"
python -m pip install -r requirements.txt

echo 🚀 Iniciando servidor...
echo.
echo 📱 Acesso local: http://localhost:5000
echo 🌍 Acesso rede: http://%COMPUTERNAME%:5000
echo 👤 Login: admin / admin123
echo.
echo ⚠️  Para parar o servidor, pressione Ctrl+C
echo.

python app.py
pause
'''
        
        with open(self.web_dir / "start_server.bat", "w", encoding="utf-8") as f:
            f.write(windows_script)
        
        # Script Linux/Mac
        linux_script = '''#!/bin/bash
echo "========================================"
echo " Sistema FONTES v3.0 - Servidor Web"
echo "========================================"
echo ""

echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "📥 Instale Python3 primeiro"
    exit 1
fi

echo "📦 Verificando dependências..."
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt

echo "🚀 Iniciando servidor..."
echo ""
echo "📱 Acesso local: http://localhost:5000"
echo "🌍 Acesso rede: http://$(hostname):5000"
echo "👤 Login: admin / admin123"
echo ""
echo "⚠️  Para parar o servidor, pressione Ctrl+C"
echo ""

python3 app.py
'''
        
        with open(self.web_dir / "start_server.sh", "w", encoding="utf-8") as f:
            f.write(linux_script)
        
        # Tornar executável no Linux/Mac
        try:
            os.chmod(self.web_dir / "start_server.sh", 0o755)
        except:
            pass
        
        print("✅ Scripts de inicialização criados")
    
    def create_requirements(self):
        """Criar arquivo requirements.txt"""
        requirements = '''Flask==2.3.3
Flask-SocketIO==5.3.6
gunicorn==21.2.0
waitress==2.1.2
python-socketio==5.9.0
python-engineio==4.7.1
'''
        
        with open(self.web_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        
        print("✅ Requirements.txt criado")
    
    def create_readme(self):
        """Criar documentação"""
        readme_content = '''# Sistema FONTES v3.0 - Servidor Web

## 🌐 Aplicação Web do Sistema FONTES

Esta versão permite acesso ao Sistema FONTES através de navegador web, possibilitando uso em rede local ou hospedagem online.

## 🚀 Como Executar

### Windows
1. Execute: `start_server.bat`
2. Aguarde a inicialização
3. Acesse: http://localhost:5000

### Linux/Mac
1. Execute: `./start_server.sh`
2. Aguarde a inicialização  
3. Acesse: http://localhost:5000

### Manual
```bash
pip install -r requirements.txt
python app.py
```

## 👤 Credenciais Padrão
- **Usuário:** admin
- **Senha:** admin123

## 🌍 Acesso em Rede

Para permitir acesso de outros computadores:
1. O servidor inicia automaticamente em `0.0.0.0:5000`
2. Outros usuários podem acessar via: `http://[IP_DO_SERVIDOR]:5000`
3. Exemplo: `http://192.168.1.100:5000`

## 📋 Requisitos
- Python 3.7+
- Conexão à internet (primeira execução)
- Porta 5000 disponível

## 🔧 Configurações

### Alterar Porta
Edite `app.py`, linha final:
```python
socketio.run(app, host='0.0.0.0', port=5000)  # Altere 5000
```

### Adicionar HTTPS
Para produção, configure certificado SSL:
```python
socketio.run(app, host='0.0.0.0', port=443, 
            certfile='cert.pem', keyfile='key.pem')
```

## 📱 Recursos
- ✅ Interface responsiva (mobile-friendly)
- ✅ Comunicação em tempo real (WebSocket)
- ✅ Autenticação de usuários
- ✅ Dashboard interativo
- ✅ Sistema de notificações

## 🆘 Suporte
- Email: suporte@fontes.inss.gov.br
- Telefone: (11) 99999-9999

## 📄 Licença
© 2025 Sistema FONTES. Todos os direitos reservados.
'''
        
        with open(self.web_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ Documentação criada")
    
    def run(self):
        """Executar processo completo"""
        print("🌐 Sistema FONTES - Gerador de Servidor Web")
        print("=" * 50)
        
        try:
            # 1. Verificar dependências
            self.check_dependencies()
            
            # 2. Criar estrutura web
            self.create_web_app()
            self.create_templates()
            self.create_static_files()
            self.create_startup_scripts()
            self.create_requirements()
            self.create_readme()
            
            print("\n" + "=" * 50)
            print("🎉 SUCESSO! Servidor web criado!")
            print("=" * 50)
            print(f"📁 Localização: {self.web_dir}")
            print("📋 Arquivos criados:")
            print("   • app.py (aplicação Flask)")
            print("   • templates/ (páginas HTML)")
            print("   • static/ (CSS, JS, imagens)")
            print("   • start_server.bat (Windows)")
            print("   • start_server.sh (Linux/Mac)")
            print("   • requirements.txt")
            print("   • README.md")
            print("\n🚀 PRÓXIMOS PASSOS:")
            print("1. Navegue para a pasta 'web_server'")
            print("2. Execute 'start_server.bat' (Windows) ou './start_server.sh' (Linux/Mac)")
            print("3. Acesse http://localhost:5000")
            print("4. Login: admin / admin123")
            print("\n✅ Pronto para uso!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            return False

if __name__ == "__main__":
    builder = WebServerBuilder()
    success = builder.run()
    
    if success:
        input("\nPressione Enter para sair...")
    else:
        input("\nOcorreram erros. Pressione Enter para sair...")
