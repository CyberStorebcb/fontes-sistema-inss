"""
Interface FONTES - Sistema INSS Melhorada
Interface moderna com animações suaves e design aprimorado
"""
import customtkinter as ctk
import tkinter as tk
import os
import sys
import math
import threading
import time
from typing import Optional

# Configurar path para importações
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Importar diálogos modernos
try:
    from utils.modern_dialogs import show_info, show_success, show_warning, show_error, ask_question, ask_question_sync, show_loading
    from utils.user_profile import UserProfileWidget
    MODERN_DIALOGS_AVAILABLE = True
except ImportError as e:
    print(f"Diálogos modernos não disponíveis: {e}")
    from tkinter import messagebox
    MODERN_DIALOGS_AVAILABLE = False

# Importar módulo de integração
try:
    from views.fontes_integration import get_fontes_integration
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"Integração não disponível: {e}")
    INTEGRATION_AVAILABLE = False

# Importar sistema de autenticação
try:
    from auth.authentication import auth_system
    from auth.admin_panel import show_admin_panel
    AUTH_AVAILABLE = True
except ImportError as e:
    print(f"Sistema de autenticação não disponível: {e}")
    AUTH_AVAILABLE = False

# Funções auxiliares para diálogos
def show_modern_info(parent, title: str, message: str):
    """Mostrar diálogo de informação moderno ou fallback"""
    if MODERN_DIALOGS_AVAILABLE:
        show_info(parent, title, message)
    else:
        messagebox.showinfo(title, message)

def show_modern_success(parent, title: str, message: str):
    """Mostrar diálogo de sucesso moderno ou fallback"""
    if MODERN_DIALOGS_AVAILABLE:
        show_success(parent, title, message)
    else:
        messagebox.showinfo(title, message)

def show_modern_warning(parent, title: str, message: str):
    """Mostrar diálogo de aviso moderno ou fallback"""
    if MODERN_DIALOGS_AVAILABLE:
        show_warning(parent, title, message)
    else:
        messagebox.showwarning(title, message)

def show_modern_error(parent, title: str, message: str):
    """Mostrar diálogo de erro moderno ou fallback"""
    if MODERN_DIALOGS_AVAILABLE:
        show_error(parent, title, message)
    else:
        messagebox.showerror(title, message)

def show_modern_question(parent, title: str, message: str) -> bool:
    """Mostrar diálogo de pergunta moderno ou fallback"""
    if MODERN_DIALOGS_AVAILABLE:
        return ask_question_sync(parent, title, message)
    else:
        return messagebox.askyesno(title, message)

