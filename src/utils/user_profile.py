"""
Perfil de Usuário - Sistema FONTES
Componente para gerenciar perfil do usuário com foto e funcionalidades
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
from pathlib import Path
from typing import Optional, Callable

class UserProfileWidget(ctk.CTkFrame):
    """Widget de perfil do usuário com foto e funcionalidades"""
    
    def __init__(self, parent, username: str, user_role: str = "Usuário", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.username = username
        self.user_role = user_role
        self.profile_image_path = None
        self.support_callback = None
        self.profile_callback = None
        
        # Configurar aparência
        self.configure(
            fg_color="transparent",
            corner_radius=10
        )
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface do perfil"""
        # Frame principal do perfil
        self.profile_frame = ctk.CTkFrame(
            self,
            fg_color=("gray95", "gray15"),
            corner_radius=12,
            border_width=1,
            border_color=("#3498db", "#2980b9")
        )
        self.profile_frame.pack(fill="x", padx=5, pady=5)
        
        # Layout horizontal
        self.profile_frame.grid_columnconfigure(1, weight=1)
        
        # Foto do perfil
        self.create_profile_image()
        
        # Informações do usuário
        self.create_user_info()
        
        # Botões de ação
        self.create_action_buttons()
    
    def create_profile_image(self):
        """Criar área da foto de perfil"""
        # Frame da foto
        self.image_frame = ctk.CTkFrame(
            self.profile_frame,
            width=60,
            height=60,
            fg_color="transparent"
        )
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.image_frame.grid_propagate(False)
        
        # Criar imagem padrão (avatar)
        self.create_default_avatar()
        
        # Label da imagem (clicável)
        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="",
            width=50,
            height=50,
            corner_radius=25
        )
        self.image_label.pack(expand=True)
        
        # Tornar a imagem clicável
        self.image_label.bind("<Button-1>", self.change_profile_image)
        self.image_label.bind("<Enter>", self.on_image_hover)
        self.image_label.bind("<Leave>", self.on_image_leave)
        
        # Tooltip
        self.create_tooltip(self.image_label, "Clique para alterar foto do perfil")
    
    def create_user_info(self):
        """Criar informações do usuário"""
        # Frame das informações
        self.info_frame = ctk.CTkFrame(
            self.profile_frame,
            fg_color="transparent"
        )
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Nome do usuário
        self.username_label = ctk.CTkLabel(
            self.info_frame,
            text=f"👤 {self.username}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#2c3e50", "#ecf0f1"),
            anchor="w"
        )
        self.username_label.pack(fill="x", pady=(0, 2))
        
        # Role do usuário
        self.role_label = ctk.CTkLabel(
            self.info_frame,
            text=f"🏷️ {self.user_role}",
            font=ctk.CTkFont(size=11),
            text_color=("#7f8c8d", "#bdc3c7"),
            anchor="w"
        )
        self.role_label.pack(fill="x")
        
        # Status online
        self.status_label = ctk.CTkLabel(
            self.info_frame,
            text="🟢 Online",
            font=ctk.CTkFont(size=10),
            text_color=("#27ae60", "#2ecc71"),
            anchor="w"
        )
        self.status_label.pack(fill="x", pady=(2, 0))
    
    def create_action_buttons(self):
        """Criar botões de ação"""
        # Frame dos botões
        self.buttons_frame = ctk.CTkFrame(
            self.profile_frame,
            fg_color="transparent"
        )
        self.buttons_frame.grid(row=0, column=2, padx=5, pady=10, sticky="ns")
        
        # Botão de perfil
        self.profile_btn = ctk.CTkButton(
            self.buttons_frame,
            text="⚙️",
            width=35,
            height=30,
            font=ctk.CTkFont(size=16),
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#1f6391"),
            corner_radius=8,
            command=self.open_profile_settings
        )
        self.profile_btn.pack(pady=(0, 5))
        self.create_tooltip(self.profile_btn, "Configurações do perfil")
        
        # Botão de suporte
        self.support_btn = ctk.CTkButton(
            self.buttons_frame,
            text="🆘",
            width=35,
            height=30,
            font=ctk.CTkFont(size=16),
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226"),
            corner_radius=8,
            command=self.open_support
        )
        self.support_btn.pack()
        self.create_tooltip(self.support_btn, "Suporte técnico")
    
    def create_default_avatar(self):
        """Criar avatar padrão"""
        try:
            # Criar uma imagem circular com iniciais
            size = 50
            img = Image.new('RGB', (size, size), '#3498db')
            draw = ImageDraw.Draw(img)
            
            # Desenhar círculo
            draw.ellipse([0, 0, size-1, size-1], fill='#3498db', outline='#2980b9', width=2)
            
            # Adicionar iniciais
            initials = self.username[:2].upper() if len(self.username) >= 2 else self.username[0].upper()
            bbox = draw.textbbox((0, 0), initials)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2
            draw.text((x, y), initials, fill='white')
            
            self.default_image = ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"Erro ao criar avatar padrão: {e}")
            self.default_image = None
    
    def change_profile_image(self, event=None):
        """Alterar foto do perfil"""
        try:
            file_types = [
                ('Imagens', '*.png *.jpg *.jpeg *.gif *.bmp'),
                ('PNG', '*.png'),
                ('JPEG', '*.jpg *.jpeg'),
                ('Todos os arquivos', '*.*')
            ]
            
            filename = filedialog.askopenfilename(
                title="Selecionar foto do perfil",
                filetypes=file_types
            )
            
            if filename:
                self.load_profile_image(filename)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem: {e}")
    
    def load_profile_image(self, image_path: str):
        """Carregar imagem do perfil"""
        try:
            # Abrir e redimensionar imagem
            img = Image.open(image_path)
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            
            # Criar máscara circular
            mask = Image.new('L', (50, 50), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse([0, 0, 50, 50], fill=255)
            
            # Aplicar máscara
            img.putalpha(mask)
            
            # Converter para PhotoImage
            self.profile_image = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.profile_image)
            
            # Salvar caminho
            self.profile_image_path = image_path
            
            # Copiar para pasta do projeto
            self.save_profile_image(image_path)
            
        except Exception as e:
            print(f"Erro ao carregar imagem do perfil: {e}")
            if self.default_image:
                self.image_label.configure(image=self.default_image)
    
    def save_profile_image(self, source_path: str):
        """Salvar imagem do perfil na pasta do projeto"""
        try:
            # Criar pasta de perfis se não existir
            profiles_dir = Path("database/profiles")
            profiles_dir.mkdir(parents=True, exist_ok=True)
            
            # Nome do arquivo baseado no usuário
            file_extension = Path(source_path).suffix
            dest_path = profiles_dir / f"{self.username}_profile{file_extension}"
            
            # Copiar arquivo
            import shutil
            shutil.copy2(source_path, dest_path)
            
            self.profile_image_path = str(dest_path)
            
        except Exception as e:
            print(f"Erro ao salvar imagem do perfil: {e}")
    
    def load_saved_profile_image(self):
        """Carregar imagem salva do perfil"""
        try:
            profiles_dir = Path("database/profiles")
            
            # Procurar por imagem do usuário
            for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                image_path = profiles_dir / f"{self.username}_profile{ext}"
                if image_path.exists():
                    self.load_profile_image(str(image_path))
                    return
            
            # Se não encontrou, usar avatar padrão
            if self.default_image:
                self.image_label.configure(image=self.default_image)
                
        except Exception as e:
            print(f"Erro ao carregar imagem salva: {e}")
    
    def on_image_hover(self, event):
        """Hover na imagem"""
        self.image_label.configure(cursor="hand2")
    
    def on_image_leave(self, event):
        """Sair do hover"""
        self.image_label.configure(cursor="")
    
    def open_profile_settings(self):
        """Abrir configurações do perfil"""
        if self.profile_callback:
            self.profile_callback()
        else:
            from ..utils.modern_dialogs import show_info
            show_info(self, "Perfil", "🛠️ Configurações do perfil em desenvolvimento")
    
    def open_support(self):
        """Abrir suporte"""
        if self.support_callback:
            self.support_callback()
        else:
            from ..utils.modern_dialogs import show_info
            show_info(self, "Suporte", "🆘 Conectando com suporte técnico...")
    
    def create_tooltip(self, widget, text):
        """Criar tooltip para widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="#333333",
                foreground="white",
                font=("Arial", 9),
                padx=5,
                pady=2
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def set_support_callback(self, callback: Callable):
        """Definir callback para suporte"""
        self.support_callback = callback
    
    def set_profile_callback(self, callback: Callable):
        """Definir callback para configurações"""
        self.profile_callback = callback
    
    def update_user_info(self, username: Optional[str] = None, role: Optional[str] = None):
        """Atualizar informações do usuário"""
        if username:
            self.username = username
            self.username_label.configure(text=f"👤 {self.username}")
        
        if role:
            self.user_role = role
            self.role_label.configure(text=f"🏷️ {self.user_role}")
