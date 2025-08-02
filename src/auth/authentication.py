"""
Sistema de Autenticação - FONTES
Gerenciamento de usuários e controle de acesso

Este módulo implementa um sistema completo de autenticação com:
- Gerenciamento de usuários e perfis
- Sistema de sessões com tokens
- Logs de acesso e auditoria
- Criptografia de senhas com PBKDF2
- Controle de tentativas de login

Autor: Sistema FONTES
Data: 2025
"""

import sqlite3
import hashlib
import os
import datetime
import uuid
import base64
from typing import Optional, Dict, List, Tuple, Union
from pathlib import Path
import logging

# Constantes do sistema
DEFAULT_SESSION_DURATION = 30  # dias
MAX_LOGIN_ATTEMPTS = 999  # Desabilitado - número muito alto para não bloquear
LOCKOUT_DURATION = 0  # Desabilitado
PBKDF2_ITERATIONS = 100000


class AuthenticationSystem:
    """
    Sistema de autenticação e controle de usuários.
    
    Fornece funcionalidades completas de autenticação incluindo:
    - Criação e gerenciamento de usuários
    - Sistema de sessões seguras
    - Logs de acesso para auditoria
    - Controle de tentativas de login
    """
    
    def __init__(self, db_path: str = "database/users.db") -> None:
        """
        Inicializar sistema de autenticação.
        
        Args:
            db_path (str): Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.session_duration = DEFAULT_SESSION_DURATION
        self.current_user: Optional[Dict] = None
        self.session_token: Optional[str] = None
        self.session_expiry: Optional[datetime.datetime] = None
        
        # Criar diretório do banco se não existir
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
        self._create_default_admin()
    
    def _create_tables(self) -> None:
        """Criar tabelas do banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    role TEXT DEFAULT 'user',
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME,
                    login_attempts INTEGER DEFAULT 0,
                    locked_until DATETIME
                )
            ''')
            
            # Tabela de sessões
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabela de logs de acesso
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    action TEXT NOT NULL,
                    ip_address TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN DEFAULT 1,
                    details TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Índices para melhor performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON access_logs(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_username ON access_logs(username)')
            
            conn.commit()
            logging.info("Tabelas do banco de dados criadas/verificadas com sucesso")
    
    def _create_default_admin(self) -> None:
        """
        Criar usuário administrador padrão.
        
        Cria um usuário admin com credenciais padrão se não existir nenhum
        usuário administrador no sistema.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar se já existe um admin
                cursor.execute("SELECT id FROM users WHERE role = 'admin'")
                if cursor.fetchone():
                    logging.info("Usuário administrador já existe")
                    return
                
                # Criar admin padrão
                admin_password = self._hash_password("admin123")
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("admin", admin_password, "Administrador", "admin@fontes.com", "admin"))
                
                conn.commit()
                logging.info("Usuário administrador padrão criado (admin/admin123)")
                
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar admin padrão: {e}")
    
    def _hash_password(self, password: str) -> str:
        """
        Gerar hash seguro da senha usando PBKDF2.
        
        Args:
            password (str): Senha em texto plano
            
        Returns:
            str: Hash da senha codificado em base64
        """
        salt = os.urandom(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, PBKDF2_ITERATIONS)
        return base64.b64encode(salt + pwdhash).decode('utf-8')
    
    def _verify_password(self, stored_password: str, provided_password: str) -> bool:
        """
        Verificar se a senha fornecida corresponde ao hash armazenado.
        Suporta tanto formato base64 quanto formato salt:hash
        
        Args:
            stored_password (str): Hash da senha armazenado
            provided_password (str): Senha fornecida pelo usuário
            
        Returns:
            bool: True se a senha estiver correta
        """
        try:
            # Verificar se é formato salt:hash (novo formato do reset_account.py)
            if ':' in stored_password:
                salt_hex, hash_hex = stored_password.split(':', 1)
                salt = bytes.fromhex(salt_hex)
                stored_hash = bytes.fromhex(hash_hex)
                pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, PBKDF2_ITERATIONS)
                return pwdhash.hex() == hash_hex
            else:
                # Formato base64 (formato original)
                stored_data = base64.b64decode(stored_password.encode('utf-8'))
                salt = stored_data[:32]
                stored_hash = stored_data[32:]
                pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, PBKDF2_ITERATIONS)
                return pwdhash == stored_hash
            
        except Exception as e:
            logging.error(f"Erro na verificação de senha: {e}")
            return False
    
    def authenticate(self, username: str, password: str, ip_address: Optional[str] = None) -> Tuple[bool, str, Optional[Dict]]:
        """
        Autenticar usuário no sistema.
        
        Args:
            username (str): Nome de usuário
            password (str): Senha fornecida
            ip_address (str, optional): Endereço IP do usuário
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (sucesso, mensagem, dados_usuario)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Buscar usuário
                cursor.execute('''
                    SELECT id, username, password_hash, full_name, email, role, is_active, 
                           login_attempts, locked_until
                    FROM users WHERE username = ?
                ''', (username,))
                
                user = cursor.fetchone()
                
                if not user:
                    self._log_access(None, username, "LOGIN_FAILED", ip_address, False, "Usuário não encontrado")
                    return False, "Usuário ou senha incorretos", None
                
                user_id, db_username, password_hash, full_name, email, role, is_active, login_attempts, locked_until = user
                
                # Verificar se conta está ativa
                if not is_active:
                    self._log_access(user_id, username, "LOGIN_BLOCKED", ip_address, False, "Conta desativada")
                    return False, "Conta desativada", None

                # Verificar senha
                if not self._verify_password(password_hash, password):
                    # Incrementar tentativas de login (apenas para log)
                    new_attempts = login_attempts + 1
                    cursor.execute('''
                        UPDATE users SET login_attempts = ? WHERE id = ?
                    ''', (new_attempts, user_id))
                    
                    conn.commit()
                    self._log_access(user_id, username, "LOGIN_FAILED", ip_address, False, f"Senha incorreta - Tentativa {new_attempts}")
                    return False, "Usuário ou senha incorretos", None                # Login bem-sucedido - resetar tentativas
                cursor.execute('''
                    UPDATE users 
                    SET login_attempts = 0, locked_until = NULL, last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                
                # Criar sessão
                session_token = str(uuid.uuid4())
                expires_at = datetime.datetime.now() + datetime.timedelta(days=self.session_duration)
                
                cursor.execute('''
                    INSERT INTO sessions (user_id, session_token, expires_at, ip_address)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, session_token, expires_at.isoformat(), ip_address))
                
                conn.commit()
                
                # Definir sessão atual
                self.current_user = {
                    'id': user_id,
                    'username': db_username,
                    'full_name': full_name,
                    'email': email,
                    'role': role
                }
                self.session_token = session_token
                self.session_expiry = expires_at
                
                self._log_access(user_id, username, "LOGIN_SUCCESS", ip_address, True, "Login realizado com sucesso")
                return True, "Login realizado com sucesso", self.current_user
                
        except Exception as e:
            logging.error(f"Erro na autenticação: {e}")
            return False, "Erro interno do sistema", None
    
    def logout(self, ip_address: Optional[str] = None):
        """Fazer logout do usuário"""
        if self.session_token:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE sessions SET is_active = 0 WHERE session_token = ?
                    ''', (self.session_token,))
                    conn.commit()
                
                if self.current_user:
                    self._log_access(self.current_user['id'], self.current_user['username'], 
                                   "LOGOUT", ip_address or "unknown", True, "Logout realizado")
                
            except Exception as e:
                logging.error(f"Erro no logout: {e}")
        
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
    
    def validate_session(self, session_token: str) -> bool:
        """Validar sessão ativa"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT s.user_id, s.expires_at, u.username, u.full_name, u.email, u.role, u.is_active
                    FROM sessions s
                    JOIN users u ON s.user_id = u.id
                    WHERE s.session_token = ? AND s.is_active = 1
                ''', (session_token,))
                
                result = cursor.fetchone()
                if not result:
                    return False
                
                user_id, expires_at, username, full_name, email, role, is_active = result
                
                # Verificar se sessão expirou
                expiry_time = datetime.datetime.fromisoformat(expires_at)
                if datetime.datetime.now() > expiry_time:
                    cursor.execute('UPDATE sessions SET is_active = 0 WHERE session_token = ?', 
                                 (session_token,))
                    conn.commit()
                    return False
                
                # Verificar se usuário ainda está ativo
                if not is_active:
                    cursor.execute('UPDATE sessions SET is_active = 0 WHERE session_token = ?', 
                                 (session_token,))
                    conn.commit()
                    return False
                
                # Atualizar sessão atual
                self.current_user = {
                    'id': user_id,
                    'username': username,
                    'full_name': full_name,
                    'email': email,
                    'role': role
                }
                self.session_token = session_token
                self.session_expiry = expiry_time
                
                return True
                
        except Exception as e:
            logging.error(f"Erro na validação de sessão: {e}")
            return False
    
    def _log_access(self, user_id: Optional[int], username: str, action: str, 
                   ip_address: Optional[str], success: bool, details: str):
        """Registrar log de acesso"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO access_logs (user_id, username, action, ip_address, success, details)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, username, action, ip_address or "unknown", success, details))
                conn.commit()
        except Exception as e:
            logging.error(f"Erro ao registrar log: {e}")
    
    def update_user(self, user_id, username, full_name, email=None, role="user"):
        """Atualizar dados de um usuário existente"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar se o novo username já existe (se diferente do atual)
            cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
            current_user = cursor.fetchone()
            
            if not current_user:
                return False, "Usuário não encontrado"
            
            current_username = current_user[1]
            
            # Se o username mudou, verificar se já existe
            if username != current_username:
                cursor.execute('SELECT id FROM users WHERE username = ? AND id != ?', (username, user_id))
                if cursor.fetchone():
                    return False, "Este nome de usuário já está em uso"
            
            # Atualizar dados
            cursor.execute('''
                UPDATE users 
                SET username = ?, full_name = ?, email = ?, role = ?
                WHERE id = ?
            ''', (username, full_name, email, role, user_id))
            
            conn.commit()
            
            # Log da alteração
            self._log_access(user_id, username, 'USER_UPDATED', 'system', True, f"Dados do usuário atualizados")
            
            return True, "Usuário atualizado com sucesso"
            
        except Exception as e:
            return False, f"Erro ao atualizar usuário: {str(e)}"
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """Deletar um usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar se usuário existe
                cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                
                if not user:
                    return False, "Usuário não encontrado"
                
                username = user[0]
                
                # Não permitir deletar o último admin
                cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin" AND is_active = 1', ())
                admin_count = cursor.fetchone()[0]
                
                cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
                user_role = cursor.fetchone()[0]
                
                if user_role == 'admin' and admin_count <= 1:
                    return False, "Não é possível remover o último administrador do sistema"
                
                # Remover sessões ativas do usuário
                cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
                
                # Remover usuário (logs são mantidos para auditoria)
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                
                conn.commit()
                
                # Log da remoção
                self._log_access(None, username, 'USER_DELETED', 'system', True, f"Usuário {username} removido do sistema")
                
                return True, f"Usuário {username} removido com sucesso"
                
        except Exception as e:
            return False, f"Erro ao remover usuário: {str(e)}"
    
    def create_user(self, username: str, password: str, full_name: str, 
                   email: Optional[str] = None, role: str = 'user') -> Tuple[bool, str]:
        """Criar novo usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar se usuário já existe
                cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                if cursor.fetchone():
                    return False, "Nome de usuário já existe"
                
                # Criar usuário
                password_hash = self._hash_password(password)
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, full_name, email, role))
                
                conn.commit()
                logging.info(f"Usuário {username} criado com sucesso")
                return True, "Usuário criado com sucesso"
                
        except Exception as e:
            logging.error(f"Erro ao criar usuário: {e}")
            return False, f"Erro ao criar usuário: {e}"
    
    def get_users(self) -> List[Dict]:
        """Obter lista de usuários"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, full_name, email, role, is_active, 
                           created_at, last_login
                    FROM users ORDER BY created_at DESC
                ''')
                
                users = []
                for row in cursor.fetchall():
                    users.append({
                        'id': row[0],
                        'username': row[1],
                        'full_name': row[2],
                        'email': row[3],
                        'role': row[4],
                        'is_active': row[5],
                        'created_at': row[6],
                        'last_login': row[7]
                    })
                
                return users
                
        except Exception as e:
            logging.error(f"Erro ao obter usuários: {e}")
            return []
    
    def get_user_logs(self, user_id):
        """Obter logs específicos de um usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Buscar usuário para obter o username
                cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
                user_row = cursor.fetchone()
                
                if not user_row:
                    return []
                
                username = user_row[0]
                
                # Buscar logs do usuário
                cursor.execute('''
                    SELECT timestamp, action, success, details, ip_address
                    FROM access_logs 
                    WHERE username = ? 
                    ORDER BY timestamp DESC
                    LIMIT 1000
                ''', (username,))
                
                logs = []
                for row in cursor.fetchall():
                    logs.append({
                        'timestamp': row[0],
                        'action': row[1],
                        'success': row[2],
                        'details': row[3],
                        'ip_address': row[4]
                    })
                
                return logs
                
        except Exception as e:
            logging.error(f"Erro ao obter logs do usuário: {e}")
            return []
    
    def get_all_logs(self, limit=1000):
        """Obter todos os logs do sistema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT timestamp, username, action, success, details, ip_address
                    FROM access_logs 
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                logs = []
                for row in cursor.fetchall():
                    logs.append({
                        'timestamp': row[0],
                        'username': row[1],
                        'action': row[2],
                        'success': row[3],
                        'details': row[4],
                        'ip_address': row[5]
                    })
                
                return logs
                
        except Exception as e:
            logging.error(f"Erro ao obter logs: {e}")
            return []
    
    def update_user_status(self, user_id: int, is_active: bool) -> Tuple[bool, str]:
        """Ativar/desativar usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET is_active = ? WHERE id = ?
                ''', (is_active, user_id))
                
                if cursor.rowcount == 0:
                    return False, "Usuário não encontrado"
                
                # Desativar sessões ativas se usuário foi desativado
                if not is_active:
                    cursor.execute('''
                        UPDATE sessions SET is_active = 0 WHERE user_id = ?
                    ''', (user_id,))
                
                conn.commit()
                status = "ativado" if is_active else "desativado"
                return True, f"Usuário {status} com sucesso"
                
        except Exception as e:
            logging.error(f"Erro ao atualizar status do usuário: {e}")
            return False, f"Erro ao atualizar usuário: {e}"
    
    def change_password(self, user_id: int, new_password: str) -> Tuple[bool, str]:
        """Alterar senha do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                password_hash = self._hash_password(new_password)
                cursor.execute('''
                    UPDATE users SET password_hash = ?, login_attempts = 0, locked_until = NULL
                    WHERE id = ?
                ''', (password_hash, user_id))
                
                if cursor.rowcount == 0:
                    return False, "Usuário não encontrado"
                
                conn.commit()
                return True, "Senha alterada com sucesso"
                
        except Exception as e:
            logging.error(f"Erro ao alterar senha: {e}")
            return False, f"Erro ao alterar senha: {e}"
    
    def get_access_logs(self, limit: int = 100) -> List[Dict]:
        """Obter logs de acesso"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT username, action, timestamp, success, details, ip_address
                    FROM access_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                logs = []
                for row in cursor.fetchall():
                    logs.append({
                        'username': row[0],
                        'action': row[1],
                        'timestamp': row[2],
                        'success': row[3],
                        'details': row[4],
                        'ip_address': row[5]
                    })
                
                return logs
                
        except Exception as e:
            logging.error(f"Erro ao obter logs: {e}")
            return []

# Instância global do sistema de autenticação
auth_system = AuthenticationSystem()
