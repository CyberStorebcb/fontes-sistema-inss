#!/usr/bin/env python3
"""
Teste da Interface de Login Limpa - Sistema FONTES v3.0
"""
import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.auth.login_clean import show_login_window

def on_success(user_data):
    """Callback de sucesso do login"""
    print(f"✅ Login realizado com sucesso!")
    print(f"Usuário: {user_data.get('username', 'N/A')}")
    print(f"Nome: {user_data.get('full_name', 'N/A')}")

if __name__ == "__main__":
    print("🏛️  FONTES - Sistema INSS v3.0")
    print("=" * 50)
    print("🚀 Inicializando interface de login LIMPA...")
    print("📝 Credenciais para teste:")
    print("   👤 Usuário: admin")
    print("   🔐 Senha: admin123")
    print("=" * 50)
    print("🔍 VERIFICAÇÃO: O botão 'ENTRAR NO SISTEMA' deve estar claramente visível!")
    print("=" * 50)
    
    try:
        # Mostrar janela de login
        login_window = show_login_window(on_success)
        login_window.mainloop()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("Pressione Enter para sair...")
