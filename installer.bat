@echo off
echo ========================================
echo  Sistema FONTES v3.0 - Instalador
echo ========================================
echo.

echo 📦 Copiando arquivos...
if not exist "C:\FONTES" mkdir "C:\FONTES"
copy "FONTES_Sistema_INSS.exe" "C:\FONTES\"
copy "*.dll" "C:\FONTES\" 2>nul

echo 🔗 Criando atalho na área de trabalho...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Sistema FONTES.lnk'); $Shortcut.TargetPath = 'C:\FONTES\FONTES_Sistema_INSS.exe'; $Shortcut.IconLocation = 'C:\FONTES\FONTES_Sistema_INSS.exe'; $Shortcut.Description = 'Sistema FONTES - INSS v3.0'; $Shortcut.Save()"

echo 📋 Criando entrada no menu iniciar...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Sistema FONTES" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Sistema FONTES"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Sistema FONTES\Sistema FONTES.lnk'); $Shortcut.TargetPath = 'C:\FONTES\FONTES_Sistema_INSS.exe'; $Shortcut.IconLocation = 'C:\FONTES\FONTES_Sistema_INSS.exe'; $Shortcut.Description = 'Sistema FONTES - INSS v3.0'; $Shortcut.Save()"

echo.
echo ✅ Instalação concluída!
echo 🚀 O Sistema FONTES foi instalado em C:\FONTES
echo 🖥️  Um atalho foi criado na área de trabalho
echo 📋 O programa está disponível no menu iniciar
echo.
echo Pressione qualquer tecla para executar o sistema...
pause >nul
start "Sistema FONTES" "C:\FONTES\FONTES_Sistema_INSS.exe"
