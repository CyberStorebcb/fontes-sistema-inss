#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Render Deploy
Versão otimizada para hospedagem no Render.com  
"""
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import os
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Template HTML integrado - Login
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Sistema FONTES</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            font-size: 64px;
            text-align: center;
            margin-bottom: 20px;
        }
        .system-title {
            color: #1976D2;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .btn-login {
            background: linear-gradient(45deg, #1976D2, #2196F3);
            border: none;
            border-radius: 10px;
            padding: 12px;
            width: 100%;
            color: white;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-login:hover {
            background: linear-gradient(45deg, #0D47A1, #1976D2);
            transform: translateY(-2px);
        }
        .form-control {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 12px 15px;
            margin-bottom: 15px;
        }
        .form-control:focus {
            border-color: #2196F3;
            box-shadow: 0 0 0 0.2rem rgba(33, 150, 243, 0.25);
        }
        .alert {
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .support-info {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="logo">🏛️</div>
        <h2 class="system-title">FONTES</h2>
        <p class="subtitle">Sistema INSS v3.0 - Portal Web</p>
        
        <div id="alert" class="alert d-none"></div>
        
        <form id="loginForm">
            <div class="mb-3">
                <label class="form-label">👤 Usuário:</label>
                <input type="text" class="form-control" id="username" required placeholder="Digite seu usuário">
            </div>
            
            <div class="mb-3">
                <label class="form-label">🔒 Senha:</label>
                <input type="password" class="form-control" id="password" required placeholder="Digite sua senha">
            </div>
            
            <button type="submit" class="btn-login">
                🔓 ENTRAR NO SISTEMA
            </button>
        </form>
        
        <div class="support-info">
            💬 Suporte: suporte@fontes.inss.gov.br<br>
            📞 (11) 99999-9999
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const alertDiv = document.getElementById('alert');
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alertDiv.className = 'alert alert-success';
                    alertDiv.textContent = data.message;
                    alertDiv.classList.remove('d-none');
                    setTimeout(() => window.location.href = '/dashboard', 1500);
                } else {
                    alertDiv.className = 'alert alert-danger';
                    alertDiv.textContent = data.message;
                    alertDiv.classList.remove('d-none');
                }
            } catch (error) {
                alertDiv.className = 'alert alert-danger';
                alertDiv.textContent = 'Erro de conexão';
                alertDiv.classList.remove('d-none');
            }
        });
    </script>
</body>
</html>
'''

# Template HTML integrado - Dashboard
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Sistema FONTES</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .navbar {
            background: rgba(0,0,0,0.3) !important;
            backdrop-filter: blur(10px);
        }
        .navbar-brand {
            font-weight: bold;
            font-size: 24px;
        }
        .service-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .service-card:hover {
            transform: translateY(-10px);
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .service-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        .service-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #4CAF50;
        }
        .service-desc {
            color: #ccc;
            font-size: 14px;
        }
        .page-title {
            text-align: center;
            margin: 40px 0;
            color: #4CAF50;
            font-weight: bold;
        }
        .footer {
            text-align: center; 
            padding: 40px;
            color: #ccc;
            font-size: 14px;
        }
        .btn-logout {
            background: #f44336;
            border: none;
            border-radius: 10px;
        }
        .btn-logout:hover {
            background: #d32f2f;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                🏛️ FONTES <small class="text-muted">v3.0</small>
            </a>
            
            <div class="navbar-nav ms-auto">
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👤 {{ user_name }}
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#" onclick="showProfile()">⚙️ Perfil</a></li>
                        <li><a class="dropdown-item" href="#" onclick="showSupport()">🆘 Suporte</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="/logout">🚪 Sair</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container py-4">
        <h1 class="page-title">📋 SELECIONE UMA CATEGORIA DE SERVIÇOS</h1>
        
        <div class="row g-4">
            <!-- Aposentadoria -->
            <div class="col-md-4">
                <div class="service-card" onclick="openService('aposentadoria', 'Aposentadoria', '👨‍🦳')">
                    <div class="service-icon">👨‍🦳</div>
                    <div class="service-title">Aposentadoria</div>
                    <div class="service-desc">Solicitações e consultas de aposentadoria por idade, tempo de contribuição e invalidez</div>
                </div>
            </div>
            
            <!-- Maternidade -->
            <div class="col-md-4">
                <div class="service-card" onclick="openService('maternidade', 'Maternidade', '🤱')">
                    <div class="service-icon">🤱</div>
                    <div class="service-title">Maternidade</div>
                    <div class="service-desc">Benefícios de maternidade, paternidade e auxílio para gestantes</div>
                </div>
            </div>
            
            <!-- Arquivos -->
            <div class="col-md-4">
                <div class="service-card" onclick="openService('arquivos', 'Arquivos', '📁')">
                    <div class="service-icon">📁</div>
                    <div class="service-title">Arquivos</div>
                    <div class="service-desc">Gestão completa de documentos, upload de arquivos e relatórios</div>
                </div>
            </div>
            
            <!-- Meu INSS -->
            <div class="col-md-4">
                <div class="service-card" onclick="openMeuINSS()">
                    <div class="service-icon">🏢</div>
                    <div class="service-title">Meu INSS</div>
                    <div class="service-desc">Acesso direto ao portal oficial do INSS</div>
                </div>
            </div>
            
            <!-- Suporte -->
            <div class="col-md-4">
                <div class="service-card" onclick="openService('suporte', 'Suporte', '🛠️')">
                    <div class="service-icon">🛠️</div>
                    <div class="service-title">Suporte</div>
                    <div class="service-desc">Atendimento técnico, tutoriais e perguntas frequentes</div>
                </div>
            </div>
            
            <!-- Solicitar Serviço -->
            <div class="col-md-4">
                <div class="service-card" onclick="openService('servicos', 'Solicitar Serviço', '📋')">
                    <div class="service-icon">📋</div>
                    <div class="service-title">Solicitar Serviço</div>
                    <div class="service-desc">Solicitações diversas e acompanhamento de processos</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        © 2025 Sistema FONTES v3.0 - Hospedado no Render.com
    </div>

    <!-- Modal -->
    <div class="modal fade" id="serviceModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-white">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalTitle"></h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="modalBody">
                    <!-- Content loaded here -->
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function openService(serviceId, serviceName, icon) {
            document.getElementById('modalTitle').innerHTML = icon + ' ' + serviceName;
            document.getElementById('modalBody').innerHTML = `
                <div class="text-center">
                    <div style="font-size: 64px; margin-bottom: 20px;">${icon}</div>
                    <h4>Funcionalidade em Desenvolvimento</h4>
                    <p>Este serviço será implementado em breve.</p>
                    <p><strong>Serviço:</strong> ${serviceName}</p>
                    <div class="mt-4">
                        <small class="text-muted">
                            💬 Para mais informações, entre em contato:<br>
                            📧 suporte@fontes.inss.gov.br<br>
                            📞 (11) 99999-9999
                        </small>
                    </div>
                </div>
            `;
            new bootstrap.Modal(document.getElementById('serviceModal')).show();
        }
        
        function openMeuINSS() {
            window.open('https://meu.inss.gov.br/', '_blank');
        }
        
        function showProfile() {
            alert('⚙️ Configurações do perfil\\n\\nFuncionalidade em desenvolvimento');
        }
        
        function showSupport() {
            alert('🆘 Central de Suporte\\n\\n📞 (11) 99999-9999\\n📧 suporte@fontes.inss.gov.br\\n💬 Chat online em breve');
        }
    </script>
</body>
</html>
'''

# Usuários do sistema
USERS = {
    'admin': {
        'password': 'admin123',
        'name': 'Administrador do Sistema',
        'role': 'admin'
    },
    'usuario': {
        'password': '123456', 
        'name': 'Usuário Padrão',
        'role': 'user'
    },
    'demo': {
        'password': 'demo123',
        'name': 'Usuário Demonstração',
        'role': 'user'
    }
}

@app.route('/')
def index():
    """Página inicial"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login do sistema"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').lower().strip()
        password = data.get('password', '').strip()
        
        if username in USERS and USERS[username]['password'] == password:
            session['user_id'] = username
            session['user_name'] = USERS[username]['name'] 
            session['user_role'] = USERS[username]['role']
            
            return jsonify({
                'success': True,
                'message': f'Bem-vindo, {USERS[username]["name"]}!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Usuário ou senha inválidos'
            }), 401
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                user_name=session.get('user_name', 'Usuário'))

@app.route('/logout')
def logout():
    """Logout do sistema"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health():
    """Health check para o Render"""
    return jsonify({
        'status': 'healthy',
        'version': '3.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/status')
def api_status():
    """API de status"""
    return jsonify({
        'status': 'online',
        'version': '3.0',
        'environment': os.environ.get('RENDER', 'local'),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
