# EvolveRH - Chatbot Corporativo para Recursos Humanos

## Visão Geral do Projeto
Este repositório contém um MVP (Minimum Viable Product) de um Chatbot Corporativo inteligente para o setor de Recursos Humanos. O projeto demonstra, de forma prática, como a inteligência artificial generativa pode transformar processos de atendimento interno e otimizar a gestão de informações corporativas.

## Objetivo Principal
Implementar um assistente virtual capaz de responder dúvidas recorrentes sobre políticas de RH de forma automática e contextualizada, reduzindo significativamente a carga operacional das equipes de Recursos Humanos e melhorando o acesso dos colaboradores a informações precisas e padronizadas.

## Escopo do MVP
O MVP contempla:
- Interface web interativa com sistema de autenticação diferenciada (RH vs Colaborador)
- Base de conhecimento alimentada por documentos corporativos em formato PDF
- Integração com Google Gemini API para processamento de linguagem natural
- Sistema de fallback multi-modelo para garantir disponibilidade
- Dashboard com métricas de uso e desempenho
- Exportação de conversas para arquivos PDF

## Funcionalidades Implementadas

### Para Colaboradores
- Chat intuitivo para consulta sobre políticas, benefícios e procedimentos
- Respostas instantâneas baseadas na documentação oficial da empresa
- Histórico de conversas e exportação para referência futura

### Para Equipe de RH
- Upload e gestão de documentos corporativos (PDF)
- Monitoramento de métricas de uso e desempenho
- Validação e ajuste das respostas geradas pelo sistema
- Controle de acesso e perfis diferenciados

## Tecnologias Utilizadas
- **Frontend:** Streamlit (Python)
- **IA Generativa:** Google Gemini API
- **Processamento de Documentos:** PyPDF2, FPDF
- **Gerenciamento de Configuração:** Python-dotenv
- **Controle de Versão:** Git

## Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior
- Chave de API do Google Gemini
- Ambiente virtual Python (recomendado)

### Passos para Execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/evolverh-api.git
   cd evolverh-api
   ```

2. Configure o ambiente virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env e adicione sua chave Gemini
   GEMINI_API_KEY=sua_chave_aqui
   ```

5. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

6. Acesse no navegador:
   ```
   http://localhost:8501
   ```

### Credenciais de Teste
- **Usuário RH:** `rh` / `rh123`
- **Usuário Colaborador:** `funcionario` / `func123`

## Arquitetura do Sistema
```
evolverh-api/
├── app.py                    # Entry point principal
├── requirements.txt          # Dependências do projeto
├── politicas.txt            # Base de conhecimento inicial
├── src/                      # Código fonte modularizado
│   ├── modules/
│   │   ├── ai_handler.py     # Integração com Gemini API
│   │   ├── pdf_handler.py    # Processamento de documentos
│   │   ├── config.py         # Configurações e credenciais
│   │   └── ui_components.py  # Componentes de interface
│   └── __init__.py
└── dados/                    # Armazenamento de documentos
    └── politicas_extraidas.txt
```

## Público-Alvo
- Colaboradores de médias e grandes empresas que necessitam acessar informações de RH
- Equipes de Recursos Humanos sobrecarregadas com atendimentos repetitivos
- Gestores interessados em transformação digital e automação de processos

## Proposta de Valor
- Redução de até 70% no tempo gasto com atendimentos repetitivos de RH
- Padronização de 100% das informações transmitidas aos colaboradores
- Melhoria na experiência do colaborador com respostas 24/7
- Liberação de tempo da equipe de RH para atividades estratégicas
- Demonstração prática do potencial da IA generativa em ambientes corporativos

## Status do Projeto
Trata-se de uma versão funcional do MVP, validada em ambiente controlado e pronta para testes em cenários reais. O sistema está em fase de refinamento contínuo, com melhorias incrementais baseadas em feedback dos usuários.

## Próximos Passos
- Integração com sistemas corporativos de RH
- Implementação de análise de sentimentos
- Expansão para suporte multilíngue
- Desenvolvimento de API para integração externa
- Criação de dashboard analítico avançado

## Contribuição
Contribuições são bem-vindas. Para sugerir melhorias ou reportar problemas:
1. Abra uma issue descrevendo a sugestão ou problema
2. Para contribuições de código, siga o fluxo de pull requests
3. Mantenha o código documentado e aderente às boas práticas

## Equipe de Desenvolvimento
- **Caué Marinho** - Processamento de documentos e extração de texto
- **Jorge Freitas** - Arquitetura do sistema e integração com IA
- **Karen Vergosa** - Design de interface e experiência do usuário
- **Maria Beatriz** - Gestão de projeto e coordenação técnica

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para detalhes.

## Contato
Para dúvidas, sugestões ou colaborações relacionadas a este projeto, utilize os canais de comunicação do repositório ou entre em contato com a equipe de desenvolvimento através dos emails institucionais fornecidos na documentação do projeto.
