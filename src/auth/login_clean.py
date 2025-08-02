"""
Interface de Login - Sistema FONTES v3.0
Versão simplificada com botão garantidamente visível
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
    """Janela de login simples com botão garantidamente visível"""
    
    def __init__(self, on_success_callback: Optional[Callable] = None):
        super().__init__()
        
        self.on_success_callback = on_success_callback
        self.login_attempts = 0
        self.password_visible = False
        
        # Configurações da janela
        self.title("🏛️ FONTES - Sistema INSS v3.0")
        self.geometry("500x700")  # Tamanho otimizado
        self.resizable(False, False)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
        # Focar no campo de usuário
        self.after(100, lambda: self.username_entry.focus())
    
    def center_window(self):
        """Centralizar janela na tela"""
        self.update_idletasks()
        
        window_width = 500
        window_height = 700
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def setup_ui(self):
        """Configurar interface simplificada"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color=("gray10", "gray15"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header com ícone e título
        self.create_header(main_frame)
        
        # Formulário de login
        self.create_login_form(main_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Criar cabeçalho com ícone centralizado"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 30))
        
        # Ícone centralizado
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🏛️",
            font=ctk.CTkFont(size=70, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        icon_label.pack(pady=(0, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="FONTES",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        title_label.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sistema INSS v3.0",
            font=ctk.CTkFont(size=16),
            text_color=("gray70", "gray50")
        )
        subtitle_label.pack()
    
    def create_login_form(self, parent):
        """Criar formulário de login com botão visível"""
        form_frame = ctk.CTkFrame(
            parent,
            fg_color=("gray15", "gray20"),
            corner_radius=15,
            border_width=2,
            border_color=("#2196F3", "#1976D2")
        )
        form_frame.pack(fill="x", pady=30, padx=20)
        
        # Container interno com padding
        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Título do formulário
        form_title = ctk.CTkLabel(
            form_content,
            text="Acesso ao Sistema",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        form_title.pack(pady=(0, 25))
        
        # Campo usuário
        username_label = ctk.CTkLabel(
            form_content,
            text="👤 Nome de Usuário:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Digite seu nome de usuário",
            font=ctk.CTkFont(size=14),
            height=45
        )
        self.username_entry.pack(fill="x", pady=(0, 15))
        
        # Campo senha
        password_label = ctk.CTkLabel(
            form_content,
            text="🔒 Senha:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        # Container para senha e botão
        password_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 20))
        password_frame.grid_columnconfigure(0, weight=1)
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Digite sua senha",
            font=ctk.CTkFont(size=14),
            height=45,
            show="●"
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Botão mostrar/ocultar senha
        self.toggle_btn = ctk.CTkButton(
            password_frame,
            text="👁️",
            width=45,
            height=45,
            command=self.toggle_password
        )
        self.toggle_btn.grid(row=0, column=1)
        
        # Checkbox lembrar
        self.remember_var = ctk.BooleanVar()
        remember_check = ctk.CTkCheckBox(
            form_content,
            text="Manter conectado",
            variable=self.remember_var,
            font=ctk.CTkFont(size=12)
        )
        remember_check.pack(pady=(0, 25))
        
        # BOTÃO ENTRAR - GARANTIDAMENTE VISÍVEL
        self.login_button = ctk.CTkButton(
            form_content,
            text="🔓 ENTRAR NO SISTEMA",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=55,
            corner_radius=12,
            fg_color=("#2196F3", "#1976D2"),
            hover_color=("#1976D2", "#0D47A1"),
            border_width=2,
            border_color=("#64B5F6", "#42A5F5"),
            command=self.login
        )
        self.login_button.pack(fill="x", pady=(0, 20))
        
        # Status
        self.status_label = ctk.CTkLabel(
            form_content,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("#2196F3", "#64B5F6")
        )
        self.status_label.pack()
        
        # Bind eventos
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
    
    def create_footer(self, parent):
        """Criar rodapé"""
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        footer_frame.pack(fill="x", pady=20)
        
        help_label = ctk.CTkLabel(
            footer_frame,
            text="💬 Precisa de ajuda? Contate o suporte",
            font=ctk.CTkFont(size=12),
            text_color=("#2196F3", "#64B5F6"),
            cursor="hand2"
        )
        help_label.pack(pady=(0, 10))
        help_label.bind("<Button-1>", self.show_help)
        
        version_label = ctk.CTkLabel(
            footer_frame,
            text="© 2025 Sistema FONTES - INSS v3.0",
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50")
        )
        version_label.pack()
    
    def toggle_password(self):
        """Alternar visibilidade da senha"""
        if self.password_visible:
            self.password_entry.configure(show="●")
            self.toggle_btn.configure(text="👁️")
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="🙈")
            self.password_visible = True
    
    def login(self):
        """Realizar login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validação básica
        if not username or not password:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        # Mostrar status
        self.status_label.configure(text="⚡ Autenticando...")
        self.login_button.configure(text="🔄 AGUARDE...", state="disabled")
        
        # Simular autenticação
        def authenticate():
            try:
                success, message, user_data = auth_system.authenticate(username, password, "127.0.0.1")
                self.after(1000, lambda: self.handle_result(success, message, user_data))
            except Exception as e:
                self.after(0, lambda: self.handle_error(str(e)))
        
        threading.Thread(target=authenticate, daemon=True).start()
    
    def handle_result(self, success, message, user_data):
        """Tratar resultado da autenticação"""
        self.status_label.configure(text="")
        self.login_button.configure(text="🔓 ENTRAR NO SISTEMA", state="normal")
        
        if success and user_data:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user_data.get('full_name', 'Usuário')}!")
            self.destroy()
            if self.on_success_callback:
                self.on_success_callback(user_data)
        else:
            messagebox.showerror("Erro", message or "Credenciais inválidas")
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
    
    def handle_error(self, error):
        """Tratar erro"""
        self.status_label.configure(text="")
        self.login_button.configure(text="🔓 ENTRAR NO SISTEMA", state="normal")
        messagebox.showerror("Erro", f"Erro interno: {error}")
    
    def show_help(self, event=None):
        """Mostrar ajuda"""
        messagebox.showinfo(
            "Suporte Técnico",
            "📞 Telefone: (11) 99999-9999\n"
            "📧 Email: suporte@fontes.inss.gov.br\n"
            "💬 Chat: Online 24/7\n\n"
            "Credenciais para teste:\n"
            "👤 Usuário: admin\n"
            "🔐 Senha: admin123"
        )

def show_login_window(on_success_callback: Optional[Callable] = None) -> LoginWindow:
    """Mostrar janela de login"""
    login_window = LoginWindow(on_success_callback)
    return login_window
