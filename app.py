import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from fpdf import FPDF
import PyPDF2
from io import BytesIO

# Importar módulos
from src.modules.config import CREDENCIAIS
from src.modules.pdf_handler import extrair_texto_pdf, salvar_politicas, carregar_politicas, gerar_pdf_conversa
from src.modules.ai_handler import buscar_resposta, gerar_resposta_simulada, testar_api_gemini
from src.modules.ui_components import login_page

# Configuração da página
st.set_page_config(
    page_title="EvolveRH - MVP",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Carregar variáveis de ambiente
load_dotenv()

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
    
    st.title("► Login - EvolveRH")
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
                st.success(f"✓ Bem-vindo, {CREDENCIAIS[username]['nome']}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("✗ Usuário ou senha incorretos")
    
    st.divider()
    
    # Informações de teste
    with st.expander("ℹ Credenciais de Teste"):
        st.markdown("""
        **Usuário RH:**
        - Usuário: `rh`
        - Senha: `rh123`
        
        **Funcionário:**
        - Usuário: `funcionario`
        - Senha: `func123`
        """)


# Interface principal
def main():
    # Verificar se usuário está logado
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return
    
    # Verificar API key
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠ API Key não configurada. Crie um arquivo .env com GEMINI_API_KEY")
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
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    with col2:
        st.title("🤖 EvolveRH")
        badge_class = "user-badge-rh" if st.session_state.user_type == "rh" else ""
        st.markdown(f"""
        MVP - Assistente Virtual  
        <span class='user-badge {badge_class}'>
        👤 {st.session_state.user_name} ({st.session_state.user_type.upper()})
        </span>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("⊣ Sair", key="logout"):
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
            st.header("⬆ Upload de Documentos")
            st.markdown("""
            <div style='background-color: #fff3e0; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <strong>⚠ ÁREA RESTRITA - RH</strong><br>
            Você tem permissão para fazer upload de políticas.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;'>
            <strong>▪ Como usar:</strong><br>
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
                if st.button("⟳ Processar", use_container_width=True, type="primary"):
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
                        st.success(f"✓ {len(arquivos_pdf)} arquivo(s) processado(s) com sucesso!")
                        time.sleep(1)
                        st.rerun()
            
            st.divider()
        
        # Mostrar arquivos carregados (para todos)
        if st.session_state.arquivos_carregados:
            st.subheader("[ ] Arquivos Carregados")
            for arquivo in st.session_state.arquivos_carregados:
                with st.expander(f"▬ {arquivo['nome']}:"):
                    st.write(f"**Tamanho:** {arquivo['tamanho'] / 1024:.2f} KB")
                    st.write(f"**Carregado em:** {arquivo['timestamp']}")
                    st.write(f"**Carregado por:** {arquivo.get('uploaded_by', 'Sistema')}")
            
            # Botão para limpar (apenas RH)
            if st.session_state.user_type == "rh":
                if st.button("⌫ Limpar Todos", use_container_width=True):
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
        st.header("ℹ Sobre")
        if st.session_state.user_type == "rh":
            st.markdown("""
            **Funcionalidades RH:**
            - ⬆ Upload de PDFs com políticas
            - ‣ Gerenciar documentos
            - ‣ Testar o chatbot
            - ▓ Visualizar estatísticas
            """)
        else:
            st.markdown("""
            **Funcionalidades:**
            - ‣ Consultar políticas da empresa
            - ▬ Exportar conversas
            - ▲ Respostas baseadas em IA
            """)
        
        st.divider()
        
        # Funcionalidades específicas por tipo de usuário
        if st.session_state.user_type == "rh":
            st.subheader("► Painel RH")
            
            # Upload de políticas
            st.markdown("**Atualizar Políticas:**")
            uploaded_file = st.file_uploader("Selecione o arquivo politicas.txt", type="txt")
            if uploaded_file is not None:
                if st.button("📤 Subir Arquivo", key="upload"):
                    # Salvar o arquivo
                    with open('politicas.txt', 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    # Recarregar políticas
                    st.session_state.politicas = carregar_politicas()
                    st.success("Políticas atualizadas com sucesso!")
                    time.sleep(1)
                    st.rerun()
            
            st.divider()
        
        # Exemplo de perguntas (para todos os usuários)
        st.subheader("• Perguntas Sugeridas")
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


# Ponto de entrada
if __name__ == "__main__":
    # Testar API antes de iniciar
    if testar_api_gemini(os.getenv("GEMINI_API_KEY")):
        main()
    else:
        print("Não foi possível conectar à API Gemini. Verifique sua chave e conexão.")