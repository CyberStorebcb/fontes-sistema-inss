"""
Sistema FONTES - Funcionalidades Integradas
Implementação independente das funcionalidades do sistema FONTES
"""
import customtkinter as ctk
from tkinter import messagebox
import os
import uuid
from datetime import datetime

class FontesIntegration:
    """Classe para funcionalidades do sistema FONTES"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        
    def gerar_protocolo(self):
        """Gerar protocolo simples"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"FT{timestamp}{str(uuid.uuid4())[:8].upper()}"
    
    # ================================================================
    # APOSENTADORIA
    # ================================================================
    
    def cadastrar_aposentadoria(self):
        """Cadastrar solicitação de aposentadoria"""
        self.show_aposentadoria_form()
    
    def show_aposentadoria_form(self):
        """Mostrar formulário de aposentadoria"""
        window = ctk.CTkToplevel(self.parent)
        window.title("🏛️ Cadastrar Solicitação de Aposentadoria")
        window.geometry("600x700")
        window.transient(self.parent)
        window.grab_set()
        
        # Centralizar
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (300)
        y = (window.winfo_screenheight() // 2) - (350)
        window.geometry(f"600x700+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="🏛️ Solicitação de Aposentadoria",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Campos do formulário
        fields = {}
        
        # Nome completo
        ctk.CTkLabel(main_frame, text="Nome Completo:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10,5))
        fields['nome'] = ctk.CTkEntry(main_frame, height=35)
        fields['nome'].pack(fill="x", padx=20, pady=(0,10))
        
        # CPF
        ctk.CTkLabel(main_frame, text="CPF:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10,5))
        fields['cpf'] = ctk.CTkEntry(main_frame, placeholder_text="000.000.000-00", height=35)
        fields['cpf'].pack(fill="x", padx=20, pady=(0,10))
        
        # Data de nascimento
        ctk.CTkLabel(main_frame, text="Data de Nascimento:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10,5))
        fields['nascimento'] = ctk.CTkEntry(main_frame, placeholder_text="DD/MM/AAAA", height=35)
        fields['nascimento'].pack(fill="x", padx=20, pady=(0,10))
        
        # Tipo de aposentadoria
        ctk.CTkLabel(main_frame, text="Tipo de Aposentadoria:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10,5))
        fields['tipo'] = ctk.CTkOptionMenu(
            main_frame,
            values=["Por Idade", "Por Tempo de Contribuição", "Por Invalidez", "Especial"],
            height=35
        )
        fields['tipo'].pack(fill="x", padx=20, pady=(0,10))
        
        # Tempo de contribuição
        ctk.CTkLabel(main_frame, text="Tempo de Contribuição (anos):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10,5))
        fields['tempo'] = ctk.CTkEntry(main_frame, placeholder_text="Ex: 35", height=35)
        fields['tempo'].pack(fill="x", padx=20, pady=(0,10))
        
        # Observações
        ctk.CTkLabel(main_frame, text="Observações:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10,5))
        fields['obs'] = ctk.CTkTextbox(main_frame, height=100)
        fields['obs'].pack(fill="x", padx=20, pady=(0,20))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="❌ Cancelar",
            command=window.destroy,
            width=120,
            height=40
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="💾 Salvar Solicitação",
            command=lambda: self.salvar_aposentadoria(fields, window),
            width=150,
            height=40
        ).pack(side="left", padx=10)
    
    def salvar_aposentadoria(self, fields, window):
        """Salvar solicitação de aposentadoria"""
        try:
            # Validar campos
            nome = fields['nome'].get().strip()
            cpf = fields['cpf'].get().strip()
            
            if not nome or not cpf:
                messagebox.showerror("Erro", "Nome e CPF são obrigatórios!")
                return
            
            # Gerar protocolo
            protocolo = self.gerar_protocolo()
            
            messagebox.showinfo(
                "Sucesso",
                f"✅ Solicitação de aposentadoria registrada!\n\n"
                f"Cliente: {nome}\n"
                f"CPF: {cpf}\n"
                f"Tipo: {fields['tipo'].get()}\n"
                f"Tempo de contribuição: {fields['tempo'].get()} anos\n"
                f"Protocolo: {protocolo}\n\n"
                f"Status: Em análise\n"
                f"Prazo: 45 dias úteis"
            )
            window.destroy()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def consultar_aposentadoria(self):
        """Consultar status de aposentadoria"""
        self.show_status_consultation()
    
    def show_status_consultation(self):
        """Mostrar consulta de status"""
        window = ctk.CTkToplevel(self.parent)
        window.title("📊 Consultar Status da Aposentadoria")
        window.geometry("500x400")
        window.transient(self.parent)
        window.grab_set()
        
        # Centralizar
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (250)
        y = (window.winfo_screenheight() // 2) - (200)
        window.geometry(f"500x400+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="📊 Consulta de Status",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Campo de busca
        ctk.CTkLabel(main_frame, text="Digite seu CPF ou Protocolo:", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        search_entry = ctk.CTkEntry(main_frame, placeholder_text="CPF ou Protocolo", height=35, width=300)
        search_entry.pack(pady=10)
        
        # Resultado
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def buscar_status():
            search_text = search_entry.get().strip()
            if not search_text:
                messagebox.showwarning("Aviso", "Digite um CPF ou protocolo para buscar!")
                return
            
            # Limpar frame de resultado
            for widget in result_frame.winfo_children():
                widget.destroy()
            
            # Mostrar resultado simulado
            ctk.CTkLabel(
                result_frame,
                text="📋 Status da Solicitação",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=10)
            
            protocolo_gerado = self.gerar_protocolo()
            status_info = f"""
            🆔 Protocolo: {protocolo_gerado}
            👤 Cliente: João Silva
            📅 Data da Solicitação: {datetime.now().strftime('%d/%m/%Y')}
            📊 Status: Em análise
            ⏱️ Prazo: 45 dias úteis
            📝 Observações: Documentação completa recebida
            """
            
            ctk.CTkLabel(
                result_frame,
                text=status_info,
                font=ctk.CTkFont(size=12),
                justify="left"
            ).pack(pady=10)
        
        # Botão buscar
        ctk.CTkButton(
            main_frame,
            text="🔍 Buscar Status",
            command=buscar_status,
            height=40
        ).pack(pady=10)
        
        # Botão fechar
        ctk.CTkButton(
            main_frame,
            text="❌ Fechar",
            command=window.destroy,
            fg_color="gray50",
            hover_color="gray40"
        ).pack(pady=10)
    
    # ================================================================
    # ARQUIVOS
    # ================================================================
    
    def meus_documentos(self):
        """Abrir gestão de documentos"""
        window = ctk.CTkToplevel(self.parent)
        window.title("📁 Meus Documentos")
        window.geometry("700x500")
        window.transient(self.parent)
        window.grab_set()
        
        # Centralizar
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (350)
        y = (window.winfo_screenheight() // 2) - (250)
        window.geometry(f"700x500+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="📁 Gestão de Documentos",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Lista de documentos simulada
        docs_frame = ctk.CTkScrollableFrame(main_frame, label_text="Documentos Cadastrados")
        docs_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Documentos simulados
        documentos = [
            ("📄 RG - Documento de Identidade", datetime.now().strftime('%d/%m/%Y'), "Ativo"),
            ("📄 CPF - Cadastro de Pessoa Física", datetime.now().strftime('%d/%m/%Y'), "Ativo"), 
            ("📄 Carteira de Trabalho", datetime.now().strftime('%d/%m/%Y'), "Ativo"),
            ("📄 Comprovante de Residência", datetime.now().strftime('%d/%m/%Y'), "Ativo"),
            ("📄 Certidão de Nascimento", datetime.now().strftime('%d/%m/%Y'), "Ativo")
        ]
        
        for i, (doc, data, status) in enumerate(documentos):
            doc_frame = ctk.CTkFrame(docs_frame)
            doc_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(doc_frame, text=doc, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(doc_frame, text=f"Enviado: {data}", text_color="gray60").pack(side="left", padx=10)
            ctk.CTkLabel(doc_frame, text=status, text_color="green").pack(side="right", padx=10, pady=10)
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="⬆️ Enviar Documento",
            command=lambda: messagebox.showinfo("Upload", "Funcionalidade de upload em desenvolvimento..."),
            height=40
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="❌ Fechar",
            command=window.destroy,
            fg_color="gray50",
            hover_color="gray40",
            height=40
        ).pack(side="right", padx=10)

# Instância singleton
_integration_instance = None

def get_fontes_integration(parent):
    """Obter instância singleton da integração"""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = FontesIntegration(parent)
    return _integration_instance
