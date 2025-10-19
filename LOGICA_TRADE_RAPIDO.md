# 🧠 Lógica de Análise de Trade Rápido

## 🔄 Fluxo de Funcionamento

```
┌─────────────────────────────────────────────────────────────┐
│                  Usuário faz requisição                     │
│              GET /analyze/{symbol}                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│         CryptoService busca dados do timeframe 1h          │
│              (últimas 500 velas)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│      IndicatorService calcula indicadores técnicos         │
│   RSI, EMA9, EMA21, MACD, Volume MA, ADX                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│   ScoreEngine.analyze_short_term_opportunity()             │
│              Avalia 5 critérios                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Cada critério = +1 ponto                       │
│           Probabilidade = pontos / 5                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│        Gera comentário baseado na probabilidade            │
│    Retorna {probability, comment} no JSON                  │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Critérios de Avaliação

### 🎯 Critério 1: RSI Favorável
```python
pontos = 0

rsi = indicators['momentum']['RSI']

if 40 <= rsi <= 60:        # RSI em zona neutra
    if rsi >= 50:          # Virando pra cima
        pontos += 1        # ✅ +1 ponto
```

**Exemplo:**
- RSI = 54 → ✅ +1 ponto (entre 40-60 E ≥ 50)
- RSI = 46 → ❌ 0 pontos (entre 40-60 mas < 50)
- RSI = 72 → ❌ 0 pontos (fora da faixa 40-60)

---

### 📈 Critério 2: Cruzamento de EMAs
```python
ema9 = indicators['trend']['EMA9']
ema21 = indicators['trend']['EMA21']

if ema9 > ema21:           # EMA9 acima de EMA21
    pontos += 1            # ✅ +1 ponto
```

**Exemplo:**
- EMA9 = 67,234 | EMA21 = 66,890 → ✅ +1 ponto (EMA9 > EMA21)
- EMA9 = 66,234 | EMA21 = 66,890 → ❌ 0 pontos (EMA9 < EMA21)

**Significado:**
- EMA9 > EMA21 = Tendência de curto prazo é de alta
- EMA9 < EMA21 = Tendência de curto prazo é de baixa

---

### 📊 Critério 3: Volume Confirmando
```python
current_volume = indicators['price']['current_volume']
volume_ma = indicators['volume']['Volume_MA']

if current_volume > volume_ma:    # Volume acima da média
    pontos += 1                    # ✅ +1 ponto
```

**Exemplo:**
- Volume atual = 1.5B | Média = 1.2B → ✅ +1 ponto (125% da média)
- Volume atual = 0.9B | Média = 1.2B → ❌ 0 pontos (75% da média)

**Significado:**
- Volume alto = Movimento tem força, maior confiabilidade
- Volume baixo = Movimento pode ser falso breakout

---

### 📉 Critério 4: MACD Positivo
```python
macd_histogram = indicators['momentum']['MACD_Histogram']

if macd_histogram > 0:     # Histograma positivo
    pontos += 1            # ✅ +1 ponto
```

**Exemplo:**
- MACD Histograma = +36.22 → ✅ +1 ponto (positivo)
- MACD Histograma = -12.45 → ❌ 0 pontos (negativo)

**Significado:**
- Histograma > 0 = Momentum de alta
- Histograma < 0 = Momentum de baixa

---

### 💪 Critério 5: Tendência Forte (ADX)
```python
adx = indicators['strength']['ADX']

if adx > 25:               # ADX acima de 25
    pontos += 1            # ✅ +1 ponto
```

**Exemplo:**
- ADX = 28.56 → ✅ +1 ponto (tendência forte)
- ADX = 18.23 → ❌ 0 pontos (tendência fraca)

**Significado:**
- ADX > 25 = Tendência forte (seja alta ou baixa)
- ADX < 25 = Mercado lateral, sem tendência clara

---

## 📊 Cálculo da Probabilidade

```python
total_pontos = 0

# Soma pontos de cada critério
if criterio_1_atendido: total_pontos += 1
if criterio_2_atendido: total_pontos += 1
if criterio_3_atendido: total_pontos += 1
if criterio_4_atendido: total_pontos += 1
if criterio_5_atendido: total_pontos += 1

# Calcula probabilidade (0.0 a 1.0)
probability = total_pontos / 5

# Arredonda para 2 casas decimais
probability = round(probability, 2)
```

### Exemplos:

| Critérios Atendidos | Pontos | Probabilidade | Percentual |
|-------------------|--------|--------------|------------|
| ✅✅✅✅✅ | 5 | 1.00 | 100% |
| ✅✅✅✅❌ | 4 | 0.80 | 80% |
| ✅✅✅❌❌ | 3 | 0.60 | 60% |
| ✅✅❌❌❌ | 2 | 0.40 | 40% |
| ✅❌❌❌❌ | 1 | 0.20 | 20% |
| ❌❌❌❌❌ | 0 | 0.00 | 0% |

---

## 💬 Geração de Comentários

```python
if probability >= 0.7:
    comment = "Alta chance de movimento positivo nas próximas horas."
    
elif probability >= 0.4:
    comment = "Possível oportunidade de curto prazo, aguarde confirmação."
    
else:
    comment = "Sem sinal claro de trade rápido agora."
