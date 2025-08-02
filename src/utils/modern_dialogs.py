"""
Diálogos Modernos - Sistema FONTES
Diálogos personalizados com design moderno e animações melhoradas
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Optional, Callable, Literal, List
import math

class ModernDialog(ctk.CTkToplevel):
    """Diálogo moderno personalizado com qualidade gráfica melhorada"""
    
    def __init__(self, 
                 parent,
                 title: str = "Aviso",
                 message: str = "",
                 dialog_type: Literal["info", "success", "warning", "error", "question"] = "info",
                 buttons: Optional[List[str]] = None,
                 width: int = 450,
                 height: int = 250,
                 callback: Optional[Callable] = None):
        
        super().__init__(parent)
        
        self.parent_window = parent
        self.callback = callback
        self.result = None
        self.animation_running = False
        self.dialog_type = dialog_type
        
        # Configurar janela com melhor qualidade
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Melhorar aparência da janela
        self.configure(fg_color=("#f0f0f0", "#1a1a1a"))
        
        # Centralizar
        self.center_window()
        
        # Configurar estilo baseado no tipo
        self.colors = self.get_colors_for_type(dialog_type)
        self.icon = self.get_icon_for_type(dialog_type)
        
        # Configurar botões padrão se não especificados
        if buttons is None:
            if dialog_type == "question":
                buttons = ["Sim", "Não"]
            else:
                buttons = ["OK"]
        
        self.buttons = buttons
        
        # Criar interface
        self.setup_ui(title, message)
        self.apply_entrance_animation()
        
        # Protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Focar na janela
        self.focus()

    def center_window(self):
        """Centralizar janela na tela"""
        self.update_idletasks()
        
        # Obter dimensões da janela pai se existir
        if self.parent_window:
            parent_x = self.parent_window.winfo_rootx()
            parent_y = self.parent_window.winfo_rooty()
            parent_width = self.parent_window.winfo_width()
            parent_height = self.parent_window.winfo_height()
            
            # Centralizar sobre a janela pai
            x = parent_x + (parent_width // 2) - (self.winfo_reqwidth() // 2)
            y = parent_y + (parent_height // 2) - (self.winfo_reqheight() // 2)
        else:
            # Centralizar na tela
            x = (self.winfo_screenwidth() // 2) - (self.winfo_reqwidth() // 2)
            y = (self.winfo_screenheight() // 2) - (self.winfo_reqheight() // 2)
        
        self.geometry(f"+{x}+{y}")

    def get_colors_for_type(self, dialog_type: str) -> dict:
        """Obter esquema de cores melhorado baseado no tipo de diálogo"""
        colors = {
            "info": {
                "primary": "#1976D2",          # Azul mais elegante
                "secondary": "#E3F2FD",        # Fundo suave
                "icon_bg": "#1565C0",          # Azul escuro para contraste
                "text": "#0D47A1",            # Texto azul escuro
                "accent": "#42A5F5",          # Azul claro para destaques
                "shadow": "#1976D240"         # Sombra sutil
            },
            "success": {
                "primary": "#388E3C",          # Verde mais profissional
                "secondary": "#E8F5E8",        # Fundo verde suave
                "icon_bg": "#2E7D32",          # Verde escuro
                "text": "#1B5E20",            # Texto verde escuro
                "accent": "#66BB6A",          # Verde claro
                "shadow": "#388E3C40"
            },
            "warning": {
                "primary": "#F57C00",          # Laranja mais vibrante
                "secondary": "#FFF3E0",        # Fundo laranja suave
                "icon_bg": "#EF6C00",          # Laranja escuro
                "text": "#E65100",            # Texto laranja escuro
                "accent": "#FF9800",          # Laranja médio
                "shadow": "#F57C0040"
            },
            "error": {
                "primary": "#D32F2F",          # Vermelho mais elegante
                "secondary": "#FFEBEE",        # Fundo vermelho suave
                "icon_bg": "#C62828",          # Vermelho escuro
                "text": "#B71C1C",            # Texto vermelho escuro
                "accent": "#EF5350",          # Vermelho claro
                "shadow": "#D32F2F40"
            },
            "question": {
                "primary": "#7B1FA2",          # Roxo mais sofisticado
                "secondary": "#F3E5F5",        # Fundo roxo suave
                "icon_bg": "#6A1B9A",          # Roxo escuro
                "text": "#4A148C",            # Texto roxo escuro
                "accent": "#AB47BC",          # Roxo claro
                "shadow": "#7B1FA240"
            }
        }
        return colors.get(dialog_type, colors["info"])

    def get_icon_for_type(self, dialog_type: str) -> str:
        """Obter ícone baseado no tipo de diálogo"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "question": "❓"
        }
        return icons.get(dialog_type, "ℹ️")

    def setup_ui(self, title: str, message: str):
        """Configurar interface do usuário com layout melhorado"""
        # Frame principal com design aprimorado
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="transparent"
        )
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header com ícone
        self.create_header()
        
        # Conteúdo da mensagem
        self.create_content(message)
        
        # Botões
        self.create_buttons()
        self.create_buttons()

    def create_header(self):
        """Criar cabeçalho com ícone melhorado e gradiente"""
        # Frame do ícone com melhor design
        self.icon_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["icon_bg"],
            corner_radius=35,
            width=70,
            height=70,
            border_width=3,
            border_color=self.colors["accent"]
        )
        self.icon_frame.pack(pady=(10, 25))
        self.icon_frame.pack_propagate(False)
        
        # Ícone maior e mais visível
        self.icon_label = ctk.CTkLabel(
            self.icon_frame,
            text=self.icon,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        self.icon_label.pack(expand=True)

    def create_content(self, message: str):
        """Criar área de conteúdo com melhor tipografia"""
        # Frame de conteúdo melhorado
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["secondary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["accent"]
        )
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Mensagem com melhor formatação
        self.message_label = ctk.CTkLabel(
            self.content_frame,
            text=message,
            font=ctk.CTkFont(size=15, weight="normal"),
            text_color=self.colors["text"],
            wraplength=380,
            justify="center"
        )
        self.message_label.pack(expand=True, padx=25, pady=20)

    def create_buttons(self):
        """Criar botões de ação com design melhorado"""
        # Frame dos botões com padding maior
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Tratamento especial para diálogos de pergunta
        if self.dialog_type == "question" and len(self.buttons) == 2:
            self.create_question_buttons()
        else:
            self.create_standard_buttons()

    def create_question_buttons(self):
        """Criar botões especiais para diálogos de pergunta (Sim/Não)"""
        # Configurar grid para 2 colunas com espaçamento
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Botão NÃO (Cancelar) - Estilo secundário
        btn_no = ctk.CTkButton(
            self.buttons_frame,
            text="❌ " + self.buttons[1],  # Adicionar ícone
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#e0e0e0", "#404040"),
            hover_color=("#d0d0d0", "#505050"),
            text_color=("#333333", "#ffffff"),
            height=45,
            corner_radius=12,
            border_width=2,
            border_color=("#cccccc", "#666666"),
            command=lambda: self.button_clicked(self.buttons[1])
        )
        btn_no.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Botão SIM (Confirmar) - Estilo primário destacado
        btn_yes = ctk.CTkButton(
            self.buttons_frame,
            text="✅ " + self.buttons[0],  # Adicionar ícone
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors["primary"],
            hover_color=self.colors["icon_bg"],
            text_color="white",
            height=45,
            corner_radius=12,
            border_width=2,
            border_color=self.colors["accent"],
            command=lambda: self.button_clicked(self.buttons[0])
        )
        btn_yes.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Focar no botão Sim por padrão
        btn_yes.focus()

    def create_standard_buttons(self):
        """Criar botões padrão para outros tipos de diálogo"""
        # Configurar grid baseado no número de botões
        for i in range(len(self.buttons)):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Criar botões com design melhorado
        for i, button_text in enumerate(self.buttons):
            if i == len(self.buttons) - 1:  # Último botão (principal)
                button = ctk.CTkButton(
                    self.buttons_frame,
                    text=button_text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    fg_color=self.colors["primary"],
                    hover_color=self.colors["icon_bg"],
                    text_color="white",
                    height=40,
                    corner_radius=10,
                    border_width=2,
                    border_color=self.colors["accent"],
                    command=lambda bt=button_text: self.button_clicked(bt)
                )
            else:  # Botões secundários
                button = ctk.CTkButton(
                    self.buttons_frame,
                    text=button_text,
                    font=ctk.CTkFont(size=13),
                    fg_color=("#e0e0e0", "#404040"),
                    hover_color=("#d0d0d0", "#505050"),
                    text_color=("#333333", "#ffffff"),
                    height=40,
                    corner_radius=10,
                    border_width=1,
                    border_color=("#cccccc", "#666666"),
                    command=lambda bt=button_text: self.button_clicked(bt)
                )
            
            # Posicionar botão
            button.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0))

    def apply_entrance_animation(self):
        """Aplicar animação de entrada"""
        self.animation_running = True
        
        # Começar com escala menor
        self.attributes("-alpha", 0.0)
        
        def animate():
            alpha = 0.0
            scale = 0.8
            steps = 20
            
            for step in range(steps + 1):
                if not self.animation_running:
                    break
                
                progress = step / steps
                # Easing out cubic
                eased_progress = 1 - (1 - progress) ** 3
                
                alpha = eased_progress
                
                self.attributes("-alpha", alpha)
                
                # Pausa entre frames
                time.sleep(0.02)
            
            self.animation_running = False
        
        # Executar animação em thread
        thread = threading.Thread(target=animate, daemon=True)
        thread.start()
        
        # Animar ícone
        self.animate_icon()

    def animate_icon(self):
        """Animar ícone com pulsação suave"""
        def pulse():
            if not self.winfo_exists():
                return
            
            # Calcular escala baseada em seno
            scale = 1.0 + 0.1 * math.sin(time.time() * 3)
            size = int(28 * scale)
            
            try:
                self.icon_label.configure(font=ctk.CTkFont(size=size))
            except:
                return
            
            # Continuar animação
            self.after(50, pulse)
        
        self.after(500, pulse)  # Começar após animação de entrada

    def button_clicked(self, button_text: str):
        """Processar clique de botão com feedback visual"""
        # Armazenar resultado
        self.result = button_text
        
        # Desabilitar todos os botões para evitar cliques múltiplos
        self.disable_all_buttons()
        
        # Aplicar feedback visual antes de fechar
        self.apply_button_feedback(button_text)
        
        # Aguardar um momento antes de fechar (para feedback visual)
        self.after(200, self.apply_exit_animation)

    def disable_all_buttons(self):
        """Desabilitar todos os botões após clique"""
        try:
            for widget in self.buttons_frame.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(state="disabled")
        except:
            pass  # Ignora erros se widgets já foram destruídos

    def apply_button_feedback(self, button_text: str):
        """Aplicar feedback visual ao botão clicado"""
        try:
            for widget in self.buttons_frame.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget.cget("text").endswith(button_text):
                    # Feedback visual para o botão clicado
                    if button_text == "Sim" or button_text == "OK":
                        widget.configure(fg_color=self.colors.get("accent", "#4CAF50"))
                    else:
                        widget.configure(fg_color="#9E9E9E")
        except:
            pass  # Ignora erros se widgets já foram destruídos

    def apply_exit_animation(self):
        """Aplicar animação de saída"""
        def animate_exit():
            steps = 10
            for step in range(steps + 1):
                progress = step / steps
                alpha = 1.0 - progress
                
                self.attributes("-alpha", alpha)
                time.sleep(0.03)
            
            self.destroy()
            
            # Chamar callback se especificado
            if self.callback:
                self.callback(self.result)
        
        thread = threading.Thread(target=animate_exit, daemon=True)
        thread.start()

    def on_closing(self):
        """Processar fechamento da janela"""
        self.result = "Cancel" if "Não" in self.buttons else self.buttons[-1]
        self.apply_exit_animation()


