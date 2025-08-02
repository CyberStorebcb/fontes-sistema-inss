#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Launcher Unificado
Ponto de entrada principal que detecta e executa a interface adequada
"""
import sys
import os
import argparse
from pathlib import Path

# Configurar path do projeto
BASE_DIR = Path(__file__).parent.absolute()
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

def check_gui_dependencies() -> bool:
    """Verificar dependências para interface gráfica"""
    try:
        import customtkinter
        import tkinter
        return True
    except ImportError:
        return False

def check_web_dependencies() -> bool:
    """Verificar dependências para interface web"""
    try:
        import flask
        return True
    except ImportError:
        return False

def run_gui_mode():
    """Executar modo interface gráfica"""
    if not check_gui_dependencies():
        print("❌ Dependências GUI ausentes. Execute: pip install customtkinter")
        return False
    
    try:
        # Importar e executar launcher GUI
        from main_launcher import main as launcher_main
        launcher_main()
        return True
    except Exception as e:
        print(f"❌ Erro ao executar interface gráfica: {e}")
        return False

def run_web_mode():
    """Executar modo servidor web"""
    if not check_web_dependencies():
        print("❌ Dependências Web ausentes. Execute: pip install flask")
        return False
    
    try:
        # Importar e executar servidor web
        from app import app
        print("🌐 Iniciando servidor web...")
        print("📍 Acesse: http://localhost:5000")
        app.run(
            host='0.0.0.0', 
            port=5000, 
            debug=False,
            use_reloader=False
        )
        return True
    except Exception as e:
        print(f"❌ Erro ao executar servidor web: {e}")
        return False

def run_console_mode():
    """Executar modo console para testes"""
    print("🖥️  Sistema FONTES v3.0 - Modo Console")
    print("=" * 50)
    
    try:
        # Importar sistema de autenticação
        from auth.authentication import auth_system
        
        # Verificar sistema
        print("✅ Sistema de autenticação carregado")
        print("✅ Banco de dados acessível")
        
        # Menu simples
        while True:
            print("\n📋 Opções disponíveis:")
            print("1. Testar login")
            print("2. Listar usuários")
            print("3. Sair")
            
            choice = input("\n👉 Escolha uma opção: ").strip()
            
            if choice == "1":
                username = input("Usuário: ").strip()
                password = input("Senha: ").strip()
                
                result = auth_system.authenticate(username, password)
                success, message, user_data = result
                
                if success:
                    print(f"✅ Login bem-sucedido: {user_data}")
                else:
                    print(f"❌ Login falhou: {message}")
            
            elif choice == "2":
                print("\n👥 Funcionalidade de listagem de usuários não implementada")
                print("💡 Use o painel administrativo na interface gráfica")
            
            elif choice == "3":
                print("👋 Saindo...")
                break
            
            else:
                print("❌ Opção inválida")
    
    except Exception as e:
        print(f"❌ Erro no modo console: {e}")
        return False
    
    return True

def main():
    """Função principal com detecção automática de modo"""
    print("🏛️ Sistema FONTES v3.0 - Iniciando...")
    
    # Parser de argumentos
    parser = argparse.ArgumentParser(description="Sistema FONTES v3.0")
    parser.add_argument(
        '--mode', 
        choices=['gui', 'web', 'console', 'auto'],
        default='auto',
        help='Modo de execução (padrão: auto)'
    )
    
    args = parser.parse_args()
    mode = args.mode
    
    # Detecção automática do melhor modo
    if mode == 'auto':
        if check_gui_dependencies():
            mode = 'gui'
            print("🖼️  Detectado: Modo Interface Gráfica")
        elif check_web_dependencies():
            mode = 'web'
            print("🌐 Detectado: Modo Servidor Web")
        else:
            mode = 'console'
            print("🖥️  Detectado: Modo Console")
    
    # Executar modo selecionado
    success = False
    
    if mode == 'gui':
        print("🚀 Iniciando interface gráfica...")
        success = run_gui_mode()
    
    elif mode == 'web':
        print("🚀 Iniciando servidor web...")
        success = run_web_mode()
    
    elif mode == 'console':
        print("🚀 Iniciando modo console...")
        success = run_console_mode()
    
    if not success:
        print("❌ Falha na inicialização do sistema")
        sys.exit(1)

if __name__ == "__main__":
    main()
