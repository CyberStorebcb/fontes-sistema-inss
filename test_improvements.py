#!/usr/bin/env python3
"""
Teste das melhorias da interface - Cards e Perfil de Usuário
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from src.utils.user_profile import UserProfileWidget
from src.utils.modern_dialogs import show_info, show_success

def test_improvements():
    """Testar melhorias da interface"""
    
    # Configurar tema
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Criar janela principal
    root = ctk.CTk()
    root.title("🎨 Teste das Melhorias - Cards e Perfil")
    root.geometry("800x600")
    root.configure(fg_color=("#f8f9fa", "#1a1a1a"))
    
    # Título
    title_label = ctk.CTkLabel(
        root, 
        text="🎨 Teste das Melhorias Implementadas",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    )
    title_label.pack(pady=20)
    
    # Área de perfil
    profile_frame = ctk.CTkFrame(root, fg_color="transparent")
    profile_frame.pack(fill="x", padx=40, pady=10)
    
    profile_label = ctk.CTkLabel(
        profile_frame,
        text="👤 Perfil de Usuário com Foto e Suporte",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    profile_label.pack(pady=(0, 10))
    
    # Perfil de usuário de teste
    def show_support():
        show_info(root, "🆘 Suporte", "Central de Suporte ativada!\n\nFuncionalidade implementada com sucesso.")
    
    def show_profile():
        show_success(root, "⚙️ Perfil", "Configurações do perfil abertas!\n\nTodas as funcionalidades estão prontas.")
    
    user_profile = UserProfileWidget(
        profile_frame,
        username="Italo Bruno da Silva",
        user_role="Administrador",
        width=350,
        height=90
    )
    user_profile.pack(pady=10)
    user_profile.set_support_callback(show_support)
    user_profile.set_profile_callback(show_profile)
    
    # Separador
    separator = ctk.CTkFrame(root, height=2, fg_color=("#e0e0e0", "#404040"))
    separator.pack(fill="x", padx=40, pady=20)
    
    # Área de cards melhorados
    cards_label = ctk.CTkLabel(
        root,
        text="🏛️ Cards Melhorados - Ícone e Texto Centralizados",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    cards_label.pack(pady=(0, 10))
    
    # Container para cards
    cards_container = ctk.CTkFrame(root, fg_color="transparent")
    cards_container.pack(fill="both", expand=True, padx=40, pady=10)
    
    # Grid para cards
    cards_container.grid_columnconfigure(0, weight=1)
    cards_container.grid_columnconfigure(1, weight=1)
    cards_container.grid_columnconfigure(2, weight=1)
    
    # Cards de exemplo melhorados
    cards_data = [
        {
            "title": "Aposentadoria",
            "icon": "🏛️",
            "color": "#2196F3",
            "description": "Solicitações e consultas de aposentadoria por idade, tempo de contribuição e invalidez"
        },
        {
            "title": "Benefícios",
            "icon": "💰",
            "color": "#4CAF50", 
            "description": "Auxílios, pensões e outros benefícios do INSS"
        },
        {
            "title": "Meu INSS",
            "icon": "🏢",
            "color": "#FF9800",
            "description": "Acesso direto ao portal Meu INSS"
        }
    ]
    
    def card_clicked(title):
        show_info(root, f"Card: {title}", f"Você clicou no card '{title}'!\n\nLayout centralizado funcionando perfeitamente.")
    
    for i, card_data in enumerate(cards_data):
        card = create_improved_card(
            cards_container,
            **card_data,
            command=lambda t=card_data["title"]: card_clicked(t)
        )
        card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
    
    # Instruções
    instructions = ctk.CTkLabel(
        root,
        text="💡 Clique nos cards para testar • Altere a foto do perfil • Teste o suporte",
        font=ctk.CTkFont(size=12),
        text_color=("#7f8c8d", "#bdc3c7")
    )
    instructions.pack(pady=10)
    
    # Rodar aplicação
    root.mainloop()

def create_improved_card(parent, title, icon, color, description, command):
    """Criar card melhorado"""
    card = ctk.CTkFrame(
        parent,
        fg_color=("gray90", "gray20"),
        corner_radius=15,
        border_width=2,
        border_color=("gray70", "gray30"),
        width=220,
        height=280
    )
    card.grid_propagate(False)
    
    # Frame interno para conteúdo
    content_frame = ctk.CTkFrame(card, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Container centralizado para ícone e título
    header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    header_frame.pack(expand=True, fill="both")
    
    # Ícone grande centralizado
    icon_label = ctk.CTkLabel(
        header_frame,
        text=icon,
        font=ctk.CTkFont(size=52, weight="bold"),
        text_color=color
    )
    icon_label.pack(expand=True, pady=(20, 5))
    
    # Título centralizado
    title_label = ctk.CTkLabel(
        header_frame,
        text=title,
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=("gray10", "white")
    )
    title_label.pack(expand=True, pady=(0, 5))
    
    # Descrição centralizada
    desc_label = ctk.CTkLabel(
        header_frame,
        text=description,
        font=ctk.CTkFont(size=12),
        text_color=("gray50", "gray70"),
        wraplength=200,
        justify="center"
    )
    desc_label.pack(expand=True, pady=(0, 20))
    
    # Indicador de status melhorado
    status_indicator = ctk.CTkFrame(
        content_frame,
        height=4,
        fg_color=color,
        corner_radius=2
    )
    status_indicator.pack(fill="x", padx=25, pady=(0, 10))
    
    # Tornar clicável
    def on_click(event):
        command()
    
    card.bind("<Button-1>", on_click)
    content_frame.bind("<Button-1>", on_click)
    header_frame.bind("<Button-1>", on_click)
    icon_label.bind("<Button-1>", on_click)
    title_label.bind("<Button-1>", on_click)
    desc_label.bind("<Button-1>", on_click)
    
    # Hover effects
    def on_enter(event):
        card.configure(border_color=color)
    
    def on_leave(event):
        card.configure(border_color=("gray70", "gray30"))
    
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    
    return card

if __name__ == "__main__":
    test_improvements()
