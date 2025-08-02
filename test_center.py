#!/usr/bin/env python3
"""
Teste de Centralização da Janela
"""
import customtkinter as ctk
import tkinter as tk

def test_window_centering():
    """Testar centralização da janela"""
    # Configurar tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Criar janela de teste
    root = ctk.CTk()
    root.title("🎯 Teste de Centralização")
    
    # Definir tamanho
    window_width = 1600
    window_height = 1000
    
    # Obter dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calcular posição central
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Garantir que não fique fora da tela
    x = max(0, x)
    y = max(0, y)
    
    # Aplicar geometria
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    # Criar conteúdo de teste
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    title_label = ctk.CTkLabel(
        main_frame,
        text="🎯 TESTE DE CENTRALIZAÇÃO",
        font=ctk.CTkFont(size=32, weight="bold"),
        text_color="#2196F3"
    )
    title_label.pack(pady=50)
    
    # Informações da tela
    info_text = f"""
📱 Resolução da Tela: {screen_width} x {screen_height}
🖥️ Tamanho da Janela: {window_width} x {window_height}
📍 Posição Calculada: X={x}, Y={y}

✅ A janela deve estar centralizada na tela!
    """
    
    info_label = ctk.CTkLabel(
        main_frame,
        text=info_text,
        font=ctk.CTkFont(size=16),
        text_color=("gray10", "white"),
        justify="center"
    )
    info_label.pack(pady=30)
    
    # Botões de teste
    btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    btn_frame.pack(pady=30)
    
    def recenter():
        """Recentralizar janela"""
        x_new = (screen_width - window_width) // 2
        y_new = (screen_height - window_height) // 2
        x_new = max(0, x_new)
        y_new = max(0, y_new)
        root.geometry(f'{window_width}x{window_height}+{x_new}+{y_new}')
        root.update()
    
    recenter_btn = ctk.CTkButton(
        btn_frame,
        text="🎯 Recentralizar",
        command=recenter,
        width=200,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="#4CAF50",
        hover_color="#45A049"
    )
    recenter_btn.pack(side="left", padx=10)
    
    close_btn = ctk.CTkButton(
        btn_frame,
        text="❌ Fechar",
        command=root.destroy,
        width=200,
        height=50,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color="#F44336",
        hover_color="#DA190B"
    )
    close_btn.pack(side="left", padx=10)
    
    # Status
    status_label = ctk.CTkLabel(
        main_frame,
        text="🟢 Sistema de centralização funcionando!",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#4CAF50"
    )
    status_label.pack(pady=20)
    
    # Forçar centralização final
    root.update_idletasks()
    recenter()
    
    # Executar
    root.mainloop()

if __name__ == "__main__":
    test_window_centering()
