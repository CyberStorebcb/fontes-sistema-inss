#!/usr/bin/env python3
"""
Setup para criar executável do Sistema FONTES
Gera um arquivo .exe que pode ser distribuído sem precisar do Python
"""
import os
import sys
import subprocess
import json
from pathlib import Path

class ExecutableBuilder:
    """Construtor de executável para o Sistema FONTES"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        
    def check_dependencies(self):
        """Verificar e instalar dependências necessárias"""
        print("🔍 Verificando dependências...")
        
        required_packages = [
            "pyinstaller",
            "customtkinter", 
            "pillow",
            "requests"
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package} - OK")
            except ImportError:
                print(f"📦 Instalando {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} - Instalado")
    
    def create_main_launcher(self):
        """Criar arquivo principal do executável"""
        launcher_content = '''#!/usr/bin/env python3
"""
Sistema FONTES v3.0 - Launcher Principal
Ponto de entrada para o executável
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# Configurar path para recursos empacotados
if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    BASE_DIR = sys._MEIPASS
else:
    # Desenvolvimento
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adicionar diretórios ao path
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

def main():
    """Função principal do sistema"""
    try:
        print("🏛️ Iniciando Sistema FONTES v3.0...")
        
        # Configurar tema padrão
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Verificar se há sessão salva
        session_file = os.path.join(BASE_DIR, "session.dat")
        has_session = os.path.exists(session_file)
        
        if has_session:
            print("🔑 Sessão encontrada, carregando interface principal...")
            # Carregar interface principal diretamente
            from views.fontes_interface import FontesMainWindow
            app = FontesMainWindow()
            app.run()
        else:
            print("🚪 Carregando tela de login...")
            # Carregar tela de login
            from auth.login_clean import show_login_window
            
            def on_login_success(user_data):
                print(f"✅ Login bem-sucedido: {user_data.get('full_name', 'Usuário')}")
                # Carregar interface principal após login
                from views.fontes_interface import FontesMainWindow
                app = FontesMainWindow()
                app.run()
            
            login_window = show_login_window(on_login_success)
            login_window.mainloop()
            
    except ImportError as e:
        messagebox.showerror(
            "Erro de Módulo",
            f"Erro ao importar módulos necessários:\\n{e}\\n\\n"
            "Verifique se todos os arquivos estão presentes."
        )
    except Exception as e:
        messagebox.showerror(
            "Erro Crítico", 
            f"Erro inesperado no sistema:\\n{e}\\n\\n"
            "Entre em contato com o suporte técnico."
        )

if __name__ == "__main__":
    main()
'''
        
        with open(self.project_dir / "main_launcher.py", "w", encoding="utf-8") as f:
            f.write(launcher_content)
        
        print("✅ Launcher principal criado")
    
    def create_spec_file(self):
        """Criar arquivo de especificação do PyInstaller"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Coletar todos os arquivos Python do projeto
a = Analysis(
    ['main_launcher.py'],
    pathex=['{self.project_dir}'],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('*.md', '.'),
        ('*.txt', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'sqlite3',
        'threading',
        'queue',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FONTES_Sistema_INSS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console para interface gráfica
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
        
        with open(self.project_dir / "fontes.spec", "w", encoding="utf-8") as f:
            f.write(spec_content)
        
        print("✅ Arquivo de especificação criado")
    
    def create_version_info(self):
        """Criar informações de versão para o executável"""
        version_info = '''# UTF-8
#
# Informações de versão para FONTES_Sistema_INSS.exe
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(3,0,0,0),
    prodvers=(3,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Sistema FONTES'),
        StringStruct(u'FileDescription', u'Sistema INSS - FONTES v3.0'),
        StringStruct(u'FileVersion', u'3.0.0.0'),
        StringStruct(u'InternalName', u'FONTES_Sistema_INSS'),
        StringStruct(u'LegalCopyright', u'© 2025 Sistema FONTES. Todos os direitos reservados.'),
        StringStruct(u'OriginalFilename', u'FONTES_Sistema_INSS.exe'),
        StringStruct(u'ProductName', u'Sistema FONTES - INSS'),
        StringStruct(u'ProductVersion', u'3.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1046, 1200])])
  ]
)
'''
        
        with open(self.project_dir / "version_info.txt", "w", encoding="utf-8") as f:
            f.write(version_info)
        
        print("✅ Informações de versão criadas")
    
    def create_installer_script(self):
        """Criar script de instalação/distribuição"""
        installer_content = '''@echo off
echo ========================================
echo  Sistema FONTES v3.0 - Instalador
echo ========================================
echo.

echo 📦 Copiando arquivos...
if not exist "C:\\FONTES" mkdir "C:\\FONTES"
copy "FONTES_Sistema_INSS.exe" "C:\\FONTES\\"
copy "*.dll" "C:\\FONTES\\" 2>nul

echo 🔗 Criando atalho na área de trabalho...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Sistema FONTES.lnk'); $Shortcut.TargetPath = 'C:\\FONTES\\FONTES_Sistema_INSS.exe'; $Shortcut.IconLocation = 'C:\\FONTES\\FONTES_Sistema_INSS.exe'; $Shortcut.Description = 'Sistema FONTES - INSS v3.0'; $Shortcut.Save()"

