# 🚀 Referência Rápida - Função `get_indicators()`

## 📦 Uso Básico

```python
from app.services.indicator_service import IndicatorService

# Seu DataFrame OHLCV
indicators = IndicatorService.get_indicators(df)
```

## 📊 Retorno da Função

```python
{
    # Osciladores
    'rsi': 65.50,                    # RSI(14): 0-100
    
    # Médias Móveis
    'ema9': 45123.45,                # EMA curto prazo
    'ema21': 44987.23,               # EMA médio prazo
    'ema200': 43500.12,              # EMA longo prazo (None se < 200 candles)
    
    # MACD
    'macd': 125.4567,                # MACD line
    'macd_signal': 118.2345,         # Signal line
    'macd_histogram': 7.2222,        # Histogram (diferença)
    
    # Volume
    'volume_ma': 1234567.89,         # Média de volume (20 períodos)
    
    # Volatilidade
    'atr': 234.56,                   # 🆕 Average True Range (14)
    
    # Extras
    'last_close': 45234.67,          # Último fechamento
    'current_volume': 2345678.90     # Volume atual
}
```

## 🎯 Interpretação dos Indicadores

### RSI (Relative Strength Index)
```
0-30   = 📉 Oversold (sobrevendido) - possível compra
30-70  = ➡️  Neutro
70-100 = 📈 Overbought (sobrecomprado) - possível venda
```

### EMAs (Médias Móveis Exponenciais)
```
Preço > EMA9 > EMA21 > EMA200  = 📈 Tendência altista forte
Preço < EMA9 < EMA21 < EMA200  = 📉 Tendência baixista forte
EMA9 cruzando EMA21 para cima  = 🟢 Golden Cross (sinal de compra)
EMA9 cruzando EMA21 para baixo = 🔴 Death Cross (sinal de venda)
```

### MACD
```
MACD > Signal                  = 📈 Sinal altista
MACD < Signal                  = 📉 Sinal baixista
Histogram > 0 e crescendo      = 💪 Força altista aumentando
Histogram < 0 e decrescendo    = 💪 Força baixista aumentando
```

### Volume MA
```
Volume atual > Volume MA       = ✅ Movimento com confirmação
Volume atual < Volume MA       = ⚠️  Movimento sem confirmação
```

### ATR (Average True Range) 🆕
```
ATR Alto                       = 🌊 Alta volatilidade (movimentos grandes)
ATR Baixo                      = 😴 Baixa volatilidade (mercado calmo)
ATR Crescente                  = 📈 Volatilidade aumentando
ATR Decrescente                = 📉 Volatilidade diminuindo
```

## 💡 Exemplos de Uso

### 1. Identificar Tendência
```python
ind = IndicatorService.get_indicators(df)

if ind['rsi'] > 70 and ind['ema9'] > ind['ema21']:
    print("🔴 Sobrecomprado em tendência de alta - cuidado!")
elif ind['rsi'] < 30 and ind['ema9'] < ind['ema21']:
    print("🟢 Sobrevendido em tendência de baixa - oportunidade?")
```

### 2. Detectar Cruzamentos MACD
```python
ind_current = IndicatorService.get_indicators(df)
ind_previous = IndicatorService.get_indicators(df.iloc[:-1])

if (ind_current['macd'] > ind_current['macd_signal'] and 
    ind_previous['macd'] <= ind_previous['macd_signal']):
    print("🟢 Golden Cross no MACD!")
```

### 3. Confirmar com Volume
```python
ind = IndicatorService.get_indicators(df)

if ind['current_volume'] > ind['volume_ma'] * 1.5:
    print("✅ Alto volume - movimento significativo!")
```

### 4. Usar ATR para Stop Loss
```python
ind = IndicatorService.get_indicators(df)
entry_price = ind['last_close']
atr = ind['atr']

# Stop loss a 2x ATR
stop_loss = entry_price - (2 * atr)
take_profit = entry_price + (3 * atr)

print(f"Entrada: ${entry_price:.2f}")
print(f"Stop Loss: ${stop_loss:.2f} (-{2*atr:.2f})")
print(f"Take Profit: ${take_profit:.2f} (+{3*atr:.2f})")
print(f"Risk/Reward: 1:{3/2}")
```

### 5. Avaliar Volatilidade
```python
ind_1h = IndicatorService.get_indicators(df_1h)
ind_1d = IndicatorService.get_indicators(df_1d)

atr_ratio = ind_1h['atr'] / ind_1d['atr']

if atr_ratio > 0.5:
    print("⚠️  Alta volatilidade intraday!")
elif atr_ratio < 0.2:
    print("😴 Mercado muito calmo no curto prazo")
```

## 🧪 Teste Rápido

```bash
# 1. Iniciar servidor
python run.py

# 2. Testar indicadores
python test_indicators.py

# 3. Ou via API
curl http://localhost:8000/analyze/BTC | jq .indicators
```

## 📐 Fórmulas

### RSI
```
RSI = 100 - (100 / (1 + RS))
onde RS = Média de ganhos / Média de perdas (14 períodos)
```

### EMA
```
EMA = (Preço atual × K) + (EMA anterior × (1 - K))
onde K = 2 / (N + 1)
```

### MACD
```
MACD = EMA(12) - EMA(26)
Signal = EMA(9) do MACD
Histogram = MACD - Signal
```

### ATR
```
TR = max[(H - L), abs(H - Cp), abs(L - Cp)]
ATR = média móvel de TR (14 períodos)
onde: H = High, L = Low, Cp = Close anterior
```

## ⚙️ Configuração

Todos os períodos podem ser ajustados em `app/config.py`:

```python
rsi_period: int = 14
ema_fast: int = 9
ema_medium: int = 21
ema_slow: int = 200
volume_ma_period: int = 20
macd_fast: int = 12
macd_slow: int = 26
macd_signal: int = 9
atr_period: int = 14  # 🆕
```

## 🎯 Casos de Uso Reais

### Trading de Curto Prazo
```python
# Usar timeframe 1h
indicators = IndicatorService.get_indicators(df_1h)

# Foco em: RSI, MACD, ATR
# ATR para stop loss dinâmico
```

### Trading de Médio Prazo
```python
# Usar timeframe 4h
indicators = IndicatorService.get_indicators(df_4h)

# Foco em: EMA9/21, MACD, Volume
```

### Investimento de Longo Prazo
```python
# Usar timeframe 1d
indicators = IndicatorService.get_indicators(df_1d)

# Foco em: EMA200, RSI semanal
```

## 📝 Checklist de Análise

Antes de tomar uma decisão:

- [ ] RSI está em zona razoável? (não extremo)
- [ ] Preço está acima/abaixo das EMAs chave?
- [ ] MACD confirma a direção?
- [ ] Volume confirma o movimento?
- [ ] ATR indica volatilidade aceitável?
- [ ] Múltiplos timeframes concordam?

## 🔗 Links Úteis

- **Documentação Completa:** `README.md`
- **Lista de Funcionalidades:** `FEATURES.md`
- **Histórico de Mudanças:** `CHANGELOG.md`
- **Resumo de Implementação:** `IMPLEMENTATION_SUMMARY.md`
- **API Docs:** http://localhost:8000/docs

---

**📚 Esta é uma referência rápida. Para detalhes completos, consulte a documentação!**

