# 📊 Guia de Análise de Trade Rápido

## 🎯 Visão Geral

A funcionalidade de **Análise de Trade Rápido** identifica oportunidades de day trade e scalping baseadas em indicadores técnicos do timeframe de 1 hora (1h).

## 🔍 Como Funciona

### Critérios de Análise

O sistema analisa **5 critérios técnicos** específicos no timeframe de 1h. Cada critério atendido adiciona **1 ponto**:

| Critério | Condição | Pontos |
|----------|----------|--------|
| **RSI** | Entre 40 e 60, virando para cima (≥ 50) | +1 |
| **Cruzamento EMA** | EMA9 acima de EMA21 | +1 |
| **Volume** | Acima da média móvel | +1 |
| **MACD** | Histograma positivo | +1 |
| **ADX** | Acima de 25 (tendência forte) | +1 |

### Cálculo de Probabilidade

```python
probabilidade = pontos_obtidos / 5
```

**Exemplo:**
- Se 4 critérios foram atendidos: `probabilidade = 4/5 = 0.80 = 80%`

### Interpretação dos Resultados

| Probabilidade | Comentário | Significado |
|--------------|-----------|-------------|
| **≥ 70%** (≥0.7) | "Alta chance de movimento positivo nas próximas horas." | 🟢 Sinal forte para possível entrada |
| **40-69%** (0.4-0.69) | "Possível oportunidade de curto prazo, aguarde confirmação." | 🟡 Sinal moderado, aguarde confirmação |
| **< 40%** (<0.4) | "Sem sinal claro de trade rápido agora." | 🔴 Não há oportunidade clara |

## 📡 Uso da API

### Endpoint

```
GET /analyze/{symbol}
```

### Resposta JSON

```json
{
  "symbol": "BTCUSDT",
  "score": 0.68,
  "diagnostic": "Momento altista - Tendência de alta moderada",
  "trade_opportunity": {
    "probability": 0.8,
    "comment": "Alta chance de movimento positivo nas próximas horas."
  },
  "timeframes": ["1h", "4h", "1d"],
  "indicators": { ... }
}
```

### Exemplo de Uso (Python)

```python
import requests

# Consulta a API
response = requests.get("http://localhost:8000/analyze/BTC")
data = response.json()

# Acessa a análise de trade rápido
trade_opp = data['trade_opportunity']
print(f"Probabilidade: {trade_opp['probability']:.0%}")
print(f"Comentário: {trade_opp['comment']}")

# Decisão baseada na probabilidade
if trade_opp['probability'] >= 0.7:
    print("🟢 Considere entrada para trade rápido")
elif trade_opp['probability'] >= 0.4:
    print("🟡 Aguarde confirmação adicional")
else:
    print("🔴 Sem oportunidade no momento")
```

## 🧪 Testando a Funcionalidade

### 1. Teste Rápido

Execute o script de teste fornecido:

```bash
python test_trade_opportunity.py
```

### 2. Teste com Símbolo Específico

```bash
python test_trade_opportunity.py ETH
```

### 3. Comparar Múltiplas Moedas

O script permite comparar oportunidades entre BTC, ETH e SOL, gerando um ranking ordenado por probabilidade.

## 📊 Exemplo de Saída

```
🔍 Testando análise de trade rápido para BTC...

📊 INFORMAÇÕES GERAIS
============================================================
Símbolo: BTCUSDT
Score Geral: 0.68
Diagnóstico: Momento altista - Tendência de alta moderada

⚡ ANÁLISE DE TRADE RÁPIDO (Timeframe 1h)
============================================================
Probabilidade: 80%
Comentário: Alta chance de movimento positivo nas próximas horas.

🟢 SINAL FORTE - Alta probabilidade de movimento positivo!

============================================================

📈 INDICADORES TÉCNICOS (1h)
============================================================
RSI: 52.34
  ✓ RSI em zona neutra (favorável para entry)
EMA9: 45823.12
EMA21: 45621.45
  ✓ EMA9 acima de EMA21 (tendência de alta)
Volume: Acima da média
  ✓ Volume confirmando movimento
MACD Histograma: 12.34 (positivo)
  ✓ MACD em zona positiva
ADX: 28.56
  ✓ Tendência forte (ADX > 25)

============================================================
```

## 💡 Dicas de Uso

### Para Day Traders

- ✅ Probabilidade ≥ 70%: Considere entrada com stop-loss apertado
- ⚠️ Probabilidade 40-69%: Aguarde breakout ou confirmação adicional
- ❌ Probabilidade < 40%: Evite operações, mercado lateral

### Boas Práticas

1. **Combine com Score Geral**: Verifique se o `score` geral também está favorável
2. **Confirme com Volume**: Volume acima da média aumenta confiabilidade
3. **Use Stop Loss**: Sempre opere com stop-loss definido
4. **Timeframe de 1h**: Ideal para trades de algumas horas (2-8h)
5. **Reavalie**: Verifique a análise a cada nova vela (1h)

### Não Recomendado

- ❌ Operar apenas baseado na probabilidade isolada
- ❌ Ignorar contexto de mercado mais amplo (timeframe diário)
- ❌ Operar sem gestão de risco (stop-loss/take-profit)

## 🔧 Implementação Técnica

### Arquivos Modificados

1. **`app/models/schemas.py`**
   - Adicionado modelo `TradeOpportunity`
   - Atualizado `AnalyzeResponse` com campo `trade_opportunity`

2. **`app/utils/score_engine.py`**
   - Adicionado método `analyze_short_term_opportunity()`
   - Implementa lógica de pontuação dos 5 critérios

3. **`app/routes/analyze.py`**
   - Integra análise de trade rápido no endpoint `/analyze/{symbol}`
   - Retorna dados no JSON de resposta

### Fluxo de Dados

```
1. Usuário solicita: GET /analyze/BTC
2. Sistema busca dados do timeframe 1h
3. Calcula indicadores técnicos (RSI, EMA, MACD, Volume, ADX)
4. ScoreEngine.analyze_short_term_opportunity() avalia critérios
5. Retorna probabilidade + comentário no JSON
```

## 📈 Casos de Uso

### Scalping (Operações de minutos)
- Monitore mudanças na probabilidade
- Entre quando probabilidade subir acima de 70%
- Saia rapidamente em alvos pequenos (0.5-1%)

### Day Trade (Operações de horas)
- Use probabilidade ≥ 60% como gatilho
- Combine com análise de suporte/resistência
- Opere com alvos de 2-5%

### Swing Trade (Operações de dias)
- Use como filtro adicional
- Confirme com score geral e timeframe diário
- Entre apenas se todos os sinais estiverem alinhados

## ⚠️ Avisos Importantes

> **IMPORTANTE**: Esta análise é apenas uma ferramenta auxiliar. Não constitui recomendação de investimento.

- 📊 Sempre faça sua própria análise
- 💰 Use gestão de risco adequada
- 📉 Mercado de cripto é altamente volátil
- 🧠 Combine com conhecimento técnico e experiência

## 🚀 Próximos Passos

Possíveis melhorias futuras:

- [ ] Adicionar histórico de acurácia das predições
- [ ] Incluir níveis de entrada/saída sugeridos
- [ ] Integrar com análise de padrões gráficos
- [ ] Notificações quando probabilidade > 70%
- [ ] Machine Learning para ajustar pesos dos critérios

---

**Criado em:** Outubro 2024  
**Versão:** 1.0  
**Autor:** Cripto Insight Team

