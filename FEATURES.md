# 🎯 Funcionalidades - Crypto Insight AI

## ✅ Funcionalidades Implementadas

### 🔌 API Endpoints

- **GET /** - Health check retornando `{"status": "ok"}`
- **GET /health** - Endpoint alternativo de health check
- **GET /price/{symbol}** - Busca candles em múltiplos timeframes (1h, 4h, 1d)
- **GET /analyze/{symbol}** - Análise técnica completa com indicadores e score

### 📊 Indicadores Técnicos

Todos calculados usando `pandas-ta`:

1. **RSI (Relative Strength Index)**
   - Período: 14
   - Identifica condições de sobrecompra/sobrevenda
   - Valores: 0-100

2. **EMA (Exponential Moving Average)**
   - EMA 9: Tendência de curto prazo
   - EMA 21: Tendência de médio prazo
   - EMA 200: Tendência de longo prazo

3. **MACD (Moving Average Convergence Divergence)**
   - MACD Line (12, 26)
   - Signal Line (9)
   - Histogram (diferença entre MACD e Signal)

4. **Volume MA (Volume Moving Average)**
   - Período: 20
   - Identifica aumentos/diminuições de volume

5. **ATR (Average True Range)** 🆕
   - Período: 14
   - Mede a volatilidade do mercado
   - Quanto maior o ATR, maior a volatilidade

### 🎯 Sistema de Scoring

**Algoritmo de Scoring Multi-Fator:**

- **RSI (25% do peso)**
  - Oversold (RSI < 30): Sinal de compra
  - Overbought (RSI > 70): Sinal de venda
  - Neutro (30-70): Ponderado linearmente

- **EMAs (35% do peso)**
  - Posição do preço em relação às EMAs
  - Cruzamentos (Golden Cross / Death Cross)
  - Tendência geral

- **MACD (25% do peso)**
  - Cruzamento de linha de sinal
  - Direção do histograma

- **Volume (15% do peso)**
  - Comparação com média de volume
  - Confirmação de movimentos

**Score Final:** 0.0 a 1.0

### 📈 Análise Multi-Timeframe

O sistema analisa 3 timeframes simultaneamente:
- **1h**: Tendências de curto prazo (peso 20%)
- **4h**: Tendências de médio prazo (peso 30%)
- **1d**: Tendências de longo prazo (peso 50%)

**Score Consolidado** combina os três timeframes com pesos diferentes.

### 🔍 Diagnósticos Automáticos

O sistema fornece diagnósticos textuais baseados no score:

| Score Range | Diagnóstico |
|------------|-------------|
| 0.75 - 1.0 | Momento fortemente altista |
| 0.65 - 0.75 | Momento altista |
| 0.55 - 0.65 | Momento neutro com viés de alta leve |
| 0.45 - 0.55 | Momento neutro - Mercado lateral |
| 0.35 - 0.45 | Momento neutro com viés de baixa leve |
| 0.25 - 0.35 | Momento baixista |
| 0.0 - 0.25 | Momento fortemente baixista |

### 💱 Exchanges Suportadas

Atualmente integrado com **Binance** via CCXT:
- Acesso gratuito (não requer API key)
- Dados em tempo real
- Alta confiabilidade

**Criptomoedas Suportadas:**
- BTC (Bitcoin)
- ETH (Ethereum)
- SOL (Solana)

### 📦 Arquitetura Modular

**Separação de Responsabilidades:**

```
app/
├── routes/          # Endpoints da API
│   ├── price.py     # Rotas de preços
│   └── analyze.py   # Rotas de análise
│
├── services/        # Lógica de negócio
│   ├── crypto_service.py    # Integração CCXT
│   └── indicator_service.py # Cálculo de indicadores
│
├── utils/           # Utilitários
│   ├── score_engine.py   # Engine de scoring
│   └── news_fetcher.py   # Placeholder para notícias
│
├── models/          # Modelos de dados
│   └── schemas.py   # Schemas Pydantic
│
├── config.py        # Configurações centralizadas
└── main.py          # Ponto de entrada
```

### 🛡️ Validação de Dados

- **Pydantic Models** para validação de entrada/saída
- **Type Hints** em todo o código
- **Error Handling** robusto com mensagens claras

### 📚 Documentação Automática

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Schema**: `/openapi.json`

### 🔧 Configuração Flexível

Sistema de configuração via `config.py`:
- Períodos dos indicadores personalizáveis
- Timeframes configuráveis
- Suporte a variáveis de ambiente (.env)

---

## 🚧 Preparado para Expansões Futuras

### 📰 Análise de Sentimento de Notícias

Estrutura pronta em `utils/news_fetcher.py`:
- Integração com APIs de notícias (NewsAPI, CryptoPanic)
- Análise de sentimento (TextBlob, VADER)
- Score de sentimento integrado ao score geral

### 🤖 Machine Learning

Fácil integração de modelos ML:
- Dados já estruturados em DataFrames
- Indicadores calculados podem ser features
- Predição de preços futuros
- Classificação de tendências

### 🔔 Sistema de Alertas

Base para implementar:
- WebSocket para atualizações em tempo real
- Notificações quando score atingir limites
- Alertas de cruzamento de indicadores

### 📊 Mais Indicadores

Adicionar facilmente:
- Bollinger Bands
- Stochastic Oscillator
- Fibonacci Retracements
- Support/Resistance Levels

### 💰 Mais Criptomoedas

Simples expansão:
- Qualquer par disponível na Binance
- Configuração via lista de símbolos
- Sem mudanças no código principal

### 🔄 Backtesting

Framework preparado para:
- Testar estratégias com dados históricos
- Calcular métricas de performance
- Otimização de parâmetros

### 🌐 WebSocket

Estrutura permite adicionar:
- Stream de preços em tempo real
- Atualizações de indicadores ao vivo
- Redução de latência

---

## 🎨 Características Técnicas

### Performance

- **Async/Await**: Operações assíncronas para melhor performance
- **Rate Limiting**: Respeita limites da exchange
- **Caching**: Preparado para implementar cache (Redis)

### Segurança

- **CORS**: Configurável por ambiente
- **Type Safety**: Type hints completos
- **Input Validation**: Pydantic schemas
- **Error Handling**: Try/except apropriados

### Qualidade de Código

- **Type Hints**: 100% tipado
- **Docstrings**: Todas as funções documentadas
- **Modular**: Código organizado e reutilizável
- **Testável**: Estrutura facilita testes

### DevOps

- **Docker**: Containerização completa
- **Docker Compose**: Orquestração simples
- **Environment Variables**: Configuração flexível
- **Logging**: Sistema de logs estruturado

---

## 📊 Exemplo de Resposta Completa

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
      "macd_histogram": 2.3,
      "atr": 45.67
    },
    "4h": {
      "rsi": 58.2,
      "ema9": 2148.90,
      "ema21": 2140.50,
      "ema200": 2095.00,
      "volume_ma": 18500.0,
      "macd": 8.3,
      "macd_signal": 7.1,
      "macd_histogram": 1.2,
      "atr": 52.34
    },
    "1d": {
      "rsi": 62.1,
      "ema9": 2145.60,
      "ema21": 2135.20,
      "ema200": 2080.00,
      "volume_ma": 22000.0,
      "macd": 15.7,
      "macd_signal": 12.4,
      "macd_histogram": 3.3,
      "atr": 78.90
    }
  },
  "score": 0.72,
  "diagnostic": "Momento neutro com viés de alta leve"
}
```

---

## 🎓 Casos de Uso

1. **Trading Assistido**: Auxílio na tomada de decisões de compra/venda
2. **Análise de Mercado**: Visão geral rápida de múltiplas moedas
3. **Backtesting**: Teste de estratégias com dados históricos
4. **Bots de Trading**: Base para automação de trades
5. **Dashboards**: Backend para painéis de análise
6. **Alertas**: Sistema de notificações de oportunidades
7. **Educação**: Ferramenta para aprender análise técnica

---

**Crypto Insight AI - Análise Técnica Profissional de Criptomoedas** 🚀

