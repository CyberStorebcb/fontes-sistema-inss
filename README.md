# Sistema FONTES v3.0 - Deploy no Render 🏛️

Sistema web moderno para serviços do INSS hospedado no Render.com

## 🚀 Deploy no Render.com

### 📋 Informações do Projeto
- **Nome:** Sistema FONTES
- **Versão:** 3.0  
- **Tecnologia:** Python Flask
- **Porta:** 5000 (configurada automaticamente pelo Render)

### 🌐 Como fazer o Deploy

#### 1. **Conectar Repositório**
- Acesse [render.com](https://render.com)
- Clique em "New +" → "Web Service"
- Conecte seu repositório GitHub

#### 2. **Configurações no Render**
```
Name: fontes-sistema-inss
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

#### 3. **Variáveis de Ambiente (opcionais)**
```
SECRET_KEY=sua-chave-secreta-aqui
RENDER=true
```

### 👤 Credenciais de Acesso
- **Admin:** `admin` / `admin123`
- **Usuário:** `usuario` / `123456`
- **Demo:** `demo` / `demo123`

### ✅ Recursos Incluídos
- ✅ Interface responsiva (Bootstrap 5)
- ✅ Sistema de login funcional
- ✅ Dashboard interativo
- ✅ 6 categorias de serviços
- ✅ Link direto para Meu INSS
- ✅ Health check para monitoramento
- ✅ Design moderno e profissional
- ✅ **Meu INSS**: Integração com serviços INSS
- ✅ **Suporte**: Sistema de suporte integrado
- ✅ **Solicitar Serviço**: Solicitações diversas

### Design Moderno
- 🎨 Interface escura moderna
- 📱 Design responsivo
- 🖱️ Navegação intuitiva por categorias
- ⚡ Performance otimizada

## 🛠️ Tecnologias

- **Python 3.8+**
- **CustomTkinter**: Interface moderna
- **SQLite**: Banco de dados
- **PIL/Pillow**: Manipulação de imagens

## 📦 Instalação

1. **Clone o repositório:**
```bash
git clone <repositorio>
cd APONSENTAR
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema:**
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
APONSENTAR/
├── main.py                          # Arquivo principal
├── README.md                        # Documentação
├── requirements.txt                 # Dependências
├── src/                            # Código fonte
│   └── views/                      # Interfaces
│       ├── fontes_interface.py     # Interface principal FONTES
│       └── fontes_integration.py   # Integração com sistema
├── logs/                           # Logs do sistema
│   └── fontes.log
└── dados/                         # Dados do sistema
```

## 🎯 Como Usar

### Iniciando o Sistema
1. Execute `python main.py`
2. A interface FONTES abrirá automaticamente
3. Clique nas categorias para acessar as funcionalidades

### Categorias Disponíveis

#### 🏛️ Aposentadoria
- **Cadastrar Solicitação**: Formulário completo para aposentadoria
- **Consultar Status**: Acompanhe o andamento da solicitação
- **Documentos Necessários**: Lista de documentos obrigatórios
- **Calcular Aposentadoria**: Simulador de aposentadoria

#### 🤱 Maternidade
- **Solicitar Benefício**: Auxílio maternidade
- **Acompanhar Processo**: Status da solicitação
- **Documentos**: Lista de documentos necessários
- **Salário Maternidade**: Informações sobre valores

#### 📁 Arquivos
- **Meus Documentos**: Gestão de documentos pessoais
- **Upload de Arquivos**: Envio de documentos
- **Buscar Documentos**: Localizar arquivos
- **Gerar Relatórios**: Relatórios personalizados

#### 🏢 Meu INSS
- **Extrato de Contribuições**: Histórico completo
- **Tempo de Contribuição**: Cálculo de tempo
- **Benefícios**: Gestão de benefícios
- **Simulações**: Simuladores diversos

#### 🛠️ Suporte
- **Chat Online**: Suporte em tempo real
- **Telefone**: Contato telefônico
- **Email**: Suporte por email
- **FAQ**: Perguntas frequentes
- **Tutoriais**: Vídeos explicativos

#### 📋 Solicitar Serviço
- **Nova Solicitação**: Formulário geral
- **Acompanhar**: Status das solicitações
- **Histórico**: Histórico completo
- **Cancelar Solicitação**: Gerenciar solicitações

## 🔧 Configurações

### Logs
- Localização: `logs/fontes.log`
- Rotação automática: 10MB, 5 arquivos
- Nível: INFO

### Integração
- Sistema compatível com base de clientes existente
- Integração transparente com dados legacy

## 🐛 Solução de Problemas

### Erro de Dependências
```bash
# Instalar dependências
pip install customtkinter pillow

# Ou usando requirements.txt
pip install -r requirements.txt
```

### Interface não Abre
1. Verifique Python 3.8+ instalado
2. Verifique dependências instaladas
3. Execute como administrador se necessário

### Erro de Importação
- Verifique se está executando do diretório correto
- Certifique-se que a estrutura de pastas está correta

## 📊 Funcionalidades por Categoria

| Categoria | Funcionalidades | Status |
|---|---|---|
| Aposentadoria | Cadastro, Consulta, Cálculos | ✅ Ativo |
| Maternidade | Solicitações, Acompanhamento | ✅ Ativo |
| Arquivos | Upload, Gestão, Relatórios | ✅ Ativo |
| Meu INSS | Extratos, Simulações | ✅ Ativo |
| Suporte | Chat, Telefone, FAQ | ✅ Ativo |
| Serviços | Solicitações Diversas | ✅ Ativo |

## 🎨 Interface

### Design Moderno
- Tema escuro elegante
- Cards interativos com hover effects
- Layout responsivo 1400x900
- Ícones intuitivos para cada categoria

### Navegação
- Grid 3x2 de categorias principais
- Header com título centralizado
- Footer com informações do sistema
- Botões de ação claros e objetivos

## 🔄 Atualizações

### v3.0 (Atual)
- ✅ Sistema focado exclusivamente em FONTES
- ✅ Interface otimizada e limpa
- ✅ Código simplificado
- ✅ Performance melhorada

## 📝 Dependências

```
customtkinter>=5.2.0  # Interface moderna
Pillow>=9.5.0         # Manipulação de imagens
```

## 🚀 Execução

```bash
# Método 1: Python diretamente
python main.py

# Método 2: Python Launcher (Windows)
py main.py

# Método 3: Com logs detalhados
python main.py --verbose
```

## 📞 Suporte

Para suporte técnico:
- **Email**: suporte@fontes.com.br
- **Telefone**: (11) 99999-9999
- **Chat**: Disponível na interface

---

**Sistema FONTES v3.0** - Interface moderna para serviços INSS 🏛️
