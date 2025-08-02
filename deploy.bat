@echo off
REM Sistema FONTES v3.0 - Script de Deploy para Windows
title Sistema FONTES - Deploy

echo ========================================
echo   Sistema FONTES v3.0 - Deploy
echo ========================================
echo.

REM Configurações
set PROJECT_NAME=fontes-sistema-inss
set DOCKER_IMAGE=%PROJECT_NAME%:latest
set CONTAINER_NAME=fontes-app
set PORT=5000

echo 🚀 Iniciando deploy...
echo.

REM Verificar Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está instalado!
    pause
    exit /b 1
)

REM Parar container existente
echo 📦 Verificando containers existentes...
docker ps -q -f name=%CONTAINER_NAME% >nul 2>&1
if not errorlevel 1 (
    echo 🛑 Parando container existente...
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
)

REM Remover imagem antiga
docker images -q %DOCKER_IMAGE% >nul 2>&1
if not errorlevel 1 (
    echo 🗑️ Removendo imagem antiga...
    docker rmi %DOCKER_IMAGE%
)

REM Build da imagem
echo 🔨 Construindo imagem Docker...
docker build -t %DOCKER_IMAGE% .
if errorlevel 1 (
    echo ❌ Falha na construção da imagem!
    pause
    exit /b 1
)

echo ✅ Imagem construída com sucesso!
echo.

REM Criar diretórios
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Executar container
echo 🚀 Iniciando container...
docker run -d ^
    --name %CONTAINER_NAME% ^
    --restart unless-stopped ^
    -p %PORT%:5000 ^
    -e FLASK_ENV=production ^
    -v "%cd%/data:/app/data" ^
    -v "%cd%/logs:/app/logs" ^
    %DOCKER_IMAGE%

if errorlevel 1 (
    echo ❌ Falha ao iniciar container!
    pause
    exit /b 1
)

echo ✅ Container iniciado com sucesso!
echo.

REM Aguardar inicialização
echo ⏳ Aguardando inicialização (10s)...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo   Deploy Concluído com Sucesso!
echo ========================================
echo.
echo 🌐 Aplicação: http://localhost:%PORT%
echo 👤 Login: admin / admin123
echo.
echo Comandos úteis:
echo   Ver logs:    docker logs -f %CONTAINER_NAME%
echo   Parar:       docker stop %CONTAINER_NAME%
echo   Reiniciar:   docker restart %CONTAINER_NAME%
echo   Remover:     docker rm -f %CONTAINER_NAME%
echo.

REM Mostrar status
echo 📋 Status atual:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | findstr %CONTAINER_NAME%
echo.

echo Pressione qualquer tecla para abrir no navegador...
pause >nul
start http://localhost:%PORT%
