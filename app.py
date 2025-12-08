import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from fpdf import FPDF

# Configuração da página
st.set_page_config(
    page_title="Chatbot RH - MVP",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
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
    st.title("🔐 Login - Chatbot RH")
    st.caption("Sistema de acesso para funcionários")
    
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if username in CREDENCIAIS and CREDENCIAIS[username]["senha"] == password:
                st.session_state.logged_in = True
                st.session_state.user_type = CREDENCIAIS[username]["tipo"]
                st.session_state.user_name = CREDENCIAIS[username]["nome"]
                st.success(f"Bem-vindo, {CREDENCIAIS[username]['nome']}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

# Função principal
def main():
    # Verificar se está logado
    if not st.session_state.get("logged_in", False):
        login_page()
        return

    # Configurar API apenas após login
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ API Key não configurada. Crie um arquivo .env com GEMINI_API_KEY")
        st.info("Obtenha em: https://aistudio.google.com/app/apikey")
        return

    # Configurar Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
        # Quebrar linhas longas
        content = msg['content']
        pdf.multi_cell(0, 10, txt=content)
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

# Função para carregar políticas
@st.cache_data
def carregar_politicas():
    try:
        with open('politicas.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        st.error("Arquivo politicas.txt não encontrado!")
        return ""

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
        # Quebrar linhas longas
        content = msg['content']
        pdf.multi_cell(0, 10, txt=content)
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin-1')

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
        'models/gemini-1.5-flash',          # Versão anterior
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
- Férias coletivas: Definidas anualmente pelo RH
- Abono pecuniário: Opção de converter 1/3 das férias em dinheiro

*Assistente Virtual de RH*"""
    
    elif 'vale-refeição' in pergunta_lower or 'vr' in pergunta_lower:
        return """**Vale-Refeição:**
- Valor: R$ 30,00 por dia útil

*Assistente Virtual de RH*"""
    
    elif 'vale-alimentação' in pergunta_lower or 'va' in pergunta_lower:
        return """**Vale-Alimentação:**
- Valor: R$ 500,00/mês para compras em supermercados

*Assistente Virtual de RH*"""
    
    elif 'salário' in pergunta_lower or 'pagamento' in pergunta_lower:
        return """**Folha de Pagamento:**
- Pagamento: dia 5 de cada mês
- Adiantamento: dia 20 (até 40% do salário)
- Descontos: INSS, IRRF, vale-transporte, plano de saúde
- 13º salário: primeira parcela em Novembro, segunda em Dezembro
- Participação nos lucros: Anual, baseada em metas da empresa

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
5. Auxílio-creche: R$ 400,00/mês para filhos até 5 anos
6. Seguro de vida: Cobertura de 100 salários mínimos
7. Vale-alimentação: R$ 500,00/mês

*Assistente Virtual de RH*"""
    
    elif 'ponto' in pergunta_lower or 'jornada' in pergunta_lower:
        return """**Regime de Ponto:**
- Jornada: 9h às 18h (com 1h de almoço)
- Flexibilidade: entrada entre 8h e 10h
- Banco de horas: horas extras convertidas em folga
- Home office: até 3 dias/semana
- Horário de verão: Ajuste automático conforme decreto municipal
- Controle de ponto: Via sistema digital, com tolerância de 10 minutos

*Assistente Virtual de RH*"""
    
    elif 'equipamento' in pergunta_lower or 'computador' in pergunta_lower or 'notebook' in pergunta_lower:
        return """**Política de Uso de Equipamentos:**
- Computadores e notebooks: Uso exclusivo para trabalho, com senha obrigatória
- Internet: Acesso limitado a sites de trabalho; bloqueio de redes sociais pessoais durante expediente
- Telefones corporativos: Uso para ligações de trabalho; recargas mensais de R$ 50,00
- Veículos da empresa: Uso autorizado apenas para deslocamentos profissionais
- Manutenção: Reportar defeitos imediatamente ao TI
- Responsabilidade: Colaborador responsável por danos ou perdas

*Assistente Virtual de RH*"""
    
    elif 'viagem' in pergunta_lower or 'viagens' in pergunta_lower:
        return """**Política de Viagens:**
- Viagens a trabalho: Aprovação prévia do gestor e RH
- Diárias: R$ 200,00/dia para alimentação e hospedagem
- Transporte: Passagens aéreas ou terrestres custeadas pela empresa
- Seguro viagem: Obrigatório para viagens internacionais
- Relatório: Apresentar relatório de viagem em até 5 dias após retorno
- Cancelamento: Comunicar com antecedência mínima de 48 horas

*Assistente Virtual de RH*"""
    
    elif 'segurança' in pergunta_lower or 'informação' in pergunta_lower or 'senha' in pergunta_lower:
        return """**Política de Segurança da Informação:**
- Senhas: Mínimo 8 caracteres, alteração a cada 90 dias
- Dados sensíveis: Não compartilhar via email não criptografado
- Backup: Dados importantes devem ser salvos em nuvem corporativa
- Acesso remoto: Via VPN obrigatória
- Incidentes: Reportar imediatamente ao TI e RH
- Treinamentos: Anuais sobre cibersegurança

*Assistente Virtual de RH*"""
    
    elif 'sustentabilidade' in pergunta_lower or 'ambiente' in pergunta_lower or 'reciclagem' in pergunta_lower:
        return """**Política de Sustentabilidade:**
- Reciclagem: Separar lixo em áreas designadas
- Energia: Desligar equipamentos ao final do expediente
- Papel: Uso de papel reciclado e impressão dupla face
- Transporte: Incentivo ao uso de transporte público ou bicicleta
- Compromisso ambiental: Participação em campanhas de conscientização

*Assistente Virtual de RH*"""
    
    elif 'licença' in pergunta_lower or 'afastamento' in pergunta_lower or 'maternidade' in pergunta_lower:
        return """**Licenças e Afastamentos:**
- Licença-maternidade: 6 meses
- Licença-paternidade: 20 dias
- Atestado médico: comunicar ao RH em até 3 dias úteis
- Luto: 5 dias corridos para parentes de primeiro grau
- Casamento: 10 dias corridos
- Doença grave: Até 90 dias por ano, com atestado médico

*Assistente Virtual de RH*"""
    
    elif 'desenvolvimento' in pergunta_lower or 'educação' in pergunta_lower or 'curso' in pergunta_lower:
        return """**Desenvolvimento Profissional:**
- Auxílio educação: até R$ 500,00/mês para cursos relacionados
- Certificações: reembolso de 80% do valor após aprovação
- Palestras e eventos: participação mediante aprovação do gestor
- Programa de mentoria: Disponível para novos colaboradores
- Avaliação de desempenho: Semestral, com feedback construtivo

*Assistente Virtual de RH*"""
    
    else:
        return """Entendi sua pergunta. Baseado nas políticas da empresa, posso ajudar com:

• **Férias:** direitos, agendamento, período aquisitivo, férias coletivas, abono
• **Benefícios:** vale-refeição, vale-transporte, plano de saúde, Gympass, auxílio-creche, seguro de vida, vale-alimentação
• **Ponto:** jornada, flexibilidade, banco de horas, home office, horário de verão
• **Folha de pagamento:** datas, descontos, 13º salário, participação nos lucros
• **Licenças:** maternidade, paternidade, atestado, luto, casamento, doença
• **Desenvolvimento:** auxílio educação, certificações, mentoria, avaliação
• **Equipamentos:** uso de computadores, internet, telefones, veículos
• **Viagens:** aprovação, diárias, transporte, seguro, relatório
• **Segurança:** senhas, dados sensíveis, backup, acesso remoto
• **Sustentabilidade:** reciclagem, energia, papel, transporte

Qual desses tópicos gostaria de saber mais?

*Assistente Virtual de RH*"""

# Interface principal
def main():
    # Verificar se usuário está logado
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return
    
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
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    with col2:
        st.title("🤖 Chatbot de RH")
        st.caption(f"MVP - Assistente Virtual | Usuário: {st.session_state.user_name}")
    with col3:
        if st.button("🚪 Sair", key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_name = None
            st.session_state.historico = []
            st.rerun()
    
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
        - Equipamentos
        - Viagens
        - Segurança da informação
        - Sustentabilidade
        """)
        
        st.divider()
        
        # Funcionalidades específicas por tipo de usuário
        if st.session_state.user_type == "rh":
            st.subheader("⚙️ Painel RH")
            
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
        st.subheader("💡 Exemplos de perguntas")
        exemplos = [
            "Quantos dias de férias tenho direito?",
            "Qual o valor do vale-refeição?",
            "Como funciona o banco de horas?",
            "Quando é o pagamento do salário?",
            "Posso trabalhar de home office?",
            "Como usar equipamentos da empresa?",
            "Quais são as regras para viagens?",
            "Como manter a segurança da informação?",
            "Qual a política de sustentabilidade?"
        ]
        
        for exemplo in exemplos:
            if st.button(f"\"{exemplo}\"", key=exemplo):
                st.session_state.pergunta_exemplo = exemplo
                st.rerun()
        
        st.divider()
        
        # Botão para exportar conversa (para todos)
        if st.session_state.historico:
            pdf_data = gerar_pdf_conversa(st.session_state.historico)
            st.download_button(
                label="📄 Exportar Conversa (PDF)",
                data=pdf_data,
                file_name="conversa_rh.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="export_conversa"
            )
        
        # Botão para recarregar políticas (apenas RH)
        if st.session_state.user_type == "rh":
            if st.button("🔄 Recarregar Políticas", use_container_width=True):
                st.session_state.politicas = carregar_politicas()
                st.success("Políticas recarregadas!")
                time.sleep(1)
                st.rerun()
        
        st.divider()
        
        # Seção de feedback
        st.subheader("📝 Feedback")
        feedback = st.text_area("Deixe seu feedback sobre o chatbot:", height=100, placeholder="O que achou? Sugestões de melhoria?")
        if st.button("Enviar Feedback", use_container_width=True) and feedback:
            # Aqui poderia salvar em arquivo ou enviar para algum lugar
            st.success("Obrigado pelo feedback! Ele será analisado pela equipe de RH.")
    
    # Área do chat
    chat_container = st.container()
    
    with chat_container:
        # Exibir histórico
        for mensagem in st.session_state.historico:
            # Limpar conteúdo para evitar tags HTML não fechadas
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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mensagens", len(st.session_state.historico))
    with col2:
        perguntas_user = len([msg for msg in st.session_state.historico if msg['role'] == 'user'])
        st.metric("Perguntas", perguntas_user)
    with col3:
        respostas_bot = len([msg for msg in st.session_state.historico if msg['role'] == 'assistant'])
        st.metric("Respostas", respostas_bot)
    
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