echo 📋 Criando entrada no menu iniciar...
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Sistema FONTES" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Sistema FONTES"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Sistema FONTES\\Sistema FONTES.lnk'); $Shortcut.TargetPath = 'C:\\FONTES\\FONTES_Sistema_INSS.exe'; $Shortcut.IconLocation = 'C:\\FONTES\\FONTES_Sistema_INSS.exe'; $Shortcut.Description = 'Sistema FONTES - INSS v3.0'; $Shortcut.Save()"

echo.
echo ✅ Instalação concluída!
echo 🚀 O Sistema FONTES foi instalado em C:\\FONTES
echo 🖥️  Um atalho foi criado na área de trabalho
echo 📋 O programa está disponível no menu iniciar
echo.
echo Pressione qualquer tecla para executar o sistema...
pause >nul
start "Sistema FONTES" "C:\\FONTES\\FONTES_Sistema_INSS.exe"
'''
        
        with open(self.project_dir / "installer.bat", "w", encoding="utf-8") as f:
            f.write(installer_content)
        
        print("✅ Script de instalação criado")
    
    def build_executable(self):
        """Construir o executável"""
        print("🔨 Construindo executável...")
        
        # Limpar builds anteriores
        if self.dist_dir.exists():
            import shutil
            shutil.rmtree(self.dist_dir)
        if self.build_dir.exists():
            import shutil
            shutil.rmtree(self.build_dir)
        
        # Executar PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--clean",
            "--noconfirm",
            "fontes.spec"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Executável criado com sucesso!")
                return True
            else:
                print(f"❌ Erro ao criar executável:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Erro durante a construção: {e}")
            return False
    
    def create_distribution_package(self):
        """Criar pacote de distribuição"""
        print("📦 Criando pacote de distribuição...")
        
        dist_package_dir = self.project_dir / "FONTES_Distribuicao"
        dist_package_dir.mkdir(exist_ok=True)
        
        # Copiar executável
        exe_path = self.dist_dir / "FONTES_Sistema_INSS.exe"
        if exe_path.exists():
            import shutil
            shutil.copy2(exe_path, dist_package_dir / "FONTES_Sistema_INSS.exe")
        
        # Copiar instalador
        installer_path = self.project_dir / "installer.bat"
        if installer_path.exists():
            import shutil
            shutil.copy2(installer_path, dist_package_dir / "Instalar_Sistema_FONTES.bat")
        
        # Criar README para distribuição
        readme_content = """# Sistema FONTES v3.0 - Pacote de Distribuição

## 🚀 INSTRUÇÕES DE INSTALAÇÃO

### OPÇÃO 1: Instalação Automática (Recomendada)
1. Execute: `Instalar_Sistema_FONTES.bat`
2. Siga as instruções na tela
3. O sistema será instalado automaticamente

### OPÇÃO 2: Execução Direta
1. Execute: `FONTES_Sistema_INSS.exe`
2. O sistema abrirá diretamente

## 👤 CREDENCIAIS PADRÃO
- **Usuário:** admin
- **Senha:** admin123

## 📋 REQUISITOS
- Windows 7 ou superior
- 4GB RAM mínimo
- 500MB espaço livre

## 🆘 SUPORTE
- Email: suporte@fontes.inss.gov.br
- Telefone: (11) 99999-9999

## 📄 LICENÇA
© 2025 Sistema FONTES. Todos os direitos reservados.
"""
        
        with open(dist_package_dir / "LEIA-ME.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"✅ Pacote criado em: {dist_package_dir}")
        return dist_package_dir
    
    def run(self):
        """Executar processo completo de construção"""
        print("🏛️ Sistema FONTES - Gerador de Executável")
        print("=" * 50)
        
        try:
            # 1. Verificar dependências
            self.check_dependencies()
            
            # 2. Criar arquivos necessários
            self.create_main_launcher()
            self.create_spec_file()
            self.create_version_info()
            self.create_installer_script()
            
            # 3. Construir executável
            if self.build_executable():
                # 4. Criar pacote de distribuição
                package_dir = self.create_distribution_package()
                
                print("\n" + "=" * 50)
                print("🎉 SUCESSO! Executável criado com sucesso!")
                print("=" * 50)
                print(f"📁 Localização: {package_dir}")
                print("📋 Arquivos criados:")
                print("   • FONTES_Sistema_INSS.exe")
                print("   • Instalar_Sistema_FONTES.bat")
                print("   • LEIA-ME.txt")
                print("\n🚀 PRÓXIMOS PASSOS:")
                print("1. Teste o executável localmente")
                print("2. Distribua a pasta 'FONTES_Distribuicao'")
                print("3. Instrua os usuários a executar 'Instalar_Sistema_FONTES.bat'")
                print("\n✅ Pronto para distribuição!")
                
                return True
            else:
                print("❌ Falha na criação do executável")
                return False
                
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            return False

if __name__ == "__main__":
    builder = ExecutableBuilder()
    success = builder.run()
    
    if success:
        input("\nPressione Enter para sair...")
    else:
        input("\nOcorreram erros. Pressione Enter para sair...")
