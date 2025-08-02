"""
Interface de Login - Sistema FONTES v3.0
Tela de autenticação com design moderno e profissional
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading

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
    """Janela de login do sistema com design profissional"""
    
    def __init__(self, on_success_callback: Optional[Callable] = None):
        super().__init__()
        
        self.on_success_callback = on_success_callback
        self.login_attempts = 0
        self.max_attempts = 999  # Desabilitado - número alto para não bloquear
        self._pulse_direction = 1  # Adicionar atributo para animação
        self.password_visible = False  # Estado da visibilidade da senha
        
        # Configurações da janela - LAYOUT OTIMIZADO PARA BOTÃO VISÍVEL
        self.title("🏛️ FONTES - Sistema INSS v3.0")
        self.geometry("600x900")  # Janela maior para garantir espaço suficiente
        self.resizable(True, True)  # Permitir redimensionamento se necessário
        self.minsize(500, 700)     # Tamanho mínimo para garantir visibilidade
        
        # Centralizar janela
        self.center_window()
        
        # Configurar tema escuro moderno
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configurar ícone (se existir)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass
        
        self.setup_ui()
        self.apply_animations()
        
        # Focar no campo de usuário
        self.after(100, lambda: self.username_entry.focus())
    
    def center_window(self):
        """Centralizar janela na tela de forma robusta"""
        self.update_idletasks()
        
        # Obter dimensões da janela - OTIMIZADO PARA VISIBILIDADE DO BOTÃO
        window_width = 600
        window_height = 900
        
        # Obter dimensões da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posição central
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Garantir que não fique fora da tela
        x = max(0, x)
        y = max(0, y)
        
        # Aplicar posicionamento
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def setup_ui(self):
        """Configurar interface do usuário com design profissional"""
        # Frame principal com gradiente simulado
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color=("gray10", "gray15"),
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Container interno com padding REDUZIDO para mais espaço
        self.content_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header com logo/título
        self.create_modern_header()
        
        # Formulário de login moderno
        self.create_modern_login_form()
        
        # Rodapé elegante
        self.create_modern_footer()
    
    def create_modern_header(self):
        """Criar cabeçalho COMPACTO e elegante"""
        # Container do header com espaçamento REDUZIDO
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))  # Reduzido de 40 para 20
        
        # Container para centralizar o ícone
        icon_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        icon_container.pack(expand=True, fill="x", pady=(0, 15))  # Reduzido de 30 para 15
        
        # Ícone principal perfeitamente centralizado - TAMANHO REDUZIDO
        self.logo_label = ctk.CTkLabel(
            icon_container,
            text="🏛️",
            font=ctk.CTkFont(size=60, weight="bold"),  # Reduzido de 80 para 60
            text_color=("#2196F3", "#64B5F6"),
            anchor="center"
        )
        self.logo_label.pack(expand=True, fill="x")
        
        # Título principal - TAMANHO REDUZIDO
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="FONTES",
            font=ctk.CTkFont(size=32, weight="bold"),  # Reduzido de 42 para 32
            text_color=("#2196F3", "#64B5F6")
        )
        self.title_label.pack(pady=(0, 5))  # Reduzido de 8 para 5
        
        # Subtítulo com mais informações - TAMANHO REDUZIDO
        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sistema INSS v3.0",
            font=ctk.CTkFont(size=14, weight="normal"),  # Reduzido de 18 para 14
            text_color=("gray70", "gray50")
        )
        self.subtitle_label.pack(pady=(0, 3))  # Reduzido de 5 para 3
        
        # Linha decorativa - MAIS FINA
        self.separator_line = ctk.CTkFrame(
            header_frame,
            height=2,  # Reduzido de 3 para 2
            fg_color=("#2196F3", "#1976D2"),
            corner_radius=2
        )
        self.separator_line.pack(fill="x", padx=60, pady=(10, 0))  # Reduzido padding
    
    def create_modern_login_form(self):
        """Criar formulário OTIMIZADO para visibilidade do botão"""
        # Frame do formulário - design elegante com espaçamento OTIMIZADO
        self.form_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=("gray15", "gray20"),
            corner_radius=20,
            border_width=2,
            border_color=("#2196F3", "#1976D2")
        )
        self.form_frame.pack(fill="x", pady=(0, 15))  # Reduzido de 30 para 15
        
        # Padding interno REDUZIDO para maximizar espaço
        self.form_content = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.form_content.pack(fill="both", expand=True, padx=25, pady=25)  # Reduzido de 40 para 25
        
        # Título do formulário - COMPACTO
        self.form_title = ctk.CTkLabel(
            self.form_content,
            text="Acesso ao Sistema",
            font=ctk.CTkFont(size=20, weight="bold"),  # Reduzido de 24 para 20
            text_color=("#2196F3", "#64B5F6")
        )
        self.form_title.pack(pady=(0, 20))  # Reduzido de 35 para 20
        
        # Campo de usuário com ícone - COMPACTO
        self.create_username_field()
        
        # Campo de senha com botão mostrar/ocultar - COMPACTO
        self.create_password_field()
        
        # Checkbox "Lembrar-me" - COMPACTO
        self.remember_var = ctk.BooleanVar()
        self.remember_checkbox = ctk.CTkCheckBox(
            self.form_content,
            text="Manter conectado",  # Texto mais curto
            variable=self.remember_var,
            font=ctk.CTkFont(size=12),  # Reduzido de 14 para 12
            text_color=("gray70", "gray50"),
            checkbox_width=18,  # Reduzido de 20 para 18
            checkbox_height=18,  # Reduzido de 20 para 18
            corner_radius=4
        )
        self.remember_checkbox.pack(pady=(15, 15))  # Reduzido espaçamento
        
        # BOTÃO ENTRAR - GARANTIDAMENTE VISÍVEL E DESTACADO
        self.login_button = ctk.CTkButton(
            self.form_content,
            text="🔓 ENTRAR NO SISTEMA",
            font=ctk.CTkFont(size=22, weight="bold"),  # Aumentado para 22
            height=70,  # Aumentado para 70px
            corner_radius=15,
            fg_color=("#2196F3", "#1976D2"),
            hover_color=("#1976D2", "#0D47A1"),
            border_width=4,  # Aumentado para 4px
            border_color=("#64B5F6", "#42A5F5"),
            text_color="white",
            command=self.login
        )
        self.login_button.pack(fill="x", pady=(10, 15), padx=5)  # Espaçamento otimizado
        
        # Indicadores de status - COMPACTOS
        self.create_status_indicators()
    
    def create_username_field(self):
        """Criar campo de usuário COMPACTO"""
        # Label com ícone - COMPACTO
        username_container = ctk.CTkFrame(self.form_content, fg_color="transparent")
        username_container.pack(fill="x", pady=(0, 12))  # Reduzido de 20 para 12
        
        self.username_label = ctk.CTkLabel(
            username_container,
            text="👤 Nome de Usuário:",
            font=ctk.CTkFont(size=14, weight="bold"),  # Reduzido de 16 para 14
            anchor="w",
            text_color=("gray80", "gray60")
        )
        self.username_label.pack(fill="x", pady=(0, 5))  # Reduzido de 8 para 5
        
        # Entry moderno - COMPACTO
        self.username_entry = ctk.CTkEntry(
            username_container,
            placeholder_text="Digite seu nome de usuário",
            font=ctk.CTkFont(size=14),  # Reduzido de 16 para 14
            height=45,  # Reduzido de 50 para 45
            corner_radius=12,
            border_width=2,
            border_color=("gray50", "gray40"),
            fg_color=("gray95", "gray10"),
            text_color=("gray10", "white")
        )
        self.username_entry.pack(fill="x")
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.username_entry.bind("<FocusIn>", self.on_username_focus)
        self.username_entry.bind("<FocusOut>", self.on_username_unfocus)
    
    def create_password_field(self):
        """Criar campo de senha COMPACTO"""
        # Label com ícone - COMPACTO
        password_container = ctk.CTkFrame(self.form_content, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 15))  # Reduzido de 25 para 15
        
        self.password_label = ctk.CTkLabel(
            password_container,
            text="🔒 Senha:",
            font=ctk.CTkFont(size=14, weight="bold"),  # Reduzido de 16 para 14
            anchor="w",
            text_color=("gray80", "gray60")
        )
        self.password_label.pack(fill="x", pady=(0, 5))  # Reduzido de 8 para 5
        
        # Container para entrada e botão
        password_input_frame = ctk.CTkFrame(password_container, fg_color="transparent")
        password_input_frame.pack(fill="x")
        password_input_frame.grid_columnconfigure(0, weight=1)
        
        # Entry de senha - COMPACTO
        self.password_entry = ctk.CTkEntry(
            password_input_frame,
            placeholder_text="Digite sua senha",
            font=ctk.CTkFont(size=14),  # Reduzido de 16 para 14
            height=45,  # Reduzido de 50 para 45
            corner_radius=12,
            border_width=2,
            border_color=("gray50", "gray40"),
            fg_color=("gray95", "gray10"),
            text_color=("gray10", "white"),
            show="●"
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))  # Reduzido espaçamento
        self.password_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<FocusIn>", self.on_password_focus)
        self.password_entry.bind("<FocusOut>", self.on_password_unfocus)
        
        # Botão mostrar/ocultar senha - COMPACTO
        self.toggle_password_btn = ctk.CTkButton(
            password_input_frame,
            text="👁️",
            font=ctk.CTkFont(size=16),  # Reduzido de 18 para 16
            width=45,  # Reduzido de 50 para 45
            height=45,  # Reduzido de 50 para 45
            corner_radius=12,
            fg_color=("gray70", "gray30"),
            hover_color=("#2196F3", "#1976D2"),
            command=self.toggle_password_visibility
        )
        self.toggle_password_btn.grid(row=0, column=1)
    
    def create_status_indicators(self):
        """Criar indicadores de status elegantes"""
        # Indicador de carregamento
        self.loading_label = ctk.CTkLabel(
            self.form_content,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("#2196F3", "#64B5F6")
        )
        self.loading_label.pack(pady=(10, 5))
        
        # Status de tentativas
        self.attempts_label = ctk.CTkLabel(
            self.form_content,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#FF5722", "#FF8A65")
        )
        self.attempts_label.pack(pady=(0, 10))
    
    def create_modern_footer(self):
        """Criar rodapé COMPACTO"""
        # Frame do footer - ESPAÇAMENTO REDUZIDO
        footer_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(10, 0))  # Reduzido de 20 para 10
        
        # Link para ajuda/suporte - COMPACTO
        self.help_label = ctk.CTkLabel(
            footer_frame,
            text="💬 Precisa de ajuda?",  # Texto mais curto
            font=ctk.CTkFont(size=11, weight="bold"),  # Reduzido de 13 para 11
            text_color=("#2196F3", "#64B5F6"),
            cursor="hand2"
        )
        self.help_label.pack(pady=(5, 5))  # Reduzido espaçamento
        self.help_label.bind("<Button-1>", self.show_admin_info)
        self.help_label.bind("<Enter>", lambda e: self.help_label.configure(text_color=("#1976D2", "#42A5F5")))
        self.help_label.bind("<Leave>", lambda e: self.help_label.configure(text_color=("#2196F3", "#64B5F6")))
        
        # Informações do sistema - COMPACTAS
        self.version_label = ctk.CTkLabel(
            footer_frame,
            text="© 2025 FONTES v3.0",  # Texto mais curto
            font=ctk.CTkFont(size=9),  # Reduzido de 11 para 9
            text_color=("gray60", "gray50"),
            justify="center"
        )
        self.version_label.pack()
    
    def toggle_password_visibility(self):
        """Alternar visibilidade da senha"""
        if self.password_visible:
            # Ocultar senha
            self.password_entry.configure(show="●")
            self.toggle_password_btn.configure(text="👁️", fg_color=("gray70", "gray30"))
            self.password_visible = False
        else:
            # Mostrar senha
            self.password_entry.configure(show="")
            self.toggle_password_btn.configure(text="🙈", fg_color=("#FF9800", "#F57C00"))
            self.password_visible = True
    
    def on_username_focus(self, event):
        """Evento de foco no campo de usuário"""
        self.username_entry.configure(border_color=("#2196F3", "#64B5F6"))
        self.username_label.configure(text_color=("#2196F3", "#64B5F6"))
    
    def on_username_unfocus(self, event):
        """Evento quando usuário perde foco"""
        self.username_entry.configure(border_color=("gray50", "gray40"))
        self.username_label.configure(text_color=("gray80", "gray60"))
    
    def on_password_focus(self, event):
        """Evento de foco no campo de senha"""
        self.password_entry.configure(border_color=("#2196F3", "#64B5F6"))
        self.password_label.configure(text_color=("#2196F3", "#64B5F6"))
    
    def on_password_unfocus(self, event):
        """Evento quando senha perde foco"""
        self.password_entry.configure(border_color=("gray50", "gray40"))
        self.password_label.configure(text_color=("gray80", "gray60"))
    
    def apply_animations(self):
        """Aplicar animações modernas de entrada"""
        # Fade in effect mais suave
        self.attributes("-alpha", 0.0)
        self.modern_fade_in()
        
        # Animação do logo mais elegante
        self.animate_modern_logo()
        
        # Animação da linha decorativa
        self.animate_separator()
    
    def modern_fade_in(self, alpha=0.0):
        """Efeito fade in moderno e suave"""
        if alpha < 1.0:
            alpha += 0.03  # Mais suave
            self.attributes("-alpha", alpha)
            self.after(25, lambda: self.modern_fade_in(alpha))
    
    def animate_modern_logo(self):
        """Animação pulsante moderna do logo"""
        def pulse():
            if hasattr(self, 'logo_label'):
                current_size = 80
                if hasattr(self, '_pulse_direction'):
                    if self._pulse_direction == "up":
                        if current_size < 85:
                            self.logo_label.configure(font=ctk.CTkFont(size=current_size + 1, weight="bold"))
                        else:
                            self._pulse_direction = "down"
                    else:
                        if current_size > 75:
                            self.logo_label.configure(font=ctk.CTkFont(size=current_size - 1, weight="bold"))
                        else:
                            self._pulse_direction = "up"
                else:
                    self._pulse_direction = "up"
                
                self.after(150, pulse)
        
        self.after(1500, pulse)  # Iniciar após 1.5 segundos
    
    def animate_separator(self):
        """Animar linha decorativa"""
        def expand_line():
            if hasattr(self, 'separator_line'):
                # Expandir de 0 para 100% da largura
                self.separator_line.pack(fill="x", padx=0, pady=(15, 0))
        
        self.after(800, expand_line)
    
    def show_loading(self, show: bool, message: str = ""):
        """Mostrar/ocultar indicador de carregamento moderno"""
        if show:
            self.loading_label.configure(text=f"⚡ {message}")
            self.login_button.configure(
                state="disabled", 
                text="🔄 AUTENTICANDO...",
                fg_color=("gray50", "gray40")
            )
            # Adicionar efeito visual de carregamento
            self.animate_loading()
        else:
            self.loading_label.configure(text="")
            self.login_button.configure(
                state="normal", 
                text="🔓 ENTRAR NO SISTEMA",
                fg_color=("#2196F3", "#1976D2")
            )
    
    def animate_loading(self):
        """Animação de carregamento no botão"""
        loading_chars = ["⚡", "⭐", "✨", "💫"]
        counter = 0
        
        def rotate():
            nonlocal counter
            if self.login_button.cget("state") == "disabled":
                char = loading_chars[counter % len(loading_chars)]
                self.login_button.configure(text=f"{char} AUTENTICANDO...")
                counter += 1
                self.after(300, rotate)
        
        rotate()
    
    def update_attempts_status(self):
        """Atualizar status das tentativas"""
        if self.login_attempts > 0:
            remaining = self.max_attempts - self.login_attempts
            if remaining > 0:
                self.attempts_label.configure(
                    text=f"⚠️ Tentativas restantes: {remaining}"
                )
            else:
                self.attempts_label.configure(
                    text="🚫 Muitas tentativas. Tente novamente mais tarde."
                )
        else:
            self.attempts_label.configure(text="")
    
    def validate_fields(self) -> bool:
        """Validar campos do formulário"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showerror("Erro", "Por favor, digite o nome de usuário")
            self.username_entry.focus()
            return False
        
        if not password:
            messagebox.showerror("Erro", "Por favor, digite a senha")
            self.password_entry.focus()
            return False
        
        if len(username) < 3:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 3 caracteres")
            self.username_entry.focus()
            return False
        
        return True
    
    def login(self):
        """Realizar login"""
        if not self.validate_fields():
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Mostrar carregamento
        self.show_loading(True, "Autenticando...")
        
        # Executar autenticação em thread separada
        def authenticate():
            try:
                success, message, user_data = auth_system.authenticate(username, password, "127.0.0.1")
                
                # Atualizar UI na thread principal
                self.after(500, lambda: self.handle_login_result(success, message, user_data))
                
            except Exception as e:
                self.after(0, lambda: self.handle_login_error(str(e)))
        
        thread = threading.Thread(target=authenticate, daemon=True)
        thread.start()
    
    def handle_login_result(self, success: bool, message: str, user_data: Optional[dict]):
        """Tratar resultado do login"""
        self.show_loading(False)
        
        if success and user_data:
            # Login bem-sucedido
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user_data['full_name']}!")
            
            # Salvar sessão se "lembrar-me" estiver marcado
            if self.remember_var.get():
                self.save_session_token()
            
            # Fechar janela de login
            self.destroy()
            
            # Chamar callback de sucesso
            if self.on_success_callback:
                self.on_success_callback(user_data)
        
        else:
            # Login falhou
            self.login_attempts += 1
            self.update_attempts_status()
            
            # Limpar senha
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
            
            messagebox.showerror("Erro de Autenticação", message)
    
    def handle_login_error(self, error_message: str):
        """Tratar erro de login"""
        self.show_loading(False)
        messagebox.showerror("Erro", f"Erro interno: {error_message}")
    
    def reset_attempts(self):
        """Resetar tentativas de login"""
        self.login_attempts = 0
        self.login_button.configure(state="normal")
        self.update_attempts_status()
    
    def save_session_token(self):
        """Salvar token de sessão para lembrar login"""
        try:
            session_file = os.path.join(os.path.dirname(__file__), "..", "..", "session.dat")
            if auth_system.session_token:
                with open(session_file, "w") as f:
                    f.write(auth_system.session_token)
        except Exception as e:
            print(f"Erro ao salvar sessão: {e}")
    
    def show_admin_info(self, event=None):
        """Mostrar informações do administrador com design moderno"""
        # Criar janela de diálogo personalizada
        admin_window = ctk.CTkToplevel(self)
        admin_window.title("🆘 Suporte Técnico")
        admin_window.geometry("450x400")
        admin_window.resizable(False, False)
        admin_window.transient(self)
        admin_window.grab_set()
        
        # Centralizar janela
        admin_window.update_idletasks()
        x = (admin_window.winfo_screenwidth() // 2) - (225)
        y = (admin_window.winfo_screenheight() // 2) - (200)
        admin_window.geometry(f"450x400+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(admin_window, fg_color=("gray10", "gray15"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Ícone
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🆘",
            font=ctk.CTkFont(size=50),
            text_color=("#2196F3", "#64B5F6")
        )
        icon_label.pack(pady=(0, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="Central de Suporte",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        title_label.pack()
        
        # Informações
        info_text = (
            "📞 Telefone: (11) 99999-9999\n"
            "📧 Email: suporte@fontes.inss.gov.br\n"
            "💬 Chat: Online 24/7\n"
            "🌐 Portal: www.fontes.inss.gov.br\n\n"
            "Para problemas de acesso, recuperação de senha\n"
            "ou suporte técnico, utilize um dos canais acima.\n\n"
            "Nosso horário de atendimento:\n"
            "Segunda a Sexta: 8h às 18h\n"
            "Sábado: 8h às 12h"
        )
        
        info_label = ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            text_color=("gray80", "gray60"),
            justify="center"
        )
        info_label.pack(pady=20)
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            main_frame,
            text="✅ Entendi",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color=("#2196F3", "#1976D2"),
            hover_color=("#1976D2", "#0D47A1"),
            command=admin_window.destroy
        )
        close_btn.pack(pady=(20, 0))

def show_login_window(on_success_callback: Optional[Callable] = None) -> LoginWindow:
    """Mostrar janela de login"""
    login_window = LoginWindow(on_success_callback)
    return login_window
