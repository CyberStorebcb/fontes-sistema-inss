"""
Interface de Login - Sistema FONTES v3.0
Versão corrigida e otimizada
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading
import time
from typing import Optional, Callable

# Configurar path
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from auth.authentication import auth_system

class LoginWindow(ctk.CTk):
    """Janela de login otimizada e robusta"""
    
    def __init__(self, on_success_callback: Optional[Callable] = None):
        super().__init__()
        
        self.on_success_callback = on_success_callback
        self.login_attempts = 0
        self.password_visible = False
        
        # Configurações da janela
        self.title("🏛️ FONTES - Sistema INSS v3.0")
        self.geometry("500x650")
        self.resizable(False, False)
        
        # Configurar tema
        try:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
        except Exception as e:
            print(f"Aviso: Erro ao configurar tema: {e}")
        
        # Centralizar janela
        self.center_window()
        
        # Proteger contra fechamento inesperado
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar interface
        self.setup_ui()
        
        # Focar no campo de usuário após inicialização
        self.after(200, self.focus_username)
    
    def center_window(self):
        """Centralizar janela na tela com tratamento de erro"""
        try:
            self.update_idletasks()
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            
            window_width = 500
            window_height = 650
            
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        except Exception as e:
            print(f"Aviso: Erro ao centralizar janela: {e}")
    
    def focus_username(self):
        """Focar no campo de usuário com tratamento de erro"""
        try:
            if hasattr(self, 'username_entry'):
                self.username_entry.focus_set()
        except Exception as e:
            print(f"Aviso: Erro ao focar campo: {e}")
    
    def on_closing(self):
        """Tratar fechamento da janela"""
        try:
            self.quit()
            self.destroy()
        except Exception as e:
            print(f"Erro ao fechar janela: {e}")
    
    def setup_ui(self):
        """Configurar interface principal"""
        try:
            # Frame principal
            main_frame = ctk.CTkFrame(self, fg_color=("gray10", "gray15"))
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Componentes
            self.create_header(main_frame)
            self.create_login_form(main_frame)
            self.create_footer(main_frame)
            
        except Exception as e:
            print(f"Erro ao configurar UI: {e}")
            messagebox.showerror("Erro", f"Erro ao configurar interface: {e}")
    
    def create_header(self, parent):
        """Criar cabeçalho"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 30))
        
        # Ícone
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🏛️",
            font=ctk.CTkFont(size=60, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        icon_label.pack(pady=(0, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="FONTES",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        title_label.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sistema INSS v3.0",
            font=ctk.CTkFont(size=14),
            text_color=("gray70", "gray50")
        )
        subtitle_label.pack()
    
    def create_login_form(self, parent):
        """Criar formulário de login"""
        form_frame = ctk.CTkFrame(
            parent,
            fg_color=("gray15", "gray20"),
            corner_radius=15,
            border_width=1,
            border_color=("#2196F3", "#1976D2")
        )
        form_frame.pack(fill="x", pady=20, padx=10)
        
        # Container interno
        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título do formulário
        form_title = ctk.CTkLabel(
            form_content,
            text="Acesso ao Sistema",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        form_title.pack(pady=(0, 20))
        
        # Campo usuário
        username_label = ctk.CTkLabel(
            form_content,
            text="👤 Nome de Usuário:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Digite seu nome de usuário",
            font=ctk.CTkFont(size=12),
            height=40
        )
        self.username_entry.pack(fill="x", pady=(0, 15))
        self.username_entry.bind("<Return>", self.focus_password)
        
        # Campo senha
        password_label = ctk.CTkLabel(
            form_content,
            text="🔒 Senha:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        # Frame para senha
        password_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 20))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Digite sua senha",
            font=ctk.CTkFont(size=12),
            height=40,
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.password_entry.bind("<Return>", self.on_enter_pressed)
        
        # Botão mostrar/ocultar senha
        self.toggle_password_btn = ctk.CTkButton(
            password_frame,
            text="👁️",
            width=40,
            height=40,
            command=self.toggle_password_visibility,
            font=ctk.CTkFont(size=14)
        )
        self.toggle_password_btn.pack(side="right")
        
        # Botão de login
        self.login_btn = ctk.CTkButton(
            form_content,
            text="🔓 ENTRAR",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            command=self.attempt_login,
            fg_color=("#2196F3", "#1976D2"),
            hover_color=("#1976D2", "#1565C0")
        )
        self.login_btn.pack(fill="x", pady=(5, 15))
        
        # Status
        self.status_label = ctk.CTkLabel(
            form_content,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("orange", "yellow")
        )
        self.status_label.pack()
    
    def create_footer(self, parent):
        """Criar rodapé"""
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="© 2024 Sistema FONTES v3.0 - Todos os direitos reservados",
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray40")
        )
        footer_label.pack()
    
    def focus_password(self, event=None):
        """Focar no campo de senha"""
        try:
            self.password_entry.focus_set()
        except Exception as e:
            print(f"Erro ao focar senha: {e}")
    
    def on_enter_pressed(self, event=None):
        """Executar login ao pressionar Enter"""
        self.attempt_login()
    
    def toggle_password_visibility(self):
        """Alternar visibilidade da senha"""
        try:
            self.password_visible = not self.password_visible
            if self.password_visible:
                self.password_entry.configure(show="")
                self.toggle_password_btn.configure(text="🙈")
            else:
                self.password_entry.configure(show="*")
                self.toggle_password_btn.configure(text="👁️")
        except Exception as e:
            print(f"Erro ao alternar visibilidade da senha: {e}")
    
    def attempt_login(self):
        """Tentar fazer login"""
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            
            if not username or not password:
                self.status_label.configure(
                    text="⚠️ Preencha todos os campos",
                    text_color=("red", "orange")
                )
                return
            
            # Desabilitar botão durante tentativa
            self.login_btn.configure(state="disabled", text="Verificando...")
            self.status_label.configure(
                text="🔄 Verificando credenciais...",
                text_color=("blue", "cyan")
            )
            self.update()
            
            # Realizar autenticação (retorna Tuple[bool, str, Optional[Dict]])
            result = auth_system.authenticate(username, password)
            success, message, user_data = result
            
            if success and user_data:
                self.status_label.configure(
                    text="✅ Login realizado com sucesso!",
                    text_color=("green", "lightgreen")
                )
                self.update()
                
                # Chamar callback de sucesso
                if self.on_success_callback:
                    self.on_success_callback(user_data)
                
                # Fechar janela
                self.after(1000, self.on_closing)
            else:
                self.login_attempts += 1
                error_msg = message or 'Credenciais inválidas'
                
                self.status_label.configure(
                    text=f"❌ {error_msg} (Tentativa {self.login_attempts}/3)",
                    text_color=("red", "orange")
                )
                
                if self.login_attempts >= 3:
                    messagebox.showerror(
                        "Acesso Bloqueado",
                        "Muitas tentativas de login.\nTente novamente mais tarde."
                    )
                    self.on_closing()
                
                # Limpar campo senha
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus_set()
        
        except Exception as e:
            self.status_label.configure(
                text=f"❌ Erro: {str(e)[:50]}...",
                text_color=("red", "orange")  
            )
            print(f"Erro no login: {e}")
        finally:
            # Reabilitar botão
            self.login_btn.configure(state="normal", text="🔓 ENTRAR")

def show_login_window(on_success_callback: Optional[Callable] = None) -> Optional[LoginWindow]:
    """Mostrar janela de login"""
    try:
        # Configurar CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Criar e retornar janela
        login_window = LoginWindow(on_success_callback)
        return login_window
        
    except Exception as e:
        print(f"Erro ao criar janela de login: {e}")
        messagebox.showerror("Erro", f"Erro ao inicializar login: {e}")
        return None

# Para compatibilidade com versões antigas
if __name__ == "__main__":
    def test_callback(user_data):
        print(f"Login de teste bem-sucedido: {user_data}")
    
    window = show_login_window(test_callback)
    if window:
        window.mainloop()
