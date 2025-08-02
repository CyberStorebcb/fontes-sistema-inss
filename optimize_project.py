#!/usr/bin/env python3
"""
Script de Limpeza e Otimização - Sistema FONTES v3.0
Remove arquivos desnecessários e organiza o projeto
"""
import os
import shutil
from pathlib import Path

def clean_project():
    """Limpar arquivos desnecessários do projeto"""
    base_dir = Path(__file__).parent
    
    # Diretórios e arquivos para remover
    to_remove = [
        # Cache Python
        '__pycache__',
        '**/__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        
        # Cache pytest
        '.pytest_cache',
        
        # Logs antigos
        'logs/*.log.*',
        
        # Arquivos temporários
        '*.tmp',
        '*.temp',
        '.DS_Store',
        'Thumbs.db',
        
        # Arquivos de backup
        '*.bak',
        '*~',
        
        # Arquivos específicos do projeto (duplicados/antigos)
        'main.py',  # Substituído por main_unified.py
        'app_web.py',  # Duplicado do app.py
    ]
    
    removed_count = 0
    
    print("🧹 Iniciando limpeza do projeto...")
    
    for pattern in to_remove:
        if '**/' in pattern:
            # Busca recursiva
            for path in base_dir.rglob(pattern.replace('**/', '')):
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"📁 Removido diretório: {path.name}")
                    else:
                        path.unlink()
                        print(f"🗑️  Removido arquivo: {path.name}")
                    removed_count += 1
        else:
            # Busca direta
            for path in base_dir.glob(pattern):
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"📁 Removido diretório: {path.name}")
                    else:
                        path.unlink()
                        print(f"🗑️  Removido arquivo: {path.name}")
                    removed_count += 1
    
    print(f"\n✅ Limpeza concluída! {removed_count} itens removidos.")

def organize_structure():
    """Organizar estrutura de diretórios"""
    base_dir = Path(__file__).parent
    
    # Diretórios essenciais
    essential_dirs = [
        'src',
        'src/auth',
        'src/models',
        'src/views', 
        'src/controllers',
        'src/utils',
        'database',
        'logs',
        'static',
        'templates',
        'tests',
        'docs',
        'scripts'
    ]
    
    print("\n📂 Organizando estrutura de diretórios...")
    
    for dir_path in essential_dirs:
        full_path = base_dir / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Criado: {dir_path}")
    
    print("✅ Estrutura organizada!")

def create_gitignore():
    """Criar/atualizar .gitignore otimizado"""
    base_dir = Path(__file__).parent
    gitignore_path = base_dir / '.gitignore'
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/*.log
*.log

# Database
database/*.db-journal
session.dat

# Temporary files
*.tmp
*.temp
*.bak

# PyInstaller
*.manifest
*.spec
build/
dist/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project specific
profile_images/
temp/
"""
    
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("📝 .gitignore atualizado!")

def main():
    """Função principal de otimização"""
    print("🏛️ Sistema FONTES v3.0 - Otimização do Projeto")
    print("=" * 50)
    
    try:
        clean_project()
        organize_structure()
        create_gitignore()
        
        print("\n🎉 Otimização concluída com sucesso!")
        print("\n📋 Próximos passos recomendados:")
        print("1. Execute: pip install -r requirements-optimized.txt")
        print("2. Use: python main_unified.py --mode auto")
        print("3. Para web: python main_unified.py --mode web")
        print("4. Para GUI: python main_unified.py --mode gui")
        
    except Exception as e:
        print(f"❌ Erro durante otimização: {e}")

if __name__ == "__main__":
    main()
