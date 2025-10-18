# 🚀 Crypto Insight AI

Backend em Python usando FastAPI para análise técnica de criptomoedas com indicadores e scoring inteligente.

## 📋 Características

- ✅ API REST com FastAPI
- ✅ Análise técnica de BTC, ETH e SOL
- ✅ Múltiplos timeframes (1h, 4h, 1d)
- ✅ Indicadores técnicos: RSI, EMA, MACD, Volume MA
- ✅ Sistema de scoring e diagnóstico
- ✅ **🤖 Análises em linguagem natural com IA (Claude)**
- ✅ Dados em tempo real via CCXT (Binance)
- ✅ Frontend moderno em Next.js + TypeScript + Tailwind CSS
- ✅ Arquitetura modular e extensível

## 📦 Estrutura do Projeto

```
Cripto Insight/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── routes/
│   │   ├── analyze.py          # Rotas de análise técnica
│   │   └── price.py            # Rotas de preços
│   ├── services/
│   │   ├── crypto_service.py   # Integração com CCXT
│   │   └── indicator_service.py # Cálculo de indicadores
│   ├── utils/
│   │   ├── ai_analyzer.py      # 🤖 Geração de comentários com IA
│   │   ├── news_fetcher.py     # Placeholder para notícias
│   │   └── score_engine.py     # Engine de scoring
│   └── models/
│       └── schemas.py          # Modelos Pydantic
├── frontend/                   # 🎨 Interface Next.js
│   ├── components/
│   │   └── CryptoCard.tsx
│   ├── lib/
│   │   └── api.ts
│   ├── pages/
│   │   └── index.tsx
│   └── styles/
│       └── globals.css
├── requirements.txt
├── README.md
└── AI_ANALYZER_GUIDE.md       # 📖 Guia completo do AI Analyzer
```

## 🛠️ Instalação

### 1. Clone ou baixe o projeto

```bash
cd "Cripto Insight"
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure a API Key do Claude (Opcional)

Para análises com IA, crie um arquivo `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **Nota:** Sem a API key, o sistema usa análise baseada em regras (fallback automático)

## 🚀 Como Rodar

### Opção 1: Usando Python diretamente

```bash
python -m app.main
```

### Opção 2: Usando Uvicorn

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📡 Endpoints

### 1. Health Check
```
GET /
```
**Resposta:**
```json
{
  "status": "ok"
}
```

### 2. Buscar Preços
```
GET /price/{symbol}
```
**Exemplo:** `/price/BTC` ou `/price/ETH`

**Resposta:**
```json
{
  "symbol": "BTC/USDT",
  "timeframes": {
    "1h": [...candles...],
    "4h": [...candles...],
    "1d": [...candles...]
  }
}
```

### 3. Análise Técnica
```
GET /analyze/{symbol}
```
**Exemplo:** `/analyze/ETH`

**Resposta:**
```json
{
  "symbol": "ETH/USDT",
  "timeframes": ["1h", "4h", "1d"],
  "indicators": {
    "1h": {
      "rsi": 65.5,
      "ema9": 2150.30,
      "ema21": 2145.80,
      "ema200": 2100.50,
      "volume_ma": 15000.0,
      "macd": 12.5,
      "macd_signal": 10.2,
      "macd_histogram": 2.3
    },
    "4h": {...},
    "1d": {...}
  },
  "score": 0.72,
  "diagnostic": "Momento neutro com viés de alta leve",
  "ai_comment": "Ethereum mostra leve força compradora nas últimas horas, com RSI neutro e volume crescente. Pode haver alta leve se romper resistência nos próximos candles."
}
```

## 📊 Indicadores Técnicos

- **RSI (14)**: Índice de Força Relativa
- **EMA 9/21/200**: Médias Móveis Exponenciais
- **MACD**: Convergência/Divergência de Médias Móveis
- **Volume MA**: Média Móvel de Volume

## 🎯 Sistema de Scoring

O score vai de **0.0 a 1.0** e considera:
- RSI (peso 25%)
- EMAs (peso 35%)
- MACD (peso 25%)
- Volume (peso 15%)

### Interpretação do Score:
- **0.75 - 1.0**: Fortemente altista
- **0.65 - 0.75**: Altista
- **0.55 - 0.65**: Neutro com viés de alta
- **0.45 - 0.55**: Neutro
- **0.35 - 0.45**: Neutro com viés de baixa
- **0.25 - 0.35**: Baixista
- **0.0 - 0.25**: Fortemente baixista

## 🔧 Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI
- **CCXT**: Biblioteca para exchanges de cripto
- **Pandas**: Manipulação de dados
- **Pandas TA**: Indicadores técnicos
- **Anthropic (Claude)**: IA para análises em linguagem natural
- **Pydantic**: Validação de dados

### Frontend
- **Next.js 14**: Framework React com SSR
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização moderna
- **Axios**: Cliente HTTP
- **Lucide React**: Ícones

## 🤖 AI Analyzer

O sistema agora inclui **geração de comentários com IA** usando Claude (Anthropic):

```python
from app.utils.ai_analyzer import generate_ai_comment

comment = generate_ai_comment(
    indicators={'rsi': 65, 'ema9': 42000, ...},
    score=0.72,
    symbol="Bitcoin",
    news=None
)
# "Bitcoin mostra leve força compradora nas últimas horas, 
#  com RSI neutro e volume crescente..."
```

📖 **Veja o guia completo:** [AI_ANALYZER_GUIDE.md](AI_ANALYZER_GUIDE.md)

## 🎨 Frontend

Interface moderna desenvolvida em Next.js:

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

Acesse: **http://localhost:3000**

📖 **Documentação:** [frontend/README.md](frontend/README.md)

## 📈 Expansões Futuras

- [x] Análise com IA em linguagem natural
- [x] Frontend moderno e responsivo
- [ ] Análise de sentimento de notícias
- [ ] Suporte para mais criptomoedas
- [ ] WebSocket para dados em tempo real
- [ ] Sistema de alertas
- [ ] Machine Learning para predições
- [ ] Backtesting de estratégias

## 📝 Documentação da API

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contribuindo

Este projeto está em desenvolvimento ativo. Sugestões e melhorias são bem-vindas!

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar.

---

**Desenvolvido com ❤️ usando FastAPI e Python**

