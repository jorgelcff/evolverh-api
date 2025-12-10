# 🚀 Guia de Deploy - EvolveRH

## ✅ Opção 1: Streamlit Cloud (RECOMENDADO - Grátis)

### Passo a Passo:

1. **Preparar o Repositório**
   - Certifique-se de que todo o código está no GitHub
   - Arquivo `.gitignore` deve incluir `.env` e `secrets.toml`

2. **Acessar Streamlit Cloud**
   - Vá para: https://streamlit.io/cloud
   - Faça login com sua conta GitHub

3. **Criar Novo App**
   - Clique em "New app"
   - Selecione o repositório: `jorgelcff/evolverh-api`
   - Branch: `main`
   - Arquivo principal: `app.py`

4. **Configurar Secrets**
   - No painel do app, vá em "Settings" → "Secrets"
   - Adicione:
   ```toml
   GEMINI_API_KEY = "sua_chave_api_aqui"
   ```

5. **Deploy Automático**
   - Clique em "Deploy"
   - Aguarde alguns minutos
   - Seu app estará disponível em: `https://seu-app.streamlit.app`

### Vantagens:
- ✅ Grátis para projetos públicos
- ✅ Deploy automático a cada push
- ✅ Suporte nativo a Streamlit
- ✅ SSL/HTTPS incluído
- ✅ Fácil gerenciamento de secrets

---

## 🐳 Opção 2: Docker + Render/Railway (Grátis/Pago)

### Usando Render.com (Grátis com limitações):

1. **Criar conta em** https://render.com

2. **Criar Web Service**
   - Conectar repositório GitHub
   - Runtime: Docker
   - Usar o `Dockerfile` já criado

3. **Configurar Variáveis de Ambiente**
   - Adicionar `GEMINI_API_KEY`

4. **Deploy**
   - Render fará build e deploy automaticamente

---

## ☁️ Opção 3: Google Cloud Run (Requer cartão)

### Passo a Passo:

1. **Instalar Google Cloud SDK**
   ```bash
   # Baixe em: https://cloud.google.com/sdk/docs/install
   ```

2. **Fazer login**
   ```bash
   gcloud auth login
   gcloud config set project SEU_PROJECT_ID
   ```

3. **Build e Deploy**
   ```bash
   gcloud run deploy evolverh-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Configurar Secret**
   ```bash
   echo "SUA_CHAVE_API" | gcloud secrets create GEMINI_API_KEY --data-file=-
   ```

---

## 🔧 Opção 4: Vercel (NÃO RECOMENDADO para Streamlit)

**⚠️ ATENÇÃO:** Vercel não suporta Streamlit nativamente. Você precisaria:

1. Converter para FastAPI/Flask
2. Criar frontend separado em React/Next.js
3. Muito trabalho de reescrita

**Não vale a pena** para este projeto!

---

## 📋 Checklist Pré-Deploy

- [ ] `.env` está no `.gitignore`
- [ ] `requirements.txt` está atualizado
- [ ] Código está no GitHub
- [ ] API Key do Gemini está válida
- [ ] Arquivo `politicas.txt` existe
- [ ] Estrutura de pastas `src/modules/` está correta

---

## 🆘 Troubleshooting

### Erro: "Module not found"
- Verificar se todos os imports estão no `requirements.txt`
- Verificar estrutura de pastas

### Erro: "API Key invalid"
- Configurar secrets corretamente na plataforma
- Verificar se a chave não foi revogada

### App não inicia
- Verificar logs da plataforma
- Testar localmente primeiro: `streamlit run app.py`

---

## 📞 Suporte

- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Render: https://render.com/docs
- Railway: https://docs.railway.app
