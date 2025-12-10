# Usando o C4 Model na Produção – EvolveRH

Este documento descreve a arquitetura do sistema EvolveRH usando os níveis de Contexto (Nível 1), Contêiner (Nível 2) e Componente (Nível 3) do Modelo C4, proporcionando uma visão hierárquica e detalhada da solução.

---

## 1. Nível de Contexto (Nível 1)

### Propósito
Fornecer uma visão macro do sistema EvolveRH, destacando sua interação com sistemas externos, usuários e outros atores relevantes. Mostrar como o assistente virtual se insere no ecossistema corporativo de Recursos Humanos.

### Contexto
Assistente Virtual Inteligente para automação de atendimento a dúvidas sobre políticas de Recursos Humanos em organizações corporativas.

### Atores e Sistemas Externos

| Atores/Sistemas | Descrição |
| :--- | :--- |
| **Colaboradores** | Funcionários que consultam informações sobre políticas, benefícios, férias e procedimentos administrativos. |
| **Profissionais de RH** | Membros da equipe de RH que utilizam o sistema para gestão de documentos, monitoramento de métricas e validação de respostas. |
| **Sistemas de Documentos Corporativos** | Repositórios existentes de políticas, manuais e regulamentos internos da organização (Fonte de dados). |
| **API Google Gemini** | Serviço externo de IA generativa para processamento de linguagem natural e geração de respostas contextualizadas (Dependência Externa). |
| **Administradores de Sistema** | Equipe de TI ou RH responsável pela manutenção, configuração e suporte técnico do sistema. |

### Interações Principais

* **Colaboradores** interagem via interface web para fazer perguntas em linguagem natural sobre políticas de RH.
* **Profissionais de RH** utilizam a interface administrativa para upload de documentos, configuração e monitoramento.
* **EvolveRH** consulta a **API Gemini** para processamento de perguntas e geração de respostas.
* **EvolveRH** acessa **Documentos Corporativos** para extrair e indexar políticas.
* **EvolveRH** persiste interações e documentos em **armazenamento local** para histórico e análise.
* **Administradores** configuram credenciais, monitoram desempenho e realizam manutenção.

---

## 2. Nível de Contêiner (Nível 2)

### Propósito
Detalhar os "contêineres" que compõem o sistema EvolveRH, mostrando aplicativos, serviços e componentes tecnológicos e como eles se conectam.

### Contêineres no Sistema EvolveRH

| Contêiner | Função Principal | Tecnologia/Stack | Responsabilidades |
| :--- | :--- | :--- | :--- |
| **Frontend Web** | Interface principal para interação com todos os tipos de usuários. | **Streamlit Framework**, Python, HTML/CSS. | Renderização de interface, captura de inputs, apresentação de respostas, gestão de sessões. |
| **Serviço de Processamento de IA** | Processamento de linguagem natural e geração de respostas contextualizadas. | Google Generative AI SDK, Python, Múltiplos modelos Gemini. | Compreensão de perguntas, integração com API externa, geração e formatação de respostas. |
| **Serviço de Processamento de Documentos** | Extração, conversão e gestão de documentos corporativos. | **PyPDF2**, FPDF, Sistema de arquivos local. | Upload, extração de texto, persistência de políticas, geração de relatórios PDF. |
| **Serviço de Dados e Configuração** | Armazenamento e gestão de dados do sistema. | Sistema de arquivos local, arquivos JSON/CSV, **Python-dotenv**. | Armazenamento de políticas e histórico, configurações do sistema, credenciais de acesso. |
| **Serviço de Autenticação e Controle de Acesso** | Gestão de identidade, autenticação e autorização. | **Streamlit session state**, Sistema de perfis baseado em configuração. | Validação de credenciais, definição de perfis de acesso, controle de permissões. |

---

## 3. Nível de Componente (Nível 3)

### Propósito
Fornecer visão detalhada dos componentes internos do contêiner **"Serviço de Processamento de IA"**, mostrando responsabilidades e interações específicas (detalhamento do `ai_handler.py`).

### Componentes no Serviço de Processamento de IA

| Componente | Função Principal | Interações |
| :--- | :--- | :--- |
| **Gerador de Contexto e Prompts** | Construir prompts estruturados combinando pergunta do usuário, histórico e políticas relevantes. | Recebe pergunta e histórico do Frontend, consulta políticas do Serviço de Dados, envia prompt para o Processador de Modelos. |
| **Processador de Modelos com Fallback** | Executar chamadas à API Gemini com sistema hierárquico de tentativas em múltiplos modelos. | Recebe prompt do Gerador, tenta modelos em ordem definida, retorna resposta ou erro para o Gerenciador de Respostas. |
| **Gerenciador de Respostas e Formatação** | Processar respostas brutas da API, aplicar formatação, validação básica e preparação para apresentação. | Recebe resposta bruta do Processador de Modelos, aplica formatação, envia resposta formatada para o Frontend. |
| **Sistema de Respostas Simuladas (Fallback Local)** | Fornecer respostas básicas baseadas em palavras-chave quando a API externa está indisponível. | Ativado pelo Processador de Modelos em caso de falhas consecutivas, fornece resposta alternativa ao Gerenciador de Respostas. |
| **Validador de Conectividade API** | Verificar disponibilidade e funcionalidade da API Gemini antes de operações críticas. | Executado na inicialização e periodicamente, notifica sistema de monitoramento sobre status. |