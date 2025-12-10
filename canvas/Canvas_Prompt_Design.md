#  Canvas de Design de Prompts – EvolveRH

Este canvas documenta o design de prompts e a estratégia de iteração para o assistente virtual EvolveRH, focando em alinhar as capacidades da IA generativa com as expectativas de uso e a base de conhecimento de RH.

---

## 1. Prompt Inicial

O prompt inicial define o tom, o contexto e as expectativas para a interação, estabelecendo claramente o papel do sistema e suas limitações.

> **Prompt Implementado:**
> "Olá! Sou o Assistente Virtual de RH da empresa. Estou aqui para ajudar você com dúvidas sobre políticas internas, benefícios, férias, e outros temas relacionados a recursos humanos. Por favor, digite sua pergunta em linguagem natural que responderei com base nas **políticas corporativas disponíveis**."

---

## 2. Respostas Esperadas

Lista das categorias principais de perguntas e suas variações linguísticas mais comuns, identificadas durante a fase de imersão com profissionais de RH e colaboradores.

| Categoria | Exemplos de Perguntas Frequentes |
| :--- | :--- |
| **Férias e Afastamentos** | "Quantos dias de férias eu tenho direito?"; "Como solicitar minhas férias?"; "Posso dividir minhas férias em períodos?"; "Qual o prazo para agendar férias?" |
| **Benefícios Corporativos** | "Quais são os benefícios oferecidos pela empresa?"; "Como funciona o vale-refeição?"; "Qual o valor do plano de saúde?"; "Temos auxílio home office?" |
| **Políticas Internas** | "Qual o horário de trabalho?"; "Como funciona o banco de horas?"; "Qual a política de dress code?"; "É permitido trabalho remoto?" |
| **Procedimentos Administrativos** | "Como solicitar atestado médico?"; "Qual o processo para pedido de demissão?"; "Como atualizar meus dados cadastrais?"; "Onde encontro a folha de ponto?" |
| **Saudações e Início de Conversa** | "Oi"; "Bom dia"; "Preciso de ajuda"; "Olá, tudo bem?" |

---

## 3. Ações Esperadas

Ações específicas que o assistente virtual deve executar em resposta a cada categoria de pergunta, garantindo consistência e alinhamento com as políticas corporativas.

### Ações por Categoria

* **Para perguntas sobre Férias:**
    * Consultar a seção de férias nas políticas carregadas.
    * Informar sobre direito, agendamento, divisão e pagamento.
    * Direcionar para o sistema específico quando aplicável.
    * Esclarecer prazos e documentação necessária.

* **Para perguntas sobre Benefícios:**
    * Listar benefícios disponíveis conforme políticas.
    * Especificar valores, condições e elegibilidade.
    * Explicar processos de solicitação e utilização.
    * Informar sobre períodos de carência quando existirem.

* **Para perguntas sobre Políticas Internas:**
    * Referenciar o capítulo específico das políticas