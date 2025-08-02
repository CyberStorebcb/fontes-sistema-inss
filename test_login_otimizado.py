#!/usr/bin/env python3
"""
Teste OTIMIZADO - Interface de Login com Botão Visível
Sistema FONTES v3.0
"""
import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.auth.login_interface import show_login_window

def on_success(user_data):
    """Callback de sucesso do login"""
    print(f"✅ Login realizado com sucesso!")
    print(f"Usuário: {user_data.get('username', 'N/A')}")
    print(f"Nome: {user_data.get('full_name', 'N/A')}")

if __name__ == "__main__":
    print("🏛️  SISTEMA FONTES - INTERFACE OTIMIZADA")
    print("=" * 60)
    print("🚀 Inicializando interface de login OTIMIZADA...")
    print("📏 Dimensões da janela: 600x900 pixels")
    print("🎯 OBJETIVO: BOTÃO 'ENTRAR' CLARAMENTE VISÍVEL!")
    print("=" * 60)
    print("📝 Credenciais para teste:")
    print("   👤 Usuário: admin")
    print("   🔐 Senha: admin123")
    print("=" * 60)
    print("✅ MELHORIAS IMPLEMENTADAS:")
    print("   • Janela maior (600x900px)")
    print("   • Layout compacto para maximizar espaço")
    print("   • Botão ENTRAR destacado (70px altura)")
    print("   • Redimensionamento permitido")
    print("   • Espaçamentos otimizados")
    print("=" * 60)
    
    try:
        # Mostrar janela de login
        login_window = show_login_window(on_success)
        login_window.mainloop()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("Pressione Enter para sair...")
