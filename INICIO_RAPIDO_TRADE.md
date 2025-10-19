# 🚀 Início Rápido - Análise de Trade Rápido

## ⚡ Em 3 Passos

### 1️⃣ Certifique-se que a API está rodando

```bash
# Se não estiver rodando, inicie:
python run.py
```

Deve aparecer:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### 2️⃣ Faça uma consulta

**Opção A: Teste rápido (recomendado)**
```bash
python test_trade_opportunity.py
```

**Opção B: Via navegador**
```
http://localhost:8000/analyze/BTC
```

**Opção C: Via Python**
```python
import requests
response = requests.get("http://localhost:8000/analyze/BTC")
trade = response.json()['trade_opportunity']
print(f"Probabilidade: {trade['probability']:.0%}")
print(f"Comentário: {trade['comment']}")
```

---

### 3️⃣ Interprete o resultado

| Probabilidade | O que fazer? |
|--------------|-------------|
| **≥ 70%** | 🟢 Alta chance! Considere entrada |
| **40-69%** | 🟡 Possível oportunidade, aguarde confirmação |
| **< 40%** | 🔴 Sem sinal claro, não entre |

---

## 📊 Exemplo de Saída

```
⚡ ANÁLISE DE TRADE RÁPIDO (Timeframe 1h)
============================================================
Probabilidade: 80%
Comentário: Alta chance de movimento positivo nas próximas horas.

🟢 SINAL FORTE - Alta probabilidade de movimento positivo!
```

---

## 🎯 O Que Está Sendo Analisado?

5 critérios técnicos no timeframe de **1 hora**:

1. ✅ **RSI** entre 40 e 60, virando pra cima
2. ✅ **EMA9** acima de EMA21 (tendência de alta)
3. ✅ **Volume** acima da média (confirmação)
4. ✅ **MACD** histograma positivo
5. ✅ **ADX** acima de 25 (tendência forte)

**Cada critério atendido = +20% de probabilidade**

---

## 💡 Dicas Rápidas

### ✅ Faça isso:
- Use probabilidade ≥ 70% como sinal de entrada
- Combine com o `score` geral (deve ser ≥ 0.6)
- Sempre use stop-loss (1-2% abaixo da entrada)
- Reavalie a cada 1 hora

### ❌ Evite isso:
- Entrar com probabilidade < 40%
- Ignorar o contexto geral do mercado
- Operar sem stop-loss
- Confiar apenas em 1 indicador

---

## 📚 Documentação Completa

- **`TRADE_RAPIDO_GUIA.md`** → Guia completo com todos os detalhes
- **`EXEMPLO_RESPOSTA_API.md`** → Exemplos de respostas JSON
- **`RESUMO_TRADE_RAPIDO.md`** → Resumo da implementação

---

## 🧪 Scripts de Teste

### test_trade_opportunity.py
```bash
python test_trade_opportunity.py          # Testa BTC
python test_trade_opportunity.py ETH      # Testa ETH
```

**Recursos:**
- Exibe probabilidade e comentário
- Mostra indicadores técnicos do timeframe 1h
- Compara múltiplas moedas (BTC, ETH, SOL)

### example_trade_opportunity.py
```bash
python example_trade_opportunity.py
```

**Recursos:**
- Menu interativo com 3 opções
- Monitoramento contínuo (atualiza a cada 1min)
- Ranking de oportunidades

---

## 🔍 Consulta via API

### Endpoint
```
GET /analyze/{symbol}
```

### Parâmetros
- `{symbol}`: BTC, ETH, SOL, ADA, etc.

### Resposta (campo novo)
```json
{
  "trade_opportunity": {
    "probability": 0.8,
    "comment": "Alta chance de movimento positivo nas próximas horas."
  }
}
```

---

## 📈 Exemplo Prático de Uso

```python
import requests

def verificar_oportunidade(symbol):
    """Verifica se há oportunidade de trade"""
    
    # Consulta API
    url = f"http://localhost:8000/analyze/{symbol}"
    response = requests.get(url)
    data = response.json()
    
    # Extrai informações
    trade = data['trade_opportunity']
    prob = trade['probability']
    score = data['score']
    
    # Decisão
    if prob >= 0.7 and score >= 0.6:
        print(f"🟢 {symbol}: ENTRAR!")
        print(f"   Probabilidade: {prob:.0%}")
        print(f"   Score: {score:.2f}")
        return True
    
    elif prob >= 0.4:
        print(f"🟡 {symbol}: Aguardar confirmação")
        print(f"   Probabilidade: {prob:.0%}")
        return False
    
    else:
        print(f"🔴 {symbol}: Sem oportunidade")
        return False

# Uso
verificar_oportunidade("BTC")
verificar_oportunidade("ETH")
verificar_oportunidade("SOL")
```

---

## ⚠️ Avisos

> **IMPORTANTE**: Esta é uma ferramenta de **suporte à decisão**, não uma recomendação de investimento.

- 📊 Faça sua própria análise
- 💰 Use gestão de risco
- 📉 Mercado cripto é volátil
- 🧠 Combine com experiência

---

## 🆘 Problemas Comuns

### API não conecta
```bash
# Verifique se está rodando:
Get-Process python

# Se não estiver, inicie:
python run.py
```

### Erro "Module not found"
```bash
# Instale dependências:
pip install -r requirements.txt
```

### Timeout na requisição
```bash
# Aumente timeout:
requests.get(url, timeout=30)
```

---

## 📞 Próximos Passos

1. ✅ Teste com `python test_trade_opportunity.py`
2. 📖 Leia `TRADE_RAPIDO_GUIA.md` para detalhes
3. 🎯 Use em operações reais (com cautela!)
4. 📊 Acompanhe resultados e ajuste estratégia

---

**Pronto para começar?** Execute:
```bash
python test_trade_opportunity.py
```

🚀 **Bons trades!**

