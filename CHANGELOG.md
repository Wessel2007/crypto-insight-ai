# 📝 Changelog - Crypto Insight AI

## [1.1.0] - 2025-10-18

### ✨ Novas Funcionalidades

#### **Nova Função: `get_indicators(df)`**

Implementada função principal para cálculo de indicadores técnicos com formato otimizado para API.

**Localização:** `app/services/indicator_service.py`

**Características:**
- Recebe um DataFrame OHLCV (colunas: timestamp, open, high, low, close, volume)
- Retorna dicionário formatado e pronto para JSON
- Valores arredondados adequadamente
- Tratamento robusto de valores NaN
- Validação de dados insuficientes

**Indicadores Calculados:**

1. **RSI (14)** - Relative Strength Index
   - Formato: 2 casas decimais
   - Range: 0-100

2. **EMA 9, 21, 200** - Exponential Moving Averages
   - Formato: 2 casas decimais
   - Detecta tendências de curto, médio e longo prazo

3. **MACD (12, 26, 9)** - Moving Average Convergence Divergence
   - MACD Line
   - MACD Signal Line
   - MACD Histogram
   - Formato: 4 casas decimais (alta precisão)

4. **Volume MA (20)** - Volume Moving Average
   - Formato: 2 casas decimais
   - Média dos últimos 20 candles

5. **ATR (14)** 🆕 - Average True Range
   - Formato: 2 casas decimais
   - Mede volatilidade do mercado
   - **NOVO INDICADOR!**

**Dados Adicionais:**
- `last_close`: Último preço de fechamento
- `current_volume`: Volume atual

### 🔧 Melhorias Técnicas

#### **Função `safe_float()`**
- Conversão segura para float
- Tratamento de valores NaN
- Arredondamento configurável
- Previne erros em dados faltantes

#### **Validação de Dados**
- Verifica se há dados suficientes (mínimo 14 candles)
- Retorna None para indicadores sem dados
- EMA200 só calculada se houver 200+ candles

### 📊 Schema Atualizado

**Arquivo:** `app/models/schemas.py`

Adicionado campo `atr` ao `IndicatorData`:
```python
class IndicatorData(BaseModel):
    rsi: Optional[float] = None
    ema9: Optional[float] = None
    ema21: Optional[float] = None
    ema200: Optional[float] = None
    volume_ma: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    atr: Optional[float] = None  # 🆕 NOVO
```

### 🛣️ Rotas Atualizadas

**Arquivo:** `app/routes/analyze.py`

- Atualizada para usar a nova função `get_indicators(df)`
- Simplificação do código
- Melhor estruturação dos dados
- Suporte ao novo campo ATR

### 📚 Documentação Atualizada

- ✅ FEATURES.md - Adicionado ATR aos indicadores
- ✅ Exemplos de resposta JSON atualizados
- ✅ Novo script de teste: `test_indicators.py`

### 🧪 Novos Testes

**Arquivo:** `test_indicators.py`

Script completo para testar a função `get_indicators`:
- Teste de indicadores individuais
- Teste com múltiplas criptomoedas
- Exibição formatada dos resultados
- Informações sobre cada indicador

### 📈 Exemplo de Uso

```python
from app.services.indicator_service import IndicatorService
import pandas as pd

# Seu DataFrame OHLCV
df = crypto_service.get_candles('BTC/USDT', '1h', 200)

# Calcula todos os indicadores
indicators = IndicatorService.get_indicators(df)

# Resultado formatado e pronto para API
print(indicators)
# {
#     'rsi': 65.50,
#     'ema9': 45123.45,
#     'ema21': 44987.23,
#     'ema200': 43500.12,
#     'macd': 125.4567,
#     'macd_signal': 118.2345,
#     'macd_histogram': 7.2222,
#     'volume_ma': 1234567.89,
#     'atr': 234.56,  # 🆕
#     'last_close': 45234.67,
#     'current_volume': 2345678.90
# }
```

### 🎯 Resposta da API Atualizada

**Endpoint:** `GET /analyze/{symbol}`

```json
{
  "symbol": "BTC/USDT",
  "timeframes": ["1h", "4h", "1d"],
  "indicators": {
    "1h": {
      "rsi": 65.50,
      "ema9": 45123.45,
      "ema21": 44987.23,
      "ema200": 43500.12,
      "volume_ma": 1234567.89,
      "macd": 125.4567,
      "macd_signal": 118.2345,
      "macd_histogram": 7.2222,
      "atr": 234.56
    },
    "4h": { ... },
    "1d": { ... }
  },
  "score": 0.72,
  "diagnostic": "Momento neutro com viés de alta leve"
}
```

### 🔍 Detalhes do ATR

**O que é ATR?**
- Average True Range
- Indicador de volatilidade desenvolvido por J. Welles Wilder
- Não indica direção, apenas intensidade dos movimentos

**Como interpretar:**
- **ATR Alto:** Mercado volátil, grandes movimentos de preço
- **ATR Baixo:** Mercado calmo, pequenos movimentos de preço
- **ATR Crescente:** Volatilidade aumentando
- **ATR Decrescente:** Volatilidade diminuindo

**Usos práticos:**
- Definir Stop Loss (ex: 2x ATR)
- Avaliar risco da posição
- Identificar breakouts
- Ajustar tamanho de posição

### 🚀 Performance

- ✅ Cálculos otimizados com pandas-ta
- ✅ Tratamento eficiente de NaN
- ✅ Arredondamento no momento certo
- ✅ Sem cálculos redundantes

### 🐛 Correções

- Melhor tratamento de valores None
- Validação robusta de dados insuficientes
- Nomenclatura consistente de colunas MACD

---

## [1.0.0] - 2025-10-18

### 🎉 Lançamento Inicial

- ✅ FastAPI + Uvicorn
- ✅ Integração com CCXT/Binance
- ✅ Endpoints /price e /analyze
- ✅ Indicadores: RSI, EMA, MACD, Volume MA
- ✅ Sistema de scoring multi-timeframe
- ✅ Documentação completa
- ✅ Suporte para BTC, ETH, SOL
- ✅ Docker e Docker Compose
- ✅ Testes automatizados

---

**Próximas Versões Planejadas:**

- [ ] v1.2.0: Análise de sentimento de notícias
- [ ] v1.3.0: Mais indicadores (Bollinger Bands, Stochastic)
- [ ] v1.4.0: WebSocket para dados em tempo real
- [ ] v1.5.0: Sistema de alertas
- [ ] v2.0.0: Machine Learning para predições