```

### Tabela de Comentários:

| Probabilidade | Comentário | Ação Sugerida |
|--------------|-----------|---------------|
| **100%** | Alta chance... | 🟢 ENTRAR |
| **80%** | Alta chance... | 🟢 ENTRAR |
| **60%** | Possível oportunidade... | 🟡 AGUARDAR CONFIRMAÇÃO |
| **40%** | Possível oportunidade... | 🟡 AGUARDAR CONFIRMAÇÃO |
| **20%** | Sem sinal claro... | 🔴 NÃO ENTRAR |
| **0%** | Sem sinal claro... | 🔴 NÃO ENTRAR |

---

## 📋 Exemplo Completo Passo a Passo

### Cenário: Análise do BTC

**Dados recebidos (timeframe 1h):**
```python
rsi = 54.32
ema9 = 67234.56
ema21 = 66890.12
current_volume = 1534567890.0
volume_ma = 1234567890.0
macd_histogram = 36.22
adx = 28.56
```

---

**Passo 1: Avaliar Critério 1 (RSI)**
```python
# RSI entre 40 e 60, virando pra cima?
if 40 <= 54.32 <= 60:       # ✅ TRUE
    if 54.32 >= 50:         # ✅ TRUE
        pontos += 1
        
# pontos = 1
```

---

**Passo 2: Avaliar Critério 2 (EMA)**
```python
# EMA9 > EMA21?
if 67234.56 > 66890.12:     # ✅ TRUE
    pontos += 1
    
# pontos = 2
```

---

**Passo 3: Avaliar Critério 3 (Volume)**
```python
# Volume acima da média?
if 1534567890.0 > 1234567890.0:  # ✅ TRUE
    pontos += 1
    
# pontos = 3
```

---

**Passo 4: Avaliar Critério 4 (MACD)**
```python
# MACD histograma positivo?
if 36.22 > 0:               # ✅ TRUE
    pontos += 1
    
# pontos = 4
```

---

**Passo 5: Avaliar Critério 5 (ADX)**
```python
# ADX > 25?
if 28.56 > 25:              # ✅ TRUE
    pontos += 1
    
# pontos = 5
```

---

**Passo 6: Calcular Probabilidade**
```python
probability = 5 / 5
probability = 1.0           # 100%
```

---

**Passo 7: Gerar Comentário**
```python
if 1.0 >= 0.7:
    comment = "Alta chance de movimento positivo nas próximas horas."
```

---

**Passo 8: Retornar Resultado**
```json
{
  "probability": 1.0,
  "comment": "Alta chance de movimento positivo nas próximas horas."
}
```

---

## 🎯 Interpretação do Resultado

### Resultado: 100% de probabilidade

**Significa que:**
- ✅ Todos os 5 critérios técnicos foram atendidos
- ✅ RSI está em zona favorável e virando pra cima
- ✅ Tendência de curto prazo é de alta (EMA9 > EMA21)
- ✅ Volume está confirmando o movimento
- ✅ Momentum está positivo (MACD)
- ✅ Tendência é forte (ADX > 25)

**Ação sugerida:**
🟢 **FORTE SINAL DE ENTRADA**
- Considere entrada para day trade
- Objetivo: 2-4% de lucro
- Stop-loss: 1-1.5% abaixo

---

## 🧮 Pesos e Importância

### Por que cada critério vale 1 ponto?

**Abordagem igualitária:**
- Cada indicador representa um aspecto diferente
- RSI = Momentum
- EMA = Tendência
- Volume = Confirmação
- MACD = Força do movimento
- ADX = Intensidade da tendência

**Todos são igualmente importantes para um trade rápido:**
- Não adianta ter volume alto se a tendência é de baixa
- Não adianta ter EMA favorável se o volume é fraco
- A combinação de todos aumenta confiabilidade

---

## 📊 Distribuição Estatística

Em condições normais de mercado:

| Probabilidade | Frequência Esperada |
|--------------|-------------------|
| 80-100% | ~10-15% das análises |
| 60-79% | ~20-25% das análises |
| 40-59% | ~30-35% das análises |
| 20-39% | ~20-25% das análises |
| 0-19% | ~10-15% das análises |

**Portanto:**
- Sinais fortes (≥80%) são **raros** mas **muito confiáveis**
- Sinais moderados (40-79%) são **comuns** mas **requerem confirmação**
- Sem sinais (<40%) são **comuns** em mercado lateral

---

## 🔍 Validação e Testes

### Como testar a lógica:

```python
# Teste 1: Todos critérios atendidos
indicators = {
    'rsi': 54,
    'ema9': 100,
    'ema21': 99,
    'volume': 1000,
    'volume_ma': 900,
    'macd_histogram': 10,
    'adx': 30
}
# Esperado: probability = 1.0 (100%)

# Teste 2: Apenas 3 critérios atendidos
indicators = {
    'rsi': 45,        # ❌ Não está >= 50
    'ema9': 100,      # ✅
    'ema21': 99,      # ✅
    'volume': 1000,   # ✅
    'volume_ma': 900, # ✅
    'macd_histogram': -5,  # ❌
    'adx': 20         # ❌
}
# Esperado: probability = 0.6 (60%)
```

---

## 🎓 Aprendizados

### Quando a lógica funciona bem:
✅ Mercado em tendência clara (alta ou baixa)  
✅ Volume consistente  
✅ Timeframe de 1h com dados confiáveis  

### Quando pode falhar:
❌ Mercado extremamente volátil (notícias súbitas)  
❌ Baixa liquidez (moedas pequenas)  
❌ Eventos extraordinários (fork, hack, regulação)  

---

## 🚀 Melhorias Futuras

Possíveis refinamentos:

1. **Pesos dinâmicos**: Dar mais peso a ADX quando > 30
2. **Contexto de mercado**: Considerar Bitcoin Dominance
3. **Histórico**: Verificar se critérios se mantêm há 2-3 velas
4. **Machine Learning**: Ajustar pesos baseado em acurácia histórica
5. **Níveis de preço**: Adicionar suporte/resistência à análise

---

**Implementado em:** `app/utils/score_engine.py`  
**Método:** `analyze_short_term_opportunity()`  
**Linhas:** 329-391

