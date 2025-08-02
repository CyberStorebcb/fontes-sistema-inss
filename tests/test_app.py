"""
Sistema FONTES v3.0 - Testes Automatizados
Módulo de testes para validação da aplicação Flask
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import json

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app, USERS
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que o arquivo app.py está no diretório correto")
    sys.exit(1)

def validate_user(username, password):
    """Função auxiliar para validar usuário"""
    return username in USERS and USERS[username]['password'] == password

def is_valid_user(username):
    """Função auxiliar para verificar se usuário existe"""
    return username in USERS if username else False


class TestFONTESSystem(unittest.TestCase):
    """Classe de testes para o Sistema FONTES"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = self.app.test_client()
        
        # Context para testes que precisam de sessão
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        self.app_context.pop()
    
    def test_home_page(self):
        """Teste da página inicial"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect para login
    
    def test_login_page_get(self):
        """Teste da página de login (GET)"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FONTES', response.data)
        self.assertIn(b'ENTRAR NO SISTEMA', response.data)
    
    def test_login_valid_credentials(self):
        """Teste de login com credenciais válidas"""
        response = self.client.post('/login', 
            data=json.dumps({'username': 'admin', 'password': 'admin123'}),
            content_type='application/json',
            follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    def test_login_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        response = self.client.post('/login',
            data=json.dumps({'username': 'invalid', 'password': 'invalid'}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_login_empty_fields(self):
        """Teste de login com campos vazios"""
        response = self.client.post('/login',
            data=json.dumps({'username': '', 'password': ''}),
            content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_dashboard_without_login(self):
        """Teste de acesso ao dashboard sem login"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect para login
    
    def test_dashboard_with_login(self):
        """Teste de acesso ao dashboard com login"""
        # Primeiro faz login
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['usuario'] = 'admin'
        
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Bem-vindo', response.data)
    
    def test_logout(self):
        """Teste de logout"""
        # Primeiro faz login
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['usuario'] = 'admin'
        
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout realizado com sucesso', response.data)
    
    def test_health_check(self):
        """Teste do endpoint de health check"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_api_status(self):
        """Teste do endpoint de status da API"""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'online')
        self.assertEqual(data['version'], '3.0')
        self.assertIn('timestamp', data)
    
    def test_validate_user_function(self):
        """Teste da função validate_user"""
        # Testa usuários válidos
        self.assertTrue(validate_user('admin', 'admin123'))
        self.assertTrue(validate_user('demo', 'demo123'))
        self.assertTrue(validate_user('usuario', '123456'))
        
        # Testa usuários inválidos
        self.assertFalse(validate_user('invalid', 'invalid'))
        self.assertFalse(validate_user('admin', 'wrongpass'))
        self.assertFalse(validate_user('', ''))
        self.assertFalse(validate_user(None, None))
    
    def test_is_valid_user_function(self):
        """Teste da função is_valid_user"""
        self.assertTrue(is_valid_user('admin'))
        self.assertTrue(is_valid_user('demo'))
        self.assertTrue(is_valid_user('user'))
        self.assertFalse(is_valid_user('invalid'))
        self.assertFalse(is_valid_user(''))
        self.assertFalse(is_valid_user(None))
    
    def test_session_management(self):
        """Teste de gerenciamento de sessão"""
        # Testa login e criação de sessão
        response = self.client.post('/login', data={
            'usuario': 'admin',
            'senha': 'admin123'
        })
        
        with self.client.session_transaction() as sess:
            self.assertIn('user_id', sess)
            self.assertIn('usuario', sess)
            self.assertEqual(sess['usuario'], 'admin')
    
    def test_csrf_protection(self):
        """Teste de proteção CSRF (quando habilitada)"""
        # Este teste verificaria a proteção CSRF em produção
        pass
    
    def test_error_404(self):
        """Teste de página não encontrada"""
        response = self.client.get('/pagina-inexistente')
        self.assertEqual(response.status_code, 404)
    
    def test_security_headers(self):
        """Teste de headers de segurança"""
        response = self.client.get('/')
        
        # Verifica se não há informações sensíveis nos headers
        self.assertNotIn('Server', response.headers)
        # Em produção, deveria ter headers de segurança como:
        # X-Frame-Options, X-Content-Type-Options, etc.


class TestIntegration(unittest.TestCase):
    """Testes de integração"""
    
    def setUp(self):
        """Configuração para testes de integração"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_full_user_flow(self):
        """Teste do fluxo completo do usuário"""
        # 1. Acessa página inicial
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # 2. Vai para login
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        
        # 3. Faz login
        response = self.client.post('/login', data={
            'usuario': 'admin',
            'senha': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        
        # 4. Acessa dashboard
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        
        # 5. Faz logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_api_endpoints(self):
        """Teste dos endpoints da API"""
        # Health check
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        # Status
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)


class TestPerformance(unittest.TestCase):
    """Testes de performance básicos"""
    
    def setUp(self):
        """Configuração para testes de performance"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_response_time(self):
        """Teste de tempo de resposta básico"""
        import time
        
        start_time = time.time()
        response = self.client.get('/')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 2.0)  # Resposta em menos de 2 segundos
    
    def test_concurrent_requests(self):
        """Teste básico de requisições concorrentes"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = self.client.get('/')
            results.append(response.status_code)
        
        # Cria 10 threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=make_request)
            threads.append(t)
        
        # Inicia todas as threads
        start_time = time.time()
        for t in threads:
            t.start()
        
        # Espera todas terminarem
        for t in threads:
            t.join()
        
        end_time = time.time()
        
        # Verifica resultados
        self.assertEqual(len(results), 10)
        self.assertTrue(all(status == 200 for status in results))
        self.assertLess(end_time - start_time, 5.0)  # Todas em menos de 5 segundos


def run_tests():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 EXECUTANDO TESTES DO SISTEMA FONTES v3.0")
    print("=" * 60)
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(TestFONTESSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️  Erros: {len(result.errors)}")
    
    if result.failures:
        print("\n🔴 FALHAS:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n🔴 ERROS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return True
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
