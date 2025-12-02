import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Configuração da página
st.set_page_config(
    page_title="Chatbot RH - MVP",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se a API key está configurada
if not os.getenv("GEMINI_API_KEY"):
    st.error("⚠️ API Key não configurada. Crie um arquivo .env com GEMINI_API_KEY")
    st.info("Obtenha em: https://aistudio.google.com/app/apikey")
    st.stop()

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Função para carregar políticas
@st.cache_data
def carregar_politicas():
    try:
        with open('politicas.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error("Arquivo politicas.txt não encontrado!")
        return ""

# Função para buscar resposta com múltiplos modelos de fallback
def buscar_resposta(pergunta, historico_conversa, politicas):
    contexto = f"""
    Você é um assistente virtual de RH especializado em responder dúvidas de colaboradores.
    Use APENAS as informações fornecidas nas políticas da empresa para responder.
    
    POLÍTICAS DA EMPRESA:
    {politicas}
    
    HISTÓRICO DA CONVERSA (últimas 5 mensagens):
    {historico_conversa}
    
    PERGUNTA: {pergunta}
    
    INSTRUÇÕES IMPORTANTES:
    1. Responda baseado APENAS nas políticas fornecidas acima
    2. Seja claro, direto e amigável
    3. Se não encontrar a informação nas políticas, diga: "Não encontrei essa informação nas políticas disponíveis."
    4. Formate com marcadores quando apropriado
    5. Assine como "Assistente Virtual de RH"
    6. Mantenha a resposta em português brasileiro
    
    RESPOSTA:
    """
    
    # Lista de modelos para tentar (em ordem de preferência)
    modelos = [
        'models/gemini-2.0-flash',          # Modelo rápido e estável
        'models/gemini-2.0-flash-001',      # Outra versão do Flash
        'models/gemini-flash-latest',       # Última versão Flash
        'models/gemini-pro-latest',         # Última versão Pro
        'models/gemini-2.0-flash-lite',     # Versão mais leve
    ]
    
    for modelo_nome in modelos:
        try:
            model = genai.GenerativeModel(modelo_nome)
            response = model.generate_content(
                contexto,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=500,
                )
            )
            return response.text
        except Exception as e:
            print(f"Modelo {modelo_nome} falhou: {str(e)}")
            continue  # Tenta o próximo modelo
    
    # Se todos os modelos falharem, retorna resposta simulada
    return gerar_resposta_simulada(pergunta, politicas)

# Função de fallback caso todos os modelos falhem
def gerar_resposta_simulada(pergunta, politicas):
    """Gera uma resposta simulada baseada em palavras-chave das políticas"""
    pergunta_lower = pergunta.lower()
    
    # Respostas baseadas em palavras-chave
    if any(palavra in pergunta_lower for palavra in ['oi', 'olá', 'hello', 'bom dia', 'tudo bem']):
        return "Olá! Sou o Assistente Virtual de RH. Como posso ajudar você hoje?"
    
    elif 'férias' in pergunta_lower or 'ferias' in pergunta_lower:
        return """**Sobre Férias:**
- Todo colaborador tem direito a 30 dias de férias após 12 meses de trabalho
- As férias podem ser divididas em até 3 períodos
- Agendamento com 30 dias de antecedência
- Período aquisitivo: Janeiro a Dezembro

*Assistente Virtual de RH*"""
    
    elif 'vale-refeição' in pergunta_lower or 'vr' in pergunta_lower:
        return """**Vale-Refeição:**
- Valor: R$ 30,00 por dia útil

*Assistente Virtual de RH*"""
    
    elif 'salário' in pergunta_lower or 'pagamento' in pergunta_lower:
        return """**Folha de Pagamento:**
- Pagamento: dia 5 de cada mês
- Adiantamento: dia 20 (até 40% do salário)
- Descontos: INSS, IRRF, vale-transporte, plano de saúde

*Assistente Virtual de RH*"""
    
    elif 'home office' in pergunta_lower or 'remoto' in pergunta_lower:
        return """**Home Office:**
- Permitido até 3 dias por semana
- Necessária aprovação prévia do gestor

*Assistente Virtual de RH*"""
    
    elif 'benefício' in pergunta_lower:
        return """**Benefícios Disponíveis:**
1. Vale-refeição: R$ 30,00/dia útil
2. Vale-transporte: com desconto de 6% do salário
3. Plano de saúde: cobertura completa após 3 meses
4. Gympass: disponível para todos colaboradores

*Assistente Virtual de RH*"""
    
    elif 'ponto' in pergunta_lower or 'jornada' in pergunta_lower:
        return """**Regime de Ponto:**
- Jornada: 9h às 18h (com 1h de almoço)
- Flexibilidade: entrada entre 8h e 10h
- Banco de horas: horas extras convertidas em folga
- Home office: até 3 dias/semana

*Assistente Virtual de RH*"""
    
    else:
        return """Entendi sua pergunta. Baseado nas políticas da empresa, posso ajudar com:

• **Férias:** direitos, agendamento, período aquisitivo
• **Benefícios:** vale-refeição, vale-transporte, plano de saúde
• **Ponto:** jornada, flexibilidade, banco de horas
• **Folha de pagamento:** datas, descontos, 13º salário
• **Home office:** regras, aprovação
• **Licenças:** maternidade, paternidade, atestado

Qual desses tópicos gostaria de saber mais?

*Assistente Virtual de RH*"""

# Interface principal
def main():
    # CSS customizado
    st.markdown("""
    <style>
    .chat-message {padding: 1rem; border-radius: 10px; margin-bottom: 1rem;}
    .user-message {background-color: #e3f2fd; border-left: 4px solid #2196f3;}
    .bot-message {background-color: #f5f5f5; border-left: 4px solid #4caf50;}
    .stButton button {width: 100%; margin-bottom: 0.5rem;}
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    with col2:
        st.title("🤖 Chatbot de RH")
        st.caption("MVP - Assistente Virtual para Dúvidas Corporativas")
    
    # Inicializar histórico na session state
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    
    if 'politicas' not in st.session_state:
        st.session_state.politicas = carregar_politicas()
    
    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Sobre")
        st.markdown("""
        Este é um MVP de chatbot de RH que responde dúvidas baseadas nas políticas internas da empresa.
        
        **Temas disponíveis:**
        - Férias e descanso
        - Benefícios
        - Ponto e jornada
        - Folha de pagamento
        - Desenvolvimento
        - Código de conduta
        """)
        
        st.divider()
        
        # Exemplo de perguntas
        st.subheader("💡 Exemplos de perguntas")
        exemplos = [
            "Quantos dias de férias tenho direito?",
            "Qual o valor do vale-refeição?",
            "Como funciona o banco de horas?",
            "Quando é o pagamento do salário?",
            "Posso trabalhar de home office?"
        ]
        
        for exemplo in exemplos:
            if st.button(f"\"{exemplo}\"", key=exemplo):
                st.session_state.pergunta_exemplo = exemplo
                st.rerun()
    
    # Área do chat
    chat_container = st.container()
    
    with chat_container:
        # Exibir histórico
        for mensagem in st.session_state.historico:
            if mensagem['role'] == 'user':
                st.markdown(f"""
                <div class='chat-message user-message'>
                    <strong>Você:</strong> {mensagem['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-message bot-message'>
                    <strong>Assistente:</strong> {mensagem['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Verificar se temos uma pergunta de exemplo para processar
    if 'pergunta_exemplo' in st.session_state and st.session_state.pergunta_exemplo:
        pergunta = st.session_state.pergunta_exemplo
        # Limpar a pergunta de exemplo após usar
        del st.session_state.pergunta_exemplo
        
        # Processar a pergunta do exemplo
        st.session_state.historico.append({'role': 'user', 'content': pergunta})
        
        # Preparar histórico para contexto
        historico_texto = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.historico[-5:]]
        )
        
        # Mostrar indicador de carregamento
        with st.spinner("Consultando políticas..."):
            # Buscar resposta
            resposta = buscar_resposta(pergunta, historico_texto, st.session_state.politicas)
            
            # Adicionar resposta ao histórico
            st.session_state.historico.append({'role': 'assistant', 'content': resposta})
            
        # Rerun para mostrar a resposta
        st.rerun()
    
    # Chat input para perguntas manuais
    pergunta = st.chat_input("Digite sua pergunta sobre políticas da empresa...")
    
    if pergunta:
        # Adicionar pergunta ao histórico
        st.session_state.historico.append({'role': 'user', 'content': pergunta})
        
        # Preparar histórico para contexto
        historico_texto = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.historico[-5:]]
        )
        
        # Mostrar indicador de carregamento
        with st.spinner("Consultando políticas..."):
            # Buscar resposta
            resposta = buscar_resposta(pergunta, historico_texto, st.session_state.politicas)
            
            # Adicionar resposta ao histórico
            st.session_state.historico.append({'role': 'assistant', 'content': resposta})
            
        # Rerun para mostrar a resposta
        st.rerun()
    
    # Botão para limpar histórico
    if st.session_state.historico:
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧹 Limpar Conversa", use_container_width=True):
                st.session_state.historico = []
                st.rerun()
    
    # Footer
    st.divider()
    st.caption("MVP Chatbot RH v1.0 • Uso interno • Baseado em políticas atualizadas em Dezembro/2024")

# Teste da API antes de rodar o app
def testar_api_gemini():
    """Testa a conexão com a API Gemini"""
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content("Teste de conexão")
        print(f"✅ API Gemini funcionando: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Erro na API Gemini: {e}")
        return False

# Ponto de entrada
if __name__ == "__main__":
    # Testar API antes de iniciar
    if testar_api_gemini():
        main()
    else:
        print("Não foi possível conectar à API Gemini. Verifique sua chave e conexão.")