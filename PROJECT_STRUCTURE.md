# 📁 Estrutura do Projeto - Crypto Insight AI

```
Cripto Insight/
│
├── 📄 README.md                    # Documentação principal
├── 📄 QUICKSTART.md                # Guia rápido de início
├── 📄 DEPLOYMENT.md                # Guia de deployment
├── 📄 FEATURES.md                  # Lista de funcionalidades
├── 📄 PROJECT_STRUCTURE.md         # Este arquivo
│
├── 📄 requirements.txt             # Dependências Python
├── 📄 run.py                       # Script para rodar a aplicação
├── 📄 examples.py                  # Exemplos de uso da API
├── 📄 test_api.py                  # Testes automatizados
│
├── 🐳 Dockerfile                   # Configuração Docker
├── 🐳 docker-compose.yml           # Docker Compose
├── 📄 .dockerignore                # Arquivos ignorados no Docker
├── 📄 .gitignore                   # Arquivos ignorados no Git
│
└── 📁 app/                         # Código da aplicação
    │
    ├── 📄 __init__.py              # Inicialização do módulo
    ├── 📄 main.py                  # Ponto de entrada FastAPI
    ├── 📄 config.py                # Configurações centralizadas
    │
    ├── 📁 routes/                  # Rotas da API
    │   ├── 📄 __init__.py
    │   ├── 📄 price.py             # GET /price/{symbol}
    │   └── 📄 analyze.py           # GET /analyze/{symbol}
    │
    ├── 📁 services/                # Lógica de negócio
    │   ├── 📄 __init__.py
    │   ├── 📄 crypto_service.py    # Integração com CCXT/Binance
    │   └── 📄 indicator_service.py # Cálculo de indicadores técnicos
    │
    ├── 📁 utils/                   # Utilitários
    │   ├── 📄 __init__.py
    │   ├── 📄 score_engine.py      # Engine de scoring e diagnóstico
    │   └── 📄 news_fetcher.py      # Placeholder para notícias (futuro)
    │
    └── 📁 models/                  # Modelos de dados
        ├── 📄 __init__.py
        └── 📄 schemas.py           # Schemas Pydantic
```

---

## 📊 Fluxo de Dados

```
Cliente HTTP Request
    ↓
FastAPI (main.py)
    ↓
Routes (price.py / analyze.py)
    ↓
Services (crypto_service.py)
    ↓
CCXT → Binance API
    ↓
DataFrame (pandas)
    ↓
Indicator Service (indicator_service.py)
    ↓
Indicadores Calculados (pandas-ta)
    ↓
Score Engine (score_engine.py)
    ↓
Score + Diagnóstico
    ↓
Response Schema (schemas.py)
    ↓
JSON Response → Cliente
```

---

## 🔧 Arquivos Principais

### **main.py**
- Configuração do FastAPI
- CORS Middleware
- Registro de rotas
- Health check endpoint

### **crypto_service.py**
- Integração com CCXT
- Busca de candles da Binance
- Normalização de símbolos
- Múltiplos timeframes

### **indicator_service.py**
- Cálculo de RSI
- Cálculo de EMAs (9, 21, 200)
- Cálculo de MACD
- Média Móvel de Volume

### **score_engine.py**
- Análise de RSI
- Análise de EMAs
- Análise de MACD
- Análise de Volume
- Score consolidado multi-timeframe
- Geração de diagnósticos

### **schemas.py**
- CandleData
- PriceResponse
- IndicatorData
- AnalyzeResponse
- HealthResponse

---

## 📝 Arquivos de Documentação

| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Documentação completa do projeto |
| `QUICKSTART.md` | Início rápido para começar a usar |
| `DEPLOYMENT.md` | Guias de deployment (Docker, Cloud, VPS) |
| `FEATURES.md` | Lista detalhada de funcionalidades |
| `PROJECT_STRUCTURE.md` | Visão geral da estrutura |

---

## 🧪 Arquivos de Teste e Exemplos

| Arquivo | Descrição |
|---------|-----------|
| `examples.py` | Exemplos práticos de uso da API |
| `test_api.py` | Testes automatizados com pytest |

---

## ⚙️ Arquivos de Configuração

| Arquivo | Descrição |
|---------|-----------|
| `requirements.txt` | Dependências Python |
| `config.py` | Configurações da aplicação |
| `.env.example` | Exemplo de variáveis de ambiente |
| `Dockerfile` | Container Docker |
| `docker-compose.yml` | Orquestração Docker |

---

## 🚀 Comandos Principais

### Instalação
```bash
pip install -r requirements.txt
```

### Execução
```bash
python run.py
```

### Testes
```bash
python examples.py
# ou
pytest test_api.py -v
```

### Docker
```bash
docker-compose up -d
```

---

## 📡 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Health check |
| GET | `/health` | Health check alternativo |
| GET | `/docs` | Documentação Swagger |
| GET | `/redoc` | Documentação ReDoc |
| GET | `/price/{symbol}` | Busca candles (1h, 4h, 1d) |
| GET | `/analyze/{symbol}` | Análise técnica completa |

---

## 🎯 Símbolos Suportados

- **BTC** / BTC/USDT - Bitcoin
- **ETH** / ETH/USDT - Ethereum
- **SOL** / SOL/USDT - Solana

---

**Estrutura modular e extensível pronta para produção! 🚀**

