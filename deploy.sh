#!/bin/bash
# Sistema FONTES v3.0 - Script de Deploy Automatizado

echo "🚀 Iniciando deploy do Sistema FONTES v3.0..."

# Configurações
PROJECT_NAME="fontes-sistema-inss"
DOCKER_IMAGE="$PROJECT_NAME:latest"
CONTAINER_NAME="fontes-app"
PORT="5000"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    error "Docker não está instalado!"
    exit 1
fi

# Parar container existente
if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
    log "Parando container existente..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Remover imagem antiga
if docker images -q $DOCKER_IMAGE | grep -q .; then
    log "Removendo imagem antiga..."
    docker rmi $DOCKER_IMAGE
fi

# Build da nova imagem
log "Construindo nova imagem Docker..."
if docker build -t $DOCKER_IMAGE .; then
    log "✅ Imagem construída com sucesso!"
else
    error "❌ Falha na construção da imagem!"
    exit 1
fi

# Executar container
log "Iniciando container..."
if docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    -p $PORT:5000 \
    -e FLASK_ENV=production \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    $DOCKER_IMAGE; then
    log "✅ Container iniciado com sucesso!"
else
    error "❌ Falha ao iniciar container!"
    exit 1
fi

# Aguardar inicialização
log "Aguardando inicialização do serviço..."
sleep 10

# Verificar saúde
if curl -f http://localhost:$PORT/api/health &> /dev/null; then
    log "✅ Aplicação está funcionando!"
    log "🌐 Acesse: http://localhost:$PORT"
    log "👤 Login: admin / admin123"
else
    warning "⚠️  Aplicação pode estar inicializando ainda..."
    log "📋 Verifique os logs: docker logs $CONTAINER_NAME"
fi

# Mostrar status
echo ""
log "📋 Status do Deploy:"
echo "Container: $(docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep $CONTAINER_NAME)"
echo ""
log "🎉 Deploy concluído!"
echo ""
echo "Comandos úteis:"
echo "  Ver logs:      docker logs -f $CONTAINER_NAME"
echo "  Parar:         docker stop $CONTAINER_NAME"
echo "  Reiniciar:     docker restart $CONTAINER_NAME"
echo "  Remover:       docker rm -f $CONTAINER_NAME"
