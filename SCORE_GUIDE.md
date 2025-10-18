# 📊 Guia da Função `calculate_score()`

## 🎯 Visão Geral

A função `calculate_score()` analisa indicadores técnicos e retorna um score numérico com diagnóstico textual para auxiliar na tomada de decisões de trading.

---

## 📦 Uso Básico

```python
from app.services.indicator_service import IndicatorService
from app.utils.score_engine import ScoreEngine

# 1. Calcular indicadores
indicators = IndicatorService.get_indicators(df)

# 2. Calcular score
result = ScoreEngine.calculate_score(indicators)

# 3. Usar resultado
print(f"Score: {result['normalized_score']}")
print(f"Diagnóstico: {result['diagnostic']}")
```

---

## 📊 Formato de Retorno

```python
{
    'raw_score': 3,                    # Score bruto (-5 a +5)
    'normalized_score': 0.60,          # Score normalizado (-1 a +1)
    'diagnostic': "🟢 Bom momento de compra - Sinais técnicos favoráveis",
    'signals': [                       # Lista de sinais detectados
        "✅ RSI em zona de sobrevenda (oportunidade)",
        "✅ EMA9 acima EMA21 (tendência de alta)",
        "✅ MACD Histogram positivo (momentum favorável)"
    ],
    'score_breakdown': {               # Quais indicadores foram analisados
        'rsi': 'analyzed',
        'ema_trend': 'analyzed',
        'ema_long_term': 'analyzed',
        'macd': 'analyzed',
        'volume': 'analyzed',
        'volatility': 'analyzed'
    }
}
```

---

## 📐 Regras de Pontuação

### Sistema de Pontos (-5 a +5)

| Condição | Pontos | Significado |
|----------|--------|-------------|
| **RSI < 30** | +1 | 🟢 Zona de sobrevenda (oportunidade de compra) |
| **RSI > 70** | -1 | 🔴 Zona de sobrecompra (momento de cautela) |
| **EMA9 > EMA21** | +1 | 🟢 Tendência de alta de curto prazo |
| **EMA9 < EMA21** | -1 | 🔴 Tendência de baixa de curto prazo |
| **EMA21 > EMA200** | +1 | 🟢 Tendência de alta de longo prazo |
| **MACD Histogram > 0** | +1 | 🟢 Momentum positivo |
| **Volume > Volume MA** | +1 | 🟢 Movimento com confirmação |
| **ATR > 20% do preço** | -1 | 🔴 Alta volatilidade (alto risco) |

**Score Máximo:** +5 (todos os sinais positivos)  
**Score Mínimo:** -5 (todos os sinais negativos)

---

## 🎯 Interpretação do Score Normalizado

### Escala: -1.0 a +1.0

| Score | Diagnóstico | Ação Sugerida |
|-------|-------------|---------------|
| **≥ 0.60** | 🟢 Bom momento de compra | Considere COMPRAR |
| **0.20 a 0.59** | 🟡 Neutro de alta | Aguarde confirmação |
| **-0.20 a 0.19** | ⚪ Neutro | Mercado indefinido |
| **-0.60 a -0.21** | 🟠 Leve tendência de baixa | Evite comprar |
| **≤ -0.60** | 🔴 Evite compra agora | NÃO compre |

---

## 💡 Exemplos de Uso

### Exemplo 1: Análise Básica

```python
# Buscar dados
df = crypto_service.get_candles('BTC/USDT', '1d', 200)

# Calcular indicadores
indicators = IndicatorService.get_indicators(df)

# Calcular score
result = ScoreEngine.calculate_score(indicators)

# Decisão
if result['normalized_score'] >= 0.6:
    print("✅ Momento favorável para compra!")
    for signal in result['signals']:
        print(f"  {signal}")
else:
    print("⚠️ Aguardar momento mais favorável")
```

### Exemplo 2: Múltiplos Timeframes

```python
timeframes = ['1h', '4h', '1d']
scores = {}

for tf in timeframes:
    df = crypto_service.get_candles('ETH/USDT', tf, 200)
    indicators = IndicatorService.get_indicators(df)
    result = ScoreEngine.calculate_score(indicators)
    scores[tf] = result['normalized_score']

# Decisão baseada em múltiplos timeframes
if all(score > 0.2 for score in scores.values()):
    print("✅ Tendência positiva em todos os timeframes!")
```

### Exemplo 3: Comparar Múltiplas Moedas

```python
symbols = ['BTC', 'ETH', 'SOL']
results = {}

for symbol in symbols:
    df = crypto_service.get_candles(f'{symbol}/USDT', '1d', 200)
    indicators = IndicatorService.get_indicators(df)
    result = ScoreEngine.calculate_score(indicators)
    results[symbol] = result

# Encontrar melhor oportunidade
best = max(results.items(), key=lambda x: x[1]['normalized_score'])
print(f"Melhor oportunidade: {best[0]}")
print(f"Score: {best[1]['normalized_score']:.2f}")
print(f"Diagnóstico: {best[1]['diagnostic']}")
```

### Exemplo 4: Alertas Automáticos

```python
def check_trading_opportunities():
    symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']
    
    for symbol in symbols:
        df = crypto_service.get_candles(f'{symbol}/USDT', '1d', 200)
        indicators = IndicatorService.get_indicators(df)
        result = ScoreEngine.calculate_score(indicators)
        
        # Alerta para boas oportunidades
        if result['normalized_score'] >= 0.6:
            print(f"🚨 ALERTA: {symbol} - {result['diagnostic']}")
            print(f"   Score: {result['normalized_score']:.2f}")
            for signal in result['signals']:
                print(f"   {signal}")
            print()

check_trading_opportunities()
```

---

## 🧪 Como Testar

### Opção 1: Script de Teste

```bash
python test_score.py
```

