"""
Diálogo de Login do Meu INSS
Permite ao usuário inserir credenciais e fazer login automático no site do Meu INSS
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import webbrowser
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os


class MeuInssLoginDialog(ctk.CTkToplevel):
    """Diálogo para login no Meu INSS"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configurações da janela
        self.title("🏛️ Login Meu INSS")
        self.geometry("450x550")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centralizar na tela
        self.center_window()
        
        # Variáveis
        self.login_successful = False
        self.driver = None
        
        # Configurar UI
        self.setup_ui()
        
        # Protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centralizar a janela na tela"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"450x550+{x}+{y}")
    
    def setup_ui(self):
        """Configurar interface do usuário"""
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(main_frame, height=80, corner_radius=15)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_propagate(False)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏛️ Acesso ao Meu INSS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#1f538d", "#3d8bff")
        )
        title_label.grid(row=0, column=0, pady=20)
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Faça login com suas credenciais do GOV.BR",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Formulário
        form_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        form_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Campo CPF/Username
        cpf_label = ctk.CTkLabel(
            form_frame,
            text="CPF ou Login:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        cpf_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        self.cpf_entry = ctk.CTkEntry(
            form_frame,
            height=40,
            font=ctk.CTkFont(size=14),
            placeholder_text="Digite seu CPF ou login GOV.BR"
        )
        self.cpf_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))
        
        # Campo Senha
        senha_label = ctk.CTkLabel(
            form_frame,
            text="Senha:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        senha_label.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.senha_entry = ctk.CTkEntry(
            form_frame,
            height=40,
            font=ctk.CTkFont(size=14),
            placeholder_text="Digite sua senha",
            show="*"
        )
        self.senha_entry.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Checkbox para lembrar dados
        self.remember_var = ctk.BooleanVar()
        remember_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Lembrar dados (apenas nesta sessão)",
            variable=self.remember_var,
            font=ctk.CTkFont(size=12)
        )
        remember_checkbox.grid(row=4, column=0, sticky="w", padx=20, pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        
        # Botão Cancelar
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            command=self.cancel_login
        )
        cancel_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Botão Abertura Manual
        manual_button = ctk.CTkButton(
            buttons_frame,
            text="🌐 Abrir Manual",
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("orange", "darkorange"),
            hover_color=("darkorange", "orangered"),
            command=self.open_manual
        )
        manual_button.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        
        # Botão Login Automático
        self.login_button = ctk.CTkButton(
            buttons_frame,
            text="🔐 Login Auto",
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#1f538d", "#3d8bff"),
            hover_color=("#174a7e", "#2b7ae4"),
            command=self.start_login
        )
        self.login_button.grid(row=0, column=2, sticky="ew", padx=(5, 0))
        
        # Progress bar (inicialmente oculta)
        self.progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=1, column=0)
        
        # Inicialmente ocultar progress
        self.progress_frame.grid_remove()
        
        # Informações importantes
        info_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        info_frame.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        
        info_text = """ℹ️ INFORMAÇÕES IMPORTANTES:

• Use suas credenciais do GOV.BR
• O navegador será aberto automaticamente
• Aguarde o carregamento completo da página
• Mantenha esta janela aberta durante o processo"""
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=11),
            justify="left",
            anchor="w"
        )
        info_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Focar no campo CPF
        self.cpf_entry.focus()
        
        # Bind Enter para fazer login
        self.bind('<Return>', lambda e: self.start_login())
        self.cpf_entry.bind('<Return>', lambda e: self.senha_entry.focus())
        self.senha_entry.bind('<Return>', lambda e: self.start_login())
    
    def show_progress(self, show=True):
        """Mostrar/ocultar barra de progresso"""
        if show:
            self.progress_frame.grid()
        else:
            self.progress_frame.grid_remove()
    
    def update_progress(self, value, text=""):
        """Atualizar barra de progresso"""
        self.progress_bar.set(value)
        self.progress_label.configure(text=text)
        self.update()
    
    def validate_inputs(self):
        """Validar campos de entrada"""
        cpf = self.cpf_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not cpf:
            messagebox.showerror("Erro", "Por favor, digite seu CPF ou login.")
            self.cpf_entry.focus()
            return False
        
        if not senha:
            messagebox.showerror("Erro", "Por favor, digite sua senha.")
            self.senha_entry.focus()
            return False
        
        if len(cpf) > 0 and cpf.isdigit() and len(cpf) != 11:
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos.")
            self.cpf_entry.focus()
            return False
        
        return True
    
    def start_login(self):
        """Iniciar processo de login"""
        if not self.validate_inputs():
            return
        
        # Desabilitar botão e mostrar progress
        self.login_button.configure(state="disabled", text="🔄 Entrando...")
        self.show_progress(True)
        
        # Executar login em thread separada
        thread = threading.Thread(target=self.perform_login, daemon=True)
        thread.start()
    
    def perform_login(self):
        """Realizar login automático no Meu INSS"""
        try:
            self.update_progress(0.1, "Preparando navegador...")
            
            # Configurar Chrome com opções mais robustas
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument(f"--user-data-dir=C:/temp/chrome_meu_inss_{int(time.time())}")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User-Agent mais realista
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
            
            self.update_progress(0.2, "Iniciando navegador...")
            
            # Inicializar driver
            try:
                # Usar webdriver-manager para obter ChromeDriver automaticamente
                chrome_service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                
                # Executar scripts para mascarar automação
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                })
                
            except Exception as e:
                # Tentar com Edge se Chrome não funcionar
                try:
                    from selenium.webdriver.edge.options import Options as EdgeOptions
                    from selenium.webdriver.edge.service import Service as EdgeService
                    
                    edge_options = EdgeOptions()
                    edge_options.add_argument("--start-maximized")
                    edge_options.add_argument("--disable-blink-features=AutomationControlled")
                    edge_service = EdgeService(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=edge_service, options=edge_options)
                except Exception as edge_error:
                    raise Exception(f"Navegador não disponível. Chrome: {str(e)}, Edge: {str(edge_error)}")
            
            self.update_progress(0.3, "Acessando página do Meu INSS...")
            
            # Navegar para página inicial do Meu INSS
            meu_inss_url = "https://meu.inss.gov.br/central/index.html"
            self.driver.get(meu_inss_url)
            
            self.update_progress(0.4, "Aguardando carregamento da página...")
            
            # Aguardar carregamento mais tempo
            wait = WebDriverWait(self.driver, 45)  # Aumentar timeout para páginas lentas
            
            # Aguardar que a página carregue completamente
            try:
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                time.sleep(5)  # Aguardar JavaScript adicional carregar
                print("✅ Página do Meu INSS carregada completamente")
            except TimeoutException:
                print("⚠️ Timeout no carregamento, continuando...")
                time.sleep(3)
            
            self.update_progress(0.45, "Procurando botão 'Entrar com gov.br'...")
            
            # Procurar e clicar no botão "Entrar com gov.br"
            govbr_selectors = [
                "button:contains('Entrar com gov')",
                "a:contains('Entrar com gov')",
                ".btn-primary:contains('gov')",
                "#loginButton",
                ".login-gov",
                "button[class*='gov']",
                "a[href*='sso.acesso.gov.br']",
                "button[onclick*='gov']"
            ]
            
            govbr_button = None
            print("Procurando botão 'Entrar com gov.br'...")
            
            for i, selector in enumerate(govbr_selectors):
                try:
                    print(f"Tentando seletor gov.br {i+1}: {selector}")
                    if 'contains' in selector:
                        # Extrair texto do seletor contains
                        if 'Entrar com gov' in selector:
                            govbr_button = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar com gov')] | //a[contains(text(), 'Entrar com gov')]"))
                            )
                        elif 'gov' in selector:
                            govbr_button = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'gov.br') or contains(@class, 'gov') or contains(@onclick, 'gov')]"))
                            )
                    else:
                        govbr_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    print(f"Botão gov.br encontrado com seletor: {selector}")
                    break
                except TimeoutException:
                    print(f"Seletor gov.br {selector} não encontrou elemento")
                    continue
                except Exception as e:
                    print(f"Erro no seletor {selector}: {e}")
                    continue
            
            if govbr_button:
                print("Clicando no botão 'Entrar com gov.br'...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", govbr_button)
                time.sleep(1)
                govbr_button.click()
                time.sleep(3)
            else:
                print("Botão gov.br não encontrado, tentando navegar diretamente...")
                # Se não encontrar o botão, navegar diretamente para o login
                login_url = "https://sso.acesso.gov.br/login?client_id=autorizar.meu.inss.gov.br&authorization_id=19867bb4a91"
                self.driver.get(login_url)
            
            self.update_progress(0.5, "Tratando permissões de localização...")
            
            # Aguardar possível popup de localização e clicar em "Permitir" ou similar
            try:
                # Aguardar por popup de localização (pode aparecer ou não)
                time.sleep(3)  # Aguardar mais tempo para popup aparecer
                
                # Procurar botões de permissão de localização
                location_permission_selectors = [
                    "button:contains('Permitir ao acesso')",
                    "button:contains('Permitir')", 
                    "button:contains('Allow')",
                    "button:contains('Permitir acesso')",
                    ".permission-allow",
                    "#allow-location",
                    "button[class*='allow']",
                    "button[class*='permit']"
                ]
                
                permission_found = False
                for selector in location_permission_selectors:
                    try:
                        if 'contains' in selector:
                            text = selector.split("'")[1]
                            permission_btn = WebDriverWait(self.driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]"))
                            )
                        else:
                            permission_btn = WebDriverWait(self.driver, 3).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                        
                        print(f"✅ Clicando em permissão de localização: {selector}")
                        permission_btn.click()
                        time.sleep(2)
                        permission_found = True
                        break
                    except TimeoutException:
                        continue
                    except Exception as e:
                        print(f"Erro na permissão {selector}: {e}")
                        continue
                
                if not permission_found:
                    print("ℹ️ Nenhuma permissão de localização encontrada (pode ser normal)")
                        
            except Exception as e:
                print(f"ℹ️ Erro ao tratar permissões (pode ser normal): {e}")
            
            self.update_progress(0.55, "Aguardando página de login GOV.BR...")
            
            # Aguardar estar na página de login do GOV.BR
            try:
                wait.until(lambda driver: "sso.acesso.gov.br" in driver.current_url)
                print(f"✅ Redirecionado para GOV.BR: {self.driver.current_url}")
            except TimeoutException:
                print("⚠️ Não foi redirecionado para GOV.BR, tentando navegar diretamente...")
                login_url = "https://sso.acesso.gov.br/login?client_id=autorizar.meu.inss.gov.br&authorization_id=19867bb4a91"
                self.driver.get(login_url)
                time.sleep(3)
            
            # Aguardar carregamento da nova página com mais tempo
            try:
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                time.sleep(5)  # Aguardar mais tempo para JavaScript carregar
                print("✅ Página GOV.BR carregada")
            except TimeoutException:
                print("⚠️ Timeout no carregamento GOV.BR, continuando...")
                time.sleep(3)
            
            self.update_progress(0.6, "Localizando campos de login...")
            
            # Aguardar e preencher campo de usuário/CPF
            try:
                # Seletores mais específicos e atualizados para GOV.BR
                user_selectors = [
                    "#accountId",  # Seletor mais comum do GOV.BR
                    "input[name='accountId']",
                    "input[id='accountId']",
                    "input[placeholder*='CPF']",
                    "input[placeholder*='usuário']",
                    "input[placeholder*='login']",
                    "input[name='username']",
                    "input[name='login']", 
                    "input[name='cpf']",
                    "input[id='username']",
                    "input[id='login']",
                    "input[id='cpf']",
                    "input[type='text']:first-of-type",
                    "input[type='text']:visible"
                ]
                
                user_field = None
                print("Procurando campo de usuário...")
                
                for i, selector in enumerate(user_selectors):
                    try:
                        print(f"Tentando seletor {i+1}: {selector}")
                        if selector.endswith(":visible"):
                            # Para seletor :visible, usar JavaScript
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector.replace(":visible", ""))
                            for elem in elements:
                                if elem.is_displayed() and elem.is_enabled():
                                    user_field = elem
                                    break
                        else:
                            user_field = WebDriverWait(self.driver, 8).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                        
                        if user_field and user_field.is_displayed():
                            print(f"Campo encontrado com seletor: {selector}")
                            break
                        else:
                            user_field = None
                    except TimeoutException:
                        print(f"Seletor {selector} não encontrou elemento")
                        continue
                    except Exception as e:
                        print(f"Erro no seletor {selector}: {e}")
                        continue
                
                if not user_field:
                    # Debug: listar todos os inputs disponíveis
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    input_info = []
                    for inp in inputs:
                        try:
                            if inp.is_displayed():
                                info = {
                                    'type': inp.get_attribute('type'),
                                    'name': inp.get_attribute('name'),
                                    'id': inp.get_attribute('id'),
                                    'placeholder': inp.get_attribute('placeholder'),
                                    'class': inp.get_attribute('class')
                                }
                                input_info.append(str(info))
                        except:
                            pass
                    
                    debug_info = f"Inputs visíveis encontrados: {'; '.join(input_info[:5])}"  # Primeiros 5
                    raise Exception(f"Campo de usuário não encontrado. {debug_info}")
                
                self.update_progress(0.7, "Preenchendo CPF/usuário...")
                
                # Preencher usuário com mais cuidado
                self.driver.execute_script("arguments[0].scrollIntoView(true);", user_field)
                time.sleep(1)
                user_field.clear()
                time.sleep(0.5)
                
                # Digitar caractere por caractere para parecer mais humano
                cpf_text = self.cpf_entry.get().strip()
                for char in cpf_text:
                    user_field.send_keys(char)
                    time.sleep(0.1)
                
                time.sleep(1)
                print(f"CPF/usuário preenchido: {cpf_text}")
                
                self.update_progress(0.75, "Procurando campo de senha...")
                
                # Aguardar e preencher campo de senha
                password_selectors = [
                    "#password",  # Seletor mais comum do GOV.BR
                    "input[name='password']",
                    "input[id='password']",
                    "input[type='password']",
                    "input[name='senha']",
                    "input[id='senha']",
                    "input[placeholder*='senha']",
                    "input[placeholder*='password']"
                ]
                
                password_field = None
                print("Procurando campo de senha...")
                
                for i, selector in enumerate(password_selectors):
                    try:
                        print(f"Tentando seletor senha {i+1}: {selector}")
                        password_field = WebDriverWait(self.driver, 8).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if password_field.is_displayed():
                            print(f"Campo senha encontrado com seletor: {selector}")
                            break
                        else:
                            password_field = None
                    except TimeoutException:
                        print(f"Seletor senha {selector} não encontrou elemento")
                        continue
                    except Exception as e:
                        print(f"Erro no seletor senha {selector}: {e}")
                        continue
                
                if not password_field:
                    raise Exception("Campo de senha não encontrado")
                
                self.update_progress(0.8, "Preenchendo senha...")
                
                self.driver.execute_script("arguments[0].scrollIntoView(true);", password_field)
                time.sleep(1)
                password_field.clear()
                time.sleep(0.5)
                
                # Digitar senha caractere por caractere
                senha_text = self.senha_entry.get().strip()
                for char in senha_text:
                    password_field.send_keys(char)
                    time.sleep(0.1)
                
                time.sleep(1)
                print("Senha preenchida")
                
                self.update_progress(0.85, "Procurando botão de login...")
                
                # Procurar e clicar no botão de login com seletores mais específicos
                login_selectors = [
                    "button:contains('Continuar')",
                    "#submit-button",  # Botão comum do GOV.BR
                    "button[type='submit']",
                    "input[type='submit']",
                    "button[name='submit']",
                    "button[id='submit']",
                    "button[id='login']",
                    ".btn-primary",
                    "button:contains('Entrar')",
                    "button:contains('Acessar')",
                    "input[value='Entrar']",
                    "input[value='Acessar']",
                    "input[value='Continuar']"
                ]
                
                login_button = None
                print("Procurando botão de login...")
                
                for i, selector in enumerate(login_selectors):
                    try:
                        print(f"Tentando seletor botão {i+1}: {selector}")
                        if 'contains' in selector:
                            text = selector.split("'")[1]
                            login_button = WebDriverWait(self.driver, 8).until(
                                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}') or contains(@value, '{text}')] | //input[contains(@value, '{text}')]"))
                            )
                        else:
                            login_button = WebDriverWait(self.driver, 8).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                        
                        if login_button.is_displayed():
                            print(f"Botão encontrado com seletor: {selector}")
                            break
                        else:
                            login_button = None
                    except TimeoutException:
                        print(f"Seletor botão {selector} não encontrou elemento")
                        continue
                    except Exception as e:
                        print(f"Erro no seletor botão {selector}: {e}")
                        continue
                
                self.update_progress(0.9, "Fazendo login...")
                
                if login_button:
                    # Scroll para o botão e clicar
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
                    time.sleep(1)
                    print("Clicando no botão de login...")
                    login_button.click()
                else:
                    # Tentar submit do formulário como alternativa
                    print("Tentando submit do formulário...")
                    user_field.submit()
                
                self.update_progress(0.95, "Aguardando redirecionamento...")
                
                # Aguardar redirecionamento ou mensagem de erro (mais tempo)
                time.sleep(8)  # Aguardar mais tempo para processamento
                
                # Verificar se houve erro de forma mais robusta
                current_url = self.driver.current_url
                print(f"URL atual após login: {current_url}")
                
                # Verificar se ainda está na página de login (indicando erro)
                if "sso.acesso.gov.br/login" in current_url:
                    # Procurar mensagens de erro específicas
                    error_selectors = [
                        ".alert-danger",
                        ".alert-error", 
                        ".error-message",
                        ".mensagem-erro",
                        "[class*='error']",
                        "[class*='alert']",
                        ".invalid-feedback",
                        ".form-error",
                        ".text-danger"
                    ]
                    
                    error_message = "Credenciais podem estar incorretas"
                    for selector in error_selectors:
                        try:
                            error_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if error_elem.is_displayed():
                                error_text = error_elem.text.strip()
                                if error_text:
                                    error_message = error_text
                                    print(f"Erro encontrado: {error_text}")
                                    break
                        except:
                            continue
                    
                    raise Exception(f"Login não realizado: {error_message}")
                
                # Verificar se foi redirecionado para Meu INSS (sucesso)
                elif "meu.inss.gov.br" in current_url or "autorizar" in current_url:
                    print("Login realizado com sucesso - redirecionado para Meu INSS")
                    self.update_progress(1.0, "Login realizado com sucesso!")
                else:
                    print(f"Redirecionado para URL inesperada: {current_url}")
                    # Mesmo assim, considerar sucesso se saiu da página de login
                    self.update_progress(1.0, "Login aparentemente realizado!")
                
                # Sucesso
                self.login_successful = True
                
                # Fechar diálogo após 3 segundos
                self.after(3000, self.destroy)
                
                # Mostrar mensagem de sucesso
                self.after(100, lambda: messagebox.showinfo(
                    "Sucesso", 
                    "Login realizado com sucesso!\n\n"
                    "Você foi conectado ao Meu INSS através do GOV.BR.\n"
                    "O navegador permanecerá aberto para você usar os serviços.\n\n"
                    "✅ Processo completo automatizado:\n"
                    "• Acesso ao Meu INSS\n"
                    "• Login via GOV.BR\n"
                    "• Preenchimento automático\n"
                    "• Redirecionamento finalizado"
                ))
                
            except TimeoutException:
                current_url = self.driver.current_url
                raise Exception(f"Tempo limite esgotado. Verifique sua conexão.\nURL atual: {current_url}")
            except Exception as e:
                current_url = self.driver.current_url if self.driver else "N/A"
                raise Exception(f"Erro ao preencher formulário: {str(e)}\nURL: {current_url}")
                
        except Exception as e:
            # Fechar driver em caso de erro
            self.cleanup_driver()  # Usar método mais seguro
            
            # Capturar mensagem de erro
            error_message = str(e)
            
            # Mostrar erro na thread principal
            self.after(100, lambda msg=error_message: self.handle_login_error(msg))
    
    def cleanup_driver(self):
        """Limpar recursos do WebDriver de forma segura"""
        if self.driver:
            try:
                # Fechar todas as abas
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
            except:
                pass
            
            try:
                # Encerrar o driver
                self.driver.quit()
            except:
                pass
            
            self.driver = None
            print("🧹 WebDriver encerrado com segurança")
    
    def on_closing(self):
        """Fechar janela"""
        self.cleanup_driver()
        self.destroy()
    
    def cancel_login(self):
        """Cancelar login"""
        self.cleanup_driver()
        self.destroy()
    
    def open_manual(self):
        """Abrir site manualmente no navegador"""
        open_meu_inss_direct()
        self.destroy()
    
    def handle_login_error(self, error_message):
        """Tratar erro de login na thread principal"""
        self.show_progress(False)
        self.login_button.configure(state="normal", text="🔐 Fazer Login")
        
        # Melhorar a mensagem de erro baseada no tipo
        if "Campo de usuário não encontrado" in error_message:
            user_message = (
                "Não foi possível localizar o campo de usuário na página.\n\n"
                "Isso pode acontecer se:\n"
                "• O site do GOV.BR foi atualizado\n"
                "• Há problemas de conectividade\n"
                "• A página não carregou completamente\n\n"
                "Tente novamente ou faça login manualmente no navegador."
            )
        elif "Campo de senha não encontrado" in error_message:
            user_message = (
                "Não foi possível localizar o campo de senha na página.\n\n"
                "O site pode ter sido atualizado. Tente fazer login manualmente."
            )
        elif "Tempo limite esgotado" in error_message:
            user_message = (
                "A página demorou muito para carregar.\n\n"
                "Verifique sua conexão com a internet e tente novamente."
            )
        elif "Login não realizado" in error_message:
            user_message = (
                "As credenciais podem estar incorretas.\n\n"
                "Verifique:\n"
                "• CPF ou login correto\n"
                "• Senha correta (case-sensitive)\n"
                "• Se sua conta não está bloqueada\n\n"
                "Tente fazer login manualmente para verificar."
            )
        elif "Navegador não disponível" in error_message:
            user_message = (
                "Não foi possível iniciar o navegador.\n\n"
                "Certifique-se de que o Google Chrome ou Microsoft Edge estão instalados."
            )
        else:
            user_message = f"Erro técnico:\n{error_message}\n\nTente fazer login manualmente no navegador."
        
        # Oferecer opção de abrir manualmente
        result = messagebox.askyesno(
            "Erro no Login Automático",
            f"{user_message}\n\n"
            "Deseja abrir o site do Meu INSS manualmente no navegador?"
        )
        
        if result:
            # Abrir site manualmente
            open_meu_inss_direct()


def show_meu_inss_login(parent=None):
    """Mostrar diálogo de login do Meu INSS"""
    dialog = MeuInssLoginDialog(parent)
    dialog.focus()
    return dialog


# Função alternativa para abrir direto no navegador
def open_meu_inss_direct():
    """Abrir Meu INSS diretamente no navegador padrão"""
    url = "https://sso.acesso.gov.br/login?client_id=autorizar.meu.inss.gov.br&authorization_id=19867bb4a91"
    webbrowser.open(url)
    
    messagebox.showinfo(
        "Meu INSS",
        "O site do Meu INSS foi aberto no seu navegador padrão.\n\n"
        "Faça login com suas credenciais do GOV.BR para acessar os serviços do INSS."
    )


if __name__ == "__main__":
    # Teste do diálogo
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.withdraw()  # Ocultar janela principal
    
    dialog = show_meu_inss_login(root)
    root.mainloop()
