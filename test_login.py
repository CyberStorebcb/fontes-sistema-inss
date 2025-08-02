#!/usr/bin/env python3
"""
Teste da Nova Interface de Login
"""
import sys
import os

# Adicionar path do projeto
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

auth_dir = os.path.join(src_dir, "auth")
if auth_dir not in sys.path:
    sys.path.append(auth_dir)

from login_interface import show_login_window

def on_login_success(user_data):
    """Callback de sucesso do login"""
    print(f"Login realizado com sucesso! Usuário: {user_data['full_name']}")

if __name__ == "__main__":
    print("🏛️ Testando Nova Interface de Login - FONTES v3.0")
    print("=" * 50)
    print("Credenciais de teste:")
    print("Usuário: admin")
    print("Senha: admin123")
    print("=" * 50)
    
    # Mostrar interface de login
    login_window = show_login_window(on_login_success)
    login_window.mainloop()
    
    print("Teste da interface de login finalizado!")
