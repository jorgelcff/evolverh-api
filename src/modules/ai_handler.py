import google.generativeai as genai


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
    6. Mantenha a resposta em português brasileiro e não use nenhum emoji na resposta, de forma alguma.
    
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


def testar_api_gemini(api_key):
    """Testa a conexão com a API Gemini"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content("Teste de conexão")
        print(f"✅ API Gemini funcionando: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Erro na API Gemini: {e}")
        return False
