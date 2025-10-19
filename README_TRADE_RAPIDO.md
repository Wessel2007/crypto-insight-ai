# 🚀 Trade Rápido - README

## ✅ O Que Foi Feito

Adicionada análise de **oportunidades de trade rápido** (day trade/scalp) baseada em 5 critérios técnicos do timeframe **1h**.

---

## 🎯 Como Funciona

### 5 Critérios Avaliados

Cada critério atendido = **+20% de probabilidade**

1. ✅ RSI entre 40-60, virando pra cima
2. ✅ EMA9 > EMA21 (tendência de alta)
3. ✅ Volume acima da média
4. ✅ MACD histograma positivo
5. ✅ ADX > 25 (tendência forte)

### Resultado

```json
{
  "trade_opportunity": {
    "probability": 0.8,
    "comment": "Alta chance de movimento positivo nas próximas horas."
  }
}
```

---

## ⚡ Teste Rápido

```bash
# 1. Certifique-se que a API está rodando
python run.py

# 2. Execute o teste (em outro terminal)
python test_trade_opportunity.py
```

---

## 📊 Interpretação

| Probabilidade | O que fazer? |
|--------------|-------------|
| **≥ 70%** | 🟢 Considere entrada |
| **40-69%** | 🟡 Aguarde confirmação |
| **< 40%** | 🔴 Não entre |

---

## 📚 Documentação

### Início Rápido
👉 `INICIO_RAPIDO_TRADE.md` - Comece aqui!

### Detalhes
- `TRADE_RAPIDO_GUIA.md` - Guia completo
- `LOGICA_TRADE_RAPIDO.md` - Como funciona a lógica
- `EXEMPLO_RESPOSTA_API.md` - Exemplos de JSON
- `RESUMO_TRADE_RAPIDO.md` - Resumo técnico
- `IMPLEMENTACAO_TRADE_RAPIDO_COMPLETA.md` - Tudo sobre a implementação

### Scripts
- `test_trade_opportunity.py` - Teste básico
- `example_trade_opportunity.py` - Exemplos avançados

---

## 🔍 Exemplo de Uso

```python
import requests

# Consulta a API
response = requests.get("http://localhost:8000/analyze/BTC")
data = response.json()

# Verifica oportunidade
trade = data['trade_opportunity']

if trade['probability'] >= 0.7:
    print("🟢 ENTRAR NO TRADE!")
    print(f"Probabilidade: {trade['probability']:.0%}")
else:
    print("⏸️ Aguardar melhor momento")
```

---

## 📡 API Endpoint

```
GET /analyze/{symbol}
```

**Novo campo na resposta:**
```json
"trade_opportunity": {
  "probability": 0.8,
  "comment": "Alta chance de movimento positivo nas próximas horas."
}
```

---

## ✅ Arquivos Modificados

### Código (3 arquivos)
- `app/models/schemas.py` - Schema TradeOpportunity
- `app/utils/score_engine.py` - Lógica de análise
- `app/routes/analyze.py` - Integração com API

### Criados (8 arquivos)
- 📄 6 arquivos de documentação (`.md`)
- 🧪 2 scripts de teste (`.py`)

---

## 🎯 Status

### ✅ PRONTO PARA USO!

- [x] Implementado e testado
- [x] API funcionando
- [x] Documentação completa
- [x] Sem erros de linter
- [x] Compatível com código existente

---

## 🚀 Próximos Passos

1. Execute: `python test_trade_opportunity.py`
2. Leia: `INICIO_RAPIDO_TRADE.md`
3. Use: Integre em seu sistema de trading

---

**Versão:** 1.0.0 | **Status:** ✅ Completo | **Data:** Outubro 2024

