#  Canvas de Definição de Objetivos – EvolveRH

Este documento detalha os objetivos operacionais do projeto EvolveRH, traduzindo metas estratégicas em ações técnicas específicas e estabelecendo mecanismos claros para monitoramento e avaliação de resultados.

---

## 1. Revisão do Objetivo Geral

Reavaliação e confirmação do objetivo principal do projeto, com ajustes para alinhamento ao escopo técnico e operacional definido na fase de Ideação.

> **Objetivo Geral Confirmado:** Desenvolver um assistente virtual inteligente baseado em IA generativa para automatizar respostas a dúvidas frequentes de colaboradores sobre políticas de recursos humanos, reduzindo a carga operacional da equipe de RH em pelo menos **70%** e melhorando a experiência do colaborador através de respostas rápidas, consistentes e disponíveis 24/7.

---

## 2. Refinamento de Objetivos Específicos

Detalhamento dos objetivos específicos com foco em aspectos operacionais e técnicos, garantindo alinhamento com as capacidades do sistema desenvolvido.

* **Implementar** um sistema de chat baseado em IA generativa que compreenda perguntas em linguagem natural e forneça respostas contextualizadas **exclusivamente** com base nas políticas corporativas carregadas, atingindo precisão mínima de **90%** nas respostas validadas.
* **Desenvolver** um sistema de gestão documental que permita o upload e processamento automático de documentos PDF contendo políticas da empresa, com capacidade de extração de texto estruturada e persistência em base de conhecimento unificada.
* **Criar** uma interface diferenciada por tipo de usuário (**RH vs colaborador**) que ofereça funcionalidades específicas para cada perfil, incluindo dashboard de métricas para RH e acesso simplificado ao chat para colaboradores.
* **Estabelecer** um mecanismo de fallback multi-modelo que garanta disponibilidade do serviço mesmo em cenários de indisponibilidade parcial da API Gemini, mantendo tempo de resposta abaixo de **5 segundos** em **95%** das interações.
* **Implementar** sistema de autenticação básico com credenciais diferenciadas que controle acesso a funcionalidades sensíveis como upload de documentos e visualização de métricas detalhadas.

---

## 3. Mapeamento de Indicadores Operacionais de Sucesso

Tradução dos indicadores estratégicos em métricas operacionais mensuráveis, com definição de ferramentas e processos para coleta e análise contínua.

| Indicador Operacional | Mecanismo de Coleta e Avaliação |
| :--- | :--- |
| **Tempo médio de resposta do chatbot** | Medido automaticamente pelo sistema a cada interação, com registro em log estruturado e consolidação em dashboard de métricas. |
| **Precisão das respostas** | Avaliada através de amostragem periódica onde respostas do sistema são comparadas com respostas padrão validadas por especialistas de RH, utilizando escala de concordância de **0 a 100%**. |
| **Taxa de utilização do sistema** | Monitorada através do número de sessões ativas por dia, perguntas processadas por hora e usuários únicos por semana, com dados extraídos dos logs de autenticação e interação. |
| **Satisfação do usuário** | Medida através de pesquisas periódicas embutidas na interface, utilizando escala Likert de **5 pontos** e campo para feedback qualitativo opcional. |
| **Eficiência no processamento de documentos** | Avaliada pelo tempo médio de processamento por página de PDF, taxa de sucesso na extração de texto e volume de documentos processados sem erros. |

---

## 4. Metas Quantitativas Refinadas

Estabelecimento de metas específicas, mensuráveis e temporais para cada indicador operacional, considerando a capacidade técnica atual e recursos disponíveis.

* **Tempo de Resposta:** Reduzir o tempo médio de resposta do chatbot para menos de **3 segundos** em **85%** das interações dentro dos primeiros **3 meses** de operação, com meta de sustentação abaixo de **5 segundos** em **95%** das interações.
* **Precisão:** Alcançar precisão mínima de **90%** nas respostas do sistema dentro de **2 meses** através de refinamentos iterativos nos prompts e base de conhecimento, com meta de evolução para **95%** em **6 meses**.
* **Processamento de Documentos:** Processar documentos PDF com tamanho médio de 10 páginas em menos de **30 segundos** totais, mantendo taxa de sucesso na extração de texto acima de **98%** para documentos com formato padrão.
* **Volume de Atendimento:** Atender pelo menos **200 perguntas diárias** sem degradação de performance após **1 mês** de operação estável, com capacidade de escalabilidade para **500 perguntas diárias** sem modificações arquiteturais significativas.
* **Disponibilidade:** Manter disponibilidade do sistema acima de **99%** em regime operacional padrão, considerando apenas indisponibilidades não planejadas relacionadas à infraestrutura do projeto.

---

## 5. Priorização Baseada em Impacto e Viabilidade

Classificação dos objetivos por ordem de prioridade com base em critérios de impacto operacional, viabilidade técnica, custo e prazo de implementação.

| Prioridade | Objetivo | Justificativa |
| :--- | :--- | :--- |
| **Alta** | Implementação do núcleo de chat com IA generativa e processamento básico de documentos. | Impacto direto na redução de carga operacional do RH e fundamentação técnica para demais componentes. |
| **Média** | Desenvolvimento da interface diferenciada por tipo de usuário e dashboard de métricas. | Melhoria na usabilidade e capacidade de medição de resultados, com complexidade técnica moderada. |
| **Média** | Sistema de autenticação e controle de acesso básico. | Requisito para gestão segura de documentos sensíveis, com possibilidade de evolução futura. |
| **Baixa** | Mecanismos avançados de fallback e resiliência. | Agregam confiabilidade, mas não são críticos para operação inicial, podendo ser refinados iterativamente. |

---

## 6. Identificação de Ações e Recursos Necessários

Detalhamento das ações práticas e recursos específicos requeridos para alcançar cada objetivo estabelecido.

* **Ação:** Configurar e integrar API Gemini com sistema de fallback multi-modelo.
    * **Recursos:** Chave de API Google Gemini, desenvolvedor com experiência em integração de APIs de IA, ambiente de testes com simulação de falhas controladas.
* **Ação:** Desenvolver módulo de processamento de documentos PDF com PyPDF2.
    * **Recursos:** Biblioteca PyPDF2, documentos de exemplo em diversos formatos, pipeline de validação de extração de texto.
* **Ação:** Implementar interface Streamlit com componentes modulares reutilizáveis.
    * **Recursos:** Framework Streamlit, designer UX para protótipos de interface, componentes de UI para autenticação e exibição de chat.
* **Ação:** Criar sistema de persistência de políticas e histórico de conversas.
    * **Recursos:** Estrutura de diretórios para armazenamento, sistema de logs estruturados, mecanismo de backup periódico.
* **Ação:** Estabelecer processo de validação contínua com usuários reais.
    * **Recursos:** Painel de colaboradores voluntários para testes, formulários de feedback integrados, protocolo para revisão periódica de respostas.
* **Ação:** Configurar monitoramento de métricas de performance e uso.
    * **Recursos:** Dashboard Streamlit para visualização, sistema de alertas para degradação de performance, relatórios periódicos de utilização.
* **Ação:** Desenvolver documentação técnica e de usuário.
    * **Recursos:** Template para documentação, exemplos de casos de uso, guias de instalação e configuração.