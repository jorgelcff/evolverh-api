import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from fpdf import FPDF
import PyPDF2
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Chatbot RH - MVP",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Carregar variáveis de ambiente
load_dotenv()

# Credenciais fake para simulação
CREDENCIAIS = {
    "rh": {"senha": "rh123", "tipo": "rh", "nome": "Funcionário RH", "email": "rh@example.com"},
    "funcionario": {"senha": "func123", "tipo": "empresa", "nome": "Funcionário Empresa", "email": "funcionario@example.com"}
}

# Função de login
def login_page():
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    
    st.title("🔐 Login - Chatbot RH")
    st.caption("Sistema de acesso para funcionários")
    
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submitted = st.form_submit_button("Entrar", use_container_width=True)
        
        if submitted:
            if username in CREDENCIAIS and CREDENCIAIS[username]["senha"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = CREDENCIAIS[username]["tipo"]
                st.session_state.user_name = CREDENCIAIS[username]["nome"]
                st.session_state.user_email = CREDENCIAIS[username]["email"]
                st.success(f"✅ Bem-vindo, {CREDENCIAIS[username]['nome']}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos")
    
    st.divider()
    
    # Informações de teste
    with st.expander("ℹ️ Credenciais de Teste"):
        st.markdown("""
        **Usuário RH:**
        - Usuário: `rh`
        - Senha: `rh123`
        
        **Funcionário:**
        - Usuário: `funcionario`
        - Senha: `func123`
        """)

# Função para extrair texto de PDF
def extrair_texto_pdf(arquivo_pdf):
    """Extrai texto de um arquivo PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(arquivo_pdf)
        texto_completo = []
        
        for pagina_num, pagina in enumerate(pdf_reader.pages, 1):
            texto = pagina.extract_text()
            if texto.strip():
                texto_completo.append(f"--- Página {pagina_num} ---\n{texto}")
        
        return "\n\n".join(texto_completo)
    except Exception as e:
        st.error(f"Erro ao processar PDF: {str(e)}")
        return None

# Função para salvar políticas extraídas
def salvar_politicas(texto, nome_arquivo="politicas_extraidas.txt"):
    """Salva o texto extraído em arquivo"""
    try:
        os.makedirs("dados", exist_ok=True)
        caminho = os.path.join("dados", nome_arquivo)
        
        with open(caminho, 'w', encoding='utf-8') as file:
            file.write(texto)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar políticas: {str(e)}")
        return False

# Função para carregar políticas
def carregar_politicas():
    """Carrega políticas de múltiplas fontes"""
    politicas_completas = []
    
    # Tentar carregar de politicas.txt (arquivo original)
    if os.path.exists('politicas.txt'):
        try:
            with open('politicas.txt', 'r', encoding='utf-8') as file:
                politicas_completas.append("=== POLÍTICAS ORIGINAIS ===\n" + file.read())
        except Exception as e:
            pass
    
    # Tentar carregar políticas extraídas de PDFs
    caminho_extraidas = os.path.join("dados", "politicas_extraidas.txt")
    if os.path.exists(caminho_extraidas):
        try:
            with open(caminho_extraidas, 'r', encoding='utf-8') as file:
                politicas_completas.append("\n\n=== POLÍTICAS DE DOCUMENTOS CARREGADOS ===\n" + file.read())
        except Exception as e:
            pass
    
    # Se tiver políticas na session_state (upload recente)
    if 'politicas_uploaded' in st.session_state and st.session_state.politicas_uploaded:
        politicas_completas.append("\n\n=== DOCUMENTOS DA SESSÃO ATUAL ===\n" + st.session_state.politicas_uploaded)
    
    return "\n\n".join(politicas_completas) if politicas_completas else "Nenhuma política carregada ainda."

# Função para gerar PDF da conversa
def gerar_pdf_conversa(historico):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Historico da Conversa - Chatbot RH", ln=True, align='C')
    pdf.ln(10)
    
    for msg in historico:
        role = "Voce" if msg['role'] == 'user' else "Assistente"
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"{role}:", ln=True)
        pdf.set_font("Arial", size=12)
        content = msg['content']
        pdf.multi_cell(0, 10, txt=content)
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

# Função para buscar resposta
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
    
    modelos = [
        'models/gemini-2.0-flash',
        'models/gemini-2.0-flash-001',
        'models/gemini-flash-latest',
        'models/gemini-pro-latest',
        'models/gemini-2.0-flash-lite',
        'models/gemini-1.5-flash',
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
            continue
    
    return gerar_resposta_simulada(pergunta, politicas)

# Função de fallback
def gerar_resposta_simulada(pergunta, politicas):
    """Gera uma resposta simulada baseada em palavras-chave"""
    pergunta_lower = pergunta.lower()
    
    if any(palavra in pergunta_lower for palavra in ['oi', 'olá', 'hello', 'bom dia', 'tudo bem']):
        return "Olá! Sou o Assistente Virtual de RH. Como posso ajudar você hoje?"
    
    elif 'férias' in pergunta_lower or 'ferias' in pergunta_lower:
        return """**Sobre Férias:**
- Todo colaborador tem direito a 30 dias de férias após 12 meses de trabalho
- As férias podem ser divididas em até 3 períodos
- Agendamento com 30 dias de antecedência

*Assistente Virtual de RH*"""
    
    else:
        return """Entendi sua pergunta. Por favor, consulte as políticas carregadas ou entre em contato com o RH.

*Assistente Virtual de RH*"""

# Interface principal
def main():
    # Verificar se usuário está logado
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return
    
    # Verificar API key
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ API Key não configurada. Crie um arquivo .env com GEMINI_API_KEY")
        st.info("Obtenha em: https://aistudio.google.com/app/apikey")
        return
    
    # Configurar Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # CSS customizado
    st.markdown("""
    <style>
    .chat-message {padding: 1rem; border-radius: 10px; margin-bottom: 1rem;}
    .user-message {background-color: #e3f2fd; border-left: 4px solid #2196f3;}
    .bot-message {background-color: #f5f5f5; border-left: 4px solid #4caf50;}
    .stButton button {width: 100%; margin-bottom: 0.5rem;}
    .user-badge {
        background-color: #4caf50;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .user-badge-rh {
        background-color: #ff9800;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    with col2:
        st.title("🤖 Chatbot de RH")
        badge_class = "user-badge-rh" if st.session_state.user_type == "rh" else ""
        st.markdown(f"""
        MVP - Assistente Virtual  
        <span class='user-badge {badge_class}'>
        👤 {st.session_state.user_name} ({st.session_state.user_type.upper()})
        </span>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("🚪 Sair", key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_name = None
            st.session_state.historico = []
            st.rerun()
    
    # Inicializar session state
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    
    if 'politicas' not in st.session_state:
        st.session_state.politicas = carregar_politicas()
    
    if 'politicas_uploaded' not in st.session_state:
        st.session_state.politicas_uploaded = ""
    
    if 'arquivos_carregados' not in st.session_state:
        st.session_state.arquivos_carregados = []
    
    # Sidebar
    with st.sidebar:
        # Seção de Upload (apenas para RH)
        if st.session_state.user_type == "rh":
            st.header("📤 Upload de Documentos")
            st.markdown("""
            <div style='background-color: #fff3e0; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <strong>⚠️ ÁREA RESTRITA - RH</strong><br>
            Você tem permissão para fazer upload de políticas.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <strong>📋 Como usar:</strong><br>
            1. Faça upload dos PDFs com políticas<br>
            2. Aguarde o processamento<br>
            3. Os documentos ficarão disponíveis para todos!
            </div>
            """, unsafe_allow_html=True)
            
            # Upload de múltiplos arquivos PDF
            arquivos_pdf = st.file_uploader(
                "Selecione um ou mais arquivos PDF",
                type=['pdf'],
                accept_multiple_files=True,
                help="Faça upload dos documentos de políticas da empresa"
            )
            
            if arquivos_pdf:
                if st.button("🔄 Processar PDFs", use_container_width=True, type="primary"):
                    textos_extraidos = []
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, arquivo in enumerate(arquivos_pdf):
                        status_text.text(f"Processando: {arquivo.name}...")
                        
                        # Extrair texto do PDF
                        texto = extrair_texto_pdf(arquivo)
                        
                        if texto:
                            textos_extraidos.append(f"\n\n=== DOCUMENTO: {arquivo.name} ===\n{texto}")
                            
                            # Verificar se arquivo já existe
                            arquivo_existe = False
                            for arq in st.session_state.arquivos_carregados:
                                if arq['nome'] == arquivo.name:
                                    arquivo_existe = True
                                    break
                            
                            if not arquivo_existe:
                                st.session_state.arquivos_carregados.append({
                                    'nome': arquivo.name,
                                    'tamanho': arquivo.size,
                                    'timestamp': time.strftime("%d/%m/%Y %H:%M"),
                                    'uploaded_by': st.session_state.user_name
                                })
                        
                        progress_bar.progress((idx + 1) / len(arquivos_pdf))
                    
                    if textos_extraidos:
                        # Juntar todos os textos
                        texto_completo = "\n".join(textos_extraidos)
                        
                        # Adicionar ao texto já existente (não sobrescrever)
                        if st.session_state.politicas_uploaded:
                            st.session_state.politicas_uploaded += "\n\n" + texto_completo
                        else:
                            st.session_state.politicas_uploaded = texto_completo
                        
                        # Salvar em arquivo
                        salvar_politicas(st.session_state.politicas_uploaded)
                        
                        # Recarregar políticas
                        st.session_state.politicas = carregar_politicas()
                        
                        status_text.empty()
                        progress_bar.empty()
                        st.success(f"✅ {len(arquivos_pdf)} arquivo(s) processado(s) com sucesso!")
                        time.sleep(1)
                        st.rerun()
            
            st.divider()
        
        # Mostrar arquivos carregados (para todos)
        if st.session_state.arquivos_carregados:
            st.subheader("📁 Arquivos Carregados")
            for arquivo in st.session_state.arquivos_carregados:
                with st.expander(f"📄 {arquivo['nome']}"):
                    st.write(f"**Tamanho:** {arquivo['tamanho'] / 1024:.2f} KB")
                    st.write(f"**Carregado em:** {arquivo['timestamp']}")
                    st.write(f"**Carregado por:** {arquivo.get('uploaded_by', 'Sistema')}")
            
            # Botão para limpar (apenas RH)
            if st.session_state.user_type == "rh":
                if st.button("🗑️ Limpar Todos os Arquivos", use_container_width=True):
                    st.session_state.arquivos_carregados = []
                    st.session_state.politicas_uploaded = ""
                    caminho = os.path.join("dados", "politicas_extraidas.txt")
                    if os.path.exists(caminho):
                        os.remove(caminho)
                    st.session_state.politicas = carregar_politicas()
                    st.success("Arquivos removidos!")
                    time.sleep(1)
                    st.rerun()
            
            st.divider()
        
        # Informações
        st.header("ℹ️ Sobre")
        if st.session_state.user_type == "rh":
            st.markdown("""
            **Funcionalidades RH:**
            - 📤 Upload de PDFs com políticas
            - 🗑️ Gerenciar documentos
            - 💬 Testar o chatbot
            - 📊 Visualizar estatísticas
            """)
        else:
            st.markdown("""
            **Funcionalidades:**
            - 💬 Consultar políticas da empresa
            - 📄 Exportar conversas
            - 🤖 Respostas baseadas em IA
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
            if st.button(f'"{exemplo}"', key=exemplo):
                st.session_state.pergunta_exemplo = exemplo
                st.rerun()
        
        st.divider()
        
    # Área do chat
    chat_container = st.container()
    
    with chat_container:
        # Mostrar aviso se não houver políticas
        if not st.session_state.politicas or st.session_state.politicas == "Nenhuma política carregada ainda.":
            if st.session_state.user_type == "rh":
                st.warning("⚠️ Nenhum documento carregado ainda. Faça upload de PDFs na barra lateral para começar!")
            else:
                st.info("ℹ️ Aguarde o RH carregar os documentos de políticas da empresa.")
        
        # Exibir histórico
        for mensagem in st.session_state.historico:
            content = mensagem['content'].strip()
            if content.endswith('</div>'):
                content = content[:-6].strip()
            
            if mensagem['role'] == 'user':
                st.markdown(f"""
                <div class='chat-message user-message'>
                    <strong>Você:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-message bot-message'>
                    <strong>Assistente:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
    
    # Verificar pergunta de exemplo
    if 'pergunta_exemplo' in st.session_state and st.session_state.pergunta_exemplo:
        pergunta = st.session_state.pergunta_exemplo
        del st.session_state.pergunta_exemplo
        
        st.session_state.historico.append({'role': 'user', 'content': pergunta})
        
        historico_texto = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.historico[-5:]]
        )
        
        with st.spinner("Consultando políticas..."):
            resposta = buscar_resposta(pergunta, historico_texto, st.session_state.politicas)
            st.session_state.historico.append({'role': 'assistant', 'content': resposta})
            
        st.rerun()
    
    # Chat input
    pergunta = st.chat_input("Digite sua pergunta sobre políticas da empresa...")
    
    if pergunta:
        st.session_state.historico.append({'role': 'user', 'content': pergunta})
        
        historico_texto = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.historico[-5:]]
        )
        
        with st.spinner("Consultando políticas..."):
            resposta = buscar_resposta(pergunta, historico_texto, st.session_state.politicas)
            st.session_state.historico.append({'role': 'assistant', 'content': resposta})
            
        st.rerun()
    
    # Botão para limpar histórico
    if st.session_state.historico:
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧹 Limpar Conversa", use_container_width=True):
                st.session_state.historico = []
                st.rerun()
    
    # Footer com estatísticas
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mensagens", len(st.session_state.historico))
    with col2:
        perguntas = len([msg for msg in st.session_state.historico if msg['role'] == 'user'])
        st.metric("Perguntas", perguntas)
    with col3:
        respostas = len([msg for msg in st.session_state.historico if msg['role'] == 'assistant'])
        st.metric("Respostas", respostas)
    with col4:
        st.metric("PDFs", len(st.session_state.arquivos_carregados))
    
    st.caption(f"MVP Chatbot RH v2.0 • Uso interno • Usuário: {st.session_state.user_name}")


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