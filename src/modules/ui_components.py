import streamlit as st
import time
from src.modules.config import CREDENCIAIS


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
