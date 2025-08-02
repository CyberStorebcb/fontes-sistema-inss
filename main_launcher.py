#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Launcher Principal
Versão simplificada e robusta
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox
import time

# Configurar path para recursos empacotados
if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    # Desenvolvimento
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adicionar diretórios ao path
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

def check_dependencies():
    """Verificar se as dependências estão disponíveis"""
    try:
        import customtkinter
        return True, None
    except ImportError as e:
        return False, str(e)

def show_simple_loading():
    """Mostrar splash screen simples"""
    splash = tk.Tk()
    splash.title("FONTES v3.0")
    splash.geometry("350x150")
    splash.resizable(False, False)
    splash.configure(bg="#1a1a1a")
    
    # Centralizar
    splash.eval('tk::PlaceWindow . center')
    
    # Conteúdo
    title = tk.Label(
        splash, 
        text="🏛️ Sistema FONTES v3.0", 
        font=("Arial", 14, "bold"),
        fg="white", bg="#1a1a1a"
    )
    title.pack(pady=20)
    
    status = tk.Label(
        splash,
        text="Iniciando sistema...",
        font=("Arial", 10),
        fg="#cccccc", bg="#1a1a1a"
    )
    status.pack(pady=10)
    
    # Atualizar e aguardar
    splash.update()
    time.sleep(1.5)
    
    status.config(text="Carregando interface...")
    splash.update()
    time.sleep(1)
    
    splash.destroy()

def main():
    """Função principal do sistema"""
    try:
        print("🏛️ Iniciando Sistema FONTES v3.0...")
        
        # Verificar dependências
        deps_ok, error = check_dependencies()
        if not deps_ok:
            messagebox.showerror(
                "Dependências Ausentes",
                f"CustomTkinter não está disponível:\n{error}\n\n"
                "Execute: pip install customtkinter"
            )
            return
        
        # Mostrar loading
        show_simple_loading()
        
        # Importar após verificação
        import customtkinter as ctk
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Verificar sessão
        session_file = os.path.join(BASE_DIR, "session.dat")
        has_session = os.path.exists(session_file)
        
        if has_session:
            print("🔑 Sessão encontrada, carregando interface principal...")
            try:
                from views.fontes_interface import FontesMainWindow
                app = FontesMainWindow()
                app.run()
            except Exception as e:
                print(f"Erro ao carregar interface: {e}")
                # Fallback para login
                has_session = False
        
        if not has_session:
            print("🚪 Carregando tela de login...")
            
            def on_login_success(user_data):
                print(f"✅ Login bem-sucedido: {user_data.get('full_name', 'Usuário')}")
                try:
                    from views.fontes_interface import FontesMainWindow
                    app = FontesMainWindow()
                    app.run()
                except Exception as e:
                    print(f"Erro ao carregar interface principal: {e}")
                    messagebox.showerror(
                        "Erro de Interface",
                        f"Erro ao carregar interface principal:\n{e}"
                    )
            
            try:
                from auth.login_clean import show_login_window
                login_window = show_login_window(on_login_success)
                if login_window:
                    login_window.mainloop()
                else:
                    print("Erro: Não foi possível criar janela de login")
            except Exception as e:
                print(f"Erro ao carregar login: {e}")
                messagebox.showerror(
                    "Erro de Login",
                    f"Erro ao carregar tela de login:\n{e}"
                )
                    
    except ImportError as e:
        messagebox.showerror(
            "Erro de Módulo",
            f"Erro ao importar módulos necessários:\n{e}\n\n"
            "Verifique se todos os arquivos estão presentes."
        )
        print(f"Erro de importação: {e}")
        
    except Exception as e:
        messagebox.showerror(
            "Erro Crítico", 
            f"Erro inesperado no sistema:\n{e}\n\n"
            "Entre em contato com o suporte técnico."
        )
        print(f"Erro crítico: {e}")

if __name__ == "__main__":
    main()
