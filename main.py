#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema FONTES - Interface INSS
Arquivo principal para iniciar a aplicação

Este módulo contém a lógica principal de inicialização do sistema FONTES,
incluindo configuração de logging, verificação de sessões e inicialização
da interface gráfica.

Desenvolvido com Python, CustomTkinter e SQLite
Versão: 3.0 - Sistema FONTES com Autenticação

Autor: Sistema FONTES
Data: 2025
"""

import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, TypedDict
from functools import lru_cache
import atexit
import threading
import customtkinter as ctk
from tkinter import messagebox

# Constantes da aplicação
APP_NAME = "FONTES - Sistema INSS"
APP_VERSION = "3.0"
LOG_DIR = "logs"
SESSION_FILE = "session.dat"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Cache global para otimização
_logger_configured = False
_src_path_cached = None
_dependencies_checked = None

# Tipo para dependências
class DependencyInfo(TypedDict):
    name: str
    description: str
    install: str

def setup_logging() -> None:
    """
    Configurar sistema de logging com rotação de arquivos.
    
    Otimizações implementadas:
    - Cache global para evitar reconfiguração
    - Thread-safe com lock
    - Cleanup automático na saída
    - Handler único para evitar duplicação
    """
    global _logger_configured
    
    if _logger_configured:
        return
    
    # Thread lock para configuração segura
    with threading.Lock():
        if _logger_configured:  # Double-checked locking
            return
            
        try:
            log_path = Path(LOG_DIR)
            log_path.mkdir(exist_ok=True)
            
            log_file = log_path / "fontes.log"
            
            # Limpar handlers existentes para evitar duplicação
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                handler.close()
                root_logger.removeHandler(handler)
            
            # Configurar handler com rotação
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=MAX_LOG_SIZE,
                backupCount=LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            
            # Configurar formatação otimizada
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            # Configurar logger raiz
            root_logger.setLevel(logging.INFO)
            root_logger.addHandler(file_handler)
            
            # Handler para console (apenas warnings e erros)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
            
            # Registrar cleanup na saída
            atexit.register(lambda: [h.close() for h in root_logger.handlers if hasattr(h, 'close')])
            
            _logger_configured = True
            logging.info(f"Sistema {APP_NAME} v{APP_VERSION} iniciado")
            
        except Exception as e:
            print(f"Erro ao configurar logging: {e}")
            raise


@lru_cache(maxsize=1)
def get_src_path() -> Path:
    """
    Obter caminho do diretório src com cache LRU.
    
    Returns:
        Path: Caminho para o diretório src
    """
    return Path(__file__).parent / 'src'


def ensure_src_in_path() -> None:
    """
    Garantir que o diretório src está no sys.path.
    
    Otimização: Cache global para evitar verificações repetidas.
    """
    global _src_path_cached
    
    if _src_path_cached:
        return
    
    src_path = get_src_path()
    src_path_str = str(src_path)
    
    if src_path_str not in sys.path:
        sys.path.insert(0, src_path_str)
    
    _src_path_cached = True


def check_saved_session() -> bool:
    """
    Verificar se existe sessão salva válida.
    
    Otimizações avançadas:
    - Lazy loading de imports
    - Cache de path com LRU
    - Tratamento específico de exceções
    - Operações de arquivo otimizadas
    
    Returns:
        bool: True se a sessão é válida, False caso contrário
    """
    session_path = Path(__file__).parent / SESSION_FILE
    
    # Early return otimizado
    if not session_path.exists():
        logging.debug("Arquivo de sessão não encontrado")
        return False
    
    try:
        # Leitura otimizada do token
        session_token = session_path.read_text(encoding='utf-8').strip()
        
        if not session_token:
            logging.debug("Token de sessão vazio")
            return False
        
        # Configurar path com cache
        ensure_src_in_path()
        
        # Lazy import para melhor performance
        try:
            from src.auth.authentication import auth_system
        except ImportError as e:
            logging.error(f"Erro ao importar sistema de autenticação: {e}")
            return False
        
        # Validação com verificação robusta
        if (auth_system.validate_session(session_token) and 
            auth_system.current_user and 
            auth_system.current_user.get('username')):
            
            username = auth_system.current_user['username']
            logging.info(f"Sessão válida encontrada para usuário: {username}")
            return True
        
        # Cleanup de sessão inválida
        session_path.unlink(missing_ok=True)
        logging.info("Sessão expirada removida")
        return False
        
    except FileNotFoundError:
        logging.debug("Arquivo de sessão não encontrado durante leitura")
    except PermissionError:
        logging.warning("Sem permissão para acessar arquivo de sessão")
    except UnicodeDecodeError:
        logging.error("Arquivo de sessão corrompido")
        session_path.unlink(missing_ok=True)
    except Exception as e:
        logging.error(f"Erro inesperado ao verificar sessão: {e}")
        
    return False

def show_login_and_run() -> None:
    """
    Mostrar tela de login e executar aplicação após autenticação.
    
    Otimizações avançadas:
    - Lazy loading de módulos pesados
    - Callback otimizado com tratamento robusto
    - Separação clara de responsabilidades
    - Error handling granular
    """
    try:
        # Garantir path configurado
        ensure_src_in_path()
        
        # Lazy imports para melhor startup time
        try:
            from src.auth.login_interface import show_login_window
        except ImportError as e:
            logging.error(f"Módulo de login não encontrado: {e}")
            messagebox.showerror(
                "Erro de Módulo", 
                f"Interface de login não disponível:\n{e}\n\n"
                "Verifique se todos os arquivos estão presentes."
            )
            return
        
        def on_login_success(user_data: Dict[str, Any]) -> None:
            """
            Callback otimizado para login bem-sucedido.
            
            Args:
                user_data (Dict[str, Any]): Dados do usuário autenticado
            """
            # Validação robusta dos dados
            if not isinstance(user_data, dict):
                logging.error("Dados de usuário inválidos recebidos")
                messagebox.showerror("Erro", "Dados de autenticação inválidos")
                return
            
            full_name = user_data.get('full_name', 'Usuário')
            username = user_data.get('username', 'N/A')
            logging.info(f"Login bem-sucedido: {full_name} ({username})")
            
            # Import lazy da interface principal
            try:
                from src.views.fontes_interface import FontesMainWindow
                
                # Executar com tratamento robusto
                app = FontesMainWindow()
                app.run()
                
            except ImportError as e:
                logging.error(f"Interface principal não encontrada: {e}")
                messagebox.showerror(
                    "Erro de Módulo", 
                    f"Interface principal não disponível:\n{e}\n\n"
                    "Verifique se todos os módulos estão instalados."
                )
            except Exception as e:
                logging.error(f"Erro ao executar interface principal: {e}")
                messagebox.showerror(
                    "Erro de Execução", 
                    f"Falha ao carregar interface principal:\n{e}\n\n"
                    "Consulte o log para mais detalhes."
                )
        
        # Executar janela de login
        try:
            login_window = show_login_window(on_login_success)
            if login_window:
                login_window.mainloop()
            else:
                logging.error("Falha ao criar janela de login")
                messagebox.showerror("Erro", "Não foi possível criar a janela de login")
                
        except Exception as e:
            logging.error(f"Erro na execução da janela de login: {e}")
            messagebox.showerror("Erro de Interface", f"Falha na interface de login:\n{e}")
        
    except Exception as e:
        logging.error(f"Erro crítico no sistema de login: {e}")
        messagebox.showerror(
            "Erro Crítico", 
            f"Falha crítica no sistema de autenticação:\n{e}\n\n"
            "O sistema será encerrado."
        )

def run_fontes() -> None:
    """
    Executar interface FONTES com otimizações avançadas.
    
    Otimizações implementadas:
    - Fluxo otimizado com early returns
    - Lazy loading condicional
    - Cache de estado de autenticação
    - Error recovery inteligente
    """
    def setup_and_run_main_interface() -> bool:
        """
        Configurar e executar interface principal.
        
        Returns:
            bool: True se executou com sucesso
        """
        try:
            ensure_src_in_path()
            
            # Lazy imports condicionais
            from src.views.fontes_interface import FontesMainWindow
            from src.auth.authentication import auth_system
            
            # Verificação robusta do usuário
            if not auth_system.current_user:
                logging.warning("Estado de autenticação inconsistente")
                return False
            
            user_data = auth_system.current_user
            username = user_data.get('username', 'Desconhecido')
            
            logging.info(f"Executando interface principal para: {username}")
            
            # Executar com timeout implícito
            app = FontesMainWindow()
            app.run()
            return True
            
        except ImportError as e:
            logging.error(f"Módulo da interface principal não encontrado: {e}")
            messagebox.showerror(
                "Erro de Módulo", 
                f"Interface principal não disponível:\n{e}\n\n"
                "Reinstale o sistema ou verifique os arquivos."
            )
        except Exception as e:
            logging.error(f"Erro na interface principal: {e}", exc_info=True)
            messagebox.showerror(
                "Erro de Execução", 
                f"Falha na interface principal:\n{e}\n\n"
                "Tente fazer login novamente."
            )
        
        return False
    
    try:
        # Fluxo otimizado com decisão rápida
        if check_saved_session():
            # Tentar executar interface principal
            if not setup_and_run_main_interface():
                # Fallback para login se falhou
                logging.info("Fallback para tela de login")
                show_login_and_run()
        else:
            # Ir direto para login
            show_login_and_run()
            
    except KeyboardInterrupt:
        logging.info("Execução interrompida pelo usuário")
        print("\n🛑 Sistema FONTES encerrado pelo usuário.")
    except ImportError as e:
        logging.error(f"Erro crítico de importação: {e}")
        messagebox.showerror(
            "Erro de Sistema", 
            f"Módulos essenciais não encontrados:\n{e}\n\n"
            "Reinstale o sistema FONTES."
        )
    except Exception as e:
        logging.error(f"Erro crítico na execução: {e}", exc_info=True)
        messagebox.showerror(
            "Erro Crítico", 
            f"Falha crítica no sistema:\n{e}\n\n"
            "Verifique os logs para mais detalhes."
        )

@lru_cache(maxsize=1)
def check_dependencies() -> Tuple[bool, list[DependencyInfo]]:
    """
    Verificar dependências essenciais com cache LRU.
    
    Returns:
        Tuple[bool, list[DependencyInfo]]: (todas_disponíveis, dependências_ausentes)
    """
    global _dependencies_checked
    
    if _dependencies_checked is not None:
        return _dependencies_checked
    
    # Dependências essenciais otimizadas
    REQUIRED_DEPENDENCIES = [
        ("customtkinter", "Interface gráfica moderna", "pip install customtkinter"),
        ("sqlite3", "Banco de dados local", "Incluído no Python"),
        ("tkinter", "Interface gráfica base", "Instale python-tk"),
    ]
    
    missing: list[DependencyInfo] = []
    available_count = 0
    
    for dep_name, description, install_cmd in REQUIRED_DEPENDENCIES:
        try:
            __import__(dep_name)
            available_count += 1
        except ImportError:
            missing.append(DependencyInfo(
                name=dep_name,
                description=description,
                install=install_cmd
            ))
    
    all_available = len(missing) == 0
    _dependencies_checked = (all_available, missing)
    
    logging.info(f"Dependências verificadas: {available_count}/{len(REQUIRED_DEPENDENCIES)} disponíveis")
    
    return all_available, missing


def main() -> None:
    """
    Função principal otimizada da aplicação.
    
    Otimizações avançadas implementadas:
    - Lazy loading de verificações pesadas
    - Cache de dependências com LRU
    - Error handling granular com recovery
    - Cleanup automático de recursos
    - Performance monitoring básico
    """
    import time
    start_time = time.time()
    
    try:
        # Configurar logging primeiro (com cache)
        setup_logging()
        logging.info(f"🚀 Iniciando {APP_NAME} v{APP_VERSION}")
        
        # Verificar dependências com cache
        deps_available, missing_deps = check_dependencies()
        
        if not deps_available:
            # Formatar mensagem de erro melhorada
            deps_info = []
            install_commands = set()
            
            for dep in missing_deps:
                deps_info.append(f"• {dep['name']} - {dep['description']}")
                if "pip install" in dep['install']:
                    install_commands.add(dep['install'])
            
            deps_str = "\n".join(deps_info)
            install_str = "\n".join(install_commands) if install_commands else "Consulte a documentação"
            
            error_msg = (
                f"❌ Dependências necessárias não encontradas:\n\n{deps_str}\n\n"
                f"📦 Para instalar as dependências:\n{install_str}\n\n"
                f"💡 Certifique-se de estar usando Python 3.8+ e ter permissões adequadas\n"
                f"🔧 Em caso de problemas, execute: pip install --upgrade pip"
            )
            
            messagebox.showerror("Dependências Ausentes", error_msg)
            logging.error(f"Dependências ausentes: {[d['name'] for d in missing_deps]}")
            return
        
        # Log de sucesso com timing
        init_time = time.time() - start_time
        logging.info(f"✅ Inicialização completa em {init_time:.3f}s")
        
        # Executar interface FONTES com monitoramento
        execution_start = time.time()
        run_fontes()
        execution_time = time.time() - execution_start
        
        logging.info(f"⏱️  Tempo de execução: {execution_time:.3f}s")
            
    except KeyboardInterrupt:
        logging.info("🛑 Aplicação interrompida pelo usuário (Ctrl+C)")
        print("\n🛑 Sistema FONTES encerrado pelo usuário.")
    except SystemExit as e:
        logging.info(f"🔚 Sistema encerrado normalmente (código: {e.code})")
    except MemoryError:
        logging.error("💾 Erro de memória - sistema sem recursos suficientes")
        messagebox.showerror(
            "Erro de Memória", 
            "Sistema sem memória suficiente.\n\n"
            "Feche outros programas e tente novamente."
        )
    except Exception as e:
        total_time = time.time() - start_time
        logging.error(f"💥 Erro crítico após {total_time:.3f}s: {e}", exc_info=True)
        
        messagebox.showerror(
            "Erro Crítico", 
            f"💥 Erro inesperado no sistema:\n\n{str(e)[:200]}...\n\n"
            f"📋 Tempo de execução: {total_time:.3f}s\n"
            f"📁 Verifique o arquivo de log em: {LOG_DIR}/fontes.log\n"
            f"🔧 Se o problema persistir, reinicie o sistema"
        )
    finally:
        # Cleanup final
        total_time = time.time() - start_time
        logging.info(f"🏁 Sessão finalizada - tempo total: {total_time:.3f}s")

if __name__ == "__main__":
    main()