class AnimatedCard(ctk.CTkFrame):
    """Card animado para categorias"""
    
    def __init__(self, parent, title, icon, color, description, command, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title = title
        self.icon = icon
        self.color = color
        self.description = description
        self.command = command
        self.is_hovered = False
        self.animation_running = False
        
        # Configurar aparência inicial
        self.configure(
            fg_color=("gray90", "gray20"),
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30")
        )
        
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        """Configurar interface do card com layout melhorado"""
        # Frame interno para conteúdo
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Container centralizado para ícone e título
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.header_frame.pack(expand=True, fill="both")
        
        # Ícone grande centralizado - tamanho aumentado
        self.icon_label = ctk.CTkLabel(
            self.header_frame,
            text=self.icon,
            font=ctk.CTkFont(size=64, weight="bold"),
            text_color=self.color
        )
        self.icon_label.pack(expand=True, pady=(30, 10))
        
        # Título centralizado
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.title,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray10", "white")
        )
        self.title_label.pack(expand=True, pady=(0, 8))
        
        # Descrição centralizada
        self.desc_label = ctk.CTkLabel(
            self.header_frame,
            text=self.description,
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray70"),
            wraplength=220,
            justify="center"
        )
        self.desc_label.pack(expand=True, pady=(0, 30))
        
        # Indicador de status melhorado
        self.status_indicator = ctk.CTkFrame(
            self.content_frame,
            height=4,
            fg_color=self.color,
            corner_radius=2
        )
        self.status_indicator.pack(fill="x", padx=25, pady=(0, 10))
    
    def setup_animations(self):
        """Configurar animações do card"""
        # Bind eventos
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        # Bind para todos os widgets filhos
        for widget in self.winfo_children():
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
            widget.bind("<Button-1>", self.on_click)
            
            # Bind recursivo para subwidgets
            for subwidget in widget.winfo_children():
                subwidget.bind("<Enter>", self.on_enter)
                subwidget.bind("<Leave>", self.on_leave)
                subwidget.bind("<Button-1>", self.on_click)
    
    def on_enter(self, event):
        """Animação ao entrar com mouse"""
        if not self.is_hovered and not self.animation_running:
            self.is_hovered = True
            self.animate_hover_in()
    
    def on_leave(self, event):
        """Animação ao sair com mouse"""
        if self.is_hovered and not self.animation_running:
            self.is_hovered = False
            self.animate_hover_out()
    
    def on_click(self, event):
        """Animação ao clicar"""
        self.animate_click()
        if self.command:
            self.after(150, self.command)
    
    def animate_hover_in(self):
        """Animação suave de hover entrada"""
        self.animation_running = True
        
        def animate():
            # Mudança de cor suave
            self.configure(
                fg_color=("gray95", "gray15"),
                border_color=self.color
            )
            
            # Efeito de elevação com tamanho aumentado
            self.icon_label.configure(font=ctk.CTkFont(size=68, weight="bold"))
            self.title_label.configure(text_color=self.color)
            
            self.animation_running = False
        
        self.after(10, animate)
    
    def animate_hover_out(self):
        """Animação suave de hover saída"""
        self.animation_running = True
        
        def animate():
            # Voltar ao estado original
            self.configure(
                fg_color=("gray90", "gray20"),
                border_color=("gray70", "gray30")
            )
            
            self.icon_label.configure(font=ctk.CTkFont(size=64, weight="bold"))
            self.title_label.configure(text_color=("gray10", "white"))
            
            self.animation_running = False
        
        self.after(10, animate)
    
    def animate_click(self):
        """Animação de clique"""
        def animate():
            # Efeito de "pressionar" com novo tamanho
            self.configure(border_width=3)
            self.icon_label.configure(font=ctk.CTkFont(size=60, weight="bold"))
            
            def restore():
                self.configure(border_width=2)
                self.icon_label.configure(font=ctk.CTkFont(size=68 if self.is_hovered else 64, weight="bold"))
            
            self.after(100, restore)
        
        self.after(10, animate)

