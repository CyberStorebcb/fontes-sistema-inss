@echo off
title Sistema FONTES - Configurar Git para Deploy
echo ========================================
echo  SISTEMA FONTES v3.0 - CONFIGURAR GIT
echo ========================================
echo.

echo 🔍 Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git não encontrado!
    echo.
    echo 📥 INSTALANDO GIT...
    echo ⏳ Isso pode levar alguns minutos...
    echo.
    
    REM Baixar Git para Windows
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git-installer.exe'}"
    
    echo 🚀 Iniciando instalação do Git...
    start /wait git-installer.exe /VERYSILENT /NORESTART
    
    echo ✅ Git instalado!
    echo 🔄 Reinicie o terminal ou execute este script novamente
    
    del git-installer.exe
    pause
    exit /b 0
)

echo ✅ Git encontrado!
git --version

echo.
echo 🚀 CONFIGURANDO REPOSITÓRIO...
echo.

REM Verificar se já é um repositório Git
if not exist ".git" (
    echo 📁 Inicializando repositório Git...
    git init
    echo ✅ Repositório inicializado!
) else (
    echo ✅ Repositório Git já existe!
)

echo.
echo ⚙️ CONFIGURAÇÕES DO GIT
echo.

REM Configurar nome e email (se não configurado)
git config user.name >nul 2>&1
if errorlevel 1 (
    set /p username="Digite seu nome: "
    git config user.name "%username%"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    set /p email="Digite seu email: "
    git config user.email "%email%"
)

echo ✅ Git configurado!
echo 👤 Nome: 
git config user.name
echo 📧 Email: 
git config user.email

echo.
echo 📦 ADICIONANDO ARQUIVOS...
git add .
git status

echo.
echo 💬 FAZENDO COMMIT...
git commit -m "Sistema FONTES v3.0 - Deploy Render"

echo.
echo ========================================
echo  ✅ REPOSITÓRIO PRONTO PARA DEPLOY!
echo ========================================
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Crie um repositório no GitHub:
echo    https://github.com/new
echo    Nome: fontes-sistema-inss
echo.
echo 2. Execute estes comandos:
echo    git remote add origin https://github.com/SEU_USUARIO/fontes-sistema-inss.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. No Render.com:
echo    - New ^> Web Service
echo    - Conecte seu repositório
echo    - Deploy automático!
echo.
echo ========================================

pause
