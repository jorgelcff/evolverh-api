# Diagrama de Componentes para EvolveRH API

Este diagrama detalha a arquitetura de software da solução EvolveRH, descrevendo os módulos, componentes internos, tecnologias e os principais fluxos de dados do sistema.

---

## Componentes Principais

### 1. Módulo de IA Generativa (`ai_handler.py`) – (Processamento de IA)

| Componente | Função | Tecnologia/Dependência |
| :--- | :--- | :--- |
| **Gerador de Respostas Contextualizadas** | Processa perguntas em linguagem natural e gera respostas baseadas em políticas corporativas. | **Google Gemini API**, Contexto das políticas, Histórico de conversa, Templates de prompts. |
| **Sistema de Fallback Multi-modelo** | Garante disponibilidade através de tentativa sequencial em 6 modelos Gemini alternativos. | Google Generative AI SDK com tratamento de exceções, Configuração de API, Lista hierárquica de modelos. |
| **Gerador de Respostas Simuladas** | Fornece respostas baseadas em palavras-chave quando a API falha. | Lógica condicional Python com mapeamento de tópicos, Palavras-chave predefinidas, Templates de resposta. |

---

### 2. Módulo de Processamento de Documentos (`pdf_handler.py`) – (Gestão de Dados)

| Componente | Função | Tecnologia/Dependência |
| :--- | :--- | :--- |
| **Extrator de Texto de PDF** | Converte documentos PDF em texto estruturado preservando formatação. | **PyPDF2** com processamento por página, Arquivos PDF uploadados, encoding UTF-8. |
| **Gerenciador de Base de Conhecimento** | Consolida políticas de múltiplas fontes em base unificada. | Sistema de arquivos com hierarquia de fontes, Arquivos de políticas, Documentos processados, Session state. |
| **Gerador de Relatórios PDF** | Cria documentos PDF com histórico de conversas e métricas. | **FPDF** com formatação estruturada, Histórico de mensagens, Metadados da sessão. |

---

### 3. Módulo de Interface e Controle (`app.py` + `ui_components.py`) – (Interface e Controle)

| Componente | Função | Tecnologia/Dependência |
| :--- | :--- | :--- |
| **Sistema de Autenticação** | Gerencia login, perfis de usuário e controle de acesso. | **Streamlit session state** com credenciais configuráveis, Arquivo de configuração, Tipos de usuário definidos. |
| **Controlador de Fluxo de Conversa** | Orquestra interações entre usuário, IA e base de conhecimento. | **Streamlit callbacks** e state management, Handlers de IA, Processamento de documentos, Interface. |
| **Gerenciador de Interface Responsiva** | Renderiza componentes UI adaptados ao tipo de usuário (RH vs Colaborador). | **Streamlit components** com CSS customizado, Templates HTML/CSS, Componentes modulares. |

---

## Fluxos de Dados Principais

### ➡️ Fluxo de Consulta (Usuário Colaborador)

$$
\text{Usuário} \rightarrow \text{Interface} \rightarrow \text{Controlador} \rightarrow \text{IA Generativa} \rightarrow \text{Base de Conhecimento} \rightarrow \text{Resposta} \rightarrow \text{Interface} \rightarrow \text{Usuário}
$$

### Fluxo de Upload de Documentos (Usuário RH)

$$
\text{Usuário RH} \rightarrow \text{Interface} \rightarrow \text{Extrator PDF} \rightarrow \text{Gerenciador Base Conhecimento} \rightarrow \text{Persistência} \rightarrow \text{Confirmação}
$$

### Fluxo de Autenticação

$$
\text{Usuário} \rightarrow \text{Formulário Login} \rightarrow \text{Validação Credenciais} \rightarrow \text{Definição Perfil} \rightarrow \text{Renderização Interface Personalizada}
$$

---

## Dependências Técnicas (Dependência Externa)

* **Streamlit:** Framework principal para interface web e gestão de estado.
* **Google Generative AI:** API central para processamento de linguagem natural (Geração de IA).
* **PyPDF2:** Biblioteca para extração de texto de documentos PDF.
* **FPDF:** Geração de relatórios em formato PDF.
* **Python-dotenv:** Gerenciamento de variáveis de ambiente e configurações.

---

## Legenda de Componentes

| Categoria | Descrição |
| :--- | :--- |
| **Processamento de IA** | Componentes relacionados a inteligência artificial e geração de respostas. |
| **Gestão de Dados** | Componentes de processamento, armazenamento e recuperação de informações. |
| **Interface e Controle** | Componentes de interação com usuário e orquestração do sistema. |
| **Dependência Externa** | Serviços ou bibliotecas externas ao sistema principal. |
| **Fluxo de Dados** | Comunicação e transferência de informações entre componentes. |