class LoadingSpinner(ctk.CTkFrame):
    """Spinner de carregamento animado"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        self.angle = 0
        self.is_spinning = False
        
        # Canvas para desenhar o spinner
        self.canvas = tk.Canvas(
            self,
            width=40,
            height=40,
            bg="#212121",
            highlightthickness=0
        )
        self.canvas.pack()
        
    def start_spin(self):
        """Iniciar animação do spinner"""
        self.is_spinning = True
        self.animate()
    
    def stop_spin(self):
        """Parar animação do spinner"""
        self.is_spinning = False
    
    def animate(self):
        """Animar o spinner"""
        if not self.is_spinning:
            return
        
        self.canvas.delete("all")
        
        # Desenhar arcos do spinner
        for i in range(8):
            start_angle = self.angle + (i * 45)
            alpha = 1.0 - (i * 0.12)
            color = f"#{int(33 + alpha * 100):02x}{int(150 + alpha * 105):02x}{int(243):02x}"
            
            self.canvas.create_arc(
                5, 5, 35, 35,
                start=start_angle,
                extent=30,
                fill=color,
                outline=""
            )
        
        self.angle = (self.angle + 15) % 360
        self.after(50, self.animate)

class FontesMainWindow:
    """Janela principal com design moderno e animações"""
    
    def __init__(self):
        """Inicializar janela principal"""
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Criar janela principal
        self.root = ctk.CTk()
        self.root.title("🏛️ FONTES - Sistema INSS")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        
        # Configurar layout responsivo
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Variáveis de controle
        self.loading = False
        
        # Inicializar integração
        self.integration = None
        if INTEGRATION_AVAILABLE:
            try:
                self.integration = get_fontes_integration(self.root)
            except Exception as e:
                print(f"Erro ao inicializar integração: {e}")
                self.integration = None
        
        # Configurar interface
        self.setup_interface()
        
        # Centralizar na tela
        self.center_window()
        
        # Animação de entrada
        self.animate_window_entrance()
    
    def center_window(self):
        """Centralizar janela na tela de forma robusta"""
        # Atualizar geometria da janela
        self.root.update_idletasks()
        
        # Obter dimensões da janela
        window_width = 1600
        window_height = 1000
        
        # Obter dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posição central
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Garantir que a janela não fique fora da tela
        x = max(0, x)
        y = max(0, y)
        
        # Aplicar geometria centralizada
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Forçar atualização
        self.root.update()
    
    def animate_window_entrance(self):
        """Animação de entrada da janela com centralização garantida"""
        # Garantir que a janela esteja centralizada antes da animação
        self.root.after(50, self.center_window)
        
        self.root.attributes('-alpha', 0.0)
        
        def fade_in():
            alpha = self.root.attributes('-alpha')
            if alpha < 1.0:
                self.root.attributes('-alpha', alpha + 0.05)
                self.root.after(20, fade_in)
            else:
                # Centralizar novamente após a animação para garantir posição
                self.center_window()
        
        self.root.after(100, fade_in)
    
    def setup_interface(self):
        """Configurar interface principal"""
        # Header melhorado
        self.create_header()
        
        # Container principal com animação
        self.create_main_container()
        
        # Footer com informações
        self.create_footer()
    
    def create_header(self):
        """Criar cabeçalho moderno com gradiente"""
        # Frame do header
        self.header_frame = ctk.CTkFrame(
            self.root,
            height=140,
            fg_color=("gray15", "gray10"),
            corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Menu de usuário (lado esquerdo)
        self.create_user_menu()
        
        # Container do título com animação
        title_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_container.grid(row=0, column=1, pady=20)
        
        # Logo/Título principal com gradiente simulado
        self.title_label = ctk.CTkLabel(
            title_container,
            text="🏛️FONTES",
            font=ctk.CTkFont(size=52, weight="bold"),
            text_color="#2196F3"
        )
        self.title_label.pack()
        
        # Subtítulo animado
        self.subtitle_label = ctk.CTkLabel(
            title_container,
            text="SISTEMA INSS - INSTITUTO NACIONAL DO SEGURO SOCIAL",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray60", "gray50")
        )
        self.subtitle_label.pack(pady=(5, 0))
        
        # Linha decorativa
        line_frame = ctk.CTkFrame(
            title_container,
            height=3,
            fg_color="#2196F3",
            corner_radius=2
        )
        line_frame.pack(fill="x", padx=50, pady=(10, 0))
        
        # Menu de ações (lado direito)
        self.create_actions_menu()
        
        # Animação do subtítulo
        self.animate_subtitle()
    
    def create_user_menu(self):
        """Criar menu de informações do usuário com perfil melhorado"""
        if not AUTH_AVAILABLE or not auth_system.current_user:
            return
        
        # Container para o perfil do usuário
        user_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        user_container.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Obter informações do usuário
        username = auth_system.current_user.get('full_name', 'Usuário')
        user_role = "Administrador" if auth_system.current_user.get('role') == 'admin' else "Usuário"
        
        # Criar widget de perfil
        if MODERN_DIALOGS_AVAILABLE:
            self.user_profile = UserProfileWidget(
                user_container,
                username=username,
                user_role=user_role,
                width=280,
                height=80
            )
            self.user_profile.pack(fill="x")
            
            # Configurar callbacks
            self.user_profile.set_support_callback(self.open_support_center)
            self.user_profile.set_profile_callback(self.open_profile_settings)
            
            # Carregar imagem salva do perfil
            self.user_profile.load_saved_profile_image()
        else:
            # Fallback para o sistema antigo
            self.create_user_menu_fallback(user_container, username, user_role)
    
    def create_user_menu_fallback(self, parent, username: str, user_role: str):
        """Menu de usuário fallback"""
        # Avatar do usuário
        avatar_frame = ctk.CTkFrame(
            parent,
            width=60, height=60,
            fg_color=("#2196F3", "#1976D2"),
            corner_radius=30
        )
        avatar_frame.pack(pady=(0, 5))
        
        # Inicial do nome do usuário
        initial = username[0].upper()
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text=initial,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        avatar_label.pack(expand=True)
        
        # Nome do usuário
        user_name = ctk.CTkLabel(
            parent,
            text=f"👋 {username}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray70", "gray60")
        )
        user_name.pack()
        
        # Função do usuário
        role_text = f"👑 {user_role}" if user_role == "Administrador" else f"👤 {user_role}"
        user_role_label = ctk.CTkLabel(
            parent,
            text=role_text,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray70")
        )
        user_role_label.pack()
    
    def open_support_center(self):
        """Abrir central de suporte"""
        try:
            if MODERN_DIALOGS_AVAILABLE:
                show_modern_info(
                    self.root, 
                    "🆘 Central de Suporte", 
                    "Bem-vindo à Central de Suporte!\n\n"
                    "📞 Telefone: (11) 99999-9999\n"
                    "📧 Email: suporte@fontes.inss.gov.br\n"
                    "💬 Chat: Disponível 24/7\n\n"
                    "Como podemos ajudá-lo hoje?"
                )
            else:
                messagebox.showinfo("Suporte", "Central de Suporte - Em breve mais funcionalidades!")
        except Exception as e:
            print(f"Erro ao abrir suporte: {e}")
    
    def open_profile_settings(self):
        """Abrir configurações do perfil"""
        try:
            if MODERN_DIALOGS_AVAILABLE:
                show_modern_info(
                    self.root,
                    "⚙️ Configurações do Perfil",
                    "Configurações do Perfil\n\n"
                    "• Alterar senha\n"
                    "• Atualizar informações pessoais\n"
                    "• Configurar notificações\n"
                    "• Gerenciar sessões\n\n"
                    "Funcionalidades em desenvolvimento..."
                )
            else:
                messagebox.showinfo("Perfil", "Configurações do perfil - Em desenvolvimento!")
        except Exception as e:
            print(f"Erro ao abrir configurações: {e}")
    
    def create_actions_menu(self):
        """Criar menu de ações"""
        if not AUTH_AVAILABLE:
            return
        
        actions_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, padx=20, pady=20, sticky="e")
        
        # Botão de administração (só para admins)
        if auth_system.current_user and auth_system.current_user.get('role') == 'admin':
            admin_btn = ctk.CTkButton(
                actions_frame,
                text="🛡️ Admin",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=80,
                height=35,
                fg_color=("#FF9800", "#F57C00"),
                hover_color=("#F57C00", "#FF9800"),
                command=self.show_admin_panel
            )
            admin_btn.pack(pady=(0, 5))
        
        # Botão de logout
        logout_btn = ctk.CTkButton(
            actions_frame,
            text="🚪 Sair",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=80,
            height=35,
            fg_color=("#F44336", "#D32F2F"),
            hover_color=("#D32F2F", "#F44336"),
            command=self.logout
        )
        logout_btn.pack()
    
    def show_admin_panel(self):
        """Mostrar painel de administração"""
        try:
            show_admin_panel(self.root)
        except Exception as e:
            show_modern_error(self.root, "Erro", f"Erro ao abrir painel de administração:\n{e}")
    
    def logout(self):
        """Fazer logout do sistema"""
        if show_modern_question(self.root, "Logout", "Deseja realmente sair do sistema?"):
            try:
                # Remover sessão salva
                session_file = os.path.join(os.path.dirname(__file__), "..", "..", "session.dat") 
                if os.path.exists(session_file):
                    os.remove(session_file)
                
                # Fazer logout no sistema de autenticação
                if AUTH_AVAILABLE:
                    auth_system.logout()
                
                # Fechar aplicação
                self.root.quit()
                self.root.destroy()
                
                # Mostrar nova tela de login
                def show_login():
                    from auth.login_interface import show_login_window
                    
                    def on_login_success(user_data):
                        # Reiniciar aplicação
                        new_app = FontesMainWindow()
                        new_app.run()
                    
                    login_window = show_login_window(on_login_success)
                    login_window.mainloop()
                
                # Executar login em thread separada
                threading.Thread(target=show_login, daemon=True).start()
                
            except Exception as e:
                show_modern_error(self.root, "Erro", f"Erro ao fazer logout:\n{e}")
    
    def animate_subtitle(self):
        """Animar o subtítulo"""
        def pulse():
            # Efeito de pulsação no subtítulo
            current_color = self.subtitle_label.cget("text_color")
            if current_color == ("gray60", "gray50"):
                self.subtitle_label.configure(text_color="#2196F3")
            else:
                self.subtitle_label.configure(text_color=("gray60", "gray50"))
            
            self.root.after(2000, pulse)
        
        self.root.after(1000, pulse)
    
    def create_main_container(self):
        """Criar container principal com grid de categorias"""
        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=("gray95", "gray17"),
            corner_radius=20,
            scrollbar_button_color=("gray70", "gray30"),
            scrollbar_button_hover_color=("#2196F3", "#1976D2")
        )
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configurar grid responsivo
        for i in range(3):  # 3 colunas
            self.main_frame.grid_columnconfigure(i, weight=1, minsize=350)
        
        # Título da seção
        section_title = ctk.CTkLabel(
            self.main_frame,
            text="📋 SELECIONE UMA CATEGORIA DE SERVIÇOS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#2196F3", "#64B5F6")
        )
        section_title.grid(row=0, column=0, columnspan=3, pady=(20, 30))
        
        # Criar cards das categorias com animação escalonada
        self.create_category_cards()
    
    def create_category_cards(self):
        """Criar cards das categorias com animações"""
        categories = [
            {
                "title": "Aposentadoria",
                "icon": "👨‍",
                "color": "#1976D2",
                "description": "Solicitações e consultas de aposentadoria por idade, tempo de contribuição e invalidez",
                "functions": [
                    ("Cadastrar Solicitação", self.cadastrar_aposentadoria),
                    ("Consultar Status", self.consultar_aposentadoria),
                    ("Documentos Necessários", self.docs_aposentadoria),
                    ("Calcular Aposentadoria", self.calcular_aposentadoria)
                ]
            },
            {
                "title": "Maternidade",
                "icon": "🤱",
                "color": "#E91E63",
                "description": "Benefícios de maternidade, paternidade e auxílio para gestantes",
                "functions": [
                    ("Solicitar Benefício", self.solicitar_maternidade),
                    ("Acompanhar Processo", self.acompanhar_maternidade),
                    ("Documentos", self.docs_maternidade),
                    ("Salário Maternidade", self.salario_maternidade)
                ]
            },
            {
                "title": "Arquivos",
                "icon": "📁",
                "color": "#FF9800",
                "description": "Gestão completa de documentos, upload de arquivos e relatórios",
                "functions": [
                    ("Meus Documentos", self.meus_documentos),
                    ("Upload de Arquivos", self.upload_arquivos),
                    ("Buscar Documentos", self.buscar_documentos),
                    ("Gerar Relatórios", self.gerar_relatorios)
                ]
            },
            {
                "title": "Meu INSS",
                "icon": "🏢",
                "color": "#4CAF50",
                "description": "Acesso direto ao site do Meu INSS",
                "direct_action": self.abrir_meu_inss_direto
            },
            {
                "title": "Suporte",
                "icon": "🛠️",
                "color": "#607D8B",
                "description": "Atendimento técnico, tutoriais e perguntas frequentes",
                "functions": [
                    ("Chat Online", self.chat_suporte),
                    ("Suporte Telefônico", self.telefone_suporte),
                    ("Email", self.email_suporte),
                    ("FAQ", self.faq_suporte),
                    ("Tutoriais", self.tutoriais_suporte)
                ]
            },
            {
                "title": "Solicitar Serviço",
                "icon": "📋",
                "color": "#3F51B5",
                "description": "Solicitações diversas e acompanhamento de processos",
                "functions": [
                    ("Nova Solicitação", self.nova_solicitacao),
                    ("Acompanhar Solicitação", self.acompanhar_solicitacao),
                    ("Histórico", self.historico_solicitacoes),
                    ("Cancelar Solicitação", self.cancelar_solicitacao)
                ]
            }
        ]
        
        # Criar cards com animação escalonada
        for i, category in enumerate(categories):
            row = (i // 3) + 1
            col = i % 3
            
            # Criar card animado
            # Verificar se é ação direta ou lista de funções
            if "direct_action" in category:
                command = category["direct_action"]
            else:
                command = lambda cat=category: self.show_category_functions(cat)
            
            card = AnimatedCard(
                self.main_frame,
                title=category["title"],
                icon=category["icon"],
                color=category["color"],
                description=category["description"],
                command=command,
                width=350,
                height=260
            )
            
            card.grid(
                row=row, 
                column=col, 
                padx=20, 
                pady=20, 
                sticky="nsew"
            )
            
            # Animação de entrada escalonada
            self.animate_card_entrance(card, i * 100)
    
    def animate_card_entrance(self, card, delay):
        """Animar entrada do card"""
        # Começar invisível
        card.configure(fg_color="transparent")
        
        def show_card():
            card.configure(fg_color=("gray90", "gray20"))
        
        self.root.after(delay, show_card)
    
    def create_footer(self):
        """Criar footer com informações"""
        footer_frame = ctk.CTkFrame(
            self.root,
            height=50,
            fg_color=("gray15", "gray10"),
            corner_radius=0
        )
        footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        
        # Informações do sistema
        info_label = ctk.CTkLabel(
            footer_frame,
            text="FONTES v3.0 - Sistema INSS | Desenvolvido com Python & CustomTkinter | © 2025",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50")
        )
        info_label.pack(pady=15)
    
    def show_loading(self):
        """Mostrar indicador de carregamento"""
        if self.loading:
            return
        
        self.loading = True
        
        # Criar overlay de carregamento
        self.loading_overlay = ctk.CTkFrame(
            self.root,
            fg_color=("gray90", "gray10")
        )
        self.loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Spinner de carregamento
        self.spinner = LoadingSpinner(self.loading_overlay)
        self.spinner.place(relx=0.5, rely=0.5, anchor="center")
        self.spinner.start_spin()
        
        # Texto de carregamento
        loading_label = ctk.CTkLabel(
            self.loading_overlay,
            text="Carregando...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2196F3"
        )
        loading_label.place(relx=0.5, rely=0.55, anchor="center")
    
    def hide_loading(self):
        """Esconder indicador de carregamento"""
        if not self.loading:
            return
        
        self.loading = False
        self.spinner.stop_spin()
        self.loading_overlay.destroy()
    
    def show_category_functions(self, category):
        """Mostrar funções de uma categoria"""
        self.show_loading()
        
        def show_functions():
            self.hide_loading()
            
            # Criar janela de funções
            functions_window = ctk.CTkToplevel(self.root)
            functions_window.title(f"{category['icon']} {category['title']}")
            functions_window.geometry("600x500")
            functions_window.transient(self.root)
            functions_window.grab_set()
            
            # Centralizar
            functions_window.update_idletasks()
            x = (functions_window.winfo_screenwidth() // 2) - (300)
            y = (functions_window.winfo_screenheight() // 2) - (250)
            functions_window.geometry(f"600x500+{x}+{y}")
            
            # Frame principal
            main_frame = ctk.CTkFrame(functions_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            title_label = ctk.CTkLabel(
                main_frame,
                text=f"{category['icon']} {category['title']}",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=category['color']
            )
            title_label.pack(pady=20)
            
            # Descrição
            desc_label = ctk.CTkLabel(
                main_frame,
                text=category['description'],
                font=ctk.CTkFont(size=12),
                text_color=("gray60", "gray50"),
                wraplength=500
            )
            desc_label.pack(pady=(0, 20))
            
            # Botões das funções
            for func_name, func_command in category['functions']:
                func_btn = ctk.CTkButton(
                    main_frame,
                    text=func_name,
                    command=func_command,
                    width=400,
                    height=40,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    fg_color=category['color'],
                    hover_color=self.darken_color(category['color'])
                )
                func_btn.pack(pady=5)
            
            # Botão fechar
            close_btn = ctk.CTkButton(
                main_frame,
                text="❌ Fechar",
                command=functions_window.destroy,
                width=200,
                height=35,
                fg_color="gray",
                hover_color="darkgray"
            )
            close_btn.pack(pady=20)
        
        # Simular carregamento
        self.root.after(800, show_functions)
    
    def darken_color(self, color):
        """Escurecer uma cor hex"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, c - 30) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    # ================================================================
    # FUNÇÕES DAS CATEGORIAS (implementações básicas)
    # ================================================================
    
    # Aposentadoria
    def cadastrar_aposentadoria(self):
        if self.integration:
            self.integration.cadastrar_aposentadoria()
        else:
            show_modern_info(self.root, "Aposentadoria", "🏛️ Cadastrar Solicitação de Aposentadoria")
    
    def consultar_aposentadoria(self):
        if self.integration:
            self.integration.consultar_aposentadoria()
        else:
            show_modern_info(self.root, "Aposentadoria", "📊 Consultar Status da Aposentadoria")
    
    def docs_aposentadoria(self):
        show_modern_info(self.root, "Aposentadoria", "📄 Documentos Necessários para Aposentadoria")
    
    def calcular_aposentadoria(self):
        show_modern_info(self.root, "Aposentadoria", "🧮 Calcular Aposentadoria")
    
    # Maternidade
    def solicitar_maternidade(self):
        show_modern_info(self.root, "Maternidade", "🤱 Solicitar Benefício Maternidade")
    
    def acompanhar_maternidade(self):
        show_modern_info(self.root, "Maternidade", "👀 Acompanhar Processo de Maternidade")
    
    def docs_maternidade(self):
        show_modern_info(self.root, "Maternidade", "📄 Documentos para Maternidade")
    
    def salario_maternidade(self):
        show_modern_info(self.root, "Maternidade", "💰 Salário Maternidade")
    
    # Arquivos
    def meus_documentos(self):
        if self.integration:
            self.integration.meus_documentos()
        else:
            show_modern_info(self.root, "Arquivos", "📁 Meus Documentos")
    
    def upload_arquivos(self):
        show_modern_info(self.root, "Arquivos", "⬆️ Upload de Arquivos")
    
    def buscar_documentos(self):
        show_modern_info(self.root, "Arquivos", "🔍 Buscar Documentos")
    
    def gerar_relatorios(self):
        show_modern_info(self.root, "Arquivos", "📊 Gerar Relatórios")
    
    def abrir_meu_inss_direto(self):
        """Abrir diretamente o site do Meu INSS"""
        import webbrowser
        try:
            show_modern_info(self.root, "Meu INSS", "🏢 Abrindo o site do Meu INSS...")
            webbrowser.open("https://meu.inss.gov.br/")
        except Exception as e:
            show_modern_error(self.root, "Erro", f"Erro ao abrir o site do Meu INSS:\n{e}")

    # Suporte
    def chat_suporte(self):
        show_modern_info(self.root, "Suporte", "💬 Chat Online")
    
    def telefone_suporte(self):
        show_modern_info(self.root, "Suporte", "📞 Suporte Telefônico\n\n☎️ (11) 99999-9999")
    
    def email_suporte(self):
        show_modern_info(self.root, "Suporte", "📧 Suporte por Email\n\n✉️ suporte@fontes.inss.gov.br")
    
    def faq_suporte(self):
        show_modern_info(self.root, "Suporte", "❓ Perguntas Frequentes")
    
    def tutoriais_suporte(self):
        show_modern_info(self.root, "Suporte", "🎥 Tutoriais em Vídeo")
    
    # Solicitar Serviço
    def nova_solicitacao(self):
        show_modern_info(self.root, "Serviços", "📝 Nova Solicitação de Serviço")
    
    def acompanhar_solicitacao(self):
        show_modern_info(self.root, "Serviços", "👀 Acompanhar Solicitação")
    
    def historico_solicitacoes(self):
        show_modern_info(self.root, "Serviços", "📚 Histórico de Solicitações")
    
    def cancelar_solicitacao(self):
        show_modern_info(self.root, "Serviços", "❌ Cancelar Solicitação")
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FontesMainWindow()
    app.run()
