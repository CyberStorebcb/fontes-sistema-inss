// Sistema FONTES v3.0 - JavaScript Otimizado

class FONTESSystem {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupFormValidation();
        this.setupNotifications();
    }

    init() {
        console.log('🚀 Sistema FONTES v3.0 iniciado');
        this.showWelcomeMessage();
        this.setupLoadingStates();
        this.setupTooltips();
    }

    showWelcomeMessage() {
        const welcomeContainer = document.getElementById('welcome-message');
        if (welcomeContainer) {
            welcomeContainer.innerHTML = `
                <div class="alert alert-success fade-in-up">
                    <h5><i class="fas fa-check-circle"></i> Sistema Carregado com Sucesso!</h5>
                    <p>Bem-vindo ao sistema FONTES v3.0. Todos os recursos estão disponíveis.</p>
                </div>
            `;
            
            // Remove mensagem após 5 segundos
            setTimeout(() => {
                if (welcomeContainer) {
                    welcomeContainer.style.opacity = '0';
                    setTimeout(() => welcomeContainer.remove(), 300);
                }
            }, 5000);
        }
    }

    setupEventListeners() {
        // Botões de serviço
        document.querySelectorAll('.service-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const service = card.dataset.service;
                this.handleServiceClick(service, card);
            });
        });

        // Formulário de login
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin(loginForm);
            });
        }

        // Botões de ação
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.addButtonFeedback(btn);
            });
        });

        // Navegação suave
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    handleServiceClick(service, cardElement) {
        // Adiciona feedback visual
        cardElement.style.transform = 'scale(0.95)';
        setTimeout(() => {
            cardElement.style.transform = '';
        }, 150);

        // Lógica específica por serviço
        switch(service) {
            case 'consulta':
                this.openConsultaModal();
                break;
            case 'beneficios':
                this.openBeneficiosModal();
                break;
            case 'documentos':
                this.openDocumentosModal();
                break;
            case 'agendamento':
                this.openAgendamentoModal();
                break;
            case 'calculadora':
                this.openCalculadoraModal();
                break;
            case 'simulacao':
                this.openSimulacaoModal();
                break;
            default:
                this.showNotification('Funcionalidade em desenvolvimento', 'info');
        }
    }

    openConsultaModal() {
        const modalHtml = `
            <div class="modal fade" id="consultaModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-search"></i> Consulta de Benefícios
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="consultaForm">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label class="form-label">CPF</label>
                                            <input type="text" class="form-control" id="cpf" placeholder="000.000.000-00" maxlength="14">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label class="form-label">Data de Nascimento</label>
                                            <input type="date" class="form-control" id="dataNascimento">
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Tipo de Consulta</label>
                                    <select class="form-control" id="tipoConsulta">
                                        <option value="">Selecione...</option>
                                        <option value="beneficios">Benefícios Ativos</option>
                                        <option value="contribuicoes">Histórico de Contribuições</option>
                                        <option value="simulacao">Simulação de Aposentadoria</option>
                                        <option value="extrato">Extrato Previdenciário</option>
                                    </select>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-primary" onclick="fontesSystem.realizarConsulta()">
                                <i class="fas fa-search"></i> Consultar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.showModal(modalHtml, 'consultaModal');
        this.setupCPFMask();
    }

    openBeneficiosModal() {
        const modalHtml = `
            <div class="modal fade" id="beneficiosModal" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-money-check-alt"></i> Gerenciar Benefícios
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="service-card">
                                        <div class="service-icon">💰</div>
                                        <h6 class="service-title">Aposentadoria por Idade</h6>
                                        <p class="service-description">Consulte requisitos e solicite</p>
                                        <button class="btn btn-primary btn-sm mt-2">Acessar</button>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="service-card">
                                        <div class="service-icon">⏰</div>
                                        <h6 class="service-title">Aposentadoria por Tempo</h6>
                                        <p class="service-description">Verifique tempo de contribuição</p>
                                        <button class="btn btn-primary btn-sm mt-2">Acessar</button>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="service-card">
                                        <div class="service-icon">🏥</div>
                                        <h6 class="service-title">Auxílio-Doença</h6>
                                        <p class="service-description">Solicite auxílio por incapacidade</p>
                                        <button class="btn btn-primary btn-sm mt-2">Acessar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.showModal(modalHtml, 'beneficiosModal');
    }

    openCalculadoraModal() {
        const modalHtml = `
            <div class="modal fade" id="calculadoraModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-calculator"></i> Calculadora Previdenciária
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="calculadoraForm">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label class="form-label">Salário Atual (R$)</label>
                                            <input type="number" class="form-control" id="salarioAtual" placeholder="5000.00" step="0.01">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label class="form-label">Tempo de Contribuição (anos)</label>
                                            <input type="number" class="form-control" id="tempoContribuicao" placeholder="25" min="0" max="50">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label class="form-label">Idade Atual</label>
                                            <input type="number" class="form-control" id="idadeAtual" placeholder="45" min="18" max="80">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label class="form-label">Sexo</label>
                                            <select class="form-control" id="sexo">
                                                <option value="">Selecione...</option>
                                                <option value="M">Masculino</option>
                                                <option value="F">Feminino</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                                <div id="resultadoCalculadora" class="mt-4" style="display: none;">
                                    <div class="alert alert-success">
                                        <h6><i class="fas fa-chart-line"></i> Resultado da Simulação</h6>
                                        <div id="resultadoConteudo"></div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                            <button type="button" class="btn btn-primary" onclick="fontesSystem.calcularAposentadoria()">
                                <i class="fas fa-calculator"></i> Calcular
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.showModal(modalHtml, 'calculadoraModal');
    }

    showModal(html, modalId) {
        // Remove modal existente
        const existingModal = document.getElementById(modalId);
        if (existingModal) {
            existingModal.remove();
        }

        // Adiciona novo modal
        document.body.insertAdjacentHTML('beforeend', html);
        
        // Mostra modal
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    handleLogin(form) {
        const formData = new FormData(form);
        const usuario = formData.get('usuario');
        const senha = formData.get('senha');

        if (!usuario || !senha) {
            this.showNotification('Preencha todos os campos', 'error');
            return;
        }

        this.showLoading(true);

        // Simula requisição
        setTimeout(() => {
            this.showLoading(false);
            
            if (usuario === 'admin' && senha === 'admin123') {
                this.showNotification('Login realizado com sucesso!', 'success');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                this.showNotification('Usuário ou senha inválidos', 'error');
            }
        }, 2000);
    }

    realizarConsulta() {
        const cpf = document.getElementById('cpf').value;
        const dataNascimento = document.getElementById('dataNascimento').value;
        const tipoConsulta = document.getElementById('tipoConsulta').value;

        if (!cpf || !dataNascimento || !tipoConsulta) {
            this.showNotification('Preencha todos os campos obrigatórios', 'error');
            return;
        }

        if (!this.validarCPF(cpf)) {
            this.showNotification('CPF inválido', 'error');
            return;
        }

        this.showLoading(true);

        // Simula consulta
        setTimeout(() => {
            this.showLoading(false);
            this.showNotification('Consulta realizada com sucesso!', 'success');
            
            // Fecha modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('consultaModal'));
            modal.hide();
        }, 3000);
    }

    calcularAposentadoria() {
        const salario = parseFloat(document.getElementById('salarioAtual').value);
        const tempo = parseInt(document.getElementById('tempoContribuicao').value);
        const idade = parseInt(document.getElementById('idadeAtual').value);
        const sexo = document.getElementById('sexo').value;

        if (!salario || !tempo || !idade || !sexo) {
            this.showNotification('Preencha todos os campos', 'error');
            return;
        }

        // Cálculo simplificado
        const idadeMinima = sexo === 'M' ? 65 : 62;
        const tempoMinimo = sexo === 'M' ? 35 : 30;
        
        const anosRestantes = Math.max(0, idadeMinima - idade);
        const tempoRestante = Math.max(0, tempoMinimo - tempo);
        
        const valorEstimado = salario * 0.8; // Aproximação
        
        const resultado = `
            <div class="row">
                <div class="col-md-6">
                    <strong>Situação Atual:</strong><br>
                    • Idade: ${idade} anos<br>
                    • Tempo de contribuição: ${tempo} anos<br>
                    • Salário atual: R$ ${salario.toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                </div>
                <div class="col-md-6">
                    <strong>Para se aposentar:</strong><br>
                    • Anos restantes: ${anosRestantes} anos<br>
                    • Tempo restante: ${tempoRestante} anos<br>
                    • Valor estimado: R$ ${valorEstimado.toLocaleString('pt-BR', {minimumFractionDigits: 2})}
                </div>
            </div>
        `;

        document.getElementById('resultadoConteudo').innerHTML = resultado;
        document.getElementById('resultadoCalculadora').style.display = 'block';
    }

    setupFormValidation() {
        // Validação em tempo real
        document.querySelectorAll('input[required]').forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.getAttribute('name') || field.id;

        if (field.hasAttribute('required') && !value) {
            this.showFieldError(field, `${fieldName} é obrigatório`);
            return false;
        }

        if (field.type === 'email' && value && !this.validateEmail(value)) {
            this.showFieldError(field, 'Email inválido');
            return false;
        }

        this.clearFieldError(field);
        return true;
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    setupCPFMask() {
        const cpfInput = document.getElementById('cpf');
        if (cpfInput) {
            cpfInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                e.target.value = value;
            });
        }
    }

    validarCPF(cpf) {
        cpf = cpf.replace(/[^\d]/g, '');
        
        if (cpf.length !== 11) return false;
        if (/^(\d)\1{10}$/.test(cpf)) return false;
        
        let soma = 0;
        for (let i = 0; i < 9; i++) {
            soma += parseInt(cpf.charAt(i)) * (10 - i);
        }
        
        let digito1 = 11 - (soma % 11);
        if (digito1 > 9) digito1 = 0;
        
        soma = 0;
        for (let i = 0; i < 10; i++) {
            soma += parseInt(cpf.charAt(i)) * (11 - i);
        }
        
        let digito2 = 11 - (soma % 11);
        if (digito2 > 9) digito2 = 0;
        
        return digito1 === parseInt(cpf.charAt(9)) && digito2 === parseInt(cpf.charAt(10));
    }

    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    setupNotifications() {
        // Container para notificações
        if (!document.getElementById('notifications-container')) {
            const container = document.createElement('div');
            container.id = 'notifications-container';
            container.style.position = 'fixed';
            container.style.top = '20px';
            container.style.right = '20px';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
    }

    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('notifications-container');
        const notification = document.createElement('div');
        
        const colors = {
            success: 'alert-success',
            error: 'alert-danger',
            warning: 'alert-warning',
            info: 'alert-info'
        };

        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        notification.className = `alert ${colors[type]} alert-dismissible fade show`;
        notification.style.minWidth = '300px';
        notification.style.marginBottom = '10px';
        notification.innerHTML = `
            <i class="${icons[type]}"></i> ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;

        container.appendChild(notification);

        // Remove automaticamente
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }

    showLoading(show) {
        let loader = document.getElementById('global-loader');
        
        if (show) {
            if (!loader) {
                loader = document.createElement('div');
                loader.id = 'global-loader';
                loader.innerHTML = `
                    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                                background: rgba(0,0,0,0.8); z-index: 10000; 
                                display: flex; align-items: center; justify-content: center;">
                        <div class="text-center text-white">
                            <div class="loading-spinner"></div>
                            <p class="mt-3">Processando...</p>
                        </div>
                    </div>
                `;
                document.body.appendChild(loader);
            }
            loader.style.display = 'block';
        } else {
            if (loader) {
                loader.style.display = 'none';
            }
        }
    }

    setupLoadingStates() {
        // Intercepta formulários para mostrar loading
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', () => {
                this.showLoading(true);
            });
        });
    }

    setupTooltips() {
        // Inicializa tooltips do Bootstrap
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    addButtonFeedback(button) {
        // Efeito de clique
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }

    // Utilities
    formatCurrency(value) {
        return value.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }

    formatDate(date) {
        return new Date(date).toLocaleDateString('pt-BR');
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    window.fontesSystem = new FONTESSystem();
});

// Service Worker para PWA (opcional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