Este script testa:
- ✅ Cenários simulados
- ✅ Dados reais de BTC, ETH, SOL
- ✅ Integração via API

### Opção 2: Teste Manual

```python
from app.services.indicator_service import IndicatorService
from app.services.crypto_service import CryptoService
from app.utils.score_engine import ScoreEngine

# Setup
crypto = CryptoService()
df = crypto.get_candles('BTC/USDT', '1d', 200)

# Calcular
indicators = IndicatorService.get_indicators(df)
result = ScoreEngine.calculate_score(indicators)

# Ver resultado
print(result)
```

### Opção 3: Via API

```bash
curl http://localhost:8000/analyze/BTC | jq
```

---

## 📈 Cenários de Exemplo

### Cenário 1: Alta Forte (Score +0.80)

```python
indicators = {
    'rsi': 25,           # Oversold (+1)
    'ema9': 50000,
    'ema21': 49000,      # EMA9 > EMA21 (+1)
    'ema200': 45000,     # EMA21 > EMA200 (+1)
    'macd_histogram': 100,  # Positivo (+1)
    'current_volume': 1500,
    'volume_ma': 1000,   # Volume alto (+1)
    'atr': 500,
    'last_close': 50000  # ATR normal (0)
}
# Score: +5 → Normalizado: +1.0
# Diagnóstico: 🟢 Bom momento de compra
```

### Cenário 2: Baixa Forte (Score -0.80)

```python
indicators = {
    'rsi': 75,           # Overbought (-1)
    'ema9': 48000,
    'ema21': 49000,      # EMA9 < EMA21 (-1)
    'ema200': 50000,     # Tendência baixa (0)
    'macd_histogram': -50,  # Negativo (0)
    'current_volume': 800,
    'volume_ma': 1000,   # Volume baixo (0)
    'atr': 12000,
    'last_close': 48000  # ATR > 20% (-1)
}
# Score: -3 → Normalizado: -0.60
# Diagnóstico: 🔴 Evite compra agora
```

### Cenário 3: Neutro (Score 0.00)

```python
indicators = {
    'rsi': 50,           # Neutro (0)
    'ema9': 50000,
    'ema21': 49800,      # Levemente acima (+1)
    'ema200': 48000,     # (+1)
    'macd_histogram': 10,   # Positivo (+1)
    'current_volume': 950,
    'volume_ma': 1000,   # Volume baixo (0)
    'atr': 800,
    'last_close': 50000  # ATR normal (0)
}
# Score: +3 → Normalizado: +0.60
# Diagnóstico: 🟢 Bom momento de compra
```

---

## ⚠️ Avisos Importantes

### 1. Não é Conselho Financeiro
Esta ferramenta é apenas para análise técnica. **NÃO** substitui análise fundamentalista ou consultoria financeira profissional.

### 2. Use Múltiplos Timeframes
Sempre analise mais de um timeframe antes de tomar decisões:
```python
# ✅ BOM
score_1h = calculate_score(indicators_1h)
score_4h = calculate_score(indicators_4h)
score_1d = calculate_score(indicators_1d)

# ❌ RUIM
score_1h = calculate_score(indicators_1h)
# Decidir baseado apenas em 1 timeframe
```

### 3. Combine com Outros Fatores
- 📰 Notícias do mercado
- 📊 Volume global
- 🌍 Eventos macroeconômicos
- 💰 Gerenciamento de risco

### 4. Gestão de Risco
```python
# Sempre use stop loss!
indicators = IndicatorService.get_indicators(df)
atr = indicators['atr']
entry_price = indicators['last_close']

stop_loss = entry_price - (2 * atr)
take_profit = entry_price + (3 * atr)
```

---

## 🔧 Personalização

### Ajustar Limites de Score

Você pode personalizar os limites editando `app/utils/score_engine.py`:

```python
# Valores atuais
if normalized_score >= 0.6:
    diagnostic = "🟢 Bom momento de compra"
elif normalized_score >= 0.2:
    diagnostic = "🟡 Neutro de alta"
# ...

# Você pode ajustar para ser mais/menos conservador
if normalized_score >= 0.8:  # Mais conservador
    diagnostic = "🟢 Bom momento de compra"
```

### Adicionar Novas Regras

```python
# Em calculate_score(), adicione:

# Regra 7: Bollinger Bands (exemplo)
if bb_upper and bb_lower and last_close:
    if last_close < bb_lower:
        score += 1
        signals.append("✅ Preço abaixo Bollinger inferior")
```

---

## 📚 Referências

### Documentação Relacionada
- **QUICK_REFERENCE.md** - Referência dos indicadores
- **IMPLEMENTATION_SUMMARY.md** - Detalhes técnicos
- **FEATURES.md** - Lista de funcionalidades

### Scripts de Teste
- **test_score.py** - Testes completos da função
- **test_indicators.py** - Testes dos indicadores
- **examples.py** - Exemplos da API

---

## 🎓 Dicas de Trading

### 1. Confirmação Multi-Timeframe
```python
# Score positivo em 3 timeframes = sinal forte
if all([score_1h > 0.2, score_4h > 0.2, score_1d > 0.2]):
    print("✅ Sinal confirmado em todos os timeframes!")
```

### 2. Divergências
```python
# Score 1h muito diferente do 1d = cautela
if abs(score_1h - score_1d) > 0.6:
    print("⚠️ Divergência entre timeframes")
```

### 3. Esperar Confirmação
```python
# Aguardar score melhorar por 2+ períodos
if previous_score < 0.2 and current_score >= 0.6:
    print("✅ Score melhorando - possível entrada")
```

---

**🎯 Use esta ferramenta como parte de uma estratégia completa de trading!**

*Lembre-se: Mercado de criptomoedas é volátil. Invista apenas o que pode perder.*

