import streamlit as st
import os
import PyPDF2
from fpdf import FPDF


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


def gerar_pdf_conversa(historico):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Historico da Conversa - EvolveRH", ln=True, align='C')
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
