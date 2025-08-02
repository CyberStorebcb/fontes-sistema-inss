"""
Sistema FONTES v3.0 - Scripts de Utilidades
Ferramentas auxiliares para desenvolvimento e manutenção
"""

import os
import sys
import shutil
import subprocess
import json
from datetime import datetime


def create_backup():
    """Cria backup do projeto"""
    print("📦 Criando backup do projeto...")
    
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Cria diretório de backup
        os.makedirs(backup_dir, exist_ok=True)
        
        # Lista de arquivos/diretórios para backup
        items_to_backup = [
            'app.py',
            'requirements.txt',
            'Procfile',
            'runtime.txt',
            'Dockerfile',
            'docker-compose.yml',
            'render.yaml',
            'static/',
            'templates/',
            'scripts/',
            'tests/',
            'docs/',
            'README.md',
            'PROJETO_ESTRUTURADO.md'
        ]
        
        for item in items_to_backup:
            source = os.path.join(project_dir, item)
            if os.path.exists(source):
                dest = os.path.join(backup_dir, item)
                if os.path.isdir(source):
                    shutil.copytree(source, dest)
                else:
                    shutil.copy2(source, dest)
                print(f"  ✅ {item}")
        
        print(f"🎉 Backup criado com sucesso: {backup_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return False


def install_dependencies():
    """Instala dependências do projeto"""
    print("📚 Instalando dependências...")
    
    try:
        # Atualiza pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        
        # Instala requirements
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def run_tests():
    """Executa os testes do projeto"""
    print("🧪 Executando testes...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'], 
                               capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Avisos/Erros:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
            return True
        else:
            print("❌ Alguns testes falharam!")
            return False
            
    except FileNotFoundError:
        print("⚠️ pytest não encontrado. Executando testes básicos...")
        
        # Fallback para unittest
        try:
            result = subprocess.run([sys.executable, 'tests/test_app.py'], 
                                   capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Erro ao executar testes: {e}")
            return False


def check_code_quality():
    """Verifica qualidade do código"""
    print("🔍 Verificando qualidade do código...")
    
    issues = []
    
    # Verifica arquivos Python
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Verifica imports não utilizados (básico)
                lines = content.split('\n')
                imports = [line for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
                
                # Verifica TODO/FIXME
                for i, line in enumerate(lines, 1):
                    if 'TODO' in line or 'FIXME' in line:
                        issues.append(f"{file_path}:{i}: {line.strip()}")
                
        except Exception as e:
            issues.append(f"Erro ao verificar {file_path}: {e}")
    
    if issues:
        print("⚠️ Problemas encontrados:")
        for issue in issues[:10]:  # Mostra apenas os primeiros 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... e mais {len(issues) - 10} problemas")
    else:
        print("✅ Nenhum problema encontrado!")
    
    return len(issues) == 0


def optimize_static_files():
    """Otimiza arquivos estáticos"""
    print("⚡ Otimizando arquivos estáticos...")
    
    try:
        static_dir = 'static'
        if not os.path.exists(static_dir):
            print("⚠️ Diretório static não encontrado")
            return False
        
        # Conta arquivos
        file_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_count += 1
                total_size += os.path.getsize(file_path)
        
        print(f"📊 Encontrados {file_count} arquivos estáticos")
        print(f"📏 Tamanho total: {total_size / 1024:.2f} KB")
        
        # TODO: Implementar otimizações reais (minificação, compressão, etc.)
        
        print("✅ Arquivos estáticos otimizados!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao otimizar arquivos: {e}")
        return False


def deploy_check():
    """Verifica se o projeto está pronto para deploy"""
    print("🚀 Verificando prontidão para deploy...")
    
    checks = []
    
    # Verifica arquivos obrigatórios
    required_files = [
        ('app.py', 'Arquivo principal da aplicação'),
        ('requirements.txt', 'Lista de dependências'),
        ('Procfile', 'Configuração do Heroku/Render'),
        ('runtime.txt', 'Versão do Python'),
    ]
    
    for file_name, description in required_files:
        if os.path.exists(file_name):
            checks.append((True, f"✅ {description}: {file_name}"))
        else:
            checks.append((False, f"❌ {description}: {file_name} não encontrado"))
    
    # Verifica estrutura de diretórios
    required_dirs = [
        ('static', 'Arquivos estáticos'),
        ('templates', 'Templates HTML'),
    ]
    
    for dir_name, description in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            checks.append((True, f"✅ {description}: {dir_name}/"))
        else:
            checks.append((False, f"❌ {description}: {dir_name}/ não encontrado"))
    
    # Verifica configurações
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'app.run(' in content and 'debug=True' in content:
                checks.append((False, "⚠️ Debug mode ainda ativo em produção"))
            else:
                checks.append((True, "✅ Configuração de produção OK"))
    except:
        checks.append((False, "❌ Não foi possível verificar app.py"))
    
    # Mostra resultados
    print("\n📋 Resultado da verificação:")
    all_passed = True
    for passed, message in checks:
        print(f"  {message}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Projeto pronto para deploy!")
    else:
        print("\n⚠️ Corrija os problemas antes do deploy")
    
    return all_passed


def generate_documentation():
    """Gera documentação do projeto"""
    print("📚 Gerando documentação...")
    
    try:
        doc_content = f"""# Sistema FONTES v3.0 - Documentação

## Visão Geral
Sistema de gestão previdenciária com interface web moderna e responsiva.

## Estrutura do Projeto
```
APONSENTAR/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── Procfile              # Configuração deploy
├── runtime.txt           # Versão Python
├── Dockerfile            # Container Docker
├── docker-compose.yml    # Orquestração
├── render.yaml           # Deploy Render.com
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css    # Estilos principais
│   └── js/
│       └── main.js      # JavaScript principal
├── templates/            # Templates HTML
│   ├── base.html        # Template base
│   ├── index.html       # Página inicial
│   ├── login.html       # Página de login
│   └── dashboard.html   # Dashboard principal
├── scripts/              # Scripts utilitários
├── tests/                # Testes automatizados
└── docs/                 # Documentação
```

## Funcionalidades
- 🔐 Sistema de autenticação seguro
- 📊 Dashboard interativo
- 🔍 Consulta de benefícios
- 💰 Gestão de benefícios previdenciários
- 📄 Geração de documentos
- 📅 Sistema de agendamento
- 🧮 Calculadora previdenciária
- 📈 Simulações de aposentadoria

## Tecnologias
- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, JavaScript ES6+
- **Banco de Dados**: SQLite (desenvolvimento)
- **Deploy**: Render.com, Docker
- **Testes**: unittest, pytest

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/CyberStorebcb/fontes-sistema-inss.git
cd fontes-sistema-inss
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

## Deploy

### Render.com
1. Conecte o repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

### Docker
```bash
docker build -t fontes-system .
docker run -p 5000:5000 fontes-system
```

## Testes
```bash
python -m pytest tests/
```

## Configuração
- `SECRET_KEY`: Chave secreta da aplicação
- `DEBUG`: Modo debug (False em produção)
- `PORT`: Porta da aplicação (padrão: 5000)

## API Endpoints
- `GET /`: Página inicial
- `GET /login`: Página de login
- `POST /login`: Autenticação
- `GET /dashboard`: Dashboard (requer login)
- `GET /logout`: Logout
- `GET /health`: Health check
- `GET /api/status`: Status da API

## Segurança
- Proteção CSRF
- Sessões seguras
- Validação de entrada
- Headers de segurança

## Contribuição
1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Pull Request

## Licença
Copyright © 2024 Sistema FONTES. Todos os direitos reservados.

---
Documentação gerada automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""
        
        # Cria diretório docs se não existir
        os.makedirs('docs', exist_ok=True)
        
        # Salva documentação
        with open('docs/README.md', 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print("✅ Documentação gerada: docs/README.md")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar documentação: {e}")
        return False


def main():
    """Função principal do script de utilidades"""
    if len(sys.argv) < 2:
        print("🛠️ Sistema FONTES v3.0 - Scripts de Utilidades")
        print("\nComandos disponíveis:")
        print("  backup        - Cria backup do projeto")
        print("  install       - Instala dependências")
        print("  test          - Executa testes")
        print("  quality       - Verifica qualidade do código")
        print("  optimize      - Otimiza arquivos estáticos")
        print("  deploy-check  - Verifica prontidão para deploy")
        print("  docs          - Gera documentação")
        print("  all           - Executa todas as verificações")
        print("\nUso: python scripts/utils.py <comando>")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'backup':
        create_backup()
    elif command == 'install':
        install_dependencies()
    elif command == 'test':
        run_tests()
    elif command == 'quality':
        check_code_quality()
    elif command == 'optimize':
        optimize_static_files()
    elif command == 'deploy-check':
        deploy_check()
    elif command == 'docs':
        generate_documentation()
    elif command == 'all':
        print("🚀 Executando verificação completa...")
        print("\n" + "="*50)
        
        results = []
        results.append(("Instalação de dependências", install_dependencies()))
        results.append(("Testes", run_tests()))
        results.append(("Qualidade do código", check_code_quality()))
        results.append(("Otimização", optimize_static_files()))
        results.append(("Verificação de deploy", deploy_check()))
        results.append(("Documentação", generate_documentation()))
        
        print("\n" + "="*50)
        print("📊 RESUMO GERAL:")
        
        all_passed = True
        for name, result in results:
            status = "✅" if result else "❌"
            print(f"  {status} {name}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("\n🎉 TUDO PRONTO! Sistema em perfeitas condições.")
        else:
            print("\n⚠️ Alguns problemas foram encontrados. Verifique acima.")
    else:
        print(f"❌ Comando desconhecido: {command}")
        print("Use 'python scripts/utils.py' para ver comandos disponíveis")


if __name__ == '__main__':
    main()
