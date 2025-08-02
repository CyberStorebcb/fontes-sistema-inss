#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Launcher Principal
Ponto de entrada para o executável
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# Configurar path para recursos empacotados
if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
else:
    # Desenvolvimento
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adicionar diretórios ao path
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

def main():
    """Função principal do sistema"""
    try:
        print("🏛️ Iniciando Sistema FONTES v3.0...")
        
        # Configurar tema padrão
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Verificar se há sessão salva
        session_file = os.path.join(BASE_DIR, "session.dat")
        has_session = os.path.exists(session_file)
        
        if has_session:
            print("🔑 Sessão encontrada, carregando interface principal...")
            # Carregar interface principal diretamente
            from views.fontes_interface import FontesMainWindow
            app = FontesMainWindow()
            app.run()
        else:
            print("🚪 Carregando tela de login...")
            # Carregar tela de login
            from auth.login_clean import show_login_window
            
            def on_login_success(user_data):
                print(f"✅ Login bem-sucedido: {user_data.get('full_name', 'Usuário')}")
                # Carregar interface principal após login
                from views.fontes_interface import FontesMainWindow
                app = FontesMainWindow()
                app.run()
            
            login_window = show_login_window(on_login_success)
            login_window.mainloop()
            
    except ImportError as e:
        messagebox.showerror(
            "Erro de Módulo",
            f"Erro ao importar módulos necessários:\n{e}\n\n"
            "Verifique se todos os arquivos estão presentes."
        )
    except Exception as e:
        messagebox.showerror(
            "Erro Crítico", 
            f"Erro inesperado no sistema:\n{e}\n\n"
            "Entre em contato com o suporte técnico."
        )

if __name__ == "__main__":
    main()
