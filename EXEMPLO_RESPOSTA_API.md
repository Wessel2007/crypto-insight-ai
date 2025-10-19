# 📡 Exemplo de Resposta da API - Trade Rápido

## 🔍 Endpoint Consultado

```
GET http://localhost:8000/analyze/BTC
```

---

## ✅ Cenário 1: Alta Probabilidade (80%)

**Condições:**
- RSI: 54 (entre 40-60, virando pra cima) ✅
- EMA9 > EMA21 ✅
- Volume acima da média ✅
- MACD histograma positivo ✅
- ADX > 25 ✅

**Pontos:** 5/5 = **100%**

### Resposta JSON:

```json
{
  "symbol": "BTCUSDT",
  "timeframes": ["1h", "4h", "1d"],
  
  "score": 0.72,
  "diagnostic": "Momento altista - Tendência de alta moderada",
  
  "ai_comment": "Bitcoin apresenta sinais técnicos favoráveis com RSI em zona neutra e médias móveis alinhadas positivamente. Volume crescente confirma movimento.",
  
  "trade_opportunity": {
    "probability": 1.0,
    "comment": "Alta chance de movimento positivo nas próximas horas."
  },
  
  "indicators": {
    "1h": {
      "trend": {
        "EMA9": 67234.56,
        "EMA21": 66890.12,
        "EMA50": 66234.45,
        "EMA200": 64123.78,
        "SMA100": 65456.89
      },
      "momentum": {
        "RSI": 54.32,
        "Stochastic_RSI_K": 62.45,
        "Stochastic_RSI_D": 58.23,
        "MACD": 234.56,
        "MACD_Signal": 198.34,
        "MACD_Histogram": 36.22
      },
      "volatility": {
        "ATR": 456.78,
        "BB_Upper": 68234.56,
        "BB_Middle": 67123.45,
        "BB_Lower": 66012.34
      },
      "volume": {
        "Volume_MA": 1234567890.0,
        "MFI": 58.34,
        "OBV": 9876543210.0
      },
      "strength": {
        "ADX": 28.56
      },
      "price": {
        "last_close": 67245.89,
        "current_volume": 1534567890.0
      }
    },
    "4h": { ... },
    "1d": { ... }
  },
  
  "chart_data": {
    "symbol": "BTCUSDT",
    "timeframe": "4h",
    "candles": [ ... ]
  }
}
```

### 💡 Interpretação:

🟢 **SINAL FORTE DE ENTRADA**
- Probabilidade: 100%
- Score geral: 0.72 (altista)
- Todos os 5 critérios atendidos

**Sugestão:**
- Tipo: Day Trade
- Entrada: ~$67,245
- Alvo: +2-4% (~$68,590 - $69,935)
- Stop: -1.5% (~$66,237)

---

## ⚠️ Cenário 2: Probabilidade Moderada (60%)

**Condições:**
- RSI: 48 (entre 40-60, mas não virando pra cima) ❌
- EMA9 > EMA21 ✅
- Volume acima da média ✅
- MACD histograma positivo ✅
- ADX > 25 ❌

**Pontos:** 3/5 = **60%**

### Resposta JSON:

```json
{
  "symbol": "ETHUSDT",
  "timeframes": ["1h", "4h", "1d"],
  
  "score": 0.58,
  "diagnostic": "Momento neutro com viés de alta leve",
  
  "ai_comment": "Ethereum mostra sinais mistos. Indicadores de momentum em zona neutra, aguarde confirmação para entrada.",
  
  "trade_opportunity": {
    "probability": 0.6,
    "comment": "Possível oportunidade de curto prazo, aguarde confirmação."
  },
  
  "indicators": {
    "1h": {
      "trend": {
        "EMA9": 3567.89,
        "EMA21": 3534.56,
        "EMA50": 3512.34,
        "EMA200": 3423.12,
        "SMA100": 3478.90
      },
      "momentum": {
        "RSI": 48.23,
        "Stochastic_RSI_K": 45.67,
        "Stochastic_RSI_D": 48.92,
        "MACD": 12.34,
        "MACD_Signal": 8.56,
        "MACD_Histogram": 3.78
      },
      "volatility": {
        "ATR": 34.56,
        "BB_Upper": 3612.45,
        "BB_Middle": 3567.89,
        "BB_Lower": 3523.33
      },
      "volume": {
        "Volume_MA": 567890123.0,
        "MFI": 52.34,
        "OBV": 1234567890.0
      },
      "strength": {
        "ADX": 22.45
      },
      "price": {
        "last_close": 3569.12,
        "current_volume": 634567890.0
      }
    }
  }
}
```

### 💡 Interpretação:

🟡 **SINAL MODERADO - AGUARDE CONFIRMAÇÃO**
- Probabilidade: 60%
- Score geral: 0.58 (neutro com viés de alta)
- 3 de 5 critérios atendidos

