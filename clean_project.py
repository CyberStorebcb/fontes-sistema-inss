#!/usr/bin/env python3
"""
Script para limpeza do projeto - Remove arquivos não essenciais
Mantém apenas os arquivos necessários para o funcionamento do sistema
"""

import os
import shutil
from pathlib import Path

def remove_file_safe(filepath):
    """Remove arquivo de forma segura"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"✅ Removido: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover {filepath}: {e}")
        return False

def remove_dir_safe(dirpath):
    """Remove diretório de forma segura"""
    try:
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
            print(f"✅ Removido diretório: {dirpath}")
        return True
    except Exception as e:
        print(f"❌ Erro ao remover diretório {dirpath}: {e}")
        return False

def clean_project():
    """Limpar arquivos não essenciais do projeto"""
    
    base_path = Path(__file__).parent
    
    print("🧹 INICIANDO LIMPEZA DO PROJETO")
    print("=" * 50)
    
    # Arquivos de teste e debug (não essenciais)
    test_files = [
        "check_db.py",
        "cleanup_project.py", 
        "config.py",
        "config_new.py",
        "debug_govbr.py",
        "demo_optimizations.py",
        "final_report.py",
        "fix_imports.py",
        "quick_test.py",
        "run.py", 
        "test_advanced_optimizations.py",
        "test_auth.py",
        "test_automation.py",
        "test_modern_dialogs.py",
        "test_optimized_functions.py",
        "verify_project.py",
        "visual_config.py",
        "__init__.py"
    ]
    
    # Arquivos de documentação (não essenciais para funcionamento)
    doc_files = [
        "CORREÇÕES_APLICADAS.md",
        "DIALOGS_MODERNOS_IMPLEMENTADO.md",
        "ERROS_FINALMENTE_CORRIGIDOS.md",
        "GUIA_MEU_INSS.md",
        "INTERFACE_MELHORADA.md", 
        "PROBLEMAS_CORRIGIDOS.md",
        "PROJETO_FINALIZADO.md",
        "SISTEMA_AUTENTICACAO.md",
        "SISTEMA_COMPLETO.md",
        "SISTEMA_PRONTO.md",
        "SOLUCAO_PROBLEMAS_MEU_INSS.md",
        "TUTORIAL_LOGIN.md",
        "TYPE_ERRORS_CORRIGIDOS.md",
        "VERIFICACAO_COMPLETA.md",
        "WARNINGS_CORRIGIDOS.md"
    ]
    
    # Arquivos batch (não essenciais)
    batch_files = [
        "diagnostico.bat",
        "INICIAR_SISTEMA.bat",
        "RESET_CONTAS.bat",
        "start.bat"
    ]
    
    # Arquivos duplicados/não utilizados
    duplicate_files = [
        "requirements_new.txt",
        "reset_account.py"  # Mantém apenas se for usado
    ]
    
    print("📁 Removendo arquivos de teste e debug...")
    for file in test_files:
        remove_file_safe(base_path / file)
    
    print("\\n📚 Removendo arquivos de documentação desnecessários...")
    for file in doc_files:
        remove_file_safe(base_path / file)
        
    print("\\n⚙️ Removendo arquivos batch...")
    for file in batch_files:
        remove_file_safe(base_path / file)
        
    print("\\n🔄 Removendo arquivos duplicados...")
    for file in duplicate_files:
        remove_file_safe(base_path / file)
    
    # Limpar diretórios não essenciais
    print("\\n📂 Removendo diretórios não essenciais...")
    
    # Remove diretório docs (documentação)
    remove_dir_safe(base_path / "docs")
    
    # Remove diretório drivers se existir (selenium baixa automaticamente)
    remove_dir_safe(base_path / "drivers")
    
    # Remove cache Python
    print("\\n🗑️ Limpando cache Python...")
    remove_dir_safe(base_path / "__pycache__")
    remove_dir_safe(base_path / "src" / "__pycache__")
    remove_dir_safe(base_path / "src" / "auth" / "__pycache__")
    remove_dir_safe(base_path / "src" / "views" / "__pycache__")
    remove_dir_safe(base_path / "src" / "utils" / "__pycache__")
    remove_dir_safe(base_path / "src" / "controllers" / "__pycache__")
    remove_dir_safe(base_path / "src" / "models" / "__pycache__")
    
    # Limpar arquivos duplicados em src/views
    print("\\n🔄 Removendo arquivos duplicados em src/views...")
    remove_file_safe(base_path / "src" / "views" / "fontes_integration_new.py")
    remove_file_safe(base_path / "src" / "views" / "fontes_interface_new.py")
    
    # Verificar se controllers e models estão sendo usados
    controllers_path = base_path / "src" / "controllers"
    models_path = base_path / "src" / "models"
    
    if controllers_path.exists():
        if not any(controllers_path.iterdir()):
            print("📁 Removendo diretório controllers vazio...")
            remove_dir_safe(controllers_path)
    
    if models_path.exists():
        if not any(models_path.iterdir()):
            print("📁 Removendo diretório models vazio...")
            remove_dir_safe(models_path)
    
    print("\\n" + "=" * 50)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("\\n📋 ARQUIVOS ESSENCIAIS MANTIDOS:")
    print("   • main.py (arquivo principal)")
    print("   • requirements.txt (dependências)")
    print("   • README.md (documentação principal)")
    print("   • ESTRUTURA_PROJETO.md (estrutura)")
    print("   • pyrightconfig.json (configuração)")
    print("   • src/ (código fonte)")
    print("   • database/ (banco de dados)")
    print("   • logs/ (sistema de logs)")
    print("   • .venv/ (ambiente virtual)")
    print("   • .vscode/ (configurações VS Code)")
    print("   • .gitignore (controle de versão)")

if __name__ == "__main__":
    clean_project()
