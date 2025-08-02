#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Servidor Web Simples
Versão funcional para hospedagem imediata
"""
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import os
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Template HTML integrado
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Sistema FONTES</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            color: white;
        }
        .login-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            width: 400px;
            text-align: center;
        }
        .logo {
            font-size: 64px;
            margin-bottom: 20px;
        }
        h1 {
            color: #4CAF50;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #ccc;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="text"]::placeholder, input[type="password"]::placeholder {
            color: #ccc;
        }
        .btn-login {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn-login:hover {
            background: linear-gradient(45deg, #45a049, #3d8b40);
        }
        .support {
            margin-top: 30px;
            font-size: 14px;
            color: #ccc;
        }
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 10px;
            display: none;
        }
        .alert-error {
            background: rgba(244, 67, 54, 0.2);
            border: 1px solid #f44336;
            color: #ffcdd2;
        }
        .alert-success {
            background: rgba(76, 175, 80, 0.2);
            border: 1px solid #4CAF50;
            color: #c8e6c9;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🏛️</div>
        <h1>FONTES</h1>
        <p class="subtitle">Sistema INSS v3.0</p>
        
        <div id="alert" class="alert"></div>
        
        <form id="loginForm" onsubmit="login(event)">
            <div class="form-group">
                <label>👤 Usuário:</label>
                <input type="text" id="username" required placeholder="Digite seu usuário">
            </div>
            
            <div class="form-group">
                <label>🔒 Senha:</label>
                <input type="password" id="password" required placeholder="Digite sua senha">
            </div>
            
            <button type="submit" class="btn-login">
                🔓 ENTRAR NO SISTEMA
            </button>
        </form>
        
        <div class="support">
            💬 Problemas? Contate o suporte<br>
            📞 (11) 99999-9999
        </div>
    </div>

    <script>
        function showAlert(message, type) {
            const alert = document.getElementById('alert');
            alert.textContent = message;
            alert.className = `alert alert-${type}`;
            alert.style.display = 'block';
            
            if (type === 'success') {
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            }
        }

        async function login(event) {
            event.preventDefault();
            
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
                    showAlert(data.message, 'success');
                } else {
                    showAlert(data.message, 'error');
                }
            } catch (error) {
                showAlert('Erro de conexão', 'error');
            }
        }
    </script>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Sistema FONTES</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            margin: 0;
            color: white;
        }
        .header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .logo h1 {
            margin: 0;
            color: #4CAF50;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .main-content {
            padding: 40px 20px;
            text-align: center;
        }
        .page-title {
            font-size: 32px;
            margin-bottom: 40px;
            color: #4CAF50;
        }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .service-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease;
            border: 2px solid transparent;
        }
        .service-card:hover {
            transform: translateY(-10px);
            border-color: #4CAF50;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .service-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        .service-title {
            font-size: 24px;
            margin-bottom: 10px;
            color: #4CAF50;
        }
        .service-desc {
            color: #ccc;
            font-size: 16px;
        }
        .btn-logout {
            background: #f44336;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
        }
        .btn-logout:hover {
            background: #d32f2f;
        }
        .footer {
            text-align: center;
            padding: 40px;
            color: #ccc;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <span style="font-size: 32px;">🏛️</span>
            <h1>FONTES</h1>
        </div>
        <div class="user-menu">
            <span>👤 {{ user_name }}</span>
            <a href="/logout" class="btn-logout">🚪 Sair</a>
        </div>
    </div>

    <div class="main-content">
        <h2 class="page-title">📋 SELECIONE UMA CATEGORIA DE SERVIÇOS</h2>
        
        <div class="services-grid">
            <div class="service-card" onclick="openService('aposentadoria')">
                <div class="service-icon">👨‍🦳</div>
                <div class="service-title">Aposentadoria</div>
                <div class="service-desc">Solicitações de aposentadoria</div>
            </div>
            
            <div class="service-card" onclick="openService('maternidade')">
                <div class="service-icon">🤱</div>
                <div class="service-title">Maternidade</div>
                <div class="service-desc">Benefícios de maternidade</div>
            </div>
            
            <div class="service-card" onclick="openService('arquivos')">
                <div class="service-icon">📁</div>
                <div class="service-title">Arquivos</div>
                <div class="service-desc">Gestão de documentos</div>
            </div>
            
            <div class="service-card" onclick="openService('meu_inss')">
                <div class="service-icon">🏢</div>
                <div class="service-title">Meu INSS</div>
                <div class="service-desc">Portal do INSS</div>
            </div>
            
            <div class="service-card" onclick="openService('suporte')">
                <div class="service-icon">🛠️</div>
                <div class="service-title">Suporte</div>
                <div class="service-desc">Atendimento técnico</div>
            </div>
            
            <div class="service-card" onclick="openService('servicos')">
                <div class="service-icon">📋</div>
                <div class="service-title">Solicitar Serviço</div>
                <div class="service-desc">Novas solicitações</div>
            </div>
        </div>
    </div>

    <div class="footer">
        © 2025 Sistema FONTES v3.0 - Todos os direitos reservados
    </div>

    <script>
        function openService(serviceId) {
            alert('🚧 Funcionalidade em desenvolvimento\\n\\nServiço: ' + serviceId + '\\n\\nEsta funcionalidade será implementada em breve.');
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
    }
}

@app.route('/')
def index():
    """Página inicial - redireciona para login ou dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').lower()
        password = data.get('password', '')
        
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
    
    return render_template_string(DASHBOARD_TEMPLATE, user_name=session.get('user_name', 'Usuário'))

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/status')
def api_status():
    """API de status do sistema"""
    return jsonify({
        'status': 'online',
        'version': '3.0',
        'timestamp': datetime.now().isoformat(),
        'users_online': len([s for s in [session] if 'user_id' in s])
    })

if __name__ == '__main__':
    print("🏛️ Sistema FONTES v3.0 - Servidor Web")
    print("=" * 45)
    print("🚀 Servidor iniciando...")
    print("📱 Acesso local: http://localhost:5000")
    print("🌍 Acesso rede: http://[SEU_IP]:5000")
    print("👤 Logins disponíveis:")
    print("   • admin / admin123 (Administrador)")
    print("   • usuario / 123456 (Usuário padrão)")
    print("=" * 45)
    print("⚠️  Para parar: Ctrl+C")
    print()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Servidor finalizado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no servidor: {e}")
        input("Pressione Enter para sair...")
