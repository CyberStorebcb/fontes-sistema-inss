"""
Módulo de Autenticação - Sistema FONTES
Sistema completo de login, sessões e controle de usuários
"""

from .authentication import auth_system, AuthenticationSystem
from .login_clean import show_login_window, LoginWindow
from .admin_panel import show_admin_panel, AdminPanel

__all__ = [
    'auth_system',
    'AuthenticationSystem', 
    'show_login_window',
    'LoginWindow',
    'show_admin_panel',
    'AdminPanel'
]