**Sugestão:**
- Aguarde RSI subir acima de 50
- Ou aguarde ADX passar de 25
- Monitore próximas 1-2 horas

---

## ❌ Cenário 3: Baixa Probabilidade (20%)

**Condições:**
- RSI: 35 (abaixo de 40) ❌
- EMA9 < EMA21 ❌
- Volume acima da média ✅
- MACD histograma negativo ❌
- ADX < 25 ❌

**Pontos:** 1/5 = **20%**

### Resposta JSON:

```json
{
  "symbol": "SOLUSDT",
  "timeframes": ["1h", "4h", "1d"],
  
  "score": 0.35,
  "diagnostic": "Momento neutro com viés de baixa leve",
  
  "ai_comment": "Solana apresenta sinais técnicos desfavoráveis. RSI em zona de sobrevenda e médias móveis indicando cautela.",
  
  "trade_opportunity": {
    "probability": 0.2,
    "comment": "Sem sinal claro de trade rápido agora."
  },
  
  "indicators": {
    "1h": {
      "trend": {
        "EMA9": 142.34,
        "EMA21": 145.67,
        "EMA50": 147.89,
        "EMA200": 152.34,
        "SMA100": 149.12
      },
      "momentum": {
        "RSI": 35.67,
        "Stochastic_RSI_K": 28.34,
        "Stochastic_RSI_D": 32.56,
        "MACD": -1.23,
        "MACD_Signal": 0.56,
        "MACD_Histogram": -1.79
      },
      "volatility": {
        "ATR": 2.34,
        "BB_Upper": 146.78,
        "BB_Middle": 143.45,
        "BB_Lower": 140.12
      },
      "volume": {
        "Volume_MA": 234567890.0,
        "MFI": 38.45,
        "OBV": 567890123.0
      },
      "strength": {
        "ADX": 18.23
      },
      "price": {
        "last_close": 142.56,
        "current_volume": 267890123.0
      }
    }
  }
}
```

### 💡 Interpretação:

🔴 **SEM SINAL DE ENTRADA**
- Probabilidade: 20%
- Score geral: 0.35 (neutro com viés de baixa)
- Apenas 1 de 5 critérios atendido

**Sugestão:**
- **NÃO ENTRAR** em posição comprada
- Mercado pode estar lateral ou em baixa
- Aguarde melhora nos indicadores
- Considere revisitar em 2-4 horas

---

## 📊 Comparação dos Cenários

| Moeda | Probabilidade | Score | Decisão | Critérios Atendidos |
|-------|--------------|-------|---------|---------------------|
| BTC | 100% | 0.72 | 🟢 ENTRAR | 5/5 |
| ETH | 60% | 0.58 | 🟡 AGUARDAR | 3/5 |
| SOL | 20% | 0.35 | 🔴 NÃO ENTRAR | 1/5 |

---

## 🎯 Regras de Decisão

### Para Scalping (operações de minutos)
```python
if probability >= 0.8 and score >= 0.7:
    ação = "ENTRAR (alvo: +0.5-1%)"
```

### Para Day Trade (operações de horas)
```python
if probability >= 0.7 and score >= 0.6:
    ação = "ENTRAR (alvo: +2-4%)"
elif probability >= 0.6 and score >= 0.7:
    ação = "ENTRAR COM CAUTELA (alvo: +1.5-3%)"
```

### Para Swing Trade (operações de dias)
```python
if probability >= 0.6 and score >= 0.65:
    ação = "CONSIDERAR (combine com análise de timeframes maiores)"
```

---

## 💻 Como Obter Essa Resposta

### Python:
```python
import requests

response = requests.get("http://localhost:8000/analyze/BTC")
data = response.json()

# Acessa campos
print(f"Probabilidade: {data['trade_opportunity']['probability']:.0%}")
print(f"Comentário: {data['trade_opportunity']['comment']}")
print(f"Score Geral: {data['score']}")
```

### cURL (PowerShell):
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/analyze/BTC" -UseBasicParsing
$data = $response.Content | ConvertFrom-Json
$data.trade_opportunity
```

### Navegador:
```
http://localhost:8000/analyze/BTC
```

---

## 📝 Campos Retornados

### trade_opportunity (NOVO)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `probability` | float | Probabilidade de 0.0 a 1.0 (0% a 100%) |
| `comment` | string | Comentário descritivo sobre a oportunidade |

### Outros campos (existentes)

- `symbol`: Símbolo normalizado (ex: "BTCUSDT")
- `score`: Score geral de 0.0 a 1.0
- `diagnostic`: Diagnóstico textual do momento
- `ai_comment`: Comentário gerado por IA
- `indicators`: Indicadores de todos os timeframes
- `chart_data`: Dados para gráfico candlestick
- `timeframes`: Lista de timeframes analisados

---

**Gerado em:** Outubro 2024  
**Versão da API:** 1.0

