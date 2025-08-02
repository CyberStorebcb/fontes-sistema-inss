#!/usr/bin/env python3
"""
Teste Simples - Verificação do Botão ENTRAR
"""
import customtkinter as ctk

def teste_botao():
    # Configurar tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Criar janela
    root = ctk.CTk()
    root.title("Teste do Botão ENTRAR")
    root.geometry("400x300")
    
    # Centralizar
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 200
    y = (root.winfo_screenheight() // 2) - 150
    root.geometry(f"400x300+{x}+{y}")
    
    # Frame principal
    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    title = ctk.CTkLabel(
        main_frame,
        text="Teste de Botão",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color=("#2196F3", "#64B5F6")
    )
    title.pack(pady=20)
    
    # Botão de teste
    def click_test():
        print("✅ Botão funcionando!")
        status_label.configure(text="✅ Botão clicado com sucesso!")
    
    test_button = ctk.CTkButton(
        main_frame,
        text="🔓 ENTRAR NO SISTEMA",
        font=ctk.CTkFont(size=18, weight="bold"),
        height=60,
        corner_radius=15,
        fg_color=("#2196F3", "#1976D2"),
        hover_color=("#1976D2", "#0D47A1"),
        border_width=3,
        border_color=("#64B5F6", "#42A5F5"),
        text_color="white",
        command=click_test
    )
    test_button.pack(fill="x", pady=20, padx=20)
    
    # Status
    status_label = ctk.CTkLabel(
        main_frame,
        text="Clique no botão para testar",
        font=ctk.CTkFont(size=14),
        text_color=("gray70", "gray50")
    )
    status_label.pack(pady=10)
    
    print("🧪 Teste iniciado - Verifique se o botão aparece na tela")
    root.mainloop()

if __name__ == "__main__":
    teste_botao()
