#!/bin/bash

# Sistema FONTES v3.0 - Script de Deploy Automatizado
# Este script automatiza o processo de deploy para diferentes plataformas

set -e  # Exit on any error

echo "🚀 Sistema FONTES v3.0 - Deploy Automatizado"
echo "=============================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verifica se Git está instalado
check_git() {
    if ! command -v git &> /dev/null; then
        log_error "Git não está instalado!"
        exit 1
    fi
    log_success "Git encontrado"
}

# Verifica se Python está instalado
check_python() {
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        log_error "Python não está instalado!"
        exit 1
    fi
    
    PYTHON_CMD="python"
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    fi
    
    log_success "Python encontrado: $($PYTHON_CMD --version)"
}

# Instala dependências
install_dependencies() {
    log_info "Instalando dependências..."
    
    if [ -f "requirements.txt" ]; then
        $PYTHON_CMD -m pip install --upgrade pip
        $PYTHON_CMD -m pip install -r requirements.txt
        log_success "Dependências instaladas"
    else
        log_warning "requirements.txt não encontrado"
    fi
}

# Executa testes
run_tests() {
    log_info "Executando testes..."
    
    if [ -d "tests" ]; then
        if command -v pytest &> /dev/null; then
            pytest tests/ -v
        else
            $PYTHON_CMD -m unittest discover tests/ -v
        fi
        log_success "Testes executados com sucesso"
    else
        log_warning "Diretório de testes não encontrado"
    fi
}

# Verifica arquivos obrigatórios
check_required_files() {
    log_info "Verificando arquivos obrigatórios..."
    
    required_files=("app.py" "requirements.txt" "Procfile" "runtime.txt")
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "$file encontrado"
        else
            log_error "$file não encontrado!"
            exit 1
        fi
    done
}

# Otimiza arquivos estáticos (básico)
optimize_static() {
    log_info "Otimizando arquivos estáticos..."
    
    if [ -d "static" ]; then
        # Remove arquivos temporários
        find static/ -name "*.tmp" -delete 2>/dev/null || true
        find static/ -name "*.bak" -delete 2>/dev/null || true
        find static/ -name ".DS_Store" -delete 2>/dev/null || true
        
        log_success "Arquivos estáticos otimizados"
    else
        log_warning "Diretório static não encontrado"
    fi
}

# Commit e push para Git
git_deploy() {
    log_info "Fazendo deploy via Git..."
    
    # Verifica se há mudanças
    if git diff --quiet && git diff --staged --quiet; then
        log_warning "Nenhuma mudança para commit"
    else
        # Adiciona arquivos
        git add .
        
        # Commit com timestamp
        timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        git commit -m "Deploy automatizado - $timestamp"
        
        # Push para origin
        git push origin main || git push origin master
        
        log_success "Deploy via Git concluído"
    fi
}

# Deploy para Render.com
deploy_render() {
    log_info "Configurando deploy para Render.com..."
    
    # Verifica se render.yaml existe
    if [ ! -f "render.yaml" ]; then
        log_info "Criando render.yaml..."
        
        cat > render.yaml << EOF
services:
  - type: web
    name: fontes-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.5
EOF
        log_success "render.yaml criado"
    fi
    
    log_success "Configuração Render.com pronta"
}

# Deploy para Heroku
deploy_heroku() {
    log_info "Configurando deploy para Heroku..."
    
    if command -v heroku &> /dev/null; then
        # Verifica se é um app Heroku
        if heroku apps:info &> /dev/null; then
            log_info "Fazendo deploy para Heroku..."
            git push heroku main || git push heroku master
            log_success "Deploy Heroku concluído"
        else
            log_warning "App Heroku não configurado"
        fi
    else
        log_warning "Heroku CLI não instalado"
    fi
}

# Build Docker
build_docker() {
    log_info "Construindo imagem Docker..."
    
    if [ -f "Dockerfile" ]; then
        docker build -t fontes-system:latest .
        log_success "Imagem Docker construída"
        
        # Opcional: executar container para teste
        if [ "${DOCKER_TEST:-false}" = "true" ]; then
            log_info "Testando container Docker..."
            docker run -d --name fontes-test -p 5000:5000 fontes-system:latest
            sleep 5
            
            if curl -f http://localhost:5000/health > /dev/null 2>&1; then
                log_success "Container funcionando corretamente"
            else
                log_error "Container não está respondendo"
            fi
            
            docker stop fontes-test
            docker rm fontes-test
        fi
    else
        log_warning "Dockerfile não encontrado"
    fi
}

# Cria backup antes do deploy
create_backup() {
    log_info "Criando backup..."
    
    backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Copia arquivos importantes
    cp -r static templates scripts tests docs "$backup_dir/" 2>/dev/null || true
    cp *.py *.txt *.yml *.yaml Procfile Dockerfile docker-compose.yml "$backup_dir/" 2>/dev/null || true
    
    log_success "Backup criado: $backup_dir"
}

# Deploy completo
full_deploy() {
    log_info "Iniciando deploy completo..."
    
    create_backup
    check_required_files
    install_dependencies
    run_tests
    optimize_static
    deploy_render
    git_deploy
    
    log_success "🎉 Deploy completo realizado com sucesso!"
}

# Menu principal
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1. Deploy completo"
    echo "2. Apenas Git"
    echo "3. Apenas Docker"
    echo "4. Apenas testes"
    echo "5. Verificar sistema"
    echo "6. Sair"
    echo ""
    read -p "Digite sua escolha (1-6): " choice
    
    case $choice in
        1)
            full_deploy
            ;;
        2)
            check_git
            git_deploy
            ;;
        3)
            build_docker
            ;;
        4)
            check_python
            run_tests
            ;;
        5)
            check_git
            check_python
            check_required_files
            log_success "Sistema verificado com sucesso!"
            ;;
        6)
            log_info "Saindo..."
            exit 0
            ;;
        *)
            log_error "Opção inválida!"
            show_menu
            ;;
    esac
}

# Verifica argumentos da linha de comando
if [ $# -eq 0 ]; then
    show_menu
else
    case $1 in
        "full")
            full_deploy
            ;;
        "git")
            check_git
            git_deploy
            ;;
        "docker")
            build_docker
            ;;
        "test")
            check_python
            run_tests
            ;;
        "check")
            check_git
            check_python
            check_required_files
            ;;
        "render")
            deploy_render
            ;;
        "heroku")
            deploy_heroku
            ;;
        *)
            echo "Uso: $0 [full|git|docker|test|check|render|heroku]"
            echo "Ou execute sem argumentos para o menu interativo"
            exit 1
            ;;
    esac
fi

echo ""
log_success "Script de deploy finalizado!"
