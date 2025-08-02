#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Deploy Completo
Script unificado para todas as opções de hospedagem
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

class FontesDeployer:
    """Deploy completo do Sistema FONTES"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.system = platform.system().lower()
        
    def show_menu(self):
        """Mostrar menu de opções"""
        print("🏛️  SISTEMA FONTES v3.0 - DEPLOY COMPLETO")
        print("=" * 50)
        print("Escolha uma opção de hospedagem:")
        print()
        print("1️⃣  💻 Executável Standalone (.exe)")
        print("2️⃣  🌐 Servidor Web Local (Flask)")
        print("3️⃣  🐳 Container Docker")
        print("4️⃣  ☁️  Hospedagem na Nuvem")
        print("5️⃣  📱 Aplicativo Mobile (PWA)")
        print("6️⃣  🔧 Configurar Ambiente")
        print("0️⃣  ❌ Sair")
        print()
        
    def deploy_executable(self):
        """Deploy como executável"""
        print("💻 Criando executável standalone...")
        
        if not os.path.exists("setup_executable.py"):
            print("❌ setup_executable.py não encontrado!")
            return False
            
        try:
            subprocess.run([sys.executable, "setup_executable.py"], check=True)
            print("✅ Executável criado com sucesso!")
            print("📁 Localize o arquivo .exe na pasta 'dist'")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar executável: {e}")
            return False
    
    def deploy_web_server(self):
        """Deploy como servidor web"""
        print("🌐 Configurando servidor web...")
        
        if not os.path.exists("setup_web_server.py"):
            print("❌ setup_web_server.py não encontrado!")
            return False
            
        try:
            subprocess.run([sys.executable, "setup_web_server.py"], check=True)
            print("✅ Servidor web configurado!")
            print("🚀 Execute 'start_server.bat' para iniciar")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao configurar servidor: {e}")
            return False
    
    def deploy_docker(self):
        """Deploy com Docker"""
        print("🐳 Configurando container Docker...")
        
        # Verificar Docker
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker não instalado!")
            print("📥 Instale Docker Desktop: https://docker.com/products/docker-desktop")
            return False
        
        # Construir imagem
        try:
            print("🔨 Construindo imagem Docker...")
            subprocess.run(["docker", "build", "-t", "fontes-system", "."], check=True)
            
            print("🚀 Iniciando container...")
            subprocess.run([
                "docker", "run", "-d", 
                "--name", "fontes-app",
                "-p", "5000:5000",
                "fontes-system"
            ], check=True)
            
            print("✅ Container Docker executando!")
            print("🌐 Acesse: http://localhost:5000")
            print("👤 Login: admin / admin123")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro no Docker: {e}")
            return False
    
    def deploy_cloud(self):
        """Configurar deploy na nuvem"""
        print("☁️  Opções de hospedagem na nuvem:")
        print()
        print("1️⃣  Google Cloud Run (Gratuito até certo limite)")
        print("2️⃣  AWS Lambda + API Gateway")
        print("3️⃣  DigitalOcean App Platform ($5/mês)")
        print("4️⃣  Heroku (Descontinuado - usar alternativas)")
        print("5️⃣  Railway ($5/mês)")
        print("6️⃣  Render (Gratuito com limitações)")
        print()
        
        choice = input("Escolha uma opção (1-6): ").strip()
        
        if choice == "1":
            self.setup_google_cloud()
        elif choice == "2":
            self.setup_aws()
        elif choice == "3":
            self.setup_digitalocean()
        elif choice == "5":
            self.setup_railway()
        elif choice == "6":
            self.setup_render()
        else:
            print("❌ Opção inválida")
            return False
    
    def setup_google_cloud(self):
        """Configurar Google Cloud Run"""
        print("🌐 Google Cloud Run - Deploy Gratuito")
        print()
        print("📋 Passos necessários:")
        print("1. Crie uma conta no Google Cloud Platform")
        print("2. Instale o gcloud CLI")
        print("3. Execute os comandos abaixo:")
        print()
        print("```bash")
        print("gcloud auth login")
        print("gcloud config set project SEU_PROJECT_ID")
        print("gcloud run deploy fontes-system \\")
        print("  --source . \\")
        print("  --port 5000 \\")
        print("  --region us-central1 \\")
        print("  --allow-unauthenticated")
        print("```")
        print()
        print("🎯 Resultado: URL pública para acesso global")
    
    def setup_aws(self):
        """Configurar AWS"""
        print("🌐 AWS Lambda + API Gateway")
        print()
        print("📋 Requer conversão para Serverless:")
        print("1. Instale: pip install zappa")
        print("2. Configure: zappa init")
        print("3. Deploy: zappa deploy production")
        print()
        print("💰 Custo: ~$0.20/mês para uso normal")
    
    def setup_digitalocean(self):
        """Configurar DigitalOcean"""
        print("🌐 DigitalOcean App Platform")
        print()
        print("📋 Passos:")
        print("1. Crie conta no DigitalOcean")
        print("2. Conecte repositório GitHub")
        print("3. Configure:")
        print("   - Build Command: pip install -r requirements.txt")
        print("   - Run Command: python app.py")
        print("   - Port: 5000")
        print()
        print("💰 Custo: $5/mês (Basic Plan)")
    
    def setup_railway(self):
        """Configurar Railway"""
        print("🌐 Railway - Deploy Simples")
        print()
        print("📋 Passos:")
        print("1. Conecte GitHub no Railway.app")
        print("2. Deploy automático detecta Python")
        print("3. Ambiente configurado automaticamente")
        print()
        print("💰 Custo: $5/mês após trial gratuito")
    
    def setup_render(self):
        """Configurar Render"""
        print("🌐 Render - Hospedagem Gratuita")
        print()
        print("📋 Passos:")
        print("1. Conecte GitHub no Render.com")
        print("2. Configure:")
        print("   - Build Command: pip install -r requirements.txt")
        print("   - Start Command: python app.py")
        print()
        print("⚠️  Limitações gratuitas: Sleep após inatividade")
    
    def create_pwa(self):
        """Criar Progressive Web App"""
        print("📱 Criando PWA (Progressive Web App)...")
        
        # Criar manifest.json
        manifest = {
            "name": "Sistema FONTES",
            "short_name": "FONTES",
            "description": "Sistema INSS - Versão 3.0",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#1976D2",
            "theme_color": "#1976D2",
            "icons": [
                {
                    "src": "/static/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "/static/icon-512.png", 
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        
        import json
        with open("web_server/static/manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Service Worker básico
        sw_content = '''
// Service Worker - Sistema FONTES PWA
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('fontes-v1').then(cache => {
      return cache.addAll([
        '/',
        '/static/css/style.css',
        '/static/js/app.js',
        '/static/manifest.json'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
'''
        
        with open("web_server/static/sw.js", "w") as f:
            f.write(sw_content)
        
        print("✅ PWA configurada!")
        print("📱 Usuários podem instalar como app no celular")
    
    def configure_environment(self):
        """Configurar ambiente de desenvolvimento"""
        print("🔧 Configurando ambiente...")
        
        # Instalar dependências
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            
            packages = [
                "customtkinter",
                "flask", 
                "flask-socketio",
                "pyinstaller",
                "waitress",
                "gunicorn"
            ]
            
            for package in packages:
                print(f"📦 Instalando {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            
            print("✅ Ambiente configurado com sucesso!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro na configuração: {e}")
            return False
    
    def run(self):
        """Executar interface principal"""
        while True:
            self.show_menu()
            choice = input("Digite sua escolha (0-6): ").strip()
            
            if choice == "0":
                print("👋 Até logo!")
                break
            elif choice == "1":
                self.deploy_executable()
            elif choice == "2":
                self.deploy_web_server()
            elif choice == "3":
                self.deploy_docker()
            elif choice == "4":
                self.deploy_cloud()
            elif choice == "5":
                self.create_pwa()
            elif choice == "6":
                self.configure_environment()
            else:
                print("❌ Opção inválida!")
            
            input("\nPressione Enter para continuar...")
            print("\n" * 2)

if __name__ == "__main__":
    deployer = FontesDeployer()
    deployer.run()
