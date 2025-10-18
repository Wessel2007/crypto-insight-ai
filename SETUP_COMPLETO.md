# 🚀 Setup Completo - Crypto Insight AI

Guia completo para configurar todo o projeto (Backend + Frontend + IA).

---

## 📦 Parte 1: Backend (FastAPI)

### 1.1 Instalação Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 1.2 Configurar API Key do Claude (Opcional)

Crie arquivo `.env` na raiz:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Obtenha sua chave em: https://console.anthropic.com/

### 1.3 Rodar Backend

```bash
# Opção 1
python -m app.main

# Opção 2
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend rodando em:** http://localhost:8000  
✅ **Docs:** http://localhost:8000/docs

---

## 🎨 Parte 2: Frontend (Next.js)

### 2.1 Instalação Node.js

```bash
cd frontend

# Instalar dependências
npm install
# ou
yarn install
```

### 2.2 Configurar URL da API

Crie arquivo `.env.local` dentro de `frontend/`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2.3 Rodar Frontend

```bash
npm run dev
# ou
yarn dev
```

✅ **Frontend rodando em:** http://localhost:3000

---

## 🤖 Parte 3: Testar AI Analyzer

### 3.1 Teste Rápido

```bash
# No diretório raiz
python example_ai_analyzer.py
```

### 3.2 Testes Completos

```bash
python test_ai_analyzer.py
```

### 3.3 Teste via API

```bash
# Iniciar backend
uvicorn app.main:app --reload

# Em outro terminal
curl http://localhost:8000/analyze/BTC
```

Verifique o campo `ai_comment` na resposta JSON!

---

## ✅ Checklist Final

- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ instalado
- [ ] Ambiente virtual Python ativado
- [ ] Dependências Python instaladas (`pip install -r requirements.txt`)
- [ ] Dependências Node instaladas (`npm install` no frontend)
- [ ] Arquivo `.env` criado com `ANTHROPIC_API_KEY` (opcional)
- [ ] Arquivo `frontend/.env.local` criado com `NEXT_PUBLIC_API_URL`
- [ ] Backend rodando em http://localhost:8000
- [ ] Frontend rodando em http://localhost:3000
- [ ] Testes executados com sucesso

---

## 🎯 Testar Tudo Funcionando

### 1. Testar Backend

```bash
curl http://localhost:8000/
# Deve retornar: {"status":"ok"}

curl http://localhost:8000/analyze/BTC
# Deve retornar análise completa do Bitcoin
```

### 2. Testar Frontend

1. Abra http://localhost:3000
2. Clique em "Analisar agora" no card do Bitcoin
3. Deve aparecer:
   - Score de confiança
   - Análise IA (com 🤖)
   - Diagnóstico técnico
   - Indicadores

### 3. Testar IA

**Com API Key:**
- Comentário deve ser natural e contextualizado
- Aparece com ícone 🤖 no frontend

**Sem API Key:**
- Comentário é baseado em regras
- Ainda funciona normalmente!

---

## 🔧 Troubleshooting

### Backend não inicia

```bash
# Verificar se porta 8000 está livre
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Trocar porta
uvicorn app.main:app --reload --port 8001
```

### Frontend não conecta com backend

1. Verificar se backend está rodando
2. Verificar URL no `.env.local`
3. Verificar CORS no backend (já configurado)

### IA não funciona

1. Verificar API key no `.env`
2. Verificar saldo na conta Anthropic
3. Sistema usa fallback automaticamente se não funcionar

### Erro de dependências

```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Estrutura de Diretórios

```
Crypto Insight/
├── app/                      # Backend Python
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── utils/
│   │   └── ai_analyzer.py   # ⭐ Novo!
│   └── models/
├── frontend/                 # Frontend Next.js
│   ├── components/
│   │   └── CryptoCard.tsx   # ⭐ Atualizado!
│   ├── lib/
│   │   └── api.ts
│   ├── pages/
│   │   └── index.tsx
│   └── styles/
├── .env                      # Config backend (criar)
├── requirements.txt
├── test_ai_analyzer.py       # ⭐ Novo!
├── example_ai_analyzer.py    # ⭐ Novo!
└── AI_ANALYZER_GUIDE.md      # ⭐ Novo!
```

---

## 🎓 Próximos Passos

Após configurar tudo:

1. 📖 Leia [AI_ANALYZER_GUIDE.md](AI_ANALYZER_GUIDE.md)
2. 🧪 Execute os testes (`python test_ai_analyzer.py`)
3. 💻 Explore a API em http://localhost:8000/docs
4. 🎨 Customize o frontend em `frontend/`
5. 🚀 Deploy (veja [DEPLOYMENT.md](DEPLOYMENT.md))

---

## 💰 Custos

### Grátis
- Backend (FastAPI)
- Frontend (Next.js)
- Dados de mercado (CCXT + Binance)

### Pago (Opcional)
- **Anthropic API:** ~$0.0075/análise
  - Primeiro uso: créditos grátis
  - Fallback automático se não configurar

---

## 🆘 Suporte

- **Documentação:** http://localhost:8000/docs
- **Logs Backend:** Terminal do uvicorn
- **Logs Frontend:** Console do navegador (F12)
- **Issues:** GitHub (se aplicável)

---

## 🎉 Conclusão

Parabéns! Você agora tem:

✅ Backend com análise técnica avançada  
✅ IA gerando comentários naturais  
✅ Frontend moderno e responsivo  
✅ Sistema completo de análise de criptos  

**Divirta-se analisando criptomoedas! 🚀**