class ModernLoadingDialog(ctk.CTkToplevel):
    """Diálogo de carregamento moderno"""
    
    def __init__(self, parent, title: str = "Processando", message: str = "Aguarde..."):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("350x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.center_window()
        
        # Variáveis de animação
        self.progress_value = 0.0
        self.animation_running = True
        
        self.setup_ui(message)
        self.start_animations()
        
        # Remover botão de fechar
        self.protocol("WM_DELETE_WINDOW", lambda: None)

    def center_window(self):
        """Centralizar janela"""
        self.update_idletasks()
        if hasattr(self, 'master') and self.master:
            parent_x = self.master.winfo_rootx()
            parent_y = self.master.winfo_rooty()
            parent_width = self.master.winfo_width()
            parent_height = self.master.winfo_height()
            
            x = parent_x + (parent_width // 2) - (self.winfo_reqwidth() // 2)
            y = parent_y + (parent_height // 2) - (self.winfo_reqheight() // 2)
        else:
            x = (self.winfo_screenwidth() // 2) - (self.winfo_reqwidth() // 2)
            y = (self.winfo_screenheight() // 2) - (self.winfo_reqheight() // 2)
        
        self.geometry(f"+{x}+{y}")

    def setup_ui(self, message: str):
        """Configurar interface"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Ícone de carregamento
        self.loading_icon = ctk.CTkLabel(
            main_frame,
            text="⏳",
            font=ctk.CTkFont(size=40)
        )
        self.loading_icon.pack(pady=(0, 20))
        
        # Mensagem
        self.message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.message_label.pack(pady=(0, 20))
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            width=250,
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        # Status
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Iniciando...",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        self.status_label.pack()

    def start_animations(self):
        """Iniciar animações"""
        self.animate_icon()
        self.animate_progress()

    def animate_icon(self):
        """Animar ícone de carregamento"""
        icons = ["⏳", "⌛"]
        current = 0
        
        def rotate():
            if not self.animation_running or not self.winfo_exists():
                return
            
            nonlocal current
            self.loading_icon.configure(text=icons[current])
            current = (current + 1) % len(icons)
            
            self.after(800, rotate)
        
        rotate()

    def animate_progress(self):
        """Animar barra de progresso"""
        def update_progress():
            if not self.animation_running or not self.winfo_exists():
                return
            
            # Movimento ondulatório
            self.progress_value += 0.02
            if self.progress_value > 1.0:
                self.progress_value = 0.0
            
            # Aplicar função seno para movimento suave
            display_value = (math.sin(self.progress_value * math.pi * 2) + 1) / 2
            self.progress_bar.set(display_value)
            
            self.after(50, update_progress)
        
        update_progress()

    def update_message(self, message: str):
        """Atualizar mensagem"""
        if self.winfo_exists():
            self.message_label.configure(text=message)

    def update_status(self, status: str):
        """Atualizar status"""
        if self.winfo_exists():
            self.status_label.configure(text=status)

    def close_dialog(self):
        """Fechar diálogo"""
        self.animation_running = False
        self.after(100, self.destroy)


# Funções de conveniência para substituir messagebox
def show_info(parent, title: str, message: str, callback: Optional[Callable] = None):
    """Mostrar diálogo de informação"""
    return ModernDialog(parent, title, message, "info", ["OK"], callback=callback)

def show_success(parent, title: str, message: str, callback: Optional[Callable] = None):
    """Mostrar diálogo de sucesso"""
    return ModernDialog(parent, title, message, "success", ["OK"], callback=callback)

def show_warning(parent, title: str, message: str, callback: Optional[Callable] = None):
    """Mostrar diálogo de aviso"""
    return ModernDialog(parent, title, message, "warning", ["OK"], callback=callback)

def show_error(parent, title: str, message: str, callback: Optional[Callable] = None):
    """Mostrar diálogo de erro"""
    return ModernDialog(parent, title, message, "error", ["OK"], callback=callback)

def ask_question(parent, title: str, message: str, callback: Optional[Callable] = None):
    """Mostrar diálogo de pergunta"""
    return ModernDialog(parent, title, message, "question", ["Sim", "Não"], callback=callback)

def ask_question_sync(parent, title: str, message: str) -> bool:
    """Mostrar diálogo de pergunta síncrono que retorna booleano"""
    dialog = ModernDialog(parent, title, message, "question", ["Sim", "Não"])
    parent.wait_window(dialog)
    return dialog.result == "Sim"

def show_loading(parent, title: str = "Processando", message: str = "Aguarde..."):
    """Mostrar diálogo de carregamento"""
    return ModernLoadingDialog(parent, title, message)
