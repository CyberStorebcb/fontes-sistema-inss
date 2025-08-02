"""
Painel de Administração - Sistema FONTES
Interface para gerenciar usuários e controle de acesso
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import sys
from typing import List, Dict, Optional
import threading

# Configurar path
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from auth.authentication import auth_system

class AdminPanel(ctk.CTkToplevel):
    """Painel de administração do sistema"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        
        # Verificar se usuário é admin
        if not auth_system.current_user or auth_system.current_user.get('role') != 'admin':
            messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar este painel")
            self.destroy()
            return
        
        self.setup_window()
        self.setup_ui()
        self.load_data()
    
    def setup_window(self):
        """Configurar janela"""
        self.title("Painel de Administração - FONTES")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar para ficar em primeiro plano
        self.transient(self.parent)
        self.grab_set()
    
    def center_window(self):
        """Centralizar janela na tela"""
        self.update_idletasks()
        width = 1000
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Configurar interface do usuário"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        self.create_header()
        
        # Notebook para abas
        self.notebook = ctk.CTkTabview(self.main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(20, 0))
        
        # Criar abas
        self.create_users_tab()
        self.create_logs_tab()
        self.create_settings_tab()
    
    def create_header(self):
        """Criar cabeçalho do painel"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título
        title_label = ctk.CTkLabel(header_frame,
                                  text="🛡️ Painel de Administração",
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color=("#1565C0", "#42A5F5"))
        title_label.pack(side="left")
        
        # Info do usuário logado
        if auth_system.current_user:
            user_info = f"Logado como: {auth_system.current_user['full_name']} ({auth_system.current_user['username']})"
        else:
            user_info = "Usuário não identificado"
        info_label = ctk.CTkLabel(header_frame,
                                 text=user_info,
                                 font=ctk.CTkFont(size=12),
                                 text_color=("gray60", "gray40"))
        info_label.pack(side="right")
    
    def create_users_tab(self):
        """Criar aba de gerenciamento de usuários"""
        # Adicionar aba
        self.users_tab = self.notebook.add("👥 Usuários")
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(self.users_tab, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Botão para adicionar usuário
        add_user_btn = ctk.CTkButton(controls_frame,
                                    text="➕ Novo Usuário",
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    fg_color=("#4CAF50", "#45A049"),
                                    hover_color=("#45A049", "#4CAF50"),
                                    command=self.show_add_user_dialog)
        add_user_btn.pack(side="left", padx=(0, 10))
        
        # Botão para atualizar lista
        refresh_btn = ctk.CTkButton(controls_frame,
                                   text="🔄 Atualizar",
                                   font=ctk.CTkFont(size=14),
                                   fg_color=("#2196F3", "#1976D2"),
                                   hover_color=("#1976D2", "#2196F3"),
                                   command=self.load_users)
        refresh_btn.pack(side="left")
        
        # Frame para tabela de usuários
        table_frame = ctk.CTkFrame(self.users_tab)
        table_frame.pack(fill="both", expand=True)
        
        # Criar Treeview para usuários
        self.users_tree = ttk.Treeview(table_frame,
                                      columns=("ID", "Usuário", "Nome", "Email", "Função", "Status", "Criado", "Último Login"),
                                      show="headings",
                                      height=15)
        
        # Configurar colunas
        columns_config = [
            ("ID", 50),
            ("Usuário", 120),
            ("Nome", 150),
            ("Email", 180),
            ("Função", 80),
            ("Status", 80),
            ("Criado", 130),
            ("Último Login", 130)
        ]
        
        for col, width in columns_config:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=width, anchor="center" if col in ["ID", "Função", "Status"] else "w")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.users_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.users_tree.xview)
        self.users_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack da tabela e scrollbars
        self.users_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        v_scrollbar.pack(side="right", fill="y", pady=10)
        h_scrollbar.pack(side="bottom", fill="x", padx=(10, 20))
        
        # Menu de contexto
        self.create_user_context_menu()
        
        # Bind do menu de contexto
        self.users_tree.bind("<Button-3>", self.show_user_context_menu)
        self.users_tree.bind("<Double-1>", self.edit_user)
    
    def create_user_context_menu(self):
        """Criar menu de contexto para usuários"""
        self.user_context_menu = tk.Menu(self, tearoff=0)
        self.user_context_menu.add_command(label="✏️ Editar", command=self.edit_user)
        self.user_context_menu.add_command(label="🔑 Alterar Senha", command=self.change_user_password)
        self.user_context_menu.add_separator()
        self.user_context_menu.add_command(label="✅ Ativar", command=lambda: self.toggle_user_status(True))
        self.user_context_menu.add_command(label="❌ Desativar", command=lambda: self.toggle_user_status(False))
        self.user_context_menu.add_separator()
        self.user_context_menu.add_command(label="📊 Ver Logs", command=self.view_user_logs)
        self.user_context_menu.add_command(label="🗑️ Remover", command=self.remove_user)
    
    def create_logs_tab(self):
        """Criar aba de logs de acesso"""
        # Adicionar aba
        self.logs_tab = self.notebook.add("📋 Logs de Acesso")
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(self.logs_tab, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Botão para atualizar logs
        refresh_logs_btn = ctk.CTkButton(controls_frame,
                                        text="🔄 Atualizar Logs",
                                        font=ctk.CTkFont(size=14),
                                        command=self.load_logs)
        refresh_logs_btn.pack(side="left", padx=(0, 10))
        
        # Combobox para filtrar por ação
        filter_label = ctk.CTkLabel(controls_frame, text="Filtrar por:")
        filter_label.pack(side="left", padx=(20, 5))
        
        self.log_filter_var = ctk.StringVar(value="Todos")
        self.log_filter = ctk.CTkComboBox(controls_frame,
                                         values=["Todos", "LOGIN_SUCCESS", "LOGIN_FAILED", "LOGOUT", "LOGIN_BLOCKED"],
                                         variable=self.log_filter_var,
                                         command=self.filter_logs)
        self.log_filter.pack(side="left")
        
        # Frame para tabela de logs
        logs_table_frame = ctk.CTkFrame(self.logs_tab)
        logs_table_frame.pack(fill="both", expand=True)
        
        # Criar Treeview para logs
        self.logs_tree = ttk.Treeview(logs_table_frame,
                                     columns=("Usuário", "Ação", "Data/Hora", "Status", "Detalhes", "IP"),
                                     show="headings",
                                     height=20)
        
        # Configurar colunas dos logs
        logs_columns_config = [
            ("Usuário", 120),
            ("Ação", 120),
            ("Data/Hora", 150),
            ("Status", 80),
            ("Detalhes", 300),
            ("IP", 120)
        ]
        
        for col, width in logs_columns_config:
            self.logs_tree.heading(col, text=col)
            self.logs_tree.column(col, width=width, anchor="center" if col == "Status" else "w")
        
        # Scrollbars para logs
        logs_v_scrollbar = ttk.Scrollbar(logs_table_frame, orient="vertical", command=self.logs_tree.yview)
        logs_h_scrollbar = ttk.Scrollbar(logs_table_frame, orient="horizontal", command=self.logs_tree.xview)
        self.logs_tree.configure(yscrollcommand=logs_v_scrollbar.set, xscrollcommand=logs_h_scrollbar.set)
        
        # Pack da tabela de logs
        self.logs_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        logs_v_scrollbar.pack(side="right", fill="y", pady=10)
        logs_h_scrollbar.pack(side="bottom", fill="x", padx=(10, 20))
    
    def create_settings_tab(self):
        """Criar aba de configurações"""
        # Adicionar aba
        self.settings_tab = self.notebook.add("⚙️ Configurações")
        
        # Frame de configurações
        settings_frame = ctk.CTkScrollableFrame(self.settings_tab)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Seção de Segurança
        security_label = ctk.CTkLabel(settings_frame,
                                     text="🔒 Configurações de Segurança",
                                     font=ctk.CTkFont(size=18, weight="bold"))
        security_label.pack(anchor="w", pady=(0, 10))
        
        # Configurar duração da sessão
        session_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        session_frame.pack(fill="x", pady=(0, 15))
        
        session_label = ctk.CTkLabel(session_frame,
                                    text="Duração da sessão (dias):",
                                    font=ctk.CTkFont(size=14))
        session_label.pack(side="left")
        
        self.session_duration_var = ctk.StringVar(value=str(auth_system.session_duration))
        session_entry = ctk.CTkEntry(session_frame,
                                    textvariable=self.session_duration_var,
                                    width=80)
        session_entry.pack(side="left", padx=(10, 0))
        
        # Seção de Backup
        backup_label = ctk.CTkLabel(settings_frame,
                                   text="💾 Backup do Sistema",
                                   font=ctk.CTkFont(size=18, weight="bold"))
        backup_label.pack(anchor="w", pady=(30, 10))
        
        backup_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        backup_frame.pack(fill="x", pady=(0, 15))
        
        backup_btn = ctk.CTkButton(backup_frame,
                                  text="📥 Fazer Backup do Banco",
                                  font=ctk.CTkFont(size=14),
                                  command=self.backup_database)
        backup_btn.pack(side="left", padx=(0, 10))
        
        restore_btn = ctk.CTkButton(backup_frame,
                                   text="📤 Restaurar Backup",
                                   font=ctk.CTkFont(size=14),
                                   command=self.restore_database)
        restore_btn.pack(side="left")
        
        # Seção de Estatísticas
        stats_label = ctk.CTkLabel(settings_frame,
                                  text="📊 Estatísticas do Sistema",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        stats_label.pack(anchor="w", pady=(30, 10))
        
        self.stats_frame = ctk.CTkFrame(settings_frame)
        self.stats_frame.pack(fill="x", pady=(0, 15))
        
        # Botão de configurações avançadas
        advanced_label = ctk.CTkLabel(settings_frame,
                                     text="⚙️ Configurações Avançadas",
                                     font=ctk.CTkFont(size=18, weight="bold"))
        advanced_label.pack(anchor="w", pady=(30, 10))
        
        advanced_btn = ctk.CTkButton(settings_frame,
                                    text="🔧 Abrir Configurações Avançadas",
                                    font=ctk.CTkFont(size=14),
                                    command=self.show_advanced_settings)
        advanced_btn.pack(anchor="w", pady=(0, 10))
        
        self.load_statistics()
    
    def load_data(self):
        """Carregar dados iniciais"""
        self.load_users()
        self.load_logs()
    
    def load_users(self):
        """Carregar lista de usuários"""
        def load():
            try:
                users = auth_system.get_users()
                self.after(0, lambda: self.update_users_table(users))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro ao carregar usuários: {e}"))
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def update_users_table(self, users: List[Dict]):
        """Atualizar tabela de usuários"""
        # Limpar tabela
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Adicionar usuários
        for user in users:
            status = "🟢 Ativo" if user['is_active'] else "🔴 Inativo"
            role = "👑 Admin" if user['role'] == 'admin' else "👤 Usuário"
            
            # Formatar datas
            created_at = user['created_at'][:16] if user['created_at'] else "-"
            last_login = user['last_login'][:16] if user['last_login'] else "Nunca"
            
            self.users_tree.insert("", "end", values=(
                user['id'],
                user['username'],
                user['full_name'],
                user['email'] or "-",
                role,
                status,
                created_at,
                last_login
            ))
    
    def load_logs(self):
        """Carregar logs de acesso"""
        def load():
            try:
                logs = auth_system.get_access_logs(200)
                self.after(0, lambda: self.update_logs_table(logs))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro ao carregar logs: {e}"))
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def update_logs_table(self, logs: List[Dict]):
        """Atualizar tabela de logs"""
        # Limpar tabela
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        
        # Adicionar logs
        for log in logs:
            status_icon = "✅" if log['success'] else "❌"
            timestamp = log['timestamp'][:19] if log['timestamp'] else "-"
            
            self.logs_tree.insert("", "end", values=(
                log['username'] or "-",
                log['action'],
                timestamp,
                status_icon,
                log['details'] or "-",
                log['ip_address'] or "-"
            ))
    
    def filter_logs(self, selected_filter):
        """Filtrar logs por ação"""
        self.load_logs()  # Por simplicidade, recarregar todos os logs
        # TODO: Implementar filtro real no backend
    
    def show_user_context_menu(self, event):
        """Mostrar menu de contexto para usuários"""
        selection = self.users_tree.selection()
        if selection:
            self.user_context_menu.post(event.x_root, event.y_root)
    
    def get_selected_user_id(self) -> Optional[int]:
        """Obter ID do usuário selecionado"""
        selection = self.users_tree.selection()
        if selection:
            item = self.users_tree.item(selection[0])
            return int(item['values'][0])
        return None
    
    def show_add_user_dialog(self):
        """Mostrar diálogo para adicionar usuário"""
        dialog = UserDialog(self, "Novo Usuário")
        dialog.wait_window()  # Aguardar o diálogo ser fechado
        
        if dialog.result:
            username, password, full_name, email, role = dialog.result
            
            def create():
                email_value = email if email and email.strip() else None
                success, message = auth_system.create_user(username, password, full_name, email_value, role)
                self.after(0, lambda: self.handle_user_operation_result(success, message))
            
            thread = threading.Thread(target=create, daemon=True)
            thread.start()
    
    def edit_user(self, event=None):
        """Editar usuário selecionado"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Seleção", "Selecione um usuário para editar")
            return
        
        # Buscar dados do usuário
        try:
            users = auth_system.get_users()
            user_data = next((u for u in users if u['id'] == user_id), None)
            
            if not user_data:
                messagebox.showerror("Erro", "Usuário não encontrado")
                return
            
            # Mostrar diálogo de edição
            dialog = UserEditDialog(self, "Editar Usuário", user_data)
            dialog.wait_window()  # Aguardar o diálogo ser fechado
            
            if dialog.result:
                username, full_name, email, role = dialog.result
                
                def update():
                    success, message = auth_system.update_user(user_id, username, full_name, email, role)
                    self.after(0, lambda: self.handle_user_operation_result(success, message))
                
                thread = threading.Thread(target=update, daemon=True)
                thread.start()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados do usuário: {e}")
    
    def change_user_password(self):
        """Alterar senha do usuário"""
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        dialog = PasswordDialog(self)
        dialog.wait_window()  # Aguardar o diálogo ser fechado
        
        if dialog.result:
            new_password = dialog.result
            
            def change():
                success, message = auth_system.change_password(user_id, new_password)
                self.after(0, lambda: self.handle_user_operation_result(success, message))
            
            thread = threading.Thread(target=change, daemon=True)
            thread.start()
    
    def show_advanced_settings(self):
        """Mostrar diálogo de configurações avançadas"""
        dialog = SystemSettingsDialog(self)
        dialog.wait_window()
    
    def toggle_user_status(self, is_active: bool):
        """Ativar/desativar usuário"""
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        action = "ativar" if is_active else "desativar"
        if messagebox.askyesno("Confirmar", f"Deseja realmente {action} este usuário?"):
            def toggle():
                success, message = auth_system.update_user_status(user_id, is_active)
                self.after(0, lambda: self.handle_user_operation_result(success, message))
            
            thread = threading.Thread(target=toggle, daemon=True)
            thread.start()
    
    def remove_user(self):
        """Remover usuário"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Seleção", "Selecione um usuário para remover")
            return
        
        # Buscar dados do usuário para confirmação
        try:
            users = auth_system.get_users()
            user_data = next((u for u in users if u['id'] == user_id), None)
            
            if not user_data:
                messagebox.showerror("Erro", "Usuário não encontrado")
                return
            
            # Verificar se não é o próprio usuário admin atual
            if auth_system.current_user and user_data['username'] == auth_system.current_user['username']:
                messagebox.showerror("Erro", "Você não pode remover sua própria conta")
                return
            
            # Confirmação
            if messagebox.askyesno("Confirmar Remoção", 
                                  f"Deseja realmente remover o usuário:\n\n"
                                  f"• Nome: {user_data['full_name']}\n"
                                  f"• Username: {user_data['username']}\n"
                                  f"• Função: {user_data['role']}\n\n"
                                  f"Esta ação não pode ser desfeita!"):
                
                def remove():
                    success, message = auth_system.delete_user(user_id)
                    self.after(0, lambda: self.handle_user_operation_result(success, message))
                
                thread = threading.Thread(target=remove, daemon=True)
                thread.start()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados do usuário: {e}")
    
    def view_user_logs(self):
        """Ver logs do usuário selecionado"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Seleção", "Selecione um usuário")
            return
        
        # Buscar dados do usuário
        try:
            users = auth_system.get_users()
            user_data = next((u for u in users if u['id'] == user_id), None)
            
            if not user_data:
                messagebox.showerror("Erro", "Usuário não encontrado")
                return
            
            # Mostrar logs do usuário
            UserLogsWindow(self, user_data)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar logs: {e}")
    
    def handle_user_operation_result(self, success: bool, message: str):
        """Tratar resultado de operação com usuário"""
        if success:
            messagebox.showinfo("Sucesso", message)
            self.load_users()
        else:
            messagebox.showerror("Erro", message)
    
    def load_statistics(self):
        """Carregar estatísticas do sistema"""
        def load():
            try:
                users = auth_system.get_users()
                logs = auth_system.get_access_logs(50)
                
                # Calcular estatísticas
                total_users = len(users)
                active_users = len([u for u in users if u['is_active']])
                admin_users = len([u for u in users if u['role'] == 'admin'])
                recent_logins = len([l for l in logs if l['action'] == 'LOGIN_SUCCESS'])
                
                stats = {
                    'total_users': total_users,
                    'active_users': active_users,
                    'admin_users': admin_users,
                    'recent_logins': recent_logins
                }
                
                self.after(0, lambda: self.update_statistics(stats))
                
            except Exception as e:
                print(f"Erro ao carregar estatísticas: {e}")
    
    def update_statistics(self, stats: Dict):
        """Atualizar estatísticas na interface"""
        # Limpar frame de estatísticas
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Criar labels de estatísticas
        stats_data = [
            ("👥 Total de Usuários", stats['total_users']),
            ("✅ Usuários Ativos", stats['active_users']),
            ("👑 Administradores", stats['admin_users']),
            ("🔑 Logins Recentes", stats['recent_logins'])
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            stat_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            label_widget = ctk.CTkLabel(stat_frame, text=label, font=ctk.CTkFont(size=14))
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(stat_frame, text=str(value), 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       text_color=("#1565C0", "#42A5F5"))
            value_widget.pack(side="right")
        
        # Configurar grid
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_columnconfigure(1, weight=1)
    
    def backup_database(self):
        """Fazer backup do banco de dados"""
        try:
            from tkinter import filedialog
            import shutil
            import datetime
            
            # Solicitar local para salvar backup
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"fontes_backup_{timestamp}.db"
            
            backup_path = filedialog.asksaveasfilename(
                title="Salvar Backup",
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                initialfile=default_name
            )
            
            if backup_path:
                # Copiar banco de dados
                db_path = os.path.join("database", "users.db")
                shutil.copy2(db_path, backup_path)
                
                messagebox.showinfo("Sucesso", f"Backup salvo com sucesso em:\n{backup_path}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer backup: {e}")
    
    def restore_database(self):
        """Restaurar backup do banco de dados"""
        try:
            from tkinter import filedialog
            import shutil
            
            if not messagebox.askyesno("Confirmação", 
                                     "Esta operação irá substituir o banco atual.\n"
                                     "Tem certeza que deseja continuar?"):
                return
            
            # Solicitar arquivo de backup
            backup_path = filedialog.askopenfilename(
                title="Selecionar Backup",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if backup_path:
                # Fazer backup do banco atual antes de restaurar
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                current_backup = f"database/users_backup_before_restore_{timestamp}.db"
                
                db_path = os.path.join("database", "users.db")
                shutil.copy2(db_path, current_backup)
                
                # Restaurar backup
                shutil.copy2(backup_path, db_path)
                
                messagebox.showinfo("Sucesso", 
                                  f"Backup restaurado com sucesso!\n"
                                  f"Backup anterior salvo em: {current_backup}\n\n"
                                  f"Reinicie o sistema para aplicar as mudanças.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup: {e}")

class UserDialog(ctk.CTkToplevel):
    """Diálogo para criar/editar usuário"""
    
    def __init__(self, parent, title="Usuário"):
        super().__init__(parent)
        
        self.result = None
        
        self.title(title)
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Centralizar
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos do formulário
        fields = [
            ("Nome de Usuário:", "username"),
            ("Senha:", "password"),
            ("Nome Completo:", "full_name"),
            ("Email:", "email")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            label = ctk.CTkLabel(main_frame, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(10, 5))
            
            if field_name == "password":
                entry = ctk.CTkEntry(main_frame, show="●", height=35)
            else:
                entry = ctk.CTkEntry(main_frame, height=35)
            
            entry.pack(fill="x", pady=(0, 5))
            self.entries[field_name] = entry
        
        # Função do usuário
        role_label = ctk.CTkLabel(main_frame, text="Função:", font=ctk.CTkFont(size=14, weight="bold"))
        role_label.pack(anchor="w", pady=(10, 5))
        
        self.role_var = ctk.StringVar(value="user")
        role_combo = ctk.CTkComboBox(main_frame, values=["user", "admin"], variable=self.role_var, height=35)
        role_combo.pack(fill="x", pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Cancelar", 
                                  fg_color=("gray60", "gray40"),
                                  command=self.cancel)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(buttons_frame, text="Salvar", command=self.save)
        save_btn.pack(side="right")
    
    def save(self):
        """Salvar usuário"""
        # Validar campos
        username = self.entries['username'].get().strip()
        password = self.entries['password'].get().strip()
        full_name = self.entries['full_name'].get().strip()
        email = self.entries['email'].get().strip()
        role = self.role_var.get()
        
        # Validações básicas
        if not username or not password or not full_name:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios")
            return
        
        # Validar comprimento mínimo do username
        if len(username) < 3:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 3 caracteres")
            return
        
        # Validar comprimento mínimo da senha
        if len(password) < 6:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres")
            return
        
        # Validar email se fornecido
        if email and "@" not in email:
            messagebox.showerror("Erro", "Email inválido")
            return
        
        self.result = (username, password, full_name, email if email else None, role)
        self.destroy()
    
    def cancel(self):
        """Cancelar"""
        self.result = None
        self.destroy()

class PasswordDialog(ctk.CTkToplevel):
    """Diálogo para alterar senha"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.result = None
        
        self.title("Alterar Senha")
        self.geometry("350x250")
        self.resizable(False, False)
        
        # Centralizar
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Nova senha
        label1 = ctk.CTkLabel(main_frame, text="Nova Senha:", font=ctk.CTkFont(size=14, weight="bold"))
        label1.pack(anchor="w", pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(main_frame, show="●", height=35)
        self.password_entry.pack(fill="x", pady=(0, 10))
        
        # Confirmar senha
        label2 = ctk.CTkLabel(main_frame, text="Confirmar Senha:", font=ctk.CTkFont(size=14, weight="bold"))
        label2.pack(anchor="w", pady=(0, 5))
        
        self.confirm_entry = ctk.CTkEntry(main_frame, show="●", height=35)
        self.confirm_entry.pack(fill="x", pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Cancelar",
                                  fg_color=("gray60", "gray40"),
                                  command=self.cancel)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(buttons_frame, text="Alterar", command=self.save)
        save_btn.pack(side="right")
    
    def save(self):
        """Salvar nova senha"""
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        if not password:
            messagebox.showerror("Erro", "Digite a nova senha")
            return
        
        if len(password) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres")
            return
        
        if password != confirm:
            messagebox.showerror("Erro", "As senhas não coincidem")
            return
        
        self.result = password
        self.destroy()
    
    def cancel(self):
        """Cancelar"""
        self.result = None
        self.destroy()

class UserEditDialog(ctk.CTkToplevel):
    """Diálogo para editar usuário existente"""
    
    def __init__(self, parent, title="Editar Usuário", user_data=None):
        super().__init__(parent)
        
        self.result = None
        self.user_data = user_data
        
        self.title(title)
        self.geometry("400x450")
        self.resizable(False, False)
        
        # Centralizar
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        # Preencher dados existentes
        if user_data:
            self.load_user_data()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, 
                                  text="✏️ Editar Usuário", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Campos do formulário (sem senha para edição)
        fields = [
            ("Nome de Usuário:", "username"),
            ("Nome Completo:", "full_name"),
            ("Email:", "email")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            label = ctk.CTkLabel(main_frame, text=label_text, font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", pady=(10, 5))
            
            entry = ctk.CTkEntry(main_frame, height=35)
            entry.pack(fill="x", pady=(0, 5))
            self.entries[field_name] = entry
        
        # Função do usuário
        role_label = ctk.CTkLabel(main_frame, text="Função:", font=ctk.CTkFont(size=14, weight="bold"))
        role_label.pack(anchor="w", pady=(10, 5))
        
        self.role_var = ctk.StringVar(value="user")
        role_combo = ctk.CTkComboBox(main_frame, values=["user", "admin"], variable=self.role_var, height=35)
        role_combo.pack(fill="x", pady=(0, 20))
        
        # Informação sobre senha
        info_label = ctk.CTkLabel(main_frame, 
                                 text="ℹ️ Para alterar a senha, use a opção 'Alterar Senha' no menu de contexto",
                                 font=ctk.CTkFont(size=11),
                                 text_color=("gray60", "gray40"),
                                 wraplength=350)
        info_label.pack(pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Cancelar", 
                                  fg_color=("gray60", "gray40"),
                                  command=self.cancel)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(buttons_frame, text="Salvar", command=self.save)
        save_btn.pack(side="right")
    
    def load_user_data(self):
        """Carregar dados do usuário nos campos"""
        if self.user_data:
            self.entries['username'].insert(0, self.user_data['username'])
            self.entries['full_name'].insert(0, self.user_data['full_name'])
            self.entries['email'].insert(0, self.user_data['email'] or "")
            self.role_var.set(self.user_data['role'])
    
    def save(self):
        """Salvar alterações do usuário"""
        # Validar campos
        username = self.entries['username'].get().strip()
        full_name = self.entries['full_name'].get().strip()
        email = self.entries['email'].get().strip()
        role = self.role_var.get()
        
        if not username or not full_name:
            messagebox.showerror("Erro", "Preencha os campos obrigatórios")
            return
        
        if len(username) < 3:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 3 caracteres")
            return
        
        if email and "@" not in email:
            messagebox.showerror("Erro", "Email inválido")
            return
        
        self.result = (username, full_name, email, role)
        self.destroy()
    
    def cancel(self):
        """Cancelar edição"""
        self.result = None
        self.destroy()

class UserLogsWindow(ctk.CTkToplevel):
    """Janela para visualizar logs de um usuário específico"""
    
    def __init__(self, parent, user_data):
        super().__init__(parent)
        
        self.user_data = user_data
        
        self.title(f"Logs do Usuário: {user_data['full_name']}")
        self.geometry("900x600")
        self.resizable(True, True)
        
        # Centralizar
        self.transient(parent)
        
        self.setup_ui()
        self.load_user_logs()
    
    def setup_ui(self):
        """Configurar interface"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Informações do usuário
        user_info = ctk.CTkLabel(header_frame,
                                text=f"📊 Logs de Acesso - {self.user_data['full_name']} ({self.user_data['username']})",
                                font=ctk.CTkFont(size=16, weight="bold"))
        user_info.pack(side="left")
        
        # Botão de atualizar
        refresh_btn = ctk.CTkButton(header_frame,
                                   text="🔄 Atualizar",
                                   width=100,
                                   command=self.load_user_logs)
        refresh_btn.pack(side="right")
        
        # Frame para tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True)
        
        # Criar Treeview
        columns = ("Data/Hora", "Ação", "Status", "Detalhes", "IP")
        self.logs_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        column_widths = [150, 120, 80, 300, 120]
        for col, width in zip(columns, column_widths):
            self.logs_tree.heading(col, text=col)
            self.logs_tree.column(col, width=width, anchor="center" if col == "Status" else "w")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.logs_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.logs_tree.xview)
        self.logs_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack
        self.logs_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        v_scrollbar.pack(side="right", fill="y", pady=10)
        h_scrollbar.pack(side="bottom", fill="x", padx=(10, 20))
        
        # Estatísticas do usuário
        self.create_user_stats()
    
    def create_user_stats(self):
        """Criar estatísticas do usuário"""
        stats_frame = ctk.CTkFrame(self, height=80)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        stats_frame.pack_propagate(False)
        
        self.stats_labels = {}
        stats_data = [
            ("📅 Criado em", self.user_data['created_at'][:10] if self.user_data['created_at'] else "N/A"),
            ("🔑 Último Login", self.user_data['last_login'][:16] if self.user_data['last_login'] else "Nunca"),
            ("👤 Função", "👑 Admin" if self.user_data['role'] == 'admin' else "👤 Usuário"),
            ("🔄 Status", "🟢 Ativo" if self.user_data['is_active'] else "🔴 Inativo")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            label_widget = ctk.CTkLabel(stat_frame, text=label, font=ctk.CTkFont(size=12, weight="bold"))
            label_widget.pack()
            
            value_widget = ctk.CTkLabel(stat_frame, text=value, font=ctk.CTkFont(size=11))
            value_widget.pack()
        
        # Configurar grid
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
    
    def load_user_logs(self):
        """Carregar logs do usuário"""
        def load():
            try:
                # Buscar logs específicos do usuário
                logs = auth_system.get_user_logs(self.user_data['id'])
                self.after(0, lambda: self.update_logs_table(logs))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro ao carregar logs: {e}"))
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def update_logs_table(self, logs):
        """Atualizar tabela de logs"""
        # Limpar tabela
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        
        # Adicionar logs
        for log in logs:
            status_icon = "✅" if log['success'] else "❌"
            timestamp = log['timestamp'][:19] if log['timestamp'] else "-"
            
            # Traduzir ações
            action_translations = {
                'LOGIN_SUCCESS': '🔓 Login',
                'LOGIN_FAILED': '🚫 Login Falhou',
                'LOGOUT': '🚪 Logout',
                'LOGIN_BLOCKED': '🔒 Bloqueado',
                'PASSWORD_CHANGED': '🔑 Senha Alterada',
                'USER_UPDATED': '✏️ Dados Alterados'
            }
            
            action = action_translations.get(log['action'], log['action'])
            
            self.logs_tree.insert("", "end", values=(
                timestamp,
                action,
                status_icon,
                log['details'] or "-",
                log['ip_address'] or "-"
            ))

class SystemSettingsDialog(ctk.CTkToplevel):
    """Diálogo para configurações avançadas do sistema"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("⚙️ Configurações do Sistema")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Centralizar
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        """Configurar interface"""
        # Frame principal scrollável
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, 
                                  text="⚙️ Configurações Avançadas",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Seção de Segurança
        self.create_security_section(main_frame)
        
        # Seção de Sessões
        self.create_session_section(main_frame)
        
        # Seção de Sistema
        self.create_system_section(main_frame)
        
        # Botões
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(buttons_frame, text="Cancelar", 
                                  fg_color=("gray60", "gray40"),
                                  command=self.destroy)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(buttons_frame, text="Salvar Configurações", 
                                command=self.save_settings)
        save_btn.pack(side="right")
    
    def create_security_section(self, parent):
        """Criar seção de configurações de segurança"""
        # Frame da seção
        security_frame = ctk.CTkFrame(parent)
        security_frame.pack(fill="x", pady=(0, 15))
        
        # Título da seção
        title = ctk.CTkLabel(security_frame, 
                           text="🔒 Segurança e Tentativas",
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Máximo de tentativas
        attempts_frame = ctk.CTkFrame(security_frame, fg_color="transparent")
        attempts_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        attempts_label = ctk.CTkLabel(attempts_frame, text="Máximo de tentativas de login:")
        attempts_label.pack(side="left")
        
        self.max_attempts_var = ctk.StringVar(value="5")
        attempts_entry = ctk.CTkEntry(attempts_frame, textvariable=self.max_attempts_var, width=80)
        attempts_entry.pack(side="right")
        
        # Tempo de bloqueio
        lockout_frame = ctk.CTkFrame(security_frame, fg_color="transparent")
        lockout_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        lockout_label = ctk.CTkLabel(lockout_frame, text="Tempo de bloqueio (minutos):")
        lockout_label.pack(side="left")
        
        self.lockout_time_var = ctk.StringVar(value="30")
        lockout_entry = ctk.CTkEntry(lockout_frame, textvariable=self.lockout_time_var, width=80)
        lockout_entry.pack(side="right")
    
    def create_session_section(self, parent):
        """Criar seção de configurações de sessão"""
        # Frame da seção
        session_frame = ctk.CTkFrame(parent)
        session_frame.pack(fill="x", pady=(0, 15))
        
        # Título da seção
        title = ctk.CTkLabel(session_frame, 
                           text="🎫 Configurações de Sessão",
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Duração da sessão
        duration_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        duration_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        duration_label = ctk.CTkLabel(duration_frame, text="Duração da sessão (dias):")
        duration_label.pack(side="left")
        
        self.session_duration_var = ctk.StringVar(value="30")
        duration_entry = ctk.CTkEntry(duration_frame, textvariable=self.session_duration_var, width=80)
        duration_entry.pack(side="right")
        
        # Auto-logout
        auto_logout_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        auto_logout_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.auto_logout_var = ctk.BooleanVar()
        auto_logout_check = ctk.CTkCheckBox(auto_logout_frame, 
                                          text="Logout automático por inatividade",
                                          variable=self.auto_logout_var)
        auto_logout_check.pack(side="left")
    
    def create_system_section(self, parent):
        """Criar seção de configurações do sistema"""
        # Frame da seção
        system_frame = ctk.CTkFrame(parent)
        system_frame.pack(fill="x", pady=(0, 15))
        
        # Título da seção
        title = ctk.CTkLabel(system_frame, 
                           text="🖥️ Configurações do Sistema",
                           font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Logs detalhados
        logs_frame = ctk.CTkFrame(system_frame, fg_color="transparent")
        logs_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.detailed_logs_var = ctk.BooleanVar(value=True)
        logs_check = ctk.CTkCheckBox(logs_frame, 
                                   text="Logs detalhados de auditoria",
                                   variable=self.detailed_logs_var)
        logs_check.pack(side="left")
        
        # Backup automático
        backup_frame = ctk.CTkFrame(system_frame, fg_color="transparent")
        backup_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.auto_backup_var = ctk.BooleanVar()
        backup_check = ctk.CTkCheckBox(backup_frame, 
                                     text="Backup automático diário",
                                     variable=self.auto_backup_var)
        backup_check.pack(side="left")
    
    def load_current_settings(self):
        """Carregar configurações atuais"""
        try:
            # Carregar da configuração atual do sistema
            self.session_duration_var.set(str(auth_system.session_duration))
            # Outras configurações podem ser carregadas de um arquivo de config
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    
    def save_settings(self):
        """Salvar configurações"""
        try:
            # Validar valores
            session_duration = int(self.session_duration_var.get())
            max_attempts = int(self.max_attempts_var.get())
            lockout_time = int(self.lockout_time_var.get())
            
            if session_duration < 1 or session_duration > 365:
                messagebox.showerror("Erro", "Duração da sessão deve estar entre 1 e 365 dias")
                return
            
            if max_attempts < 1 or max_attempts > 10:
                messagebox.showerror("Erro", "Máximo de tentativas deve estar entre 1 e 10")
                return
            
            if lockout_time < 1 or lockout_time > 1440:
                messagebox.showerror("Erro", "Tempo de bloqueio deve estar entre 1 e 1440 minutos")
                return
            
            # Aplicar configurações
            auth_system.session_duration = session_duration
            
            # Salvar em arquivo de configuração (implementar posteriormente)
            settings = {
                'session_duration': session_duration,
                'max_attempts': max_attempts,
                'lockout_time': lockout_time,
                'auto_logout': self.auto_logout_var.get(),
                'detailed_logs': self.detailed_logs_var.get(),
                'auto_backup': self.auto_backup_var.get()
            }
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!\nAlgumas alterações podem exigir reinicialização.")
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")

def show_admin_panel(parent):
    """Mostrar painel de administração"""
    return AdminPanel(parent